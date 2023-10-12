Get functies bevatten soms gevoelige informatie zoals wachtwoorden van Excel files. Zie bijvoorbeelde deze getter:

```
def psma_loader(byte_io):
    return pd.read_excel(decrypt_excel_bytes(byte_io, password='xxxx'), sheet_name='Data', nrows=60, skiprows=1)
```

Die via de helper functie `decrypt_excel_bytes` uit `data_loading_functions.py` een encrypted excel file opent. Deze loaders en getters zijn dus niet iets wat we in dit `sftp_tool` willen opslaan ([[UC2 - distribute data to the students]], AC2), maar iets wat los als configuratie wordt toegevoegd. Hoe het werkt is dat `data_loading_functions.py` zoekt naar een bestand wat `local_getters.py` heet in zijn locale directory. Als dit aanwezig is worden de getters en loaders uit deze file geladen, en beschikbaar gesteld voor de gebruiker.

Let op dat je in `local_getters` eventueel ook zaken vanuit `data_loading_functions.py` moet laden, bijvoorbeeld de `decrypt_excel_bytes` functie. Dit betekend dat er een circulaire afhankelijkheid is tussen deze twee files, wat in principe niet ideaal is. Maar in dit geval is de codebase erg klein, en is dit een mooie oplossing.