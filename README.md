Projekt 1 - informatyka geodezyjna 2 


### Wymagania techniczne aby program działał poprawnie:

- system operacyjny Windows 10 lub Windows 11
- python 3.11.5
- biblioteka numpy oraz biblioteka argparse


### Transformacje zawarte w projekcie:
 
- XYZ ===> FLH
- FLH ===> XYZ
- XYZ ===> NE
- FL ===> PL1992
- FL ===> PL2000


### Transformacje dostępne są na elipsoidach:

- GRS80
- WGS84


### Opis działania programu:

1. Program wymaga podania przez użytkownika danych, na podstawie kolejnych flag

- nazwę elipsoidy odniesienia (z wypisanych powyżej)
- ścieżkę do pliku z danymi do transformacji (np. C:\Users\Asus\Documents\2 rok\IV sem\Infa II\plik_dane_flh2XYZ.txt)
  UWAGA! dane w pliku muszą być oddzielone od siebie przecinkami odpowiednio 
  w ilości kolumn 2 lub 3 w zależności ile współrzędnych mają naszej dane 
- transformacje, które chcemy wykonać (XYZ2flh, flh2XYZ, fl22000, fl21992, XYZ2NEU)
- ilość linijek nagłówka z pliku z danymi, które chcemy pominąć (liczba całkowita)

2. po wyborze powyższych wartości i załadowaniu pliku z danymi do transformacji utworzy się plik tekstowy który będzie zawierał wyniki wykonanych transformacji, a na konsoli powienien pjawić się komunikat który mówi że plik zapisano
  
3. plik będzie posiadał nazwę WYNIK_{funckja}_{elipsoida}.txt  -{funkcja} jest to funkcja którą chceliśmy wkonać a -{elipsoida) jest to model elipsoidy, której użyliśmy do obliczeń. Plik zostanie utworzony w tym samym folderze, w którym znajduję się nasz program. Wyniki będą w 2 lub 3 kolumnach o wartościach po kolei jak mamy w nazwie transformacji

### PRZYKŁADOWE WYWOŁANIE ZA POMOCĄ WIERSZA POLECEŃ

1. Użytkownik musi otworzyć terminal a następnie przejść w nim do folderu, w którym znajduję się program np.
   C:\User\asus\Desktop\program

2. Aby uruchomić program należy wpisać: python proj.py a następnie nacisnąć ENTER
   
3. Aby ułatwić użytkownikowi wpisanie po kolei odpowiednich flag, pojawią się polecenia co trzeba wpisać tak jak pokazano poniżej:
```
   -Podaj nazwę elipsoidy: GRS80
   
   -Wklej scieżkę do pliku txt z danymi: C:\Users\Asus\Documents\2 rok\IV sem\Infa II\plik_dane_XYZ2flh.txt
   
   -Podaj nazwę tranformacji, której chcesz użyć: XYZ2flh
   
   -Podaj ile linijek nagłówka pliku z danymi należy pominąć: 2
```
 5. Po poprawnym wypisaniu flag pojawi się komunikat:
    -Plik z wynikami został utworzony
    oraz:
    -Czy chcesz spróbować jeszcze raz? TAK/NIE:
    gdzie po wpisaniu TAK możemy ponownie wpisywać flagi jak w podpunkcie 3 aby wykonać inną transformację, a po wpisaniu 
    NIE program zakończy pracę a użytkownik zobaczy komunikat: 
    "Dziękujemy za skorzystanie z naszego programu."

### OPIS PLIKU Z DANYMI WEJŚCIOWYMI I WYJŚCIOWYMI

- Tranformacja XYZ2flh

Przykładowy plik z danymi wejściowymi "dane_XYZ2flh.txt":

```
Współrzedne geocentryczny ECEF stacji pemanentnej GNSS
Obserwatorium Astronomiczno-Geodezyjne w Józefosławiu
  X[m]         Y[m]        Z[m]
# -----------------------------------------------------
3664940.500,1409153.590,5009571.170
3664940.510,1409153.580,5009571.167
3664940.520,1409153.570,5009571.167
3664940.530,1409153.560,5009571.168
3664940.520,1409153.590,5009571.170
3664940.514,1409153.584,5009571.166
3664940.525,1409153.575,5009571.166
3664940.533,1409153.564,5009571.169
3664940.515,1409153.590,5009571.170
3664940.514,1409153.584,5009571.169
3664940.515,1409153.595,5009571.169
3664940.513,1409153.584,5009571.171
```

Ma on 4 linijki nagłówka, które można ominąc, gdy użytkownik wpisze "4" po fladze "Podaj ile linijek nagłówka pliku z danymi należy pominąć:"
Jak widać dane są oddzielone przecinkami i tylko w takim formacie program je poprawnie pobierze.

Przykładowy plik z danymi wyjściowymi "Wynik_XYZ2flh_GRS80.txt":

```
52.09727 21.03153 141.39866
52.09727 21.03153 141.39982
52.09727 21.03153 141.40335
52.09727 21.03153 141.40767
52.09727 21.03153 141.41013
52.09727 21.03153 141.40221
52.09727 21.03153 141.40653
52.09727 21.03153 141.41106
52.09727 21.03153 141.40726
52.09727 21.03153 141.40458
52.09727 21.03153 141.40758
52.09727 21.03153 141.40558
```
Dane po tej transformacji wyglądają następująco: są oddzielone spacją odpowiednio w kolejności szerokość geodezyjna, długość geodezyjna (obie w stopniach) i wysokość (w metrach).

- Tranformacja flh2XYZ

Przykładowy plik z danymi wejściowymi "dane_flh2XYZ.txt":

```
  Współrzędne elipsoidalne fi, lambda, h
52.2297,21.0122,78.000
52.1298,21.0123,78.100
52.2296,20.0121,77.900
51.6299,21.0124,78.200
51.2297,22.0120,78.050
50.5295,22.0119,78.150
51.2300,21.7125,78.000
52.2294,21.0122,77.950
53.4301,24.6126,78.250
54.2293,21.0118,77.800
52.2298,20.0127,78.300
52.2097,21.0128,77.850
```
Ma on 1 linijkę nagłówka, którą można ominąć, gdy użytkownik wpisze "1" po fladze "Podaj ile linijek nagłówka pliku z danymi należy pominąć:"
Również dane są oddzielone przecinkami jak w poprzednim przykładzie.

Przykładowy plik z danymi wyjściowymi "Wynik_XYZ2flh_GRS80.txt":

```
3654515.722 1403730.043 5018560.041
```
Niestety plik z wynikami pokazuje nam tylko wynik pierwszej linijki, jest to błąd, którego nie udało nam się rozwiązać

- Transformacja XYZ2NEU
Przykładowy plik z danymi wejściowymi "dane_XYZ2NEU.txt":

```
3673602.0707659787,1410163.7139986877,5002803.345368741
2.234878304399999976e+07,1.470313728000000119e+07,3.847713999999999942e+04
-2.391130946000000089e+07,-1.089180339500000142e+07,-2.229962486000000034e+06
1.256775858699999936e+07,1.288512925399999879e+07,1.944924987600000203e+07
1.982159728800000250e+07,3.882086669999999925e+06,1.731373310199999809e+07
-5.921297010999999940e+06,-2.445428761199999973e+07,-8.484889633000001311e+06
```
W pierwszym wierszu znajdują się kolejno współrzędne X[m], Y[m], Z[m] odbiornika na Ziemi. Natomiast w pozostałych wierszach pierwsza wartość to współrzędna X satelity[m], druga to współrzędna Y satelity[m], a trzecia to współrzędna Z satelity[m].

Przykładowy plik z danymi wyjściowymi "Wynik_XYZ2NEU_GRS80.txt":

```
-20549047.679 5717473.618 9754855.210
19314544.051 -1599327.517 -24268687.235
-889561.130 7525422.589 19027805.115
-4998318.921 -3479185.048 19527908.835
6058904.131 -20708041.190 -21849862.779
```

- Transformacja fl22000
Przykładowy plik z danymi wejściowymi "dane_2000_92.txt":

```
52.2297,21.0122
50.0647,19.9450
54.3722,18.6386
51.1079,17.0385
51.7592,19.4550
```
Kolejno wypisane są współrzędne fi i lambda

Przykładowy plik z danymi wyjściowymi "Wynik_fl22000_GRS80.txt":

```
5788456.487 7500833.512
5548149.630 7424469.100
6027068.915 6541498.772
5664093.136 6432667.451
5737111.071 6600451.534
```
Wynikami są współrzędne X[m] i Y[m] w układzie PL-2000

- Transformacja fl21992
Przykładowy plik z danymi wejściowymi "dane_2000_92.txt":

```
52.2297,21.0122
50.0647,19.9450
54.3722,18.6386
51.1079,17.0385
51.7592,19.4550
```
Kolejno wypisane są współrzędne fi i lambda

Przykładowy plik z danymi wyjściowymi "Wynik_fl21992_GRS80.txt":

```
486757.210 637382.204
244587.532 567613.619
723186.065 476529.315
361953.836 362728.675
432633.243 531393.816
```
Wynikami są współrzędne X[m] i Y[m] w układzie PL-1992

Mimo obecności w kodzie parametrów elipsoidy Krasowskiego, nie udało nam się zimplementować poprawnych transformacji, które biorą pod uwagę tą elipsoidę.

