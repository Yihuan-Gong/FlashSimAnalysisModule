from enum import Enum

class VelocityFilteringField(Enum):
    Vtotal = 0
    turbVtotal = 1
    compVtotal = 2
    soleVtotal = 3
    turbCompVtotal = 4
    turbSoleVtotal = 5
    scale = 6
    