import requests

# Test if the FastAPI server is running
try:
    response = requests.get('http://localhost:8000')
    print(f"Server response: {response.status_code}")
    print(f"Server message: {response.json()}")
except requests.exceptions.ConnectionError:
    print("Server is not running or not accessible")
except Exception as e:
    print(f"Error: {e}")

# Test the API endpoints
try:
    response = requests.get('http://localhost:8000/api/countries')
    print(f"Countries endpoint: {response.status_code}")
    if response.status_code == 200:
        countries = response.json()
        print(f"Found {len(countries)} countries")
        if countries:
            print(f"First country: {countries[0]}")
except requests.exceptions.ConnectionError:
    print("Server is not running or not accessible")
except Exception as e:
    print(f"Error accessing countries endpoint: {e}")

# Test the years endpoint
try:
    response = requests.get('http://localhost:8000/api/years')
    print(f"Years endpoint: {response.status_code}")
    if response.status_code == 200:
        years = response.json()
        print(f"Found {len(years)} years")
        if years:
            print(f"First year: {years[0]}")
            print(f"Last year: {years[-1]}")
except requests.exceptions.ConnectionError:
    print("Server is not running or not accessible")
except Exception as e:
    print(f"Error accessing years endpoint: {e}")

# Test the chart endpoint with sample data
try:
    chart_data = {
        "country_ids": [1],  # Afghanistan
        "year_start": 1990,
        "year_end": 2020,
        "ai": False,
        "show_density": False
    }
    response = requests.post('http://localhost:8000/api/chart', json=chart_data)
    print(f"Chart endpoint: {response.status_code}")
    if response.status_code == 200:
        chart_response = response.json()
        print(f"Chart data countries: {chart_response['countries']}")
        print(f"Chart data years count: {len(chart_response['years'])}")
        print(f"Chart data series count: {len(chart_response['series'])}")
    else:
        print(f"Chart endpoint error: {response.text}")
except requests.exceptions.ConnectionError:
    print("Server is not running or not accessible")
except Exception as e:
    print(f"Error accessing chart endpoint: {e}")