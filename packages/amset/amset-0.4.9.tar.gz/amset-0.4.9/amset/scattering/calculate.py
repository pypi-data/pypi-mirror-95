"""
This module implements methods to calculate electron scattering.
"""

import logging
import multiprocessing
import time
import traceback
from multiprocessing import cpu_count
from queue import Empty
from typing import Any, Dict, List, Optional, Union

import numba
import numpy as np
import quadpy
from pymatgen import Spin
from pymatgen.util.coord import pbc_diff
from scipy.interpolate import griddata

from amset.constants import (
    boltzmann_au,
    defaults,
    ev_to_hartree,
    hbar,
    small_val,
    spin_name,
)
from amset.core.data import AmsetData
from amset.electronic_structure.fd import fd
from amset.electronic_structure.kpoints import kpoints_to_first_bz
from amset.electronic_structure.tetrahedron import (
    TetrahedralBandStructure,
    get_cross_section_values,
    get_projected_intersections,
)
from amset.interpolation.momentum import MRTACalculator
from amset.interpolation.projections import ProjectionOverlapCalculator
from amset.interpolation.wavefunction import WavefunctionOverlapCalculator
from amset.log import log_list, log_time_taken
from amset.scattering.basic import AbstractBasicScattering
from amset.scattering.elastic import (
    AbstractElasticScattering,
    AcousticDeformationPotentialScattering,
)
from amset.scattering.inelastic import AbstractInelasticScattering
from amset.util import (
    create_shared_dict_array,
    dict_array_from_buffer,
    get_progress_bar,
)

__author__ = "Alex Ganose"
__maintainer__ = "Alex Ganose"
__email__ = "aganose@lbl.gov"

logger = logging.getLogger(__name__)

_all_scatterers: Union = (
    AbstractElasticScattering.__subclasses__()
    + AbstractInelasticScattering.__subclasses__()
    + AbstractBasicScattering.__subclasses__()
)
_scattering_mechanisms = {m.name: m for m in _all_scatterers}
basic_scatterers = [i.name for i in AbstractBasicScattering.__subclasses__()]

ni = {
    "high": {
        "triangle": quadpy.t2.schemes["xiao_gimbutas_50"](),
        "quad": quadpy.c2.schemes["sommariva_50"](),
    },
    "medium": {
        "triangle": quadpy.t2.schemes["xiao_gimbutas_06"](),
        "quad": quadpy.c2.schemes["sommariva_06"](),
    },
    "low": {
        "triangle": quadpy.t2.schemes["centroid"](),
        "quad": quadpy.c2.schemes["dunavant_00"](),
    },
}

# ni = {
#     "high": {"triangle": quadpy.t2.centroid(), "quad": quadpy.c2.dunavant_00()},
#     "medium": {"triangle": quadpy.t2.centroid(), "quad": quadpy.c2.dunavant_00()},
#     "low": {"triangle": quadpy.t2.centroid(), "quad": quadpy.c2.dunavant_00()},
# }


class ScatteringCalculator(object):
    def __init__(
        self,
        settings: Dict[str, float],
        amset_data: AmsetData,
        cutoff_pad: float,
        scattering_type: Union[str, List[str], float] = "auto",
        nworkers: int = defaults["nworkers"],
        progress_bar: bool = defaults["print_log"],
        cache_wavefunction: bool = defaults["cache_wavefunction"],
    ):
        if amset_data.temperatures is None or amset_data.doping is None:
            raise RuntimeError(
                "AmsetData doesn't contain doping levels or temperatures"
            )

        self.scattering_type = scattering_type
        self.settings = settings
        self.nworkers = nworkers if nworkers != -1 else cpu_count()
        self.scatterers = self.get_scatterers(scattering_type, settings, amset_data)
        self.amset_data = amset_data
        self.progress_bar = progress_bar
        self.cache_wavefunction = cache_wavefunction

        buf = 0.05 * ev_to_hartree
        if self.amset_data.fd_cutoffs:
            self.scattering_energy_cutoffs = (
                self.amset_data.fd_cutoffs[0] - buf,
                self.amset_data.fd_cutoffs[1] + buf,
            )
        else:
            self.scattering_energy_cutoffs = (
                min(self.amset_data.dos.energies) - buf,
                max(self.amset_data.dos.energies) + buf,
            )

        self._coeffs = None
        self._coeffs_mapping = None
        # if only basic scatterers then no need to cache overlaps
        self._basic_only = (
            len(self.elastic_scatterers) + len(self.inelastic_scatterers) == 0
        )
        if (
            isinstance(self.amset_data.overlap_calculator, ProjectionOverlapCalculator)
            and cache_wavefunction
        ):
            logger.info(
                "Caching wavefunction not supported with orbital projection "
                "overlaps. Setting cache_wavefunction to False."
            )
        elif cache_wavefunction and not self._basic_only:
            self._coeffs = {}
            self._coeffs_mapping = {}
            # precompute the coefficients we will need to for calculating overlaps
            # could do this on the fly but caching will really speed things up.
            # we need to interpolate as the wavefunction coefficients were calculated on
            # a coarse mesh but we calculate the orbital overlap on a fine mesh.
            tbs = self.amset_data.tetrahedral_band_structure
            for spin in amset_data.spins:
                spin_b_idxs = []
                spin_k_idxs = []
                for b_idx, b_energies in enumerate(self.amset_data.energies[spin]):
                    # find all k-points that fall inside Fermi cutoffs
                    k_idxs = np.where(
                        (b_energies > self.scattering_energy_cutoffs[0] - cutoff_pad)
                        & (b_energies < self.scattering_energy_cutoffs[1] + cutoff_pad)
                    )[0]

                    # find k-points connected to the k-points inside Fermi cutoffs
                    k_idxs = tbs.get_connected_kpoints(k_idxs)
                    spin_k_idxs.extend(k_idxs.tolist())
                    spin_b_idxs.extend([b_idx] * len(k_idxs))

                # calculate the coefficients for all bands and k-point simultaneously
                try:
                    self._coeffs[
                        spin
                    ] = self.amset_data.overlap_calculator.get_coefficients(
                        spin, spin_b_idxs, self.amset_data.kpoints[spin_k_idxs]
                    )
                    # because we are only storing the coefficients for the
                    # band/k-points we want, we need a way of mapping from the original
                    # band/k-point indices to the reduced indices. I.e., it allows us to
                    # get the coefficients for band b_idx, and k-point k_idx using:
                    # self._coeffs[spin][self._coeffs_mapping[b_idx, k_idx]]
                    # use a default value of 100000 as this was it will throw an error
                    # if we don't precache the correct values
                    mapping = np.full_like(self.amset_data.energies[spin], 100000)
                    mapping[spin_b_idxs, spin_k_idxs] = np.arange(len(spin_b_idxs))
                    self._coeffs_mapping[spin] = mapping.astype(int)

                except MemoryError:
                    logger.warning(
                        "Memory requirements too large to cache wavefunction "
                        "coefficients. Setting cache_wavefunction to False"
                    )
                    self._coeffs = None
                    self._coeffs_mapping = None
                    break

        self.in_queue = None
        self.out_queue = None
        self.workers = None
        self.initialize_workers()

    def initialize_workers(self):
        if self._basic_only:
            return

        logger.info(f"Forking {self.nworkers} processes to calculate scattering")
        t0 = time.perf_counter()

        if isinstance(self.amset_data.overlap_calculator, ProjectionOverlapCalculator):
            overlap_type = "projection"
        else:
            overlap_type = "wavefunction"

        if self._coeffs is None:
            coeffs_buffer = None
            coeffs_mapping_buffer = None
        else:
            coeffs_buffer, self._coeffs = create_shared_dict_array(
                self._coeffs, return_shared_data=True
            )
            coeffs_mapping_buffer, self._coeffs_mapping = create_shared_dict_array(
                self._coeffs_mapping, return_shared_data=True
            )

        amset_data_min = _AmsetDataMin.from_amset_data(self.amset_data)
        amset_data_min_reference = amset_data_min.to_reference()

        # deformation potential is a large tensor that should be put into shared memory
        elastic_scatterers = [
            s.to_reference()
            if isinstance(s, AcousticDeformationPotentialScattering)
            else s
            for s in self.elastic_scatterers
        ]

        ctx = multiprocessing.get_context("spawn")
        self.in_queue = ctx.Queue()
        self.out_queue = ctx.Queue()
        args = (
            self.amset_data.tetrahedral_band_structure.to_reference(),
            overlap_type,
            self.amset_data.overlap_calculator.to_reference(),
            self.amset_data.mrta_calculator.to_reference(),
            elastic_scatterers,
            self.inelastic_scatterers,
            amset_data_min_reference,
            coeffs_buffer,
            coeffs_mapping_buffer,
            self.in_queue,
            self.out_queue,
        )

        self.workers = []
        for _ in range(self.nworkers):
            self.workers.append(ctx.Process(target=scattering_worker, args=args))

        iterable = self.workers
        if self.progress_bar:
            iterable = get_progress_bar(self.workers, desc="workers")

        for w in iterable:
            w.start()

        log_time_taken(t0)
        return self.workers

    def terminate_workers(self):
        # The "None"s at the end of the queue signals to the workers that there are
        # no more jobs left and they must therefore exit.
        if self.workers is not None:
            for i in range(self.nworkers):
                self.in_queue.put(None)

            for w in self.workers:
                w.terminate()
                w.join(0)

            self.in_queue.close()
            self.out_queue.close()

            self.workers = None

    @property
    def basic_scatterers(self):
        return [s for s in self.scatterers if isinstance(s, AbstractBasicScattering)]

    @property
    def inelastic_scatterers(self):
        return [
            s for s in self.scatterers if isinstance(s, AbstractInelasticScattering)
        ]

    @property
    def elastic_scatterers(self):
        return [s for s in self.scatterers if isinstance(s, AbstractElasticScattering)]

    @property
    def scatterer_labels(self):
        basic_names = [s.name for s in self.basic_scatterers]
        elastic_names = [s.name for s in self.elastic_scatterers]
        inelastic_names = [s.name for s in self.inelastic_scatterers]

        return basic_names + elastic_names + inelastic_names

    @staticmethod
    def get_scatterers(
        scattering_type: Union[str, List[str], float],
        settings: Dict[str, Any],
        amset_data: AmsetData,
    ) -> List[Union[AbstractElasticScattering, AbstractInelasticScattering]]:
        if scattering_type == "auto":
            # dynamically determine the available scattering mechanism subclasses
            logger.info(
                "Examining material properties to determine possible scattering "
                "mechanisms"
            )

            scattering_type = []
            for name, mechanism in _scattering_mechanisms.items():
                req_prop = mechanism.required_properties
                if all([settings.get(x, None) is not None for x in req_prop]):
                    scattering_type.append(name)

            if not scattering_type:
                raise ValueError(
                    "No scattering mechanisms possible with material properties"
                )

        else:
            for name in scattering_type:
                missing_properties = [
                    p
                    for p in _scattering_mechanisms[name].required_properties
                    if settings.get(p, None) is None
                ]

                if missing_properties:
                    str_missing = ", ".join(missing_properties)
                    raise ValueError(
                        "{} scattering mechanism specified but the following "
                        "material properties are missing: {}".format(name, str_missing)
                    )

        str_scats = ", ".join(scattering_type)
        logger.info("Scattering mechanisms to be calculated: {}".format(str_scats))

        return [
            _scattering_mechanisms[name].from_amset_data(settings, amset_data)
            for name in scattering_type
        ]

    def calculate_scattering_rates(self):
        spins = self.amset_data.spins
        kpoints = self.amset_data.kpoints
        energies = self.amset_data.energies
        fermi_shape = self.amset_data.fermi_levels.shape
        scattering_shape = (len(self.scatterer_labels),) + fermi_shape
        rate_shape = {s: scattering_shape + energies[s].shape for s in spins}

        # rates has shape (spin, nscatterers, ndoping, ntemp, nbands, nkpoints)
        rates = {s: np.zeros(rate_shape[s]) for s in spins}
        masks = {s: np.full(rate_shape[s], True) for s in spins}

        logger.info("Scattering information:")
        log_list(["# ir k-points: {}".format(len(self.amset_data.ir_kpoints_idx))])

        for spin in spins:
            for b_idx in range(len(self.amset_data.energies[spin])):
                str_b = "Calculating rates for {} band {}"
                logger.info(str_b.format(spin_name[spin], b_idx + 1))

                t0 = time.perf_counter()
                (
                    rates[spin][..., b_idx, :],
                    masks[spin][..., b_idx, :],
                ) = self.calculate_band_rates(spin, b_idx)

                info = [
                    "max rate: {:.4g}".format(rates[spin][..., b_idx, :].max()),
                    "min rate: {:.4g}".format(rates[spin][..., b_idx, :].min()),
                ]
                log_list(info, level=logging.DEBUG)
                log_list(["time: {:.4f} s".format(time.perf_counter() - t0)])

            # fill in k-points outside Fermi-Dirac cutoffs with a default value
            rates[spin][masks[spin]] = 1e14

        # if the k-point density is low, some k-points may not have other k-points
        # within the energy tolerance leading to zero rates
        rates = _interpolate_zero_rates(
            rates, kpoints, masks, progress_bar=self.progress_bar
        )

        # enforce symmetry of interpolated points
        ir_idx = self.amset_data.ir_kpoints_idx
        ir_to_full = self.amset_data.ir_to_full_kpoint_mapping
        rates = {s: sr[..., ir_idx][..., ir_to_full] for s, sr in rates.items()}

        self.terminate_workers()
        return rates

    def calculate_band_rates(self, spin: Spin, b_idx: int):
        if self.workers is None and not self._basic_only:
            self.initialize_workers()

        vol = self.amset_data.structure.lattice.reciprocal_lattice.volume
        conversion = vol / (4 * np.pi ** 2)
        kpoints_idx = self.amset_data.ir_kpoints_idx
        nkpoints = len(kpoints_idx)

        band_energies = self.amset_data.energies[spin][b_idx, kpoints_idx]
        mask = band_energies < self.scattering_energy_cutoffs[0]
        mask |= band_energies > self.scattering_energy_cutoffs[1]
        fill_mask = mask[self.amset_data.ir_to_full_kpoint_mapping]

        n = np.sum(~fill_mask)
        logger.info("  ├── # k-points within Fermi–Dirac cut-offs: {}".format(n))

        k_idx_in_cutoff = kpoints_idx[~mask]
        ir_idx_in_cutoff = np.arange(nkpoints)[~mask]
        iterable = list(zip(k_idx_in_cutoff, ir_idx_in_cutoff))

        to_stack = []
        if len(self.basic_scatterers) > 0:
            basic_rates = np.array(
                [m.rates[spin][:, :, b_idx, kpoints_idx] for m in self.basic_scatterers]
            )
            to_stack.append(basic_rates)

        if len(self.elastic_scatterers) > 0:
            elastic_prefactors = conversion * np.array(
                [m.prefactor(spin, b_idx) for m in self.elastic_scatterers]
            )
            elastic_rates = np.zeros(elastic_prefactors.shape + (nkpoints,))

            if len(k_idx_in_cutoff) > 0:
                if self.progress_bar:
                    pbar = get_progress_bar(total=len(iterable), desc="elastic")
                else:
                    pbar = None

                for k_idx, ir_idx in iterable:
                    self.in_queue.put((spin, b_idx, k_idx, False, ir_idx))

                for _ in range(len(iterable)):
                    ir_idx, elastic_rates[..., ir_idx] = self._get_rate_from_queue()
                    if pbar:
                        pbar.update()

                if pbar:
                    pbar.close()

            elastic_rates *= elastic_prefactors[..., None]
            to_stack.append(elastic_rates)

        if len(self.inelastic_scatterers) > 0:
            inelastic_prefactors = conversion * np.array(
                [m.prefactor(spin, b_idx) for m in self.inelastic_scatterers]
            )
            inelastic_rates = np.zeros(inelastic_prefactors.shape + (nkpoints,))
            f_pop = self.settings["pop_frequency"]
            energy_diff = f_pop * 1e12 * 2 * np.pi * hbar * ev_to_hartree

            if len(k_idx_in_cutoff) > 0:
                if self.progress_bar:
                    pbar = get_progress_bar(total=len(iterable) * 2, desc="inelastic")
                else:
                    pbar = None

                inelastic_rates[:, :, :, ir_idx_in_cutoff] = 0
                for k_idx, ir_idx in iterable:
                    for ediff in [energy_diff, -energy_diff]:
                        self.in_queue.put((spin, b_idx, k_idx, ediff, ir_idx))

                for i in range(len(iterable) * 2):
                    ir_idx, rate = self._get_rate_from_queue()
                    inelastic_rates[..., ir_idx] += rate
                    if pbar:
                        pbar.update()

                if pbar:
                    pbar.close()

            inelastic_rates *= inelastic_prefactors[..., None]
            to_stack.append(inelastic_rates)

        all_band_rates = np.vstack(to_stack)

        return all_band_rates[..., self.amset_data.ir_to_full_kpoint_mapping], fill_mask

    def _get_rate_from_queue(self):
        # handle exception gracefully to avoid hanging processes
        try:
            result = self.out_queue.get(timeout=10)
        except Empty:
            # didn't receive anything for 10 seconds; this could be OK or it could
            # the processes have been killed
            if not self._workers_alive():
                self.terminate_workers()
                raise MemoryError(
                    "Some subprocessess were killed unexpectedly. Could be OOM "
                    "Killer?\nTry reducing nworkers."
                )
            else:
                return self._get_rate_from_queue()

        if isinstance(result[0], Exception):
            logger.error(
                "Scattering process ended with error:\n{}\nexiting".format(
                    str(result[1])
                )
            )
            self.terminate_workers()
            raise result[0]
        return result

    def _workers_alive(self):
        return all([worker.is_alive() for worker in self.workers])


def scattering_worker(
    tbs_reference,
    overlap_type,
    overlap_calculator_reference,
    mrta_calculator_reference,
    elastic_scatterers,
    inelastic_scatterers,
    amset_data_min_reference,
    coeffs_buffer,
    coeffs_mapping_buffer,
    in_queue,
    out_queue,
):
    try:
        tbs = TetrahedralBandStructure.from_reference(*tbs_reference)
        mrta_calculator = MRTACalculator.from_reference(*mrta_calculator_reference)
        amset_data_min = _AmsetDataMin.from_reference(*amset_data_min_reference)

        if coeffs_buffer is None:
            coeffs = None
            coeffs_mapping = None
        else:
            coeffs = dict_array_from_buffer(coeffs_buffer)
            coeffs_mapping = dict_array_from_buffer(coeffs_mapping_buffer)

        if overlap_type == "wavefunction":
            overlap_calculator = WavefunctionOverlapCalculator.from_reference(
                *overlap_calculator_reference
            )
        elif overlap_type == "projection":
            overlap_calculator = ProjectionOverlapCalculator.from_reference(
                *overlap_calculator_reference
            )
        else:
            raise ValueError("Unrecognised overlap type: {}".format(overlap_type))

        elastic_scatterers = [
            AcousticDeformationPotentialScattering.from_reference(*s)
            if isinstance(s, tuple)
            else s
            for s in elastic_scatterers
        ]

        with np.errstate(all="ignore"):
            while True:
                job = in_queue.get()

                if job is None:
                    break

                spin, b_idx, k_idx, energy_diff, ir_k_idx = job
                rate = calculate_rate(
                    tbs,
                    overlap_calculator,
                    mrta_calculator,
                    elastic_scatterers,
                    inelastic_scatterers,
                    amset_data_min,
                    coeffs,
                    coeffs_mapping,
                    spin,
                    b_idx,
                    k_idx,
                    energy_diff=energy_diff,
                )
                out_queue.put((ir_k_idx, rate))

    except BaseException as e:
        error_msg = traceback.format_exc()
        out_queue.put((e, error_msg))


class _AmsetDataMin:
    def __init__(self, structure, kpoint_mesh, velocities, fermi_levels, temperatures):
        self.structure = structure
        self.kpoint_mesh = kpoint_mesh
        self.velocities = velocities
        self.fermi_levels = fermi_levels
        self.temperatures = temperatures

    def to_reference(self):
        velocities_buffer, self.velocities = create_shared_dict_array(
            self.velocities, return_shared_data=True
        )
        return (
            self.structure,
            self.kpoint_mesh,
            velocities_buffer,
            self.fermi_levels,
            self.temperatures,
        )

    @classmethod
    def from_reference(
        cls, structure, kpoint_mesh, velocities_buffer, fermi_levels, temperatures
    ):
        return cls(
            structure,
            kpoint_mesh,
            dict_array_from_buffer(velocities_buffer),
            fermi_levels,
            temperatures,
        )

    @classmethod
    def from_amset_data(cls, amset_data):
        return cls(
            amset_data.structure,
            amset_data.kpoint_mesh,
            amset_data.velocities,
            amset_data.fermi_levels,
            amset_data.temperatures,
        )


def calculate_rate(
    tbs: TetrahedralBandStructure,
    overlap_calculator,
    mrta_calculator,
    elastic_scatterers,
    inelastic_scatterers,
    amset_data_min: _AmsetDataMin,
    coeffs,
    coeffs_mapping,
    spin,
    b_idx,
    k_idx,
    energy_diff=None,
):
    rlat = amset_data_min.structure.lattice.reciprocal_lattice.matrix
    velocity = amset_data_min.velocities[spin][b_idx, k_idx]
    energy = tbs.energies[spin][b_idx, k_idx]

    if energy_diff:
        energy += energy_diff

    (
        tet_dos,
        tet_mask,
        cs_weights,
        tet_contributions,
    ) = tbs.get_tetrahedra_density_of_states(
        spin,
        energy,
        return_contributions=True,
        symmetry_reduce=False,
        # band_idx=b_idx,  # turn this on to disable interband scattering
    )

    if len(tet_dos) == 0:
        return 0

    # next, get k-point indices and band_indices
    property_mask, band_kpoint_mask, band_mask, kpoint_mask = tbs.get_masks(
        spin, tet_mask
    )
    k = tbs.kpoints[k_idx]
    k_primes = tbs.kpoints[kpoint_mask]

    if coeffs is not None:
        # use cached coefficients to calculate the overlap on the fine mesh
        # tetrahedron vertices
        spin_coeffs = coeffs[spin]
        spin_coeffs_mapping = coeffs_mapping[spin]
        if len(spin_coeffs.shape) == 3:
            # ncl
            overlap = _get_overlap_ncl(
                spin_coeffs, spin_coeffs_mapping, b_idx, k_idx, band_mask, kpoint_mask
            )
        else:
            overlap = _get_overlap(
                spin_coeffs, spin_coeffs_mapping, b_idx, k_idx, band_mask, kpoint_mask
            )
    else:
        overlap = overlap_calculator.get_overlap(spin, b_idx, k, band_mask, k_primes)

    # put overlap back in array with shape (nbands, nkpoints)
    all_overlap = np.zeros(tbs.energies[spin].shape)
    all_overlap[band_kpoint_mask] = overlap

    # now select the properties at the tetrahedron vertices
    vert_overlap = all_overlap[property_mask]

    # get interpolated overlap at centre of tetrahedra cross sections
    tet_overlap = get_cross_section_values(vert_overlap, *tet_contributions)
    tetrahedra = tbs.tetrahedra[spin][tet_mask]

    # have to deal with the case where the tetrahedron cross section crosses the
    # zone boundary. This is a slight inaccuracy but we just treat the
    # cross section as if it is on one side of the boundary
    tet_kpoints = tbs.kpoints[tetrahedra]
    base_kpoints = tet_kpoints[:, 0][:, None, :]
    k_diff = pbc_diff(tet_kpoints, base_kpoints) + pbc_diff(base_kpoints, k)

    # project the tetrahedron cross sections onto 2D surfaces in either a triangle
    # or quadrilateral
    k_diff = np.dot(k_diff, rlat)
    intersections = get_cross_section_values(k_diff, *tet_contributions, average=False)
    projected_intersections, basis = get_projected_intersections(intersections)

    k_spacing = np.linalg.norm(np.dot(rlat, 1 / amset_data_min.kpoint_mesh))
    qpoints, weights, mapping = get_fine_mesh_qpoints(
        projected_intersections,
        basis,
        *tet_contributions[0:3],
        high_tol=k_spacing * 0.5,
        med_tol=k_spacing * 2,
        cross_section_weights=cs_weights,
    )
    qpoint_norm_sq = np.sum(qpoints ** 2, axis=-1)

    k_primes = np.dot(qpoints, np.linalg.inv(rlat)) + k
    k_primes = kpoints_to_first_bz(k_primes)

    # unit q in reciprocal cartesian coordinates
    unit_q = qpoints / np.sqrt(qpoint_norm_sq)[:, None]
    if energy_diff:
        e_fd = _get_fd(energy, amset_data_min.fermi_levels, amset_data_min.temperatures)
        emission = energy_diff <= 0
        rates = [
            s.factor(unit_q, qpoint_norm_sq, emission, e_fd)
            for s in inelastic_scatterers
        ]
        mrta_factor = 1
    else:
        mrta_factor = mrta_calculator.get_mrta_factor(
            spin, b_idx, k, tet_mask[0][mapping], k_primes
        )
        rates = [
            s.factor(unit_q, qpoint_norm_sq, spin, b_idx, k, velocity)
            for s in elastic_scatterers
        ]

    rates = np.array(rates)
    rates /= amset_data_min.structure.lattice.reciprocal_lattice.volume
    rates *= tet_overlap[mapping] * weights * mrta_factor

    # this is too expensive vs tetrahedron integration and doesn't add much more
    # accuracy; could offer this as an option
    # overlap = self.amset_data.overlap_calculator.get_overlap(
    #     spin, b_idx, k, tet_mask[0][mapping], k_primes
    # )
    # rates *= overlap * weights * mrta_factor

    # sometimes the projected intersections can be nan when the density of states
    # contribution is infinitesimally small; this catches those errors
    rates[np.isnan(rates)] = 0

    return np.sum(rates, axis=-1)


@numba.njit
def _get_overlap(
    spin_coeffs, spin_coeffs_mapping, b_idx, k_idx, band_mask, kpoint_mask
):
    res = np.zeros(band_mask.shape[0])
    initial = np.conj(spin_coeffs[spin_coeffs_mapping[b_idx, k_idx]])

    for i in range(band_mask.shape[0]):
        final = spin_coeffs[spin_coeffs_mapping[band_mask[i], kpoint_mask[i]]]
        res[i] = np.abs(np.dot(final, initial)) ** 2

    return res


@numba.njit
def _get_overlap_ncl(
    spin_coeffs, spin_coeffs_mapping, b_idx, k_idx, band_mask, kpoint_mask
):
    res = np.zeros(band_mask.shape[0])
    initial = np.conj(spin_coeffs[spin_coeffs_mapping[b_idx, k_idx]])

    for i in range(band_mask.shape[0]):
        final = spin_coeffs[spin_coeffs_mapping[band_mask[i], kpoint_mask[i]]]
        sum_ = 0j
        for j in range(final.shape[0]):
            sum_ += initial[j, 0] * final[j, 0] + initial[j, 1] * final[j, 1]
        res[i] = abs(sum_) ** 2

    return res


def _interpolate_zero_rates(
    rates, kpoints, masks: Optional = None, progress_bar: bool = defaults["print_log"]
):
    # loop over all scattering types, doping, temps, and bands and interpolate
    # zero scattering rates based on the nearest k-point
    logger.info("Interpolating missing scattering rates")
    n_rates = sum([np.product(rates[spin].shape[:-1]) for spin in rates])
    if progress_bar:
        pbar = get_progress_bar(total=n_rates, desc="progress")
    else:
        pbar = None

    t0 = time.perf_counter()
    k_idx = np.arange(len(kpoints))
    for spin in rates:
        for s, d, t, b in np.ndindex(rates[spin].shape[:-1]):

            if masks is not None:
                mask = np.invert(masks[spin][s, d, t, b])
            else:
                mask = [True] * len(rates[spin][s, d, t, b])

            non_zero_rates = rates[spin][s, d, t, b, mask] > 1e7
            # non_zero_rates = rates[spin][s, d, t, b, mask] != 0
            zero_rate_idx = k_idx[mask][~non_zero_rates]
            non_zero_rate_idx = k_idx[mask][non_zero_rates]

            if not np.any(non_zero_rates):
                # all scattering rates are zero so cannot interpolate
                # generally this means the scattering prefactor is zero. E.g.
                # for POP when studying non polar materials
                rates[spin][s, d, t, b, mask] += small_val

            elif np.sum(non_zero_rates) != np.sum(mask):
                # seems to work best when all the kpoints are +ve therefore add 0.5
                # Todo: Use cartesian coordinates?
                # interpolate log rates to avoid the bias towards large rates
                rates[spin][s, d, t, b, zero_rate_idx] = np.exp(
                    griddata(
                        points=kpoints[non_zero_rate_idx] + 0.5,
                        values=np.log(rates[spin][s, d, t, b, non_zero_rate_idx]),
                        xi=kpoints[zero_rate_idx] + 0.5,
                        method="nearest",
                    )
                )
                # rates[spin][s, d, t, b, zero_rate_idx] = 1e15

            if pbar is not None:
                pbar.update()

    if pbar is not None:
        pbar.close()
    log_time_taken(t0)

    return rates


def get_fine_mesh_qpoints(
    intersections,
    basis,
    cond_a_mask,
    cond_b_mask,
    cond_c_mask,
    high_tol=0.1,
    med_tol=0.2,
    cross_section_weights=None,
):
    if cross_section_weights is None:
        cross_section_weights = np.ones(len(intersections))

    # minimum norm in each intersection
    all_norms = np.linalg.norm(intersections, axis=-1)

    # intersections now has shape nvert, ntet, 2 (i.e., x, y coords)
    intersection_idxs = np.arange(len(intersections))
    z_coords = intersections[:, 0, 2]
    intersections = intersections[:, :, :2].transpose(1, 0, 2)
    triangle_mask = cond_a_mask | cond_c_mask

    # have to do these separately as the triangle intersections always have [0, 0, 0]
    # as the last coordinate
    norms = np.ones(len(all_norms))
    norms[triangle_mask] = np.min(all_norms[:, :3][triangle_mask], axis=-1)
    norms[cond_b_mask] = np.min(all_norms[cond_b_mask], axis=-1)

    qpoints = []
    qweights = []
    mapping = []  # maps a qpoint to an intersection index

    def _get_tri_mesh(prec, min_norm, max_norm):
        scheme = ni[prec]["triangle"]
        mask = (min_norm <= norms) & (norms < max_norm) & triangle_mask
        if not np.any(mask):
            return

        simplex = intersections[:3, mask]
        vol = quadpy.tn.get_vol(simplex)
        xy_coords = quadpy.tn.transform(scheme.points, simplex.T)
        weights = (
            scheme.weights[None] * vol[:, None] * cross_section_weights[mask][:, None]
        )

        qpoints.append(get_q(xy_coords, z_coords[mask]))
        qweights.append(weights.reshape(-1))
        mapping.append(np.repeat(intersection_idxs[mask], len(scheme.weights)))

    def _get_quad_mesh(prec, min_norm, max_norm):
        scheme = ni[prec]["quad"]
        mask = (min_norm <= norms) & (norms < max_norm) & cond_b_mask
        if not np.any(mask):
            return

        cube = intersections.reshape((2, 2, -1, 2))[:, :, mask]
        # 4 is taken from quadpy CnScheme.integrate
        # ref_vol = 2 ** numpy.prod(len(ncube.shape) - 1) which for quadrilaterals = 4
        vol = 4 * np.abs(quadpy.cn._helpers.get_detJ(scheme.points, cube))
        xy_coords = quadpy.cn.transform(scheme.points, cube).T
        weights = scheme.weights[None] * vol * cross_section_weights[mask][:, None]

        qpoints.append(get_q(xy_coords, z_coords[mask]))
        qweights.append(weights.reshape(-1))
        mapping.append(np.repeat(intersection_idxs[mask], len(scheme.weights)))

    _get_tri_mesh("high", 0, high_tol)
    _get_tri_mesh("medium", high_tol, med_tol)
    _get_tri_mesh("low", med_tol, np.Inf)
    _get_quad_mesh("high", 0, high_tol)
    _get_quad_mesh("medium", high_tol, med_tol)
    _get_quad_mesh("low", med_tol, np.Inf)

    qpoints = np.concatenate(qpoints)
    qweights = np.concatenate(qweights)
    mapping = np.concatenate(mapping)

    return get_kpoints_in_original_basis(qpoints, basis[mapping]), qweights, mapping


def get_kpoints_in_original_basis(q, basis):
    # transform k back to original lattice basis in cartesian coords
    return np.einsum("ikj,ij->ik", basis, q)


def get_q(x, z_coords):
    z = np.repeat(z_coords[:, None], len(x[0][0]), axis=-1)
    return np.stack([x[0], x[1], z], axis=-1).reshape(-1, 3)


def _get_fd(energy, fermi_levels, temperatures):
    f = np.zeros(fermi_levels.shape)

    for n, t in np.ndindex(fermi_levels.shape):
        f[n, t] = fd(energy, fermi_levels[n, t], temperatures[t] * boltzmann_au)
    return f
