# Tema 1 - ASC - Pisică Alin-Georgian

## 1. Organizare

Tema are ca scop simularea unui marketplace, bazandu-se pe problema
producer-consumer. Astfel, fiecare producator dispune de o cantitate
limitata de produse ce pot fi introduse simultan in cadrul 
marketplace-ului.

Solutia aleasa are la baza principiile multi-threading, depinzand de 
doar doua elemente cheie de sincronizare: un lock pentru crearea 
cosurilor de cumparaturi specifice consumatorilor, si un lock pentru
efectuarea operatiilor in cadrul cosurilor (explicate in detaliu in 
sectiunea _2. Implementare_).

Consider ca tema este utila pentru familiarizarea cu limbajul python,
insa nu o consider ca fiind cea mai eficienta metoda de aprofundare a 
multithreading-ului. Comentariile, todo-urile, cat si structura claselor
orienteaza dezvoltarea in mare parte intr-o singura directie, cu un numar
mare de hint-uri, partea de creativitate si gandire neramanand la 
latitudinea studentului.

## 2. Implementare

In vederea implementarii, am urmarit todo-urile din schelet. Astfel, voi
evita explicarea codului propriu zis si ma voi axa pe elementele de 
sincronizare folosite, cat si probleme intampinate si cum au fost
rezolvate.

Exceptand operatiile de _create cart_, _add to cart_ si _remove from
cart_, nu am avut nevoie nevoie de elemente de sincronizare (lock-uri,
bariere) deoarece operatiile (append) au fost efectuate asupra unor liste,
iar acestea sunt deja thread-safe.

### Lock-ul de creare a cart-urilor

In prima faza am incercat rezolvarea temei fara lock-ul mentionat, insa,
din cauza generarii id-urilor, apareau momente in care id-urile carturilor
erau generate aleator. Astfel, am decis stocarea id-ului cosului ce urmeaza
a fi creat intr-o variabila in cadrul clasei Marketplace, lucru ce a dus
la aparitia lock-ului -> pentru a putea face operatiile de incrementare
in mod corect si sigur.

### Lock-ul pentru adaugare si stergere din cos

Din moment ce adaugarea si stergerea produselor din cos aduc, de la sine,
si modificarea lungimilor cozilor fiecarui producator, este necesara
folosirea unui lock pentru a asigura continuitatea si corectitudinea
incrementarilor si decrementarilor lungimilor.

## 3. Resurse utilizate

Pentru confirmarea faptului ca listele sunt thread-safe in python, am
recurs la [Are lists thread-safe?](https://stackoverflow.com/questions/6319207/are-lists-thread-safe).

Pentru a intelege concepetele de marketplace generale, nelimitandu-ma
doar la tema curenta, am aprofundat si standardul [OpenRTB](https://www.iab.com/guidelines/openrtb/).

Pentru utilizarea lock-urilor m-am folosit de [Laboratorul 03](https://ocw.cs.pub.ro/courses/asc/laboratoare/03).

## 4. Git

https://github.com/alinp25/Tema1ASC

Voi face repository-ul public dupa ce se va finaliza deadline-ul hard.