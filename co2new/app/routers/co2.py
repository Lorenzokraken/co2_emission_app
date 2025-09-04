from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from prophet import Prophet
from sqlalchemy import func

from app.database.database import get_db
from app.models.models import Country, Year, Emission
from app.schemas.schemas import CountryBase, YearBase, ChartData, ChartRequest

router = APIRouter()

@router.get("/countries", response_model=List[CountryBase])
def get_countries(db: Session = Depends(get_db)):
    countries = db.query(Country).order_by(Country.name).all()
    return countries

@router.get("/years", response_model=List[YearBase])
def get_years(db: Session = Depends(get_db)):
    years = db.query(Year).order_by(Year.year).all()
    return years

@router.post("/chart", response_model=ChartData)
def generate_chart(chart_request: ChartRequest, db: Session = Depends(get_db)):
    try:
        country_ids = chart_request.country_ids
        year_start = chart_request.year_start
        year_end = chart_request.year_end
        ai = chart_request.ai
        show_density = chart_request.show_density
        
        # Validate input
        if not country_ids:
            raise HTTPException(status_code=400, detail="Seleziona almeno un paese")
        
        # Handle AI prediction with multiple countries
        if ai and len(country_ids) > 1:
            raise HTTPException(
                status_code=400, 
                detail="Le previsioni AI sono disponibili solo per un singolo paese. Seleziona solo un paese per le previsioni AI."
            )
        
        # Handle AI prediction for single country
        if ai and len(country_ids) == 1 and year_end == 2023:
            return predict_single_country(db, country_ids[0])
        
        # Handle normal comparison chart
        # Fetch all emissions data for the selected countries
        emissions = db.query(Emission).join(Country).join(Year).filter(
            Emission.country_id.in_(country_ids)
        ).all()
        
        # Convert to DataFrame for efficient processing
        data = []
        for e in emissions:
            data.append({
                'country_id': e.country_id,
                'country_name': e.country.name,
                'year': e.year.year,
                'co2': e.co2,
                'surface_km2': e.country.surface_km2
            })
        
        df = pd.DataFrame(data)
        
        # Filter by year range
        df = df[(df['year'] >= year_start) & (df['year'] <= year_end)]
        
        # Handle empty data
        if df.empty:
            raise HTTPException(status_code=400, detail="Nessun dato disponibile per i criteri selezionati")
        
        # Calculate density if requested
        if show_density:
            df['co2'] = df['co2'] / df['surface_km2']
        
        # Prepare data for ECharts
        chart_data = {
            "countries": [],
            "years": [],
            "series": []
        }
        
        # Collect all unique years
        all_years = sorted(df['year'].unique().tolist())
        chart_data["years"] = all_years
        
        # Collect data for each country
        for cid in country_ids:
            country_df = df[df['country_id'] == cid]
            if not country_df.empty:
                country_name = country_df.iloc[0]['country_name']
                chart_data["countries"].append(country_name)
                
                # Create data series with None for missing years
                values = []
                data_dict = dict(zip(country_df['year'], country_df['co2']))
                
                for year in all_years:
                    values.append(data_dict.get(year, None))
                
                chart_data["series"].append({
                    "name": country_name,
                    "type": "line",
                    "data": values,
                    "smooth": True
                })
        
        return chart_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante la generazione del grafico: {str(e)}")

def predict_single_country(db: Session, country_id: int):
    try:
        country = db.query(Country).filter_by(country_id=country_id).first()
        country_name = country.name if country else f"Paese {country_id}"

        emissions = db.query(Emission).join(Year).filter(
            Emission.country_id == country_id
        ).order_by(Year.year).all()

        data = [{"ds": e.year.year, "y": e.co2} for e in emissions if e.co2 is not None]
        df_full = pd.DataFrame(data)

        if df_full.empty:
            raise HTTPException(status_code=400, detail=f"Nessun dato disponibile per {country_name}.")

        df_full['ds'] = pd.to_datetime(df_full['ds'], format='%Y')
        df_train = df_full[df_full['ds'].dt.year >= 1990].copy()

        model = Prophet(changepoint_prior_scale=0.5, yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
        model.fit(df_train)

        future = model.make_future_dataframe(periods=36, freq='Y')
        forecast = model.predict(future)

        global_emissions = db.query(Year.year, func.avg(Emission.co2)).join(Emission, Emission.year_id == Year.year_id).group_by(Year.year).order_by(Year.year).all()
        # Convert global_emissions to a list of tuples if it's not already
        if global_emissions and not isinstance(global_emissions[0], (list, tuple)):
            global_emissions = [(row.year, row[1]) for row in global_emissions]
        # Debug: print the type and content of global_emissions
        # print(f"global_emissions type: {type(global_emissions)}")
        # print(f"global_emissions content: {global_emissions}")
        global_df = pd.DataFrame(global_emissions, columns=["ds", "y"])
        global_df["ds"] = pd.to_datetime(global_df["ds"], format='%Y')

        # Prepare data for ECharts
        # Historical data
        # Debug: print the type and content of data
        # print(f"data type: {type(data)}")
        # print(f"data content: {data}")
        historical_years = []
        historical_values = []
        for row in data:
            if isinstance(row['ds'], (int, float)):
                # If ds is already a year, use it directly
                historical_years.append(int(row['ds']))
            else:
                # If ds is a datetime object, extract the year
                historical_years.append(row['ds'].year)
            historical_values.append(row['y'])
        
        # Forecast data
        # Debug: print the type and content of forecast['ds']
        # print(f"forecast['ds'] type: {type(forecast['ds'])}")
        # print(f"forecast['ds'] content: {forecast['ds']}")
        forecast_years = []
        for date in forecast['ds']:
            if isinstance(date, (int, float)):
                # If date is already a year, use it directly
                forecast_years.append(int(date))
            else:
                # If date is a datetime object, extract the year
                forecast_years.append(date.year)
        forecast_values = forecast['yhat'].tolist()
        
        # Combine historical and forecast data
        all_years = sorted(list(set(historical_years + forecast_years)))
        
        # Create combined series
        combined_series = []
        for year in all_years:
            if year in historical_years:
                idx = historical_years.index(year)
                combined_series.append(historical_values[idx])
            elif year in forecast_years:
                idx = forecast_years.index(year)
                combined_series.append(forecast_values[idx])
            else:
                combined_series.append(None)
        
        chart_data = {
            "countries": [country_name],
            "years": all_years,
            "series": [
                {
                    "name": f"{country_name} (osservato + previsto)",
                    "type": "line",
                    "data": combined_series,
                    "smooth": True
                }
            ]
        }
        
        return chart_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante la generazione del grafico: {str(e)}")