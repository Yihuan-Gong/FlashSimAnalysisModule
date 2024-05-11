from astropy import units as u
from dataclasses import dataclass
from typing import Tuple, Protocol
from typing_extensions import runtime_checkable

@dataclass
@runtime_checkable
class Data2dAxisReturnModel(Protocol):
    horizontalAxis: Tuple[str, u.Quantity]
    verticalAxis: Tuple[str, u.Quantity]