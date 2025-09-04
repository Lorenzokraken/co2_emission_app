# 🌱 Applicazione di Emissioni CO2 - Versione FastAPI + React (v2.0)

Questa è una **riscrittura completa** dell'applicazione di Emissioni CO2 utilizzando tecnologie moderne: **FastAPI** per il backend e **React** per il frontend.

## 🆕 Novità della v2.0 rispetto alla v1.0

| Caratteristica | v1.0 (Flask) | v2.0 (FastAPI + React) |
|---------------|--------------|------------------------|
| **Architettura** | Monolitica | Backend/API + Frontend separati |
| **Backend** | Flask | FastAPI (async, autodocumentazione) |
| **Frontend** | Jinja2 Templates | React moderno con componenti |
| **Database** | SQLAlchemy base | SQLAlchemy avanzato con sessioni |
| **Grafici** | Matplotlib statici | ECharts interattivi |
| **Previsioni AI** | Base | Avanzate con Prophet |
| **Design** | Base | Moderno e responsive |
| **Performance** | Media | Alta |

## 📁 Struttura del Progetto

```
co2new/
├── app/                    # Backend FastAPI
│   ├── database/          # Configurazione del database
│   ├── models/            # Modelli SQLAlchemy
│   ├── routers/           # Route API
│   ├── schemas/           # Schemi Pydantic
│   └── main.py            # Applicazione FastAPI principale
├── frontend/              # Frontend React
│   ├── public/            # Asset pubblici
│   ├── src/               # Codice sorgente React
│   │   ├── components/    # Componenti React
│   │   └── ...
│   ├── static/            # File CSS statici
│   ├── package.json       # Dipendenze frontend
│   └── ...
├── co2_emissions.db       # File del database
├── requirements.txt       # Dipendenze backend
└── main.py               # Punto di ingresso dell'applicazione
```

## ⚙️ Istruzioni di Installazione

### 🖥️ Configurazione del Backend

1. Creare un ambiente virtuale:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Windows: venv\Scripts\activate
   ```

2. Installare le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

3. Eseguire il server FastAPI:
   ```bash
   python main.py
   ```

   Il backend sarà disponibile all'indirizzo http://localhost:8000

### 🌐 Configurazione del Frontend

1. Navigare nella directory del frontend:
   ```bash
   cd frontend
   ```

2. Installare le dipendenze:
   ```bash
   npm install
   ```

3. Avviare il server di sviluppo React:
   ```bash
   npm start
   ```

   Il frontend sarà disponibile all'indirizzo http://localhost:3000

## 🚀 Funzionalità dell'Applicazione

### 📊 Dashboard Principale
- **Selezione Paesi**: Confronta le emissioni di CO2 tra diversi paesi (fino a 5 contemporaneamente)
- **Intervallo Anni**: Seleziona l'intervallo di anni per l'analisi dei dati
- **Visualizzazione Densità**: Mostra le emissioni per chilometro quadrato
- **Previsioni AI**: Utilizza modelli di intelligenza artificiale per prevedere le future emissioni (solo per un singolo paese)

### ✨ Caratteristiche Speciali
- **Grafici Interattivi**: Visualizzazione avanzata con grafici a linee interattivi
- **Design Responsive**: Interfaccia adattabile a dispositivi desktop e mobile
- **Aggiornamento Automatico**: I grafici si aggiornano automaticamente quando si modificano i parametri
- **Prima Linea Arancione**: La prima serie di dati nel grafico è sempre visualizzata in arancione per una migliore identificazione

## 📚 Documentazione API

Una volta avviato il backend, è possibile accedere alla documentazione API all'indirizzo:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ Tecnologie Utilizzate

### 🔧 Backend
- **FastAPI**: Framework web veloce per la creazione di API con Python
- **SQLAlchemy**: Toolkit ORM per database Python
- **Pandas**: Libreria per l'analisi e manipolazione dei dati
- **Prophet**: Libreria di Facebook per previsioni basate su serie temporali
- **SQLite**: Database leggero e senza server

### 🎨 Frontend
- **React**: Libreria JavaScript per la creazione di interfacce utente
- **ECharts**: Libreria di visualizzazione grafica potente e flessibile
- **Axios**: Client HTTP basato su Promise per il browser e Node.js
- **CSS3**: Fogli di stile per la formattazione e il design

## 🚢 Deployment

Per costruire il frontend React per la produzione:
```bash
cd frontend
npm run build
```

I file compilati saranno nella directory `frontend/build`.

## 🐛 Risoluzione dei Problemi

### ❗ Problemi Comuni

1. **Database non trovato**: Assicurati che il file `co2_emissions.db` sia presente nella directory principale
2. **Errore di connessione al database**: Verifica che il database non sia corrotto
3. **Dipendenze mancanti**: Esegui `pip install -r requirements.txt` per il backend e `npm install` per il frontend
4. **Porte occupate**: Verifica che le porte 8000 (backend) e 3000 (frontend) non siano in uso da altri processi

### 📋 Requisiti di Sistema

- **Python 3.7+** per il backend
- **Node.js 12+** per il frontend
- **npm 6+** per la gestione delle dipendenze frontend

## 🤝 Contribuire al Progetto

1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/NuovaFeature`)
3. Commit delle modifiche (`git commit -am 'Aggiungi nuova feature'`)
4. Push al branch (`git push origin feature/NuovaFeature`)
5. Crea una nuova Pull Request

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT.

## 📧 Contatti

Creato da Lorenzo Iuliano

Per segnalazioni di bug o richieste di funzionalità, aprire una issue nel repository.