Projekt 1 - informatyka geodezyjna 2 


### Wymagania techniczne aby program działał poprawnie:

-system operacyjny Windows 10 lub Windows 11

-python 3.11.5

-biblioteka numpy oraz biblioteka argparse



### Transformacje zawarte w projekcie:
 
-XYZ ===> FLH

-FLH ===> XYZ

-XYZ ===> NEU

-FL ===> PL1992

-FL ===> PL2000


###Transformacje dostępne są na elipsoidach:

-GRS80

-WGS84

-KRASOWSKIEGO


### Opis działania programu:

1. Program wymaga podania przez użytkownika danych, na podstawie kolejnych flag
<<<<<<<
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

###OPIS PLIKU Z DANYMI WEJŚCIOWYMI I WYJŚCIOWYMI

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

