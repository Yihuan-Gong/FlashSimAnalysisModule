from dataclasses import dataclass
from typing import Tuple


@dataclass(kw_only=True)
class CoordinateModel:
    cellCoorField: Tuple[str, str] = ("gas", "x")
    cellCoorUnit: str = "kpc"

