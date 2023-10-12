### Use case 1: data beschikbaar maken

_User story:_ Als docent wil ik op een veilige manier mijn studenten toegang geven tot de persoonlijke data zodat zij hun onderzoek kunnen uitvoeren

Acceptatiecriteria:

- AC1: de student moet alleen toegang krijgen tot de data waar hij/zij rechten voor heeft
- AC2: De student krijgt de data terug in een Pandas DataFrame. Andere details die nodig zijn voor het verwerken van de data zoals passwords voor Excel files moeten niet zichtbaar zijn voor studenten.
- AC3: de data wordt _niet_ op de hardeschijf van de studenten opgeslagen, zodra de Jupyter Kernel afgesloten wordt moet de data weg zijn
- AC6: AC5 is onder voorwaarde data de beveiliging in lijn is met de industriestandaard voor dit soort online services
- AC7: identificatie zoals passwords moeten niet hard in de broncode van de studenten staan.