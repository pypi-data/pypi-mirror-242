import numpy as np
from types import SimpleNamespace
from .walkers import Walkers
from .vdcalculator import VdCalculator
from .obstacle import Obstacle
from .geometry import Geometry, Euclidean


class Solver:
    """
    A class used to represent a Solver

    Attributes
    ----------
    _delta_t : float
        the discrete time step (in seconds) used for the crowd simulation
    _tau : float
        the relaxation time in seconds (default 3)
    _imp: float
        impermeability constant b (default 1)
        impermeability constant rprime (default 0.1)

    Methods
    ----------
    delta_t()
        Returns the float corresponding to the discrete time step (in seconds) used for the crowd simulation
    tau()
        Returns the float corresponding to the relaxation time in seconds (default 3)
    delta_t(delta_t)
        Sets the float corresponding to the discrete time step (in seconds) used for the crowd simulation
    tau(tau)
        Sets the float corresponding to the relaxation time in seconds (default 3)
    """

    def __init__(
        self,
        walkers: Walkers,
        delta_t: float,
        vd_calcs: [VdCalculator],
        obstacles: [Obstacle],
        geometry: Geometry = Euclidean(),
    ) -> None:
        """
        Parameters
        ----------
        delta_t : float
            the discrete time step (in seconds) used for the crowd simulation
        """

        self._walkers = walkers
        self._delta_t = delta_t
        self._vd_calcs = vd_calcs
        self._obstacles = obstacles
        self._geometry = geometry

        # Obstacle interaction constant
        self._obs_constant = float(10)

        # Propulsion constants
        self._tau = float(0.5)

        # Kernel constants
        self._int_constant = float(7)
        self._vel_option = int(1)

        # Iterate constants
        self._current_time = float(0)

        # Propulsion term
        self._f = np.empty(walkers.x.shape)
        self._f.fill(np.nan)

        # Interaction term
        self._ksum = np.empty(walkers.x.shape)
        self._ksum.fill(np.nan)

        # Obstacles term
        self._e = np.empty(walkers.x.shape)
        self._e.fill(np.nan)

        self._ns_e = SimpleNamespace()
        self._ns_k = SimpleNamespace()

    @property
    def walkers(self) -> Walkers:
        return self._walkers

    @property
    def delta_t(self) -> float:
        return self._delta_t

    @property
    def tau(self) -> float:
        return self._tau

    @property
    def int_constant(self) -> float:
        return self._int_constant

    @property
    def vel_option(self) -> int:
        return self._vel_option

    @property
    def current_time(self) -> float:
        return self._current_time

    @property
    def f(self) -> np.ndarray:
        return self._f

    @property
    def ksum(self) -> np.ndarray:
        return self._ksum

    @property
    def e(self) -> np.ndarray:
        return self._e

    @property
    def vd_calcs(self) -> [VdCalculator]:
        return self._vd_calcs

    @property
    def obstacles(self) -> [Obstacle]:
        return self._obstacles

    @property
    def geometry(self) -> Geometry:
        return self._geometry

    @delta_t.setter
    def delta_t(self, delta_t: float) -> float:
        self._delta_t = delta_t
        return self._delta_t

    @tau.setter
    def tau(self, tau: float) -> float:
        self._tau = tau
        return self._tau

    @int_constant.setter
    def int_constant(self, int_constant: float) -> float:
        self._int_constant = int_constant
        return self._int_constant

    @vel_option.setter
    def vel_option(self, vel_option: int) -> int:
        self._vel_option = vel_option
        return self._vel_option

    def __calc_f(self, vd: np.ndarray) -> np.ndarray:
        """
        Calculates propulsion for a desired velocity field vd

        Parameters
        ----------
        vd : ndarray
            the desired velocity field (in meters per second)
        """
        return (vd - self._walkers.u) / self._tau

    def __calc_e(self) -> np.ndarray:
        """Implementation of the private method of the Solver class used to calculate
        the E term of the eq. ■, aimed to the corridor example.
        """
        ns = self._ns_e
        ns.sum = np.zeros(self._walkers.x.shape)

        for obstacle in self._obstacles:
            ns.dist = self._geometry.distance(self._walkers.x, obstacle)
            ns.dist_mag = np.linalg.norm(ns.dist, axis=1)
            ns.dist_mag_br = np.broadcast_to(ns.dist_mag[:, np.newaxis], ns.dist.shape)
            ns.sum += (
                ns.dist
                * self._obs_constant
                * np.exp(-ns.dist_mag_br / obstacle.imp_constant)
                / ns.dist_mag_br
            )

        return ns.sum

    def __calc_k(self, vd: np.ndarray) -> np.ndarray:
        ns = self._ns_k

        ns.A = self._int_constant
        ns.R = self._walkers.int_radius
        ns.theta_max = self._walkers.theta_max

        ns.X = self._walkers.x
        ns.X_mesh = np.broadcast_to(
            ns.X[np.newaxis, :, :], (ns.X.shape[0], *ns.X.shape)
        )
        ns.X_mesh_t = np.broadcast_to(
            ns.X[:, np.newaxis, :], (ns.X.shape[0], *ns.X.shape)
        )
        ns.X_mesh_flat = np.reshape(ns.X_mesh, (-1, 2))
        ns.X_mesh_t_flat = np.reshape(ns.X_mesh_t, (-1, 2))
        ns.dist_vec_flat = self._geometry.distance(ns.X_mesh_t_flat, ns.X_mesh_flat)
        ns.dist_vec_bstack = np.reshape(ns.dist_vec_flat, ns.X_mesh.shape)
        ns.dist_vec_sqr_bstack = np.square(ns.dist_vec_bstack)
        ns.dist_sqr_nstack = (
            ns.dist_vec_sqr_bstack[:, :, 0] + ns.dist_vec_sqr_bstack[:, :, 1]
        )
        ns.dist_sqr_nstack[ns.dist_sqr_nstack == 0.0] = np.nan
        ns.dist_mag_nstack = np.sqrt(ns.dist_sqr_nstack)
        ns.dist_sqr_bstack = np.broadcast_to(
            ns.dist_sqr_nstack[:, :, np.newaxis], (*ns.dist_sqr_nstack.shape, 2)
        )
        ns.dist_mag_bstack = np.broadcast_to(
            ns.dist_mag_nstack[:, :, np.newaxis], (*ns.dist_mag_nstack.shape, 2)
        )

        if self._vel_option == int(0):
            ns.U = vd
        elif self._vel_option == int(1):
            ns.U = self._walkers.u

        ns.vd_vec_bstack = np.broadcast_to(
            ns.U[:, np.newaxis, :], ns.dist_vec_bstack.shape
        )
        ns.U_mag = np.sqrt(np.sum(np.square(ns.U), axis=1))
        ns.vd_mag_nstack = np.broadcast_to(
            ns.U_mag[:, np.newaxis], ns.dist_mag_nstack.shape
        )

        # The distance points TO the i walker, but we need the vector pointing away
        # from it, so we multiply by -1
        ns.prod_org = -1 * ns.dist_vec_bstack * ns.vd_vec_bstack
        ns.prod_dot = ns.prod_org[:, :, 0] + ns.prod_org[:, :, 1]
        ns.prod_mag = ns.dist_mag_nstack * ns.vd_mag_nstack
        ns.prod_mag[ns.prod_mag == 0.0] = np.nan
        ns.theta_org = np.arccos(ns.prod_dot / ns.prod_mag)
        ns.theta = ns.theta_org < ns.theta_max

        ns.theta_bstack = np.broadcast_to(
            ns.theta[:, :, np.newaxis], (*ns.theta.shape, 2)
        )

        ns.k = np.exp((-ns.dist_sqr_bstack) / (ns.R**2))
        ns.k *= ns.dist_vec_bstack / ns.dist_mag_bstack
        ns.k *= ns.theta_bstack
        ns.k *= ns.A
        ns.k = np.nan_to_num(ns.k, copy=False)
        return ns.k

    def __calc_vd(self) -> np.ndarray:
        """"""
        sum = np.zeros(self._walkers.u.shape)
        for vd_calc in self._vd_calcs:
            sum += vd_calc(self._walkers)
        return sum

    def iterate(self) -> None:
        self._walkers.x = self.geometry.position(
            self._walkers.x + self.delta_t * self._walkers.u
        )

        self._vd = self.__calc_vd()
        self._f = self.__calc_f(self._vd)
        self._ksum = np.sum(self.__calc_k(self._vd), axis=1)
        self._e = self.__calc_e()
        self._acc = self._f + self._ksum + self._e

        self._walkers.u = self._walkers.u + self._delta_t * self._acc

        self._current_time = self._current_time + self._delta_t
