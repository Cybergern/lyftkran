Grunden i systemet är lyftare (användare):

### En lyftare:

- är medlem i en eller flera föreningar
- kan ha en eller flera roller
- kan ha ett användarnamn och lösenord om de ska kunna logga in som administratör
- kan ha en eller flera lyftarlicenser
- kan ha en eller flera domarlicenser
- har ett namn, ett kön och ett personnummer
- kan ha kontaktuppgifter i form av en postadress, telefon och e-post

### En lyftarlicens:

- gäller ett visst år 
- är kopplad till en klubb
- har ett licensnummer
- begärdes ett visst datum
- kan ha upphävts ett visst datum
- har en status


### En domarlicens:

- gäller ett visst år
- har ett boknummer
- är godkänd eller ej
- har en domarnivå

### En förening: 

- har ett namn och föreningsnummer
- tillhör ett distrikt
- har ett RF-nummer
- har ett organisationsnummer
- har noll eller flera lyftare
- kan ha kontaktuppgifter och postadress
- kan ha ett antal årsavgifter kopplade till sig

### En årsavgift:

- har ett år
- kan vara fakturerad eller betald med datum

### Ett distrikt:

- har ett namn
- har ett RF-nummer
- har ett organisationsnummer
- kan ha kontaktuppgifter i form av telefon, e-post, hemsida och postadress
- kan ha noll eller flera kontaktpersoner

### En kontaktperson:

- har en uppgift och ett namn
- kan ha kontaktuppgifter i form av e-post och telefon

### En roll:
- föreningsadministratör, distriktsadministratör, förbundsadministratör, tävlingsansvarig, tävlingskommitte eller superadmin

### En föreningsadministratör:

- är kopplad till en eller flera föreningar
- kan lägga till, ta bort och ändra lyftare i sina egna föreningar
- kan ansöka om nya licenser för lyftare i sina egna föreningar
- kan registrera resultat för sina egna föreningslag i en omgång i en serie
- kan göra andra lyftare till föreningsadministratörer för sina egna föreningar

### En distriktsadministratör:

- är kopplad till ett eller flera distrikt
- kan lägga till, ta bort och ändra tävlingar i sina egna distrikt
- kan lägga till resultat i tävlingar inom sina egna distrikt
- kan lägga till, ta bort föreningsadministratör på lyftare i föreningar i sina egna distrikt

### En förbundsadministratör:

- kan lägga till, ta bort och ändra distrikt
- kan lägga till, ta bort och ändra serier
- kan lägga till, ta bort och ändra föreningar
- kan flytta lag mellan serier
- kan byta förening på en lyftare
- kan markera årsavgifter för föreningar som betalda eller fakturerade
- kan ta bort föreningsadministratör från en lyftare
- kan ta bort distriktsadministratör från en lyftare
- kan lägga till, ta bort distriktsadministratör på andra lyftare

### En tävlingskommittemedlem

- kan lägga till, ta bort och ändra i tävlingar

### En tävlingsansvarig

- kan lägga till nya tävlingar

### En superadmin:

- kan lägga till, ta bort förbundsadministratör

### En licens:

- tillhör en lyftare i kombination med en förening
- gäller för ett visst kalenderår
- kan vara indragen med datum för indragandet
- begärs ett visst datum
- har ett licensnummer

### Ett licensnummer:

- är unikt
- består av lyftarens födelsedag i form YYMMDD följt av första bokstaven i lyftarens förnamn och därefter första bokstaven i lyftarens efternamn (skulle detta inte vara unikt tas nästa bokstav i förnamnet tills alla testats, sedan nästa bokstav i efternamnet och alla i förnamnet, osv tills alla testas, därefter testas alla bokstavskombinationer av två tecken tills man hittar en ledig kombination)

### Ett lag:

- tillhör en förening
- är med i en specifik serie
- kan ha ett eller flera omgångsresultat

### En serie:

- har ett namn
- har ett startdatum och ett slutdatum (alternativt har ett kalenderår)
- har en grentyp
- har en eller flera omgångar
- har ett eller flera lag
- har en maxgräns för antal lyftare
- kan ha en överliggande serie
- kan ha en underliggande serie 
- har ett poängsystem

### En omgång:

- har ett lagomgångsresultat per lag i serien

### En grentyp:

- har ett namn (just nu Bänkpress, Styrkelyft, Klassisk Bänkpress, Klassisk Styrkelyft och Parabänk)
- har ett eller flera moment

### Ett moment:

- har ett namn (just nu Bänkpress, Knäböj, Marklyft, Parabänk)

### Ett lagomgångsresultat:

- består av ett eller flera samlade resultat från lyftare tillhörande lagets förening i en omgång upp till maxgränsen för serien

### Ett individuellt tävlingsresultat:

- har en lyftare och invägningsvikt
- har en viktklass
- har en kategori
- har ett resultat i en grentyp
- kan ha ett lottnummer
- Ska kunna flaggas som struket och därmed inte räknas med

### En tävlingsinbjudan:

- har ett namn
- har en arrangör
- har ett startdatum, ett slutdatum och en sista anmälningsdag
- har kontaktuppgifter i form av en kontaktperson, telefon, e-post
- har en eller flera grentyper
- har en eller flera kategorier
- kan ha ett eller flera dokument
- har en beskrivning
- är kvalgrundande eller ej
- kan ha kvalgränser kopplade till varje deltagande kategori

### En genomförd tävling:

- har ett eller flera individuella tävlingsresultat
- har en tävlingsinbjudan

### En viktklass:

- har ett namn
- har en maxvikt eller en minimivikt (Exempelvis maxvikt 59 kg eller minimivikt 120.01 kg)

### Ett kön:

- har ett namn (Exempelvis Herr, Dam)

### En kategori:

- har ett namn (exempelvis Herr Veteran 60-69)

### Ett poängsystem
- har ett namn (exempelvis Wilks eller IPF)
- har en algoritm som tar in ett individuellt tävlingsresultat och producerar en poängsumma