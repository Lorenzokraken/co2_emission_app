import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactECharts from 'echarts-for-react';
import './CO2Dashboard.css';

const CO2Dashboard = () => {
  const [countries, setCountries] = useState([]);
  const [years, setYears] = useState([]);
  const [selectedCountries, setSelectedCountries] = useState(['']);
  const [yearStart, setYearStart] = useState('1923');
  const [yearEnd, setYearEnd] = useState('2023');
  const [aiPrediction, setAiPrediction] = useState(false);
  const [showDensity, setShowDensity] = useState(false);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch initial data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [countriesRes, yearsRes] = await Promise.all([
          axios.get('/api/countries'),
          axios.get('/api/years')
        ]);
        setCountries(countriesRes.data);
        setYears(yearsRes.data);
        
        // Set default year values
        const yearList = yearsRes.data.map(y => y.year);
        setYearStart(Math.min(...yearList).toString());
        setYearEnd(Math.max(...yearList).toString());
        
        // Set United States as default selected country
        const unitedStates = countriesRes.data.find(country => country.name === 'United States');
        if (unitedStates) {
          setSelectedCountries([unitedStates.country_id.toString()]);
        }
      } catch (err) {
        setError('Errore nel caricamento dei dati iniziali');
        console.error(err);
      }
    };

    fetchData();
  }, []);

  // Generate chart when settings change
  useEffect(() => {
    if (countries.length > 0 && years.length > 0) {
      generateChart();
    }
  }, [selectedCountries, yearStart, yearEnd, aiPrediction, showDensity]);

  const generateChart = async () => {
    // Filter out empty country selections
    const validCountryIds = selectedCountries.filter(id => id !== '');
    
    if (validCountryIds.length === 0) {
      setChartData(null);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/api/chart', {
        country_ids: validCountryIds.map(id => parseInt(id)),
        year_start: parseInt(yearStart),
        year_end: parseInt(yearEnd),
        ai: aiPrediction,
        show_density: showDensity
      });

      setChartData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Errore nella generazione del grafico');
      setChartData(null);
    } finally {
      setLoading(false);
    }
  };

  const addCountry = () => {
    if (selectedCountries.length < 5 && !aiPrediction) {
      setSelectedCountries([...selectedCountries, '']);
    }
  };

  const removeCountry = () => {
    if (selectedCountries.length > 1) {
      const newCountries = [...selectedCountries];
      newCountries.pop();
      setSelectedCountries(newCountries);
    }
  };

  const updateCountry = (index, value) => {
    const newCountries = [...selectedCountries];
    newCountries[index] = value;
    setSelectedCountries(newCountries);
  };

  const toggleAiPrediction = () => {
    const newAiPrediction = !aiPrediction;
    setAiPrediction(newAiPrediction);
    
    // If AI prediction is enabled, set year range for predictions
    if (newAiPrediction) {
      setYearEnd('2023');
    } else {
      // Reset to default year range when disabling AI
      if (years.length > 0) {
        const yearList = years.map(y => y.year);
        setYearEnd(Math.max(...yearList).toString());
      }
    }
  };

  const getChartOptions = () => {
    if (!chartData) return {};

    // Filter data based on selected year range
    // For AI predictions, we show all years (historical + forecast)
    let filteredYears, filteredSeries;
    
    if (aiPrediction) {
      // For AI predictions, show all years in the chart data
      filteredYears = chartData.years;
      filteredSeries = chartData.series.map((series, index) => {
        const styledSeries = {
          ...series,
          data: series.data
        };
        
        // Make the first line orange
        if (index === 0) {
          return {
            ...styledSeries,
            itemStyle: { color: '#ff9800' },
            lineStyle: { color: '#ff9800' }
          };
        }
        
        return styledSeries;
      });
    } else {
      // For normal mode, filter by selected year range
      filteredYears = chartData.years.filter(year => year >= yearStart && year <= yearEnd);
      const yearIndices = filteredYears.map(year => chartData.years.indexOf(year));
      
      // Create a copy of series with modified styling
      filteredSeries = chartData.series.map((series, index) => {
        const baseSeries = {
          ...series,
          data: yearIndices.map(index => series.data[index])
        };
        
        // Make the first line orange
        if (index === 0) {
          return {
            ...baseSeries,
            itemStyle: { color: '#ff9800' },
            lineStyle: { color: '#ff9800' }
          };
        }
        
        return baseSeries;
      });
    }

    return {
      title: {
        text: 'CO₂ Emissions Comparison'
      },
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: chartData.countries
      },
      xAxis: {
        type: 'category',
        data: filteredYears
      },
      yAxis: {
        type: 'value',
        name: showDensity ? 'CO₂ Emissions (t/km²)' : 'CO₂ Emissions (Mt)'
      },
      series: filteredSeries
    };
  };

  return (
    <div className="main-layout">
      <div className="sidebar">
        <div className="info-box">i</div>
        <h2>Controlli</h2>
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <div className="form-group">
          <label>Paesi</label>
          <div id="countries-container">
            {selectedCountries.map((countryId, index) => (
              <select
                key={index}
                value={countryId}
                onChange={(e) => updateCountry(index, e.target.value)}
                required
              >
                <option value="">Seleziona un paese</option>
                {countries.map(country => (
                  <option key={country.country_id} value={country.country_id}>
                    {country.name}
                  </option>
                ))}
              </select>
            ))}
          </div>
          <div className="country-buttons">
            <button 
              type="button" 
              className="add-country" 
              id="add-btn" 
              onClick={addCountry}
              disabled={selectedCountries.length >= 5 || aiPrediction}
            >
              +
            </button>
            <button 
              type="button" 
              className="add-country" 
              id="remove-btn" 
              onClick={removeCountry}
              disabled={selectedCountries.length <= 1}
            >
              &minus;
            </button>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="year_start">Anno inizio</label>
          <input
            type="range"
            id="year_start"
            min={Math.min(...years.map(y => y.year))}
            max={Math.max(...years.map(y => y.year))}
            value={yearStart}
            onChange={(e) => setYearStart(e.target.value)}
            required
          />
          <span>{yearStart}</span>
        </div>

        <div className="form-group">
          <label htmlFor="year_end">Anno fine</label>
          <input
            type="range"
            id="year_end"
            min={Math.min(...years.map(y => y.year))}
            max={Math.max(...years.map(y => y.year))}
            value={yearEnd}
            onChange={(e) => setYearEnd(e.target.value)}
            required
            disabled={aiPrediction}
          />
          <span>{yearEnd}</span>
        </div>

        <div className="form-group">
          <div className="checkbox-group">
            <div>
              <input 
                type="checkbox" 
                id="ai-toggle" 
                checked={aiPrediction}
                onChange={toggleAiPrediction}
                disabled={selectedCountries.filter(id => id !== '').length > 1}
              />
              <label htmlFor="ai-toggle">AI Previsioni</label>
              {selectedCountries.filter(id => id !== '').length > 1 && (
                <span style={{ fontSize: '0.7em', color: '#ff9800', marginLeft: '5px' }}>
                  (solo con 1 paese)
                </span>
              )}
            </div>
            <div>
              <input 
                type="checkbox" 
                id="density-toggle" 
                checked={showDensity}
                onChange={(e) => setShowDensity(e.target.checked)}
              />
              <label htmlFor="density-toggle">CO₂ / km²</label>
            </div>
          </div>
        </div>

        <div className="auto-generate-info">
          <p>ℹ️ Il grafico si aggiorna automaticamente quando cambi le impostazioni</p>
        </div>
        
        <div className="sidebar-footer">
          Creato da Lorenzo Iuliano
        </div>
      </div>
      
      <div className="main-content">
        <div id="plot-container">
          {loading ? (
            <div className="loading">
              <div className="spinner"></div>
              <p>Generazione grafico in corso...</p>
            </div>
          ) : chartData ? (
            <ReactECharts option={getChartOptions()} style={{ height: '500px', width: '100%' }} />
          ) : error ? (
            <div className="error-display">
              <h3>⚠️ Errore</h3>
              <div>{error}</div>
            </div>
          ) : (
            <div className="placeholder">
              <p>Seleziona uno o più paesi per visualizzare il grafico</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CO2Dashboard;