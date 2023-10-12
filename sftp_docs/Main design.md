## Introduction
Working with Public Health Information (PHI) has a lot of regulations. One of those is that the data should be removed after students are done with the project. Mailing people the data provides far too much places the data is stored. This tool aims to fix that. 

## Functional
Om verder uit te diepen wat onze behoeftes zijn hebben we de volgende use case uitgewerkt. De beperkte scope van het systeem maakt het mogelijk om alle functionele eise onder 1 use case samen te vatten. Er zijn twee actoren actief in dit systeem:

- _de onderzoeker_ deze persoon heeft een onderzoeksdoel waarvoor typisch een stuk data geanalyseerd wordt, en wat resulteerd in een ML model wat dit onderzoeksdoel dient. Gedacht kan worden aan een ML model wat een risicoinschatting kan maken voor een patient op basis van een aantal gegevens van deze patient.
- _de student_ deze persoon werkt onder leiding van de onderzoeker aan het ML model. Hiervoor is het natuurlijk nodig dat hij/zij toegang heeft tot de data. Onze aanname is dat deze student in Python werkt, en meer specifiek door gebruik te maken van een zogenaamd [Jupyter Notebook](https://jupyter.org/)

De volgende twee use cases beschrijven de tool vanuit deze twee perspectieven:
- [[UC1 - Make data available]]: data beschikbaar stellen
- [[UC2 - distribute data to the students]]: met de data werken vanuit het oogpunt van de studenten

## Technical
We hebben ervoor gekomzen om de data op te slaan op een SFTP server, waarvan de studenten de data in kunnen laden naar hun Jupyter notebook. Zie [[An SFTP server is an efficient way to safely distribute data]] voor een uitgebreide discussie. 

De technische opbouw ziet er als volgt uit:

![[flowchart_dataloading.png]]

Het volgende sequence diagram laat zien hoe de workflow rondom dit systeem in de praktijk werkt:

![[seq_diag_system.png]]
Er zijn dus twee fases: code ophalen voor data lezen, en daadwerkelijk data verwerken en inlezen naar een Pandas DataFrame. De toelichting voor deze keuze kun je vinden op [[Abstracting the dataloading code away on the SFTP server improves security]]. 

### De code ophalen
Het ophalen van de code gebeurt via `module_loading_functions.py`, dit bestand moet klaar staan in de *lokale* werkdirectory van de studenten. De volgende code moet dan uitgevoerd worden in het Jupyter Notebook of Python script:
```
from module_loading_functions import get_vicodin_module

data_loading_module = get_vicodin_module('scripts/data_loading_functions.py')
```

De functies in `data_loading_functions.py` zijn nu beschikbaar om aan te roepen, bijvoorbeeld:

```
test_data = data_loading_module.get_test_file()
```

Welke datasets de student wel of niet kan inlezen wordt bepaald door hun SFTP account ([[SFTP account decides which data is available to the students]]). Verder worden de details van de SFTP account in een config bestandje opgeslagen ([[Storing SFTP credentials in a seperate config file improves security]]). 

## Data ophalen
TODO: schrijf hier wat lijm tekst
[[A dataloading system using plugins of getters and loaders make it very easy to create new getters]]. 

[[Abstracting the dataloading code away on the SFTP server improves security]]

[[Getter functions should be stored outside the main codebase as configurable plugins]]

## Data opslaan op de SFTP server
TODO: schrijf hier wat lijm tekst

[[Using virtual roots we can serve only the right data to a particular group of students]]

## Hoe komen al deze elementen in de praktijk samen

- Je moet een SFTP server optuigen waar je zowel de code als de data klaar zet. Dit maakt gebruik van `data_loading_functions.py`. Eventueel moet je zelfs nieuwe getters schrijven. 
- Je moet voor een groep studenten een SFTP account aanmaken waaronder je de data klaar zet. 
- Je moet `module_loading_functions.py` aan de studenten sturen, samen met hun `.env` file waar de SFTP credentials in zitten. Als alles goed gegaan is kunnen de studenten dan toegang hebben tot de data vanuit hun python scripts of jupyter notebooks.


