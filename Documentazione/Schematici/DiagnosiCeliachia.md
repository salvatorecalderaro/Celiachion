# Diagnosi Celiachia

Di seguito viene descritto il percorso diagnostico (Pathway) per la diagnosi della Celiachia. Il pathway è quello previsto per i pazienti maltesi e per gli adulti italiani con figli affetti da celiachia.

Da questo pathway, in modalità bottom-up (ovvero partendo dalla positività alla malattia) si dovrà creare il set di pazienti virtuali per il training del CDSS.

## Passo 1a
Si effettua il test dei marcatori genetici (POC).
I possibili risultati sono:

* Il test **non è valido** (mancanza della barra 1). Questo può avvenire per due motivi
	* Il test è difettoso. Poiché il test andrebbe ripetuto; possiamo evitare di considerare questo caso.
	* Il paziente ha un DEFICIT di IGA totali (ovvero un valore < 7 ml/dl). In tal caso il POC è INCONCLUSIVO (non si può e non si potrà determinare nulla dal suo risultato). La prevalenza per questa evenienza è 1:600.
* Il test **è valido**, il paziente è **negativo** (presenza della barra 1, mancanza della barra 2). La prevalenza per questa evenienza è 99:100.
* Il test **è valido**, il paziente è **positivo** (presenza della barra 1, presenza della barra 2). I successivi esami del sangue chiariranno la quantità di TTG/Iga riscontrati. La prevalenza per questa evenienza è 1:100.

## Passo 1b
Si fa compilare il questionario diagnostico, che consiste nei dati anagrafici ed in una serie di domande a risposta binaria. Sulla base del questionario si determina la possibile positività del paziente, che si riscontra se anche solo una delle domande poste ottiene risposta positiva.
Tra le domande, vanno considerate con attenzione:
* Anemia
* Osteopenia
* Diarrea Cronica
* Mancata Crescita
* Disturbi Genetici (prevalenze 1:20)
* Figlia di Madre celiaca (1:11)
* Figlio di Madre celiaca (1:25)

## Passo 2 (Nel caso di positività al passo 1a o di positività al passo 1b)
Si procede all’esame del sangue.
Per prima cosa si misurano le IGA totali:
* Per valori 0:.25 ml/dl, si considera un deficit di IGA totali (prevalenza 1:600), e si passa all’esame delle TTG Igg o delle DPG Igc (nel notro caso si misurano le TTG Igg)
	* Un valore 0:7 U/ml da esito negativo
	* Un valore >7 U/ml da esito positivo (prevalenza 1:600 X 1:100)
* Per valori >.25 ml/dl si procede all’esame delle TTG Iga
	* 0:9 U/ml danno esito negativo
	* 9-16 U/ml sono considerate borderline
	* > 16 U/ml da esito positivo (prevalenza 1:100)

## Passo 3 (in caso di positività al passo 2)
Si procede alla Biopsia. IL paziente sarà classificato come segue:
* Classe 1 (negativo)
* Classe 2 (negativo)
* Classe 3a, 3b, 3c (positivo). Non vi sono al momento indicazioni sulla prevalenza delle tre classi nella diagnostica, quindi esse andranno considerate equiprobabili 1:3.
