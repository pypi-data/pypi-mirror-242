from abc import ABC, abstractmethod
import numpy as np
from .solver import Walkers


class VdCalculator(ABC):
    @abstractmethod
    def __call__(self, walkers: Walkers) -> np.ndarray:
        """"""
        pass


class RectangleVelocityBooster(VdCalculator):
    def __init__(
        self,
        x: float,
        y: float,
        dx: float,
        dy: float,
        vdx: float,
        vdy: float,
        types_mask: int = 0xFFFF,
    ) -> None:
        """"""
        self._x1 = min(x, x + dx)
        self._x2 = max(x, x + dx)
        self._y1 = min(y, y + dy)
        self._y2 = max(y, y + dy)
        self._vdx = vdx
        self._vdy = vdy
        self._types_mask = types_mask

    def __call__(self, walkers: Walkers) -> np.ndarray:
        x = walkers.x
        types = walkers.types
        speeds = walkers.speeds
        mask = (
            (x[:, 0] > self._x1)
            & (x[:, 0] < self._x2)
            & (x[:, 1] > self._y1)
            & (x[:, 1] < self._y2)
        )

        if types is not None:
            mask &= np.bitwise_and(types, self._types_mask) != 0x0000
        # mask = np.broadcast_to(mask[:, np.newaxis], x.shape)
        vds = np.asarray([[self._vdx, self._vdy]])
        if speeds is not None:
            vds = vds * speeds[:, np.newaxis]
        return np.where(mask[:,np.newaxis], vds, np.zeros((1,2)))
