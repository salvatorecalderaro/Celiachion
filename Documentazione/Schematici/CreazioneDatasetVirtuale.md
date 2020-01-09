# Creazione Dataset virtuale

A mio parere (ma vi prego di contribuire in tal senso con critiche e suggerimenti), il dataset virtuale andrà creato in questo modo:

Sappiamo che la prevalenza sulla popolazione generale è di 1:100. Possiamo quindi generare un certo numero di batch di pazienti, ognuno composto da 1 paziente positivo ed un numero random di pazienti negativi, estratto casualmente da una distribuzione gaussiana con media 100 e varianza 2 devstd.

## Pazienti Negativi

* I dati relativi al **Questionario** si limiteranno ai campi elencati. Si genereranno questionari che rispecchiano la prevalenza statistica delle patologie (ove nota) nella popolazione generale:
	* Anemia (1:4)
	* Osteopenia (1:3)
	* Diarrea Cronica (1:20)
	* Mancata Crescita (1:140)
	* Disturbi Genetici (1:1000)
	* Madre Celiaca (1:100)
		
* Il **POCT** avrà esito negativo o inconclusivo (POCT positivo altamente improbabile), mantenendo la distribuzione degli inconclusivi (1:600), e considerando un numero di test difettosi pari a 1:1200.
		
* Nel caso di POCT negativo e Questionario negativo, l’**Esame del Sangue** avrà valori mancanti. Altrimenti si seguirà la seguente logica:
	* Prima si genererà un valore per le IGA totali, seguendo il risultato del POCT (ovvero superiore alla soglia con media 7 e varianza 2 stdev se negativo, inferiore se inconclusivo con distribuzione random tra 0 e .25).
	* Nel caso di deficit delle IGA totali, si genererà un valore per le TTG Igg con media 2 e varianza 2 stdev ed il valore delle TTG Iga sarà mancante
	* Negli altri casi (ovvero in caso le IGA totali siano sufficienti) si genererà un valore per la TTG Iga da una distribuzione gaussiana con media 4.5 e varianza 2 stdev, ed il valore per le TTG Igg sarà mancante.
		
* Nel caso l’analisi del sangue risulti positiva, La **Biopsia** avrà ovviamente esito negativo (classe 1 o 2), altrimenti avrà valore mancante.
	
## Pazienti Positivi

* La distribuzione delle risposte positive nel **Questionario** andrà rivista considerata la prevalenza nota, rispetto a quella utilizzata per il questionario dei casi negativi:
	* Anemia (1:2)
	* Osteopenia (2:5)
	* Diarrea Cronica (1:3)
	* Mancata Crescita (1:5)
	* Disturbi Genetici (1:20)
	* Madre celiaca (1:18)
		
* Il **POCT** avrà esito positivo (599:600) o inconclusivo (1:600).
	
* Gli **Esami del Sangue** seguiranno una logica simile a quella per i casi negativi, ma saranno sempre positivi:
	* Prima si genererà un valore per le IGA totali. Nel caso di POCT inconclusivo avrà media .125 e varianza 1 stdev, altrimenti media 8 e varianza 2 stdev.
	* Nel caso di POCT inconclusivo si genererà un valore per le TTG Igg  con media 14 e varianza 2 stdev ed il valore delle TTG Iga rimarrà mancante. Saranno scartati i valori nel range negativo.
	* Nel caso di POCT positivo si genererà un valore per la TTG Iga da una distribuzione gaussiana con media 24 e coda lunga a destra, ed il valore per le TTG Igg rimarrà mancante. Saranno scartati i valori nel range negativo.

* La **Biopsia** avrà esito positivo (classe 3a, 3b, 3c con distribuzione 1:3 uniforme)
