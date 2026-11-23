# Dag 7 – Från Pythonobjekt till lagring

Bygg vidare på ett litet Pythonprogram som läser en kund från MySQL. Du följer raden in i ett Pythonobjekt, lägger till ett namnbyte och provar att både spara och ångra ändringen. Sist gör du motsvarande arbete med en tabell i ditt eget kursprojekt.

Du har allt för att köra, felsöka, kontrollera resultaten och göra en `commit` efter varje steg.

| Steg | Vad du gör |
| --- | --- |
| 1 | Klona, konfigurera och kör startprogrammet |
| 2 | Följ en rad från MySQL till ett Pythonobjekt |
| 3 | Läs in ett ID och hantera att kunden saknas |
| 4 | Lägg till ett validerat namnbyte och spara det |
| 5 | Läs en tillfällig ändring och ångra den |
| 6 | Läs och uppdatera en post i ditt projekt |
| 7 | Samla dina resultat och förklara vad som hände |

## Steg 1 – Få startprogrammet att läsa en kund

**Mål**  
Kör programmet med din egen lokala MySQL-anslutning.

1. Du behöver Git, Python 3.11 eller senare, en lokal MySQL-server och DBeaver. Starta MySQL och kontrollera att du kan ansluta från DBeaver.
2. Öppna lärarens mall på GitHub och välj **Use this template → Create a new repository**. Skapa ett eget **privat** repo, exempelvis `databehandling-dag07-ditt-namn`.
3. Klicka på **Code** i ditt repo och kopiera klonlänken. Kör `git clone` följt av länken. Öppna den klonade mappen i din editor. Terminalen ska stå i mappen där den här README-filen ligger.
4. Öppna [setup.sql](setup.sql) i DBeaver på den lokala servern och **kör hela skriptet**. Det skapar `course_storage` och lägger till Ada (ID 1) och Sam (ID 2) om raderna saknas. Om du gjort labbet tidigare finns sparade namn kvar.
5. Skapa en virtuell miljö, installera drivrutinen och starta programmet.

   En virtuell miljö samlar projektets Pythonpaket i mappen `.venv`. I VS Code väljer du **Git Bash** i terminalens meny vid **+**. Kör från mappen där README och `requirements.txt` ligger.

   **Windows (Git Bash i VS Code)**

   ```bash
   python --version
   python -m venv .venv
   source .venv/Scripts/activate
   python -m pip install -r requirements.txt
   python student/customer_lab.py
   ```

   `(.venv)` i terminalens prompt visar att miljön är aktiv. Nästa gång du öppnar en Git Bash-terminal i samma projekt kör du `source .venv/Scripts/activate` igen och startar programmet. Du kan lämna miljön med `deactivate`.

   **Windows (PowerShell)**

   Kör med projektets Python direkt.

   ```powershell
   python --version
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe student/customer_lab.py
   ```

   **macOS/Linux (bash)**

   ```bash
   python3 --version
   python3 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/python student/customer_lab.py
   ```

   Använd samma MySQL-användare och lösenord som i DBeaver. Kör i en vanlig terminal. När programmet frågar efter lösenordet är inmatningen dold. Anslutningen går som standard till `127.0.0.1:3306`. Om din server har en annan adress eller port kan du sätta `DB_HOST` och `DB_PORT` i terminalen.

**Kontroll**  
På ny testdata skriver programmet ut `Customer(customer_id=1, name='Ada')`. Jämför namnet med det som `setup.sql` visar i DBeaver.

**Commit**  
Anteckna vilket resultat du fick i [REFLECTION.md](REFLECTION.md). Gör din första commit så här. Lägg på samma sätt till de filer du har ändrat efter varje steg.

```text
git add REFLECTION.md
git commit -m "Verify local MySQL setup"
```

## Steg 2 – Följ raden in i Python

**Mål**  
Förklara vad som finns i tabellen, i returvärdet från `fetchone()` och i Pythonobjektet.

1. Kör frågan nedan i DBeaver. Byt sedan från `1` till `2` och jämför raderna.

   ```sql
   SELECT customer_id, name
   FROM course_storage.customers
   WHERE customer_id = 1;
   ```

2. Läs `find_customer()` i [student/customer_lab.py](student/customer_lab.py). Peka ut SQL-texten, kund-ID:t som skickas separat och de två värden som flyttas från raden till objektet. 
3. Byt kund-ID i `main()` till `2` och kör. Byt sedan tillbaka till `1`.
4. Förutsäg vad som står i databasen om du tillfälligt sätter `customer.name` till `"Bara i Python"` i `main()`. Prova, skriv ut objektet och kör din `SELECT` i DBeaver igen. Ta bort den tillfälliga tilldelningen efter kontrollen.

**Kontroll**  
Programmet kan visa båda kundernas uppgifter.

**Commit**  
`Trace customer rows into Python objects`

## Steg 3 – Hantera olika kund-ID:n

**Mål**  
Programmet ska kunna skilja mellan ett befintligt ID, ett okänt ID och felaktig inmatning.

1. Ersätt det fasta kund-ID:t i `main()` med ett värde från `input()`. Omvandla det till `int` innan du söker. Fånga `ValueError` vid omvandlingen och skriv ett tydligt meddelande för text eller tom inmatning.
2. Behåll `find_customer()` som funktion för databasläsningen. Kontrollera returvärdet i `main()`. Om det är `None`, skriv ett meddelande om vilket ID som saknas och avsluta körningen.
3. Fortsätt att skicka ID:t som parameter till `cursor.execute()`. I en parameterlista med ett enda värde behövs kommat i `(customer_id,)`.

**Kontroll**  
Kör med `1`, `2`, `999` och `abc`. ID 1 och 2 visar respektive kund. ID 999 ger ett meddelande om en saknad kund. `abc` ger ett meddelande om inmatningen.

**Commit**  
`Handle customer lookup input`

## Steg 4 – Spara ett giltigt namnbyte

**Mål**  
Skriv ett `UPDATE` med parametrar och bekräfta ändringen med `commit()`.

1. Skriv en funktion `update_customer_name(connection, customer_id, new_name)`. Använd `strip()` och avvisa namn som blir tomma före SQL. Tabellen har plats för upp till 100 tecken.
2. Bygg upp en parametriserad `UPDATE`. Sätt ett värde för `name` och använd `WHERE customer_id = %s` för att begränsa ändringen till en kund. Skicka namn och ID till `execute()` i samma ordning som platshållarna.
3. Hämta kunden i `main()` och fråga efter ett nytt namn när kunden finns. Anropa uppdateringen och kör `connection.commit()` först när skrivningen har lyckats. Låt huvudflödet sköta transaktionen så att du kan återanvända funktionen i nästa steg.
4. Prova kund **1** med ett nytt namn som skiljer sig från det sparade. Testa också ett namn med apostrof, exempelvis `Ada O'Neil`, och ett namn med mellanslag runtom. Läs sedan om kunden i DBeaver från en **ny anslutning** eller kör en separat `SELECT` efter att du har avslutat en eventuell gammal transaktion i DBeaver.
5. Prova även ett namn som bara består av mellanslag. Hantera avvisningen i `main()` så att användaren får veta varför namnet saknas.

**Kontroll**  
Giltiga namn finns kvar vid en ny läsning, även namnet med apostrof. Ett tomt namn lämnar den tidigare sparade uppgiften kvar. Kund 2 har samma namn som före körningen. Dokumentera vad du såg.

**Commit**  
`Save a validated name change`

## Steg 5 – Ångra ett namnbyte

**Mål**  
Visa skillnaden mellan vad den pågående transaktionen ser och vad som finns kvar efter `rollback()`.

1. Läs och anteckna namnet som sparades för kund 1 i steg 4. Lägg till ett val i programmet för att **spara** eller **ångra** ett namnbyte. Återanvänd samma uppdateringsfunktion.
2. Låt ångraflödet köra `UPDATE`, läsa kunden via **samma anslutning** och visa det tillfälliga namnet. Anropa därefter `connection.rollback()` innan någon `commit()` har körts för den ändringen. Läs kunden igen.
3. Testa ångraflödet med ett annat namn än det redan sparade. Exempelvis kan du utgå från `Ada O'Neil` och prova `Ada Test`. Kontrollera slutläget i en ny läsning från DBeaver.
4. Kör också sparflödet igen och kontrollera att båda valen fortfarande fungerar. Försök förklara varför tillfälliga `Ada Test` syntes under transaktionen.

**Kontroll**  
Under ångraflödet ser du först det sparade namnet, sedan det tillfälliga och därefter det sparade igen. Din nya läsning visar samma sista namn. I sparflödet visar den nya läsningen det namn du valde att spara.

**Commit**  
`Compare commit and rollback`

## Steg 6 – Använd arbetssättet i ditt eget projekt

**Mål**  
Visa ett litet användarfall hela vägen från en rad i din projektdatabas till en ändring som går att kontrollera.

1. Välj **en tabell**, **en primärnyckel** och **ett fält** som passar att ändra i projektets testdata. Skriv vilken ändring du vill demonstrera, till exempel att byta namn på en produkt.
2. Börja med en `SELECT` i DBeaver. Skriv sedan en läsfunktion i projektet med parametriserad SQL och mappa resultatet till ett litet Pythonobjekt. Kontrollera ett ID som finns och ett som saknas.
3. Lägg till en kontrollerad ändring av ditt fält. Bekräfta den med `commit()` och kontrollera resultatet i en ny läsning.
4. Spara kod och körinstruktioner **i ditt projekt**. Anteckna i labbets [REFLECTION.md](REFLECTION.md) vilken tabell du valde, var koden ligger och vad dina testfall visade.

Om projektdatabasen ännu inte går att köra, använd kund **2** i `course_storage` för att visa läsning och ändring. Anteckna vilken tabell, nyckel och vilket fält du ska använda när projektets databas är klar.

**Kontroll**  
Du kan visa resultatet före och efter ändringen, förklara var objektet skapas och visa vad som händer för ett okänt ID.

**Commit**  
`Connect a project record to MySQL`

## Steg 7 – Avsluta och reflektera

**Mål**  
Du ska kunna förklara vägen från en SQL-rad till ett objekt och sedan tillbaka till databasen.

1. Slutför testtabellen och frågorna i [REFLECTION.md](REFLECTION.md). Skriv vad du faktiskt observerade och vilken fråga du tar med dig till ORM-lektionen.
2. Kör `git status` före din sista `commit`. Spara Pythonfilerna och dina anteckningar. Använd `git push` för att spara arbetet i ditt privata labbrepo. Överföringen i steg 6 sparas i det befintliga kursprojektet.

**Kontroll**  
Öppna ditt repo på GitHub och se att de senaste filerna och dina commits syns. Förklara med ett eget exempel vad som skiljer en ändring i Pythonobjektet, en körd `UPDATE` och en bekräftad `commit()`.

**Commit**  
`Record lab results and reflection`

## Om du kör fast

| Symtom | Kontroll |
| --- | --- |
| `ModuleNotFoundError: No module named 'mysql'` | Kör installation och program med samma Python från `.venv`. |
| Programmet får ingen kontakt med MySQL | Kontrollera att MySQL körs. Jämför värd och port med DBeaver. |
| `Access denied` | Kontrollera användare och lösenord i den lokala anslutningen. Skriv in lösenordet när programmet frågar och håll det utanför dina filer och commits. |
| `Unknown database 'course_storage'` | Kör hela `setup.sql` i DBeaver på samma server som Python ansluter till. |
| Du ser ett gammalt namn i DBeaver | Kontrollera att du läser från `course_storage`, att skrivningen har körts med `commit()` och att läsningen görs i en ny anslutning. |
| Din commit syns inte i ditt privata GitHub-repo | Kör `git status` för att se om du behöver göra `git push`. Kontrollera med `git remote -v` att adressen går till **ditt eget** repo. |
