Projekt 1 - informatyka geodezyjna 2 

Wymagania techniczne aby program działał poprawnie:

-system operacyjny Windows 10 lub Windows 11

-python 3.11.5

-biblioteka numpy oraz biblioteka argparse


Transformacje zawarte w projekcie:
 
-XYZ ===> FLH

-FLH ===> XYZ

-XYZ ===> NEU

-FL ===> PL1992

-FL ===> PL2000


Transformacje dostępne są na elipsoidach:

-GRS80

-WGS84

-KRASOWSKIEGO


Opis działania programu:
1. program przyjmuje kolejno
   - dane z pliku dane do transformacji
   - elipsoide odniesienia
   - jaką transformacje chcemy wykonać
   - liczbę linijek nagłówka które chcemy pominąć
3. po wyborze powyższych wartości i załadowaniu pliku z danymi do transformacji utworzy się plik tekstowy który będzie zawierał wyniki wykonanych transformacji, a na konsoli powienien pjawić się komunikat który mówi że plik zapisano
4. plik będzie posiadał nazwę WYNIK_{funckja}.txt  -{funkcja} jest to funkcja którą chceliśmy wkonać
 
