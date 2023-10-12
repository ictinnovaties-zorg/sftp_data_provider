Voor het configureren van de get functies is het mogelijk om een functionele stijl te gebruiken. Dit om de hoeveelheid boilerplate code te minimaliseren. Een goed voorbeeld is het PSMA getter/loader functie paar:

```
psma_loader = compose(partial(decrypt_excel_bytes, password="xxxxxx"),
                    partial(pd.read_excel, sheet_name='Data', nrows=60, skiprows=1))
get_psma_file = partial(get_vicodin_data, 'database_psma_met_functies.xlsm', loader_function=psma_loader)
```

`partial` geeft als return waarde een nieuwe functie terug waar de defaults van de input parameters zijn vervangen. `get_psma_file` is dus `get_vicodin_data` waar het eerste invoer argument `database_psma_met_functies.xlsm` is en het tweede invoer argument de bijbehorende loader. Nu kun je `get_psma_file` aanroepen, en worden deze defaults gebruikt. `partial` roept dus _niet_ `get_vicodin_data` aan, maar creeert een variant van de functie met nieuwe default waardes voor de functie inputs.

Voor de loader functie combineren we partial nog met compose. Dit is nodig om de loader twee stappen moet uitvoeren: het decrypten van de Excel sheet, en daarna het omzetten van deze sheet naar een pandas dataframe. `compose` geeft net als `partial` een functie terug, die in dit geval de twee taken achter elkaar uitvoert.

Door op deze manier functioneel programmeren in te zetten kun je de getters en loaders maken door een set aan functies te configureren (`partial`) en aan elkaar te rijgen (`compose`).