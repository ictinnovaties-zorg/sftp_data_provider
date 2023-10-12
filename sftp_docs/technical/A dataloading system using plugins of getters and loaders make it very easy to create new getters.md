Elke dataset die via `data_loading_functions.py` beschikbaar gesteld wordt heeft een `get` functie (bv `get_psma_data`) die een pandas dataframe teruggeeft ([[UC1 - Make data available]], AC2). Onder de moterkap gebeurt er het volgende:

- De `get` functie roept `get_vicodin_module` aan
- deze maakt een SFTP verbinding naar de server
- het bestand wat aan `get_vicodin_module` gevraagd wordt, als het bestaat, wordt in een BytesIO stream gestopt
- Deze BytesIO stream wordt door een loader functie getrokken die er een Pandas DataFrame van maakt.
- Zodra het pandas dataframe in het geheugen staat wordt de SFTP connectie afgesloten en is er geen netwerk verbinding naar de server meer nodig ([[UC2 - distribute data to the students]], AC4).

Deze setup zorgt ervoor dat `get_vicodin_data` generiek is en dat je alleen nog maar een file op de SFTP server en een bijbehorende load functie in hoeft te stellen voor elke dataset die je bloot wil stellen. Dit wordt versterkt door het gebruik van een BytesIO stream: de code is exact hetzelfde of het bestand nu een csv, Excel of andere file is. Zolang de loader functie maar een pandas dataframe maakt van de BytesIO stream.

De volgende getter leest een excel file in:

```
def get_lymfoma_radiomics():
    return get_vicodin_data('file.xlsx', loader_function=pd.read_excel)
```

Dus zolang je een `loader` functie schrijft die een Pandas DataFrame uitspuugt, kun je de file klaar zetten op de SFTP server en kun je je hem laden met `get_vicodin_data`. 

`data_loading_functions.py` wordt niet lokaal bij de studenten neergezet, maar [[Abstracting the dataloading code away on the SFTP server improves security]]. 

Je kunt de code schrijven met normale Python functies, maar [[Functioneel programmeren is een goede optie voor het schrijven van getters]]