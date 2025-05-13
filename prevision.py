import sqlite3
import pandas as pd
from prophet import Prophet
import plotly.graph_objs as go
import plotly.offline as pyo
from datetime import datetime

# === 1. Connessione al DB ===
conn = sqlite3.connect("co2_emissions.db")
query = """
SELECT y.year AS ds, e.co2 AS y
FROM emissions e
JOIN countries c ON e.country_id = c.country_id
JOIN years y ON e.year_id = y.year_id
WHERE c.name = ?
AND e.co2 IS NOT NULL
ORDER BY y.year
"""
df = pd.read_sql_query(query, conn, params=("United States",))
conn.close()

# === 2. Prepara DataFrame ===
df['ds'] = pd.to_datetime(df['ds'], format='%Y')
df.reset_index(drop=True, inplace=True)

if df.empty or len(df) < 5:
    print("[!] Dati insufficienti per United States.")
    exit()

# === 3. Prophet ===
model = Prophet()
model.fit(df)
future = model.make_future_dataframe(periods=10, freq='Y')
forecast = model.predict(future)
forecast.reset_index(drop=True, inplace=True)

# === 4. Plotly ===
ymax = max(df["y"].max(), forecast["yhat_upper"].max()) + 500
today = datetime.now()

fig = go.Figure()

# Banda di confidenza
fig.add_trace(go.Scatter(
    x=forecast["ds"],
    y=forecast["yhat_upper"].values,
    mode='lines',
    line=dict(width=0),
    showlegend=False
))
fig.add_trace(go.Scatter(
    x=forecast["ds"],
    y=forecast["yhat_lower"].values,
    mode='lines',
    fill='tonexty',
    fillcolor='rgba(0,100,255,0.2)',
    line=dict(width=0),
    name="Intervallo di confidenza"
))

# Dati storici
fig.add_trace(go.Scatter(
    x=df["ds"],
    y=df["y"].values,
    mode='markers',
    name='Dati osservati',
    marker=dict(color='black', size=5)
))

# Previsione
fig.add_trace(go.Scatter(
    x=forecast["ds"],
    y=forecast["yhat"].values,
    mode='lines',
    name='Previsione',
    line=dict(color='blue')
))

# Linea oggi
fig.add_shape(
    type="line",
    x0=today,
    x1=today,
    y0=0,
    y1=ymax,
    line=dict(color="red", dash="dash")
)
fig.add_trace(go.Scatter(
    x=[today],
    y=[0],
    mode='lines',
    name='Oggi',
    line=dict(color="red", dash="dash"),
    showlegend=True
))

fig.update_layout(
    title="Previsioni CO₂ – United States (Plotly)",
    xaxis=dict(
        title="Anno",
        type="date"  # 👈 fondamentale per far leggere bene le date
    ),
    yaxis=dict(
        title="CO₂ Emissions (Mt)",
        range=[0, ymax]
    ),
    hovermode="x unified"
)

# === 5. Mostra nel browser ===
pyo.plot(fig, filename="co2_forecast_plotly.html")
