from dataclasses import dataclass
from typing import Tuple

@dataclass(kw_only=True)
class VelocityFieldModel:
    velxFieldName: Tuple[str, str] = ("gas", "velocity_x")
    velyFieldName: Tuple[str, str] = ("gas", "velocity_y")
    velzFieldName: Tuple[str, str] = ("gas", "velocity_z")

