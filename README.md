## 📊 CO₂ Emissions Insights
Visualizzazione interattiva e previsioni delle emissioni di anidride carbonica (CO₂) per paese e periodo. L'app è sviluppata in Python con Flask, Plotly e Prophet ed è progettata per un'esperienza utente elegante e responsiva.

## 🚀 Funzionalità principali
- Selezione da 1 a 5 paesi da confrontare

- Intervallo temporale personalizzabile

- Grafici interattivi Plotly

- Previsioni con AI (Prophet) fino al 2060

- Modalità confronto con media globale

- UI moderna (palette salvia, font eleganti, layout responsive)

- Collegamenti ai dati originali (Our World in Data)


## 🧰 Tecnologie utilizzate
Python 3.x
Flask (Web server)
SQLite (Database locale)
SQLAlchemy (ORM)
Pandas (Gestione dati)
Plotly (Grafici interattivi)
Prophet (Previsioni AI)
HTML5 + CSS3 inline (UI senza dipendenze esterne)
Heroku (Hosting)


CO2 Emission App
├── app.py
├── database/
│   └── models.py, schema.db
├── templates/
│   ├── index.html
│   ├── plot.html
│   └── forecast.html
├── static/
│   └── style.css (opzionale)
├── owid-co2-data.csv
├── surface_fixed.csv
└── README.md

## ▶️ Esecuzione locale
Clona il repository:
git clone https://github.com/tuo-nome/co2-insights.git
cd co2-insights

Crea ambiente virtuale e attivalo:
bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
Installa le dipendenze:

pip install -r requirements.txt

Esegui l'app:
python app.py
Visita http://localhost:5000


## 🚀 Deploy online
L'app è disponibile su Render:
🔗 https://tuo-progetto.onrender.com


## 📄 Fonte dati
Dati CO₂: Our World in Data
Superficie paesi: World Bank

## ✒️ Crediti
Creato con passione da Lorenzo Iuliano
Font: Inter, Poppins – UI ispirata alla sostenibilità 🌿

## 📢 Condividi
Ti piace il progetto?
⭐ Star su GitHub o condividilo con #co2insights


✅ To Do (idee future)
Download grafici (.png, .csv, .pdf)
Annotazioni su eventi storici (Kyoto, Parigi)
Selezione multipla più fluida con rimozione
Confronto CO₂ per abitante o per superficie

