
from flask import Flask, render_template, request
from database import SessionLocal
from models import Country, Year, Emission
from prophet import Prophet
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from datetime import datetime
from sqlalchemy import func

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    session = SessionLocal()
    countries = session.query(Country).order_by(Country.name).all()
    years = session.query(Year).order_by(Year.year).all()

    country_ids = []
    year_start = None
    year_end = None
    ai = False
    show_density = False

    if request.method == "POST":
        ai = request.form.get("ai") == "on"
        show_density = request.form.get("show_density") == "on"
        country_ids = [int(request.form[f"country{i}"]) for i in range(1, 6) if f"country{i}" in request.form]

        year_start = int(request.form.get("year_start", 1990))
        year_end = int(request.form.get("year_end", 2023))

        emissions = session.query(Emission).join(Country).join(Year).filter(
            Emission.country_id.in_(country_ids),
            Year.year.between(year_start, year_end)
        ).all()

        data = {cid: {} for cid in country_ids}
        for e in emissions:
            if show_density:
                surface = session.query(Country.surface_km2).filter_by(country_id=e.country_id).scalar() or 1
                data[e.country_id][e.year.year] = e.co2 / surface
            else:
                data[e.country_id][e.year.year] = e.co2

        global_emissions = session.query(Year.year, func.avg(Emission.co2))            .join(Emission.year).group_by(Year.year).order_by(Year.year).all()
        global_df = pd.DataFrame(global_emissions, columns=["ds", "y"])
        global_df["ds"] = pd.to_datetime(global_df["ds"], format='%Y')

        y_title = "CO₂ Emissions (t/km²)" if show_density else "CO₂ Emissions (Mt)"

        color_palette = [
            ('#FF6A00', 'rgba(255,106,0,0.2)'),
            ('#00BFFF', 'rgba(0,191,255,0.2)'),
            ('#32CD32', 'rgba(50,205,50,0.2)'),
            ('#FFD700', 'rgba(255,215,0,0.2)'),
            ('#FF1493', 'rgba(255,20,147,0.2)')
        ]

        fig = go.Figure()
        for i, cid in enumerate(data):
            years_sorted = sorted(data[cid].keys())
            values = [data[cid][y] for y in years_sorted]
            name = session.query(Country).filter_by(country_id=cid).first().name
            line_color, fill_color = color_palette[i % len(color_palette)]

            fig.add_trace(go.Scatter(
                x=years_sorted,
                y=values,
                mode='lines+markers',
                name=name,
                line=dict(color=line_color, width=2),
                fill='tozeroy',
                fillcolor=fill_color,
                marker=dict(color='white', size=4)
            ))

        fig.update_layout(
            title="CO₂ Emissions Comparison",
            xaxis_title="Year",
            yaxis_title=y_title,
            hovermode="x unified",
            template='plotly_dark',
            paper_bgcolor='#121212',
            plot_bgcolor='#121212',
            font=dict(color='white'),
            title_font=dict(size=22, color='#ff9800'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.08)', zeroline=False),
            yaxis=dict(gridcolor='rgba(255,255,255,0.08)', zeroline=False)
        )

        plot_html = pyo.plot(fig, include_plotlyjs='cdn', output_type='div')
        session.close()

        return render_template("plot.html", plot_html=plot_html, year_end=year_end,
                               year_start=year_start, country_ids=country_ids,
                               ai=ai, show_density=show_density)

    session.close()
    return render_template("index.html", countries=countries, years=years)


@app.route("/predict", methods=["GET"])
def predict():
    country_id = request.args.get("country_id", default=1, type=int)
    session = SessionLocal()

    try:
        country = session.query(Country).filter_by(country_id=country_id).first()
        country_name = country.name if country else f"Paese {country_id}"

        emissions = session.query(Emission).join(Year).filter(
            Emission.country_id == country_id
        ).order_by(Year.year).all()

        data = [{"ds": e.year.year, "y": e.co2} for e in emissions if e.co2 is not None]
        df_full = pd.DataFrame(data)

        if df_full.empty:
            return f"<p>Nessun dato disponibile per <strong>{country_name}</strong>.</p>"

        df_full['ds'] = pd.to_datetime(df_full['ds'], format='%Y')
        df_train = df_full[df_full['ds'].dt.year >= 1990].copy()

        model = Prophet(changepoint_prior_scale=0.5, yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
        model.fit(df_train)

        future = model.make_future_dataframe(periods=36, freq='Y')
        forecast = model.predict(future)

        global_emissions = session.query(Year.year, func.avg(Emission.co2))            .join(Emission.year).group_by(Year.year).order_by(Year.year).all()
        global_df = pd.DataFrame(global_emissions, columns=["ds", "y"])
        global_df["ds"] = pd.to_datetime(global_df["ds"], format='%Y')

        ymax = max(df_full["y"].max(), forecast["yhat_upper"].max()) + 500
        today = datetime.now()

        combined_df = pd.concat([
            df_full[["ds", "y"]].rename(columns={"y": "value"}),
            forecast[["ds", "yhat"]].rename(columns={"yhat": "value"})
        ]).drop_duplicates(subset="ds").sort_values("ds")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat_upper"],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        fig.add_trace(go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat_lower"],
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(255, 140, 0, 0.3)',
            line=dict(width=0),
            name="Intervallo di confidenza"
        ))

        fig.add_trace(go.Scatter(
            x=combined_df["ds"],
            y=combined_df["value"],
            mode='lines+markers',
            name='CO₂ Totale (osservato + previsto)',
            line=dict(color='rgba(255,140,0,1)', width=3),
            marker=dict(color='white', size=5),
            fill='tozeroy',
            fillcolor='rgba(255,94,0,0.25)'
        ))

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
            template='plotly_dark',
            paper_bgcolor='#121212',
            plot_bgcolor='#121212',
            font=dict(color='white'),
            title_font=dict(size=22, color='#ff9800'),
            legend=dict(bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(gridcolor='rgba(255,255,255,0.08)', zeroline=False),
            yaxis=dict(gridcolor='rgba(255,255,255,0.08)', zeroline=False, range=[0, ymax])
        )

        plot_html = pyo.plot(fig, include_plotlyjs='cdn', output_type='div')
        return render_template("plot.html", plot_html=plot_html, year_end=2023, country_ids=[country_id])

    except Exception as e:
        return f"<p>Errore durante la generazione del grafico: {str(e)}</p>"

    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)
