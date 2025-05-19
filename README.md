## 📊 CO₂ Emissions Insights 
Visualizzazione interattiva e previsioni delle emissioni di anidride carbonica (CO₂) per paese e periodo.
L'app è sviluppata in Python con Flask, Plotly e Prophet ed è progettata per un'esperienza utente elegante e responsiva.
APRI QUI -> 🔗[Render](https://co2-emission-app-i5yz.onrender.com/)

## 🚀 Funzionalità principali

- ✅ Selezione **fino a 5 paesi** da confrontare, tramite menù dinamici generati al click su “+”.
- ✅ I paesi selezionati vengono **mantenuti anche dopo il submit**, permettendo un confronto iterativo senza perdere i dati.
- ✅ Aggiunta una **tooltip informativa** in alto a destra che spiega lo scopo dell'app (hover su `i`).
- ✅ Miglioramenti all’**accessibilità**: ogni `label` è ora collegata correttamente all’`id` del relativo input.
- ✅ Interfaccia scura con accenti arancione fluorescente in stile dashboard moderna.

Questa pagina rappresenta il punto di partenza per l'esplorazione delle emissioni globali e le relative previsioni AI.


## 🧰 Tecnologie utilizzate
- Python 3.x
- Flask (Web server)
- SQLite (Database locale)
- SQLAlchemy (ORM)
- Pandas (Gestione dati)
- Plotly (Grafici interattivi)
- Prophet (Previsioni AI)
- HTML5 + CSS3 inline (UI senza dipendenze esterne)
- Heroku (Hosting)

```
co2_emission_app/
├── app.py                      # Script principale Flask
├── co2_emissions.db           # Database SQLite con i dati CO2
├── database.py                # Connessione DB e sessione SQLAlchemy
├── models.py                  # Modelli SQLAlchemy per Country, Year, Emission
├── requirements.txt           # Librerie necessarie
├── runtime.txt                # Versione Python per deployment (Render, Heroku)
├── README.md                  # Documentazione del progetto
├── .gitignore                 # File e cartelle da ignorare da Git
├── templates/                 # Template HTML Flask (Jinja2)
│   ├── index.html             # Pagina principale con selezione paesi e AI
│   └── plot.html              # Visualizzazione grafico interattivo Plotly
└── __pycache__/               # File compilati Python (auto-generati)



```
## ▶️ Esecuzione locale
Clona il repository:
```
git clone https://github.com/Lorenzokraken/co2-insights.git
cd co2-insights
```
Crea ambiente virtuale e attivalo:
```
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```
Installa le dipendenze:
```
pip install -r requirements.txt
```
Esegui l'app:
```
python app.py
```
Visita http://localhost:5000

👤 Autore: Lorenzo Iuliano – Progetto a scopo educativo/professionale  
🔗 [LinkedIn](https://www.linkedin.com/in/lorenzo-iuliano-852798220/)

## 🚀 Deploy online
L'app è disponibile su Render:
🔗 [Render](https://co2-emission-app-i5yz.onrender.com/)
Potresti dover riattivare il sito e aspettare un minuto.


## 📄 Fonte dati
- Dati CO₂: Our World in Data
- Superficie paesi: World Bank
- La normalizzazione dei dati è stata gestita nel progetto co2_emission_data

## ✒️ Crediti
- Creato con passione da Lorenzo Iuliano
- Font: Inter, Poppins – UI ispirata alla sostenibilità 🌿

## 📢 Condividi
Ti piace il progetto?
⭐ Star su GitHub o condividilo con #co2insights


## ✅ To Do (idee future)
- Download grafici in altri formati
- Annotazioni su eventi storici (Kyoto, Parigi)
- Selezione multipla più fluida con rimozione
- Confronto CO₂ per abitante o per superficie

