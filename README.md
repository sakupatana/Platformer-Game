# **Tasohyppelypeli**

## **Esittely**
Tämä repository kertoo tasohyppelyprojektista, joka on tehty Aalto Yliopiston CS-A1121 Ohjelmoinnin peruskurssilla Y2. Raportti kertoo sen, miten peli on rakennettu, kuinka sitä pystyy pelaamaan ja auttaa lukijaa ymmärtämään ohjelman toteutustavan sekä esittää hyvin tarkasti pelin ominaisuudet.    
Projektissa toteutettiin tasohyppelypeli, jossa pelaaja pystyy ohjaamaan hahmoa kentän läpi hyppimällä tasojen päälle ja väistämällä vastustajia keräten samalla pisteitä kolikoista. 
Pelissä on useampi kenttä, jotta pelaaja pystyy etenemään pelissä ja haastamaan itseään. Pelielämyksen parantamiseksi pelissä pystyy seuraamaan pisteiden kertymistä pelin aikana, jotta suorituksia pelissä voidaan vertailla tulostaululla toisiin pelaajiin tai pelaajan omiin edellisiin suorituksiin. 


## **Tiedosto- ja kansiorakenne**
Repository on jaetty kahteen osaan joista toinen on kansio, joka on tarkoitettu dokumenteille ja toinen on kansio, joka on tarkoitettu koodille, josta ohjelma rakentuu. 
Näin ollen dokumentit-kansiosta löytyy kaikki versiot projektin sunnitelmasta, hahmotelma tasojen piirrustuksista, UML-luokka kaavio lopullisesta rakenteesta sekä projektin loppudokumentti. 
Projekti sunnitelmista löytyy vanha ja uusi versio niemllä "V2", jossa on pieniä muutoksia aikaisempaa versioon verrattuna. Hahmotelma tasojen piirrustuksista sisältää samassa kuvassa ensimmäisen ja toisen tason määritelmän. Täytetyt objektit (väritetyt) ovat lisäystä ensimmäisestä tasosta toiseen ja numerot kuvaavat koordinaatteja tasolla. 
UML-luokka kaavio kuvaa tarkemmin mitä luokkia ohjelma sisältää ja mitä attribuutteja sekä metodeja nämä kyseiset luokat sisältävät. Tähän on tullut muutamia muutoksia suunnitellusta ja tarkempi selostus löytyy projektin loppudokumentista.  
Projektin loppudokumentti sisältää täydellisen selityksen ohjelmasta, sen toimivuudesta ja miten itse peliä voidaan pelata. Tämä dokumentti myös kertoo projektin onnistumisesta, sen hyvistä ja heikoista ominaisuuksista sekä siitä kuinka ohjelman toteuttaminen sujui projektin aikana.  

Koodi-kansiosta löytyy omat tiedostot jokaiselle luokalle, jota on ohjelman rakentamisessa käytetty. Kaikki tiedostot ovat itse toteutettuja ja laajasti kommentoituja, jotta lukijan on helppo ymmärtää mitä missäkin kohtaa on tarkoitus tapahtua. 
Tämä kansio sisältää siis kaiken koodin mitä ohjelman rakentamiseen on vaadittu. Jokaisella pelin objektilla on oma tiedosto, johon kyseisen objektin luokka on luotu kuten esimerkiksi vastustaja, este, kolikko, ja pelihahmo.
Näiden lisäksi kansiossa on tiedostot näiden objektien graphics itemeille, joissa niiden muoto ja väri luodaan. Lisäksi kansiosta löytyy tiedostot tasolle, tason neliöille ja koordinaateille, joiden avulla pelin taso ja siihen sisältyvät koordinaatit luodaan.
Tärkeinpänä kansiosta löytyy tiedosto nimeltä gameGUI.py, joka on ohjelman ydin, sillä tämä tiedosto käynnistää itse ohjelman ja hallitsee käyttäjän syötteitä pelin aikana luokan avulla. Näin ollen ohjelman saa aloitettua suorittamalla tämän tiedoston. Olen rakentanut ohjelmasta myös gameGUI.exe tiedoston, jonka avulla ohjelman saa myös käynnistettyä ilman IDEä, jotta pelaaminen on myös mahdollista niille käyttäjille, jotka eivät omista Python koodin avaamiseen vaadittavaa ympäristöä tai ei muuten vain osaa käynnistää ohjelmaa muuten. Tämä tiedosto vaatii kuitenkin sen, että kaikkien tasojen ulkoiset tiedostot niiden tulosten tallentamiseen on samassa kansiossa gameGUI.exe tiedoston kanssa, jotta ohjelma toimii ja käynnistyy oikein.  
Viimeiseksi kansiosta löytyy tiedosto nimeltä test.py, joka sisältää ohjelman testauksen hyvin kattavasti. Kokonaisuudessaan testissä testataan pelin kaikkia osa-alueita 13:sta eri testi metodilla, joista jokainen on tarkoitettu ohjelman eri ominaisuuksille. Testauksesta löytyy myös tarkemmin tieota projektin loppudokumentista.

## **Asennusohje**
Ohjelman hyödyntää kolmea eri kirjastoa, jotka ovat PyQt, Sys ja Os. Sys ja Os -kirjastoja saa hyödynnettyä käyttämällä koodissa komentoja "import sys" ja "import os". 
Testauksessa hyödynnetään unittest -kirjastoa, jonka saa ensiksi ladattua "pip install unittest" terminaalissa ja sitten hyödynnettyä komennolla "import unittest".

## **Käyttöohje**
**Pelaaminen**

Ohjelmassa on gameGUI tiedosto, joka sisältää ohjelman käynnistämisen metodit ja on muutenkin ohjelman kannalta tärkein tiedosto. Ohjelma siis käynnistyy sillä, kun gameGUI tiedosto avataan ja suoritetaan (run) esimerkiksi Pycharm IDE versiossa. 
Tässä projektissa toteutettiin myös käynnistys tiedosto nimellä gameGUI.exe, jonka avulla ohjelman voidaan käynnistää suoraan ilman kooditiedostojen avaamista. Molemmat tiedostot vaativat kuitenkin sen, että kaikkien tasojen ulkoiset tiedostot niiden tulosten tallentamiseen on samassa kansiossa gameGUI.exe ja gameGUI.py tiedoston kanssa (3kpl), jotta ohjelman toimii ja käynnistyy oikein.
Käynnistymisen jälkeen käyttöliittymä aukeaa ja keskelle ilmestyy ikkuna, jossa pelaajaa pyydetään antamaan nimi pelihahmolle, jotta peliä voidaan pelata ja yksilölliset suoritukset saadaan tallennettua pelin aikana. 
Pelihahmon nimen syötettyään, itse pelihahmo luodaan peli-ikkunaan ja tämän jälkeen pelaaja pystyy antamaan syötteitä, joiden avulla pelihahmo liikkuu kyseisessä peli-ikkunassa. Tämä tarkoittaa sitä, että pelaaja pystyy painelemaan tietokoneen näppäimistön nappuloita (A, S, D, W, R, Esc), jotka on määritelty erikseen käyttöliittymän alareunassa sijaitsevassa ohjekentässä. 
Näistä nappuloista neljällä (A, S, D, W) pystyy pelaaja liikuttamaan pelihahmoa vasemmalle (A), oikealle (D), alaspäin (S), ja hyppäämään (W). Lisäksi nappuloilla (R ja Esc) pelaajan pystyy aloittamaan saman tason pelaamisen uudestaan alusta painamalla (R) tai poistumaan kokonaan käyttöliittymästä ja ohjelmasta painamalla (Esc).
Lisäksi käyttöliittymässä on neljä eri painiketta ("Restart the level", "Exit the game", "Next level" ja "Previous level") joiden avulla pelaaja pystyy hallitsemaan peliä ja siinä etenemistä. 

**Testaus**

**Jos testauksen haluaa kokeilla (test.py tiedoston suorittaminen), täytyy jokaisessa testimetodissa syöttää pelihahmon nimeksi "Testi", jotta testaus menee onnistuneesti läpi.**