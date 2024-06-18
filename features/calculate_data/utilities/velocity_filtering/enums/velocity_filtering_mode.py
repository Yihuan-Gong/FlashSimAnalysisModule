from enum import Enum

class VelocityFilteringMode(Enum):
    Total = 0
    BulkTurb = 1
    CompSole = 2
    TurbCompSole = 3
    Simonte = 4