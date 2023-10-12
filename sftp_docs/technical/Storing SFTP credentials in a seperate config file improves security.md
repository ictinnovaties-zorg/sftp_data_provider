De SFTP credentials (username/password) worden opgeslagen in een `.env` bestandje, dit om te voorkomen dat SFTP credentials hard in de code staan ([[UC1 - Make data available]], AC7). De code pikt deze op uit het bestandje voordat de SFTP verbinding aangemaakt wordt. De student moet ervoor zorgen dat dit `.env` bestandje in de lokale werkdirectory staat. Voor het laden van het `.env` bestandje gebruiken we de `dotenv` library, deze laad `SETTING = "WAARDE"` paren uit het `.env` bestandje en stelt ze als environment variabelen beschikbaar. Deze kunnen wij dan weer oppikken door middel van `os.getenv`. De volgende entries moeten aanwezig zijn in de `.env` file:

```
SFTP_HOSTNAME='xxx.xxx.xxx.xxx'
SFTP_USERNAME='name'
SFTP_PASSWORD='password'
```

Nergens in de code worden deze waardes in de interfaces van de functies doorgegeven, de code gebruikt de waardes die uitgelezen worden uit het `.env` bestand. Dit maakt de interface simpeler, maar zorgt er ook voor dat de code niet zomaar gebruikt kan worden buiten de context van `module_loading_functions.py`.