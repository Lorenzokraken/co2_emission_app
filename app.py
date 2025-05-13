from flask import Flask, render_template, request
from database import SessionLocal
from models import Country, Year, Emission
from prophet import Prophet
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from datetime import datetime
import sqlite3
from sqlalchemy import func

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    show_global = False
    session = SessionLocal()
    countries = session.query(Country).order_by(Country.name).all()
    years = session.query(Year).order_by(Year.year).all()

    if request.method == "POST":
        show_global = request.form.get("show_global_avg") == "1"
        country_ids = [int(request.form[f"country{i}"]) for i in range(1, 6) if f"country{i}" in request.form]
        year_start = int(request.form["year_start"])
        year_end = int(request.form["year_end"])

        emissions = session.query(Emission).join(Country).join(Year).filter(
            Emission.country_id.in_(country_ids),
            Year.year.between(year_start, year_end)
        ).all()

        data = {cid: {} for cid in country_ids}
        for e in emissions:
            data[e.country_id][e.year.year] = e.co2

        # Calcolo media mondiale (visibile come riferimento)
        global_emissions = session.query(Year.year, func.avg(Emission.co2))\
            .join(Emission.year).group_by(Year.year).order_by(Year.year).all()
        global_df = pd.DataFrame(global_emissions, columns=["ds", "y"])
        global_df["ds"] = pd.to_datetime(global_df["ds"], format='%Y')

        fig = go.Figure()
        for cid in data:
            years_sorted = sorted(data[cid].keys())
            values = [data[cid][y] for y in years_sorted]
            name = session.query(Country).filter_by(country_id=cid).first().name
            fig.add_trace(go.Scatter(x=years_sorted, y=values, mode='lines+markers', name=name))

        # Linea media globale
        if show_global:
            fig.add_trace(go.Scatter(
                x=global_df["ds"],
                y=global_df["y"],
                mode='lines',
                name='Media globale',
                line=dict(color='gray', dash='dot'),
                opacity=0.4
            ))

        fig.update_layout(
            title="CO₂ Emissions Comparison",
            xaxis_title="Year",
            yaxis_title="CO₂ Emissions (Mt)",
            hovermode="x unified"
        )

        plot_html = pyo.plot(fig, include_plotlyjs='cdn', output_type='div')
        session.close()

        return render_template("plot.html", plot_html=plot_html, year_end=year_end, country_ids=country_ids)

    session.close()
    return render_template("index.html", countries=countries, years=years)

@app.route("/predict")
def predict():
    country_id = request.args.get("country_id", default=1, type=int)
    session = SessionLocal()

    country = session.query(Country).filter_by(country_id=country_id).first()
    country_name = country.name if country else f"Paese {country_id}"

    emissions = session.query(Emission).join(Year).filter(
        Emission.country_id == country_id
    ).order_by(Year.year).all()

    data = [{"ds": e.year.year, "y": e.co2} for e in emissions if e.co2 is not None]
    df_full = pd.DataFrame(data)

    if df_full.empty:
        session.close()
        return f"<p>Nessun dato disponibile per <strong>{country_name}</strong>.</p>"

    df_full['ds'] = pd.to_datetime(df_full['ds'], format='%Y')

    # Crea una copia limitata per il training (dal 1990 in poi)
    df_train = df_full[df_full['ds'].dt.year >= 1990].copy()

    # Prophet senza stagionalità per evitare curve artificiali
    model = Prophet(changepoint_prior_scale=0.5, yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
    model.fit(df_train)

    future = model.make_future_dataframe(periods=36, freq='Y')  # fino al 2060
    forecast = model.predict(future)

    # Calcolo media globale per visualizzazione (anche nel predict)
    global_emissions = session.query(Year.year, func.avg(Emission.co2))\
        .join(Emission.year).group_by(Year.year).order_by(Year.year).all()
    global_df = pd.DataFrame(global_emissions, columns=["ds", "y"])
    global_df["ds"] = pd.to_datetime(global_df["ds"], format='%Y')

    ymax = max(df_full["y"].max(), forecast["yhat_upper"].max()) + 500
    today = datetime.now()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat_upper"],
        mode='lines',
        line=dict(width=0),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat_lower"],
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(0, 100, 255, 0.2)',
        line=dict(width=0),
        name="Intervallo di confidenza"
    ))
    fig.add_trace(go.Scatter(
        x=df_full["ds"],
        y=df_full["y"],
        mode='markers',
        name='Dati osservati',
        marker=dict(color='black', size=5)
    ))
    fig.add_trace(go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat"],
        mode='lines',
        name='Previsione',
        line=dict(color='blue')
    ))

    # Media globale in trasparenza
    fig.add_trace(go.Scatter(
        x=global_df["ds"],
        y=global_df["y"],
        mode='lines',
        name='Media globale',
        line=dict(color='gray', dash='dot'),
        opacity=0.4
    ))

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
        name="Oggi",
        line=dict(color="red", dash="dash"),
        showlegend=True
    ))

    fig.update_layout(
        title=f"Previsioni CO₂ – {country_name}",
        xaxis_title="Anno",
        yaxis_title="CO₂ Emissions (Mt)",
        hovermode="x unified",
        yaxis=dict(range=[0, ymax])
    )

    plot_html = pyo.plot(fig, include_plotlyjs='cdn', output_type='div')
    session.close()
    return render_template("plot.html", plot_html=plot_html, year_end=2023, country_ids=[country_id])

if __name__ == "__main__":
    app.run(debug=True)
