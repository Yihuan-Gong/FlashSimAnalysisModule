from dataclasses import dataclass
from typing import Tuple, Protocol
from typing_extensions import runtime_checkable


@dataclass(kw_only=True)
@runtime_checkable
class CoordinateModel(Protocol):
    cellCoorField: Tuple[str, str] = ("gas", "x")
    cellCoorUnit: str = "kpc"

