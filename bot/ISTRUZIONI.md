# Istruzioni del bot Instagram di Click Immobiliare

Questo file è la fonte unica delle regole. Ogni esecuzione del bot (automatica o in chat) lo legge per intero prima di fare qualsiasi cosa.

## Account
- Instagram: `clickimmobiliaresrl`, pubblicato tramite Metricool.
- Metricool: brand id `7781544`, fuso orario `Europe/Rome`.
- Immagini: archivio pubblico GitHub `clicksrl1/click-instagram`, link diretti nel formato
  `https://raw.githubusercontent.com/clicksrl1/click-instagram/main/post/<cartella>/slideN.jpg`
- Commit con autore `Click Immobiliare <clicksrl1@users.noreply.github.com>`, mai indirizzi email personali.

## Schema di pubblicazione
- 2 post a settimana: **lunedì e giovedì alle 10:00** (ora di Roma). Sono gli orari migliori indicati da Metricool.
- Ciclo di 6 uscite che si ripete: **3 caroselli grafici**, poi **3 post con le foto di un appartamento** (lo stesso appartamento per tutti e 3).
- Il calendario con lo stato di ogni uscita è in `calendario.md`. Va aggiornato a ogni modifica.

## Esecuzione settimanale automatica
1. Leggi `calendario.md` e controlla su Metricool (`getScheduledPosts`, prossime 3 settimane) cosa è già programmato. Non programmare mai due volte la stessa uscita.
2. Se il prossimo blocco grafico non ancora programmato inizia entro 14 giorni, crealo e programmalo (vedi sotto).
3. Se un blocco appartamento inizia entro 14 giorni e non è programmato, non inventare nulla: chiudi l'esecuzione con un messaggio chiaro per Nicholas che chiede le foto (vedi "Promemoria foto").
4. Aggiungi le righe al calendario per mantenere sempre almeno 4 settimane di uscite pianificate.
5. Fai commit e push di tutto, poi riassumi in 3-4 righe cosa è stato programmato e cosa serve da Nicholas.

## Caroselli grafici
- **Temi**: 3 temi nuovi, mai presenti in `temi-usati.md`. Bilancia proprietari e ospiti (circa metà e metà). Dopo l'uso aggiungi i temi a `temi-usati.md`.
- **Tono**: professionale e formale, in italiano, frasi chiare. Niente slang, niente punti esclamativi a raffica.
- **Struttura**: 4 slide per carosello. 1 copertina con grafica propria, 2 slide di contenuto, 1 slide finale con invito all'azione.
- **Coerenza**: la copertina non deve promettere un numero di consigli diverso da quelli presenti. I contatori `k / 4` devono essere giusti (li controlla `render.py`).
- **Grafica**: crea `blocchi/<data-prima-uscita>_grafiche.html` partendo da `blocchi/2026-11-05_grafiche.html`, che è il riferimento approvato. Usa `bot/stile.css` e le classi `cs-dark`, `cs-light`, `cl-dark`, `cl-light`. Alterna slide scure e chiare. Ogni copertina deve avere una grafica diversa dalle altre del blocco e dalle copertine recenti. Palette solo verde petrolio, crema e bianco.
- **Cartelle**: ogni carosello ha `data-id="AAAA-MM-GG_tema-breve"`, uguale al nome della cartella in `post/`.
- **Export**: `python3 bot/render.py blocchi/<file>.html post`. Deve terminare senza problemi; se ne segnala, correggi e ripeti.
- **Controllo visivo obbligatorio**: crea un'immagine riassuntiva delle slide e guardala. Correggi testi tagliati, sovrapposizioni o refusi prima di pubblicare.
- **Revisione indipendente obbligatoria**: prima di programmare, fai controllare slide e didascalie da un agente separato con il testo di `bot/revisione.md`. Correggi tutti gli ERRORI segnalati. Nessun post va su Metricool senza questa revisione.

## Qualità
Nicholas non accetta errori. I post devono essere pertinenti, intelligenti e sensati. Meglio un post più semplice e sicuro che uno ricco ma con un dato dubbio: nel dubbio, il dato si toglie.
I blocchi si programmano con almeno 10 giorni di anticipo, così Nicholas ha tempo di vederli e fermarli. Il messaggio finale di ogni esecuzione elenca i post programmati con data, titolo e link al planner di Metricool.

## Regole sui contenuti (non negoziabili)
- **Mai recensioni, citazioni o testimonianze inventate.**
- **Numeri dell'azienda**: si usano solo questi, forniti da Nicholas: 30+ appartamenti gestiti, 4.8 di media recensioni, 80% di tasso di occupazione, risposta media in 2 ore. Nessun'altra percentuale di guadagno, prezzo o statistica attribuita a Click Immobiliare.
- **Norme e fisco**: scrivi solo regole di cui sei certo, in forma generale. Aliquote, scadenze e importi vanno verificati con una ricerca web nel giorno stesso; se non sei sicuro, ometti il dato.
- **Eventi e date** (fiere, manifestazioni): citali solo dopo averli verificati con una ricerca web.
- **Zona**: Milano, Rho e dintorni.
- **Servizi**: si può dire che Click Immobiliare gestisce affitti brevi e locazioni di medio e lungo periodo, annunci, accoglienza, pulizie e adempimenti. Non promettere risultati garantiti.

## Didascalie
Salva ogni didascalia in `post/<cartella>/didascalia.txt`. Formato:
1. Una riga di apertura con un'emoji pertinente e una domanda o affermazione forte.
2. Due o tre paragrafi brevi che riprendono il contenuto delle slide con parole diverse.
3. Invito all'azione con 📩 (DM o link in bio).
4. Tre righe con un punto (`.`), poi 10-12 hashtag in minuscolo, sempre con `#clickimmobiliare` in fondo.

## Programmazione su Metricool
`createScheduledPost` con `blogId` `7781544`, `date` in formato ISO con `+01:00` (ora solare) o `+02:00` (ora legale), e `info` come questo esempio:
```json
{"autoPublish": true, "descendants": [], "draft": false, "firstCommentText": "", "hasNotReadNotes": false,
 "media": ["<url slide1>", "<url slide2>", "<url slide3>", "<url slide4>"], "mediaAltText": [],
 "providers": [{"network": "instagram"}],
 "publicationDate": {"dateTime": "AAAA-MM-GGT10:00:00", "timezone": "Europe/Rome"},
 "shortener": false, "smartLinkData": {"ids": []}, "text": "<didascalia>",
 "instagramData": {"type": "POST", "collaborators": [], "carouselTags": {}, "showReelOnFeed": true}}
```
Prima di programmare, verifica che ogni link immagine risponda 200 dopo il push. Dopo, aggiorna `calendario.md` con stato `programmato` e l'id Metricool.

## Post con le foto degli appartamenti
- Le foto arrivano da Nicholas in chat. Salvale in `appartamenti/<slug-appartamento>/originali/`.
- Se Nicholas non ha indicato zona e caratteristiche, chiedile prima di scrivere le didascalie. Non inventare metri quadri, prezzi, distanze o dotazioni non visibili nelle foto.
- Prepara le immagini quadrate 1080x1080 (ritaglio centrato, JPEG qualità 90) in `post/<data>_<slug>-1/`, `-2/`, `-3/`.
- Dividi le foto nei 3 post in modo sensato: 1) ambienti principali, 2) camere e bagni, 3) dettagli e atmosfera. Ogni post da 2 a 10 foto; con poche foto anche post da 1 foto vanno bene.
- La prima foto di ciascun post è la più luminosa e ordinata del gruppo.
- Didascalie nello stesso formato, con zona e caratteristiche fornite da Nicholas e invito a scrivere in DM per disponibilità.

## Promemoria foto
Quando serve un blocco appartamento, il messaggio finale dell'esecuzione deve dire:
"Servono le foto di un appartamento per le uscite del <date>. Rispondi a questo messaggio allegando 8-12 foto dello stesso appartamento, più zona e 2-3 caratteristiche da citare: preparo e programmo io i 3 post."
Quando Nicholas risponde con le foto nella stessa sessione, prepara il blocco appartamento seguendo la sezione dedicata, con revisione indipendente.
