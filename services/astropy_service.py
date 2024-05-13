from typing import List
from astropy import units as u
import numpy as np


class AstropyService:
    def quantityListToQuantity(self, quantityList: List[u.Quantity]):
        return np.array([q.value for q in  quantityList])*quantityList[0].unit