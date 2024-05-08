# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 17:06:41 2024

@author: user
"""

from math import *
import numpy as np
from argparse import ArgumentParser


class Transformacje:
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
        elif model == "KRASOWSKI":
            self.a = 6378245.0
            self.b = 6356863.019
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
        
    def XYZ2flh(self, X, Y, Z):   # Algorytm Hirvonena
       flh = []
       for x, y, z in zip(X, Y, Z):
           r = np.sqrt(x**2 + y**2)  # promień
           fi = np.arctan(z / (r * (1 - self.e2)))
           while True:
               N = self.Np(fi)
               h = (r / np.cos(fi)) - N
               fp = fi
               fi = np.arctan(z / (r * (1 - self.e2 * N / (N + h))))
               if abs(fp - fi) < (0.000001 / 206265):
                   break
           l = np.arctan2(y, x)
           flh.append([np.rad2deg(fi), np.rad2deg(l), h])
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
        

    def XYZ2NEU(self, X, Y, Z, X0, Y0, Z0):
        wynik = []
        fi, lam, _ = [radians(coord) for coord in self.XYZ2flh(X0, Y0, Z0)]
        R_neu = np.array([[-np.sin(fi)*np.cos(lam), -np.sin(lam), np.cos(fi)*np.cos(lam)],
                          [-np.sin(fi)*np.sin(lam), np.cos(lam), np.cos(fi)*np.sin(lam)],
                          [np.cos(fi), 0, np.sin(fi)]])
        r = np.sqrt(X0**2+Y0**2)
        f = np.arctan(Z0/(r*(1-self.e2)))
        while True:
            N = self.Np(f)
            h = (r/np.cos(f))-N
            fp = f
            f = np.arctan(Z0/(r*(1-self.e2 * N/(N+h))))
            if abs(fp-f)<(0.000001/206265):
                break
        l = np.arctan2(Y0,X0)
        N = self.Np(f)
        h = r / cos(f) - N
            
        #R_neu = self.Rneu(fi, lam)
        for X, Y, Z in zip(X, Y, Z):
            X_sr = [X-X0, Y-Y0, Z-Z0] 
            X_rneu = R_neu.T @ X_sr
            result.append(X_rneu.T)
            
        return wynik
        
        
    """Tranformacja współrzędnych elipsoidalnych fi, lambda do współrzędnych w układzie 2000"""
          
    def fl22000(self, fi, lam):
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
                continue
                         
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
        
    def fl21992(self, fi, lam):
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

    """wczytywanie danych oraz funckcji z pliku """
        
    def wczytywanie(self, plik, transformacja, naglowek):
        if transformacja == "XYZ2flh":
            dane = np.genfromtxt(plik, delimiter=",", skip_header=naglowek)
            flh = self.XYZ2flh(dane[:, 0], dane[:, 1], dane[:, 2])
            np.savetxt(f"Wynik_{transformacja}.txt", flh, delimiter=";")
        elif transformacja == "flh2XYZ":
            dane = np.genfromtxt(plik, delimiter=",", skip_header=naglowek)
            xyz = self.flh2XYZ(np.deg2rad(dane[:, 0]), np.deg2rad(dane[:, 1]), dane[:, 2])
            np.savetxt(f"Wynik_{transformacja}.txt", xyz, delimiter=";")
        elif transformacja == "XYZ2NEU":
            dane = np.genfromtxt(plik, delimiter=",", skip_header=naglowek)
            neu = self.XYZ2NEU(dane[1:, 0], dane[1:, 1], dane[1:, 2], dane[0, 0], dane[0, 1], dane[0, 2])
            np.savetxt(f"WYNIK_{transformacja}.txt", neu, delimiter=";")
        elif transformacja == "fl22000":
            dane = np.genfromtxt(plik, delimiter=",", skip_header=naglowek)
            u2000 = self.fl22000(np.deg2rad(dane[:, 0]), np.deg2rad(dane[:, 1]))
            np.savetxt(f"WYNIK_{transformacja}.txt", u2000, delimiter=";")
        elif transformacja == "fl21992":
            dane = np.genfromtxt(plik, delimiter=",", skip_header=naglowek)
            u1992 = self.fl21992(np.deg2rad(dane[:, 0]), np.deg2rad(dane[:, 1]))
            np.savetxt(f"WYNIK_{transformacja}.txt", u1992, delimiter=";")
                
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-dane', type=str, help='Wpisz nazwę wraz z rozszerzeniem pliku z danymi wejsciowymi')
    parser.add_argument('-model', type=str, help='Wybierz elipsoide sposrod dostepnych: WRS84, GRS80, KRASOWSKI')
    parser.add_argument('-transformacja', type=str, help='Wybierz transformacje, z ktorej chcesz skorzystac, sposrod dostepnych: XYZ2flh, flh2XYZ, XYZ2neu, GK2000, GK1992, XYZ2NEU')
    parser.add_argument('-naglowek', type=int, help='Wpisz ile linijek nagłówka w pliku z danymi należy pominąć')
    args = parser.parse_args()
    model = {'WGS84': [6378137.000, 6356752.31424518], 'GRS80': [6378137.000, 6356752.31414036], 'KRASOWSKI': [6378245.000, 6356863.019]}
    transformacje = {'XYZ2flh': 'XYZ2flh', 'flh2XYZ': 'flh2XYZ','XYZ2NEU': 'XYZ2NEU', 'fl22000': 'fl22000', 'fl21992': 'fl21992'}
    
    wybor='TAK'
    # try:
    #     wsp = Transformacje(model[args.model])
    #     koniec = wsp.wczytywanie(args.plik, args.transformacje.upper())
    #     print("Utworzono plik ze wspolrzednymi.")
    # except AttributeError as e:
    #     print("Error:", e)    
    # except FileNotFoundError:
    #     print("Nie znaleziono podanego pliku")
    # except KeyError:
    #     print("Niepoprawna nazwa Elipsoidy lub Transformacji")
    # except IndexError:
    #     print("Dane w podanym pliku sa w nieodpowiednim formacie")
    # except ValueError:
    #     print("Dane w podanym pliku są w nieodpowiednim formacie. Prosimy wprowadzic dane w formacie jak podano w przykładzie")
    # finally:
    #     print("Dziękujemy za użycie naszego programu:)")


    try:
        while wybor =="TAK":
            if args.model==None:
                args.model = input(str('Podaj nazwe elipsoidy: '))
            if args.dane==None:
                args.dane = input(str('Wklej sciezke do pliku txt z danymi: '))
            if args.transformacja==None:
                args.transformacja = input(str('Podaj nazwę tranformacji, którą chcesz wykonać: '))
                
                obiekt = Transformacje(model[args.el.upper()])
                dane = obiekt.odczyt(args.dane, transformacje[args.t.upper()])
            
            print('Plik z wynikami zostal utworzony.')
            
            wybor = input(str("Jezeli chcesz wykonac kolejna transformacje wpisz TAK jesli chcesz zakonczyc KONIEC: ")).upper()
            args.model = None
            args.dane= None
            args.transformacja= None

    except FileNotFoundError:
        print('Podany plik nie istnieje.')
    except KeyError:
        print('Zle podana elipsoida lub transformacja.')
    except IndexError:
        print('Zly format danych w pliku.')
    except ValueError:
        print('Zly format danych w pliku.')
    finally:
        print('Koniec programu')