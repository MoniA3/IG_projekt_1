# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 17:06:41 2024

@author: user
"""

from math import *
import numpy as np


class Transformations:
    def __init__(self, model: str = "WGS84"):
        """
        Parametry elipsoid:
            a - duża półoś elipsoidy
            b - mała półoś elipsoidy 
            flat - spłaszczenie
            ecc2 - mimośród^2
        """
        if model == "WGS84":
            self.a = 6378137.0 
            self.b = 6356752.31424518
        elif model == "GRS80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        elif model == "MARS":
            self.a = 3396900.0
            self.b = 3376097.80585952
        else:
            raise NotImplementedError(f"{model} model not implemented")
        self.flat = (self.a - self.b) / self.a
        self.ecc = sqrt(2 * self.flat - self.flat ** 2) 
        self.ecc2 = (2 * self.flat - self.flat ** 2)
        
        """fukcje które są niezbędne do transformacji"""
        
        def Npu(self, fi):    
            N = self.a / np.sqrt(1 - self.e2 * np.sin(fi)**2)
            return(N)

        def Sigma(self, fi):
            A0 = 1 - (self.e2/4) - (3*(self.e2)**2)/64 -  (5*(self.e2)**3)/256
            A2 = 3/8 * (self.e2 + (self.e2)**2/4 + 15*(self.e2)**3/128)
            A4 = 15/256 * ( (self.e2)**2 + (3*((self.e2)**3))/4 )
            A6 = 35 * (self.e2)**3 / 3072
            sigma = self.a * ( A0 * fi - A2 * np.sin(2*fi) + A4 * np.sin(4*fi) - A6 * np.sin(6*fi) )
               
            return(sigma)