Projekt 1 - informatyka geodezyjna 2 

Wymagania techniczne aby program działał poprawnie 
''''
'system operacyjny Windows 10 lub Windows 11'
'python 3.11.5'
'biblioteka numpy oraz biblioteka argparse'
''''
Transformacje zawarte w projekcie 
'''
'XYZ ===> FLH'
'FLH ===> XYZ'
'XYZ ===> NEU'
'FL ===> PL1992'
'FL ===> PL2000'
'''
transformacje dostępne są na elipsoidach 
GRS80
WGS84
KRASOWSKIEGO

opis działania programu 
1. program przyjmuje z pliku dane do transformacji, elipsoide odniesienia oraz jaką transformacje chcemy wykonać
2. po wyborze powyższych wartości i załadowaniu pliku z danymi do transformacji utworzy się plik tekstowy który będzie zawierał wyniki wykonanych transformacji, a na konsoli powienien pjawić się komunikat który mówi że plik zapisano
3. plik będzie posiadał nazwę WYNIK_{funckja}.txt  -{funkcja} jest to funkcja którą chceliśmy wkonać
 
