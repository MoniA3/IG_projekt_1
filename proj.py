# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 17:06:41 2024

@author: user
"""

from math import *
import numpy as np
from argparse import ArgumentParser


class Transformations:
    def __init__(self, model: str = "WGS84"):
        """
        Parametry elipsoid:
            a - duża półoś elipsoidy
            b - mała półoś elipsoidy 
            f - biegunowe spłaszczenie elipsoidy
            e2 - mimośród^2
        """
        if model == "WGS84":
            self.a = 6378137.0 
            self.b = 6356752.31424518
        elif model == "GRS80":
            self.a = 6378137.0
            self.b = 6356752.31414036
     #  elif model == "KRASOWSKI":
         #  self.a = 6378245.0
         #  self.b = 6356863.019
        else:
            raise NotImplementedError(f"Program nie obsługuje podanej elipsoidy")
        self.f = (self.a - self.b) / self.a  
        self.e = sqrt(2 * self.f - self.f ** 2) 
        self.e2 = (2 * self.f - self.f ** 2)
        
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
        
        def XYZ2flh(self, X,Y,Z):   #Algorytm Hirvonena
            flh = []
            for X, Y, Z in zip(X,Y,Z):
                r = np.sqrt(X**2 + Y**2) #promień
                fi = np.arctan(Z / (r * (1-self.e2)))
                while True:
                    N = self.Np(fi)
                    h = (r/np.cos(fi)) - N
                    fp = fi
                    fi = np.arctan(Z / (r * (1-self.e2 * N/(N + h))))
                    if abs(fp-f)<(0.000001/206265):
                        break
                l = np.arctan2(Y, X)
                N = self.Np(f)
                h = (p/np.cos(f)) - N
                result.append([np.rad2deg(f), np.rad2deg(l), h])
            return flh
        
        
        """Transformacja współrzędnych elipsoidalnych fi, lambda, h na współrzędne geocentryczne XYZ"""
        
        def flh2XYZ(self, fi, lam, h):
            XYZ = []
            for fi, lam, h in zip(fi, lam, h):
                while True:
                    N = self.Np(fi)
                    X = (N + h) * np.cos(fi) * np.cos(lam)
                    Xp = X
                    Y = (N + h) * np.cos(fi) * np.sin(lam)
                    Z = (N * (1 - self.e2) + h) * np.sin(fi)
                    if abs(Xp - X) < (0.000001/206265):
                        break
                XYZ.append([X, Y, Z])
            return(XYZ)
        
        
        """Tranformacja współrzędnych geocentrycznych do współrzędnych topocentrycznych"""
        
        def Rneu(self, fi, lam):
            R = np.array([[-np.sin(fi)*np.cos(lam), -np.sin(lam), np.cos(fi)*np.cos(lam)],
                          [-np.sin(fi)*np.sin(lam), np.cos(lam), np.cos(fi)*np.sin(lam)],
                          [np.cos(fi), 0, np.sin(fi)]])
            return(R)
        

        def XYZ2NEU(self, X, Y, Z, X0, Y0, Z0):
            wynik = []
            r = np.sqrt(X0**2+Y0**2)
            f = np.arctan(Z0/(r*(1-self.e2)))
            while True:
                N = self.Np(f)
                h = (r/np.cos(f))-N
                fp = f
                f = np.arctan(Z0/(r*(1-self.e2*N/(N+h))))
                if abs(fp-f)<(0.000001/206265):
                    break
            l = np.arctan2(Y0,X0)
            N = self.Np(f)
            h = r / cos(f) - N
            
            R_neu = self.Rneu(fi, lam)
            for X, Y, Z in zip(X, Y, Z):
                X_sr = [X-X0, Y-Y0, Z-Z0] 
                X_rneu = R_neu.T @ X_sr
                result.append(X_rneu.T)
                
            return wynik
        
        
        """Tranformacja współrzędnych elipsoidalnych fi, lambda do współrzędnych w układzie 2000"""
          
        def GK2000(self, fi, lam):
            m0 = 0.999923
            wsp2000 = []
            for fi, lam in zip(fi,lam):
                lam0 = 0 
                strefa = 0
                if lam > np.deg2rad(13.5) and lam < np.deg2rad(16.5):
                    strefa = 5
                    lam0 = np.deg2rad(15)
                elif lam > np.deg2rad(16.5) and lam < np.deg2rad(19.5):
                    strefa = 6
                    lam0 = np.deg2rad(18)
                elif lam > np.deg2rad(19.5) and lam < np.deg2rad(22.5):
                    strefa =7
                    lam0 = np.deg2rad(21)
                elif lam > np.deg2rad(22.5) and lam < np.deg2rad(25.5):
                    strefa = 8
                    lam0 = np.deg2rad(24)
                else:
                    print("Punkt poza strefami odwzorowawczymi układu PL-2000")        
                         
                e2prim = (self.a**2 - self.b**2) / self.b**2   #drugi mimosrod elipsy
                dlam = lam - lam0
                t = np.tan(fi)
                n = np.sqrt(e2prim * (np.cos(fi))**2)
                N = self.Np(fi)
                sigma = self.Sigma(fi)
            
                XGK = sigma + ((dlam**2)/2) * N * np.sin(fi)*np.cos(fi) * ( 1+ ((dlam**2)/12)*(np.cos(fi))**2 * ( 5 - (t**2)+9*(n**2) + 4*(n**4)     )  + ((dlam**4)/360)*(np.cos(fi)**4) * (61-58*(t**2)+(t**4) + 270*(n**2) - 330*(n**2)*(t**2))  )
                YGK = (dlam*N* np.cos(fi)) * (1+(((dlam)**2/6)*(np.cos(fi))**2) *(1-(t**2)+(n**2))+((dlam**4)/120)*(np.cos(fi)**4)*(5-18*(t**2)+(t**4)+14*(n**2)-58*(n**2)*(t**2)) )
                         
                X2000 = xgk * m0
                Y2000 = ygk * m0 + strefa*1000000 + 500000
                wsp.append([X2000, Y2000])
                
            return(wsp2000) 
        
        
        """Tranformacja współrzędnych fi, lambda do współrzędnych w układzie 1992"""
        
        def GK1992(self, fi, lam):
            lam0 = (19 * np.pi)/180
            m0 = 0.9993
            wsp1992 = []
            for fi,lam in zip(fi,lam):
                e2prim = (self.a**2 - self.b**2) / self.b**2   #drugi mimosrod elipsy
                dlam = lam - lam0
                t = np.tan(fi)
                n = np.sqrt(e2prim * (np.cos(fi))**2)
                N = self.Np(fi)
                sigma = self.Sigma(fi)
                
                XGK = sigma + ((dlam**2)/2)*N*np.sin(fi)*np.cos(fi) * ( 1+ ((dlam**2)/12)*(np.cos(fi))**2 * ( 5 - (t**2)+9*(n**2) + 4*(n**4) ) + ((dlam**4)/360)*(np.cos(fi)**4) * (61-58*(t**2)+(t**4) + 270*(n**2) - 330*(n**2)*(t**2))  )
                YGK = (dlam*N* np.cos(fi)) * (1+(((dlam)**2/6)*(np.cos(fi))**2) *(1-(t**2)+(n**2))+((dlam**4)/120)*(np.cos(fi)**4)*(5-18*(t**2)+(t**4)+14*(n**2)-58*(n**2)*(t**2)) )
                            
                X1992 = XGK * m0 - 5300000
                Y1992 = YGK * m0 + 500000
                wsp.append([X1992, Y1992]) 
                
            return(wsp1992)
        