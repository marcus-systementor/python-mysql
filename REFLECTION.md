# Reflektion – Python och MySQL

Fyll i tabellen medan du arbetar. Skriv vad du faktiskt såg. Använd uppgifternas fiktiva testdata.

| Testfall | Vad förväntade jag mig? | Vad hände? |
| --- | --- | --- |
| Kund 1 och kund 2 läses från MySQL | | |
| Namnet ändras i Python och kunden läses igen | | |
| ID 999 och inmatningen `abc` provas | | |
| Giltigt namn sparas och läses från en ny anslutning | | |
| Namn som bara består av mellanslag provas | | |
| Tillfälligt namn läses före `rollback()` och sparat namn efteråt | | |

## Överföring till kursprojektet

- Tabell, primärnyckel och fält jag valde
- Vilken ändring programmet gör
- Var jag sparade koden och hur jag kör den
- Resultat före och efter ändringen samt resultat vid ett okänt ID

## Förklara med egna ord

1. Vad händer med raden från `fetchone()` innan den blir ett `Customer`-objekt?
2. Varför skickas det nya namnet som parameter? Vad hände när du provade ett namn med apostrof?
3. Vilka namn såg du före ändringen, före `rollback()` och efter `rollback()`? Vilken observation visar att `commit()` sparade den första ändringen?
4. Vilket steg vill du kunna förklara eller visa inför lektionen om ORM?
