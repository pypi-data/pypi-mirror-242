from abc import ABC, abstractmethod
from multimethod import multimethod
from .obstacle import RectangleObstacle
import numpy as np


class Geometry(ABC):
    @multimethod
    def distance(self, x1: np.ndarray, x2: np.ndarray):
        if x1.shape != x2.shape:
            raise ValueError("points should have the same shape")
        self._check_points_shape(x1)
        self._check_points_shape(x2)
        return self._distance_point_to_point(x1, x2)

    @multimethod
    def distance(self, x: np.ndarray, obs: RectangleObstacle):
        self._check_points_shape(x)
        return self._distance_point_to_rectangle(x, obs)

    @abstractmethod
    def position(self, x: np.ndarray):
        pass

    @abstractmethod
    def _distance_point_to_point(self, x1: np.ndarray, x2: np.ndarray):
        pass

    @abstractmethod
    def _distance_point_to_rectangle(self, x: np.ndarray, obs: RectangleObstacle):
        pass

    def _check_points_shape(self, x: np.ndarray):
        # Check if the shape of x is (N, 2) where N != 0
        if x.shape != (x.shape[0], 2) or x.shape[0] == 0:
            raise ValueError("points should have shape (N, 2) where N != 0")


class Euclidean(Geometry):
    def position(self, x: np.ndarray):
        return x

    def _distance_point_to_point(self, x1: np.ndarray, x2: np.ndarray):
        return x1 - x2

    def _distance_point_to_rectangle(self, x: np.ndarray, obs: RectangleObstacle):
        closest_x = np.clip(x[:, 0], obs.x1, obs.x2)
        closest_y = np.clip(x[:, 1], obs.y1, obs.y2)
        return x - np.column_stack((closest_x, closest_y))


class EuclideanXPeriodic(Euclidean):
    def __init__(self, x: float, dx: float):
        self._x = x
        self._dx = dx
        super().__init__()

    def position(self, x: np.ndarray):
        return (x - self._x) % self._dx + self._x

    def _distance_point_to_point(self, x1: np.ndarray, x2: np.ndarray):
        d = x1 - x2
        d[:, 0] = np.fmod(d[:, 0], self._dx)  # Keeps the sign, not as np.mod
        d[:, 0] = np.where(d[:, 0] > self._dx / 2, d[:, 0] - self._dx, d[:, 0])
        d[:, 0] = np.where(d[:, 0] < -self._dx / 2, d[:, 0] + self._dx, d[:, 0])
        return d

    def _distance_point_to_rectangle(self, x: np.ndarray, obs: RectangleObstacle):
        d = super()._distance_point_to_rectangle(x, obs)
        w = self._dx - obs.width
        d[:, 0] = np.fmod(d[:, 0], self._dx)  # Keeps the sign, not as np.mod
        d[:, 0] = np.where(d[:, 0] > w / 2, d[:, 0] - w, d[:, 0])
        d[:, 0] = np.where(d[:, 0] < -w / 2, d[:, 0] + w, d[:, 0])
        return d
