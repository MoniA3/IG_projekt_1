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
            flat - biegunowe spłaszczenie elipsoidy
            e2 - mimośród^2
        """
        if model == "WGS84":
            self.a = 6378137.0 
            self.b = 6356752.31424518
        elif model == "GRS80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        elif model == "KRASOWSKI":
            self.a = 6378245.0
            self.b = 6356863.019
        else:
            raise NotImplementedError(f"Program nie obsługuje tej elipsoidy")
        self.flat = (self.a - self.b) / self.a  
        self.e = sqrt(2 * self.flat - self.flat ** 2) 
        self.e2 = (2 * self.flat - self.flat ** 2)
        
        """Fukcje, które są niezbędne do transformacji"""
        
        def Np(self, fi):    #promień krzywizny w I wertykale
            N = self.a / np.sqrt(1 - self.e2 * np.sin(fi)**2)
            return(N)

        def Sigma(self, fi):
            A0 = 1 - (self.e2/4) - (3*(self.e2)**2)/64 -  (5*(self.e2)**3)/256
            A2 = 3/8 * (self.e2 + (self.e2)**2/4 + 15*(self.e2)**3/128)
            A4 = 15/256 * ( (self.e2)**2 + (3*((self.e2)**3))/4 )
            A6 = 35 * (self.e2)**3 / 3072
            sigma = self.a * ( A0 * fi - A2 * np.sin(2*fi) + A4 * np.sin(4*fi) - A6 * np.sin(6*fi) )
               
            return(sigma)
        
        
        """Tranformacja współrzędnych geocentrycznych XYZ na współrzędne elipsoidalne fi, lambda, h"""
        
        def XYZ2FLH(self, X,Y,Z):   #Algorytm Hirvonena
            result = []
            for X, Y, Z in zip(X,Y,Z):
                r = np.sqrt(X**2 + Y**2) #promień
                f = np.arctan(Z / (r * (1-self.e2)))
                while True:
                    N = self.Np(f)
                    h = (r/np.cos(f)) - N
                    fp = f
                    f = np.arctan(Z / (r * (1-self.e2*N/(N + h))))
                    if abs(fp-f)<(0.000001/206265):
                        break
                l = np.arctan2(Y,X)
                N = self.Np(f)
                h = (p/np.cos(f)) - N
                result.append([np.rad2deg(f), np.rad2deg(l), h])
            return result  
        
        
        
        
        