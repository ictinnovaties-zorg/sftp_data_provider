Een SFTP server zorgt ervoor dat de data alleen toegankelijk is voor personen met de juiste credentials, en de communicatie met de server is onder strikte encryptie ([[UC1 - Make data available]], AC6). Per project wordt een directory aangemaakt waar de specifieke data voor de studenten klaar gezet wordt. In de `scripts` directory staat de code klaar die de studenten nodig hebben om de data daadwerkelijk in te lezen.

- Elke nieuwe studentgroep heeft een eigen `.env` bestand waarin hun credentials staan
    
- Server waar SFTP op staat moet openstaan op poort 22 ([[UC2 - distribute data to the students]], AC5)
    
- Op de server is een groep genaamd `students`. Bestanden die we delen moeten de owner `root:students` hebben, denk hierom als je niet bestanden klaar zet op de SFTP server.
    
- De SFTP server is geconfigureerd door gebruik te maken van een virtual root. Dit zorgt ervoor dat studenten alleen de spullen die ook daadwerkelijk te zien zijn. ([[UC1 - Make data available]], AC1)
    
- De link naar de scripts directory werkt niet met een softlink, dus dit moet via een mount.

