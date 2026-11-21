# Yatra App (`yatra-app`)

A modular FastAPI backend for travel planning and destination information.
Yatra App combines weather forecasts, currency exchange rates, and place
recommendations, with standard and server-sent event (SSE) endpoints.

## Features

- **Travel planning**: Aggregates weather, places, and currency information.
- **Real-time streaming**: Streams plan data incrementally using SSE.
- **Places**: Provides recommendations from the built-in Manali, Goa, and
  Jaipur catalog.
- **Weather and currency**: Retrieves forecast and exchange-rate data from
  external APIs.
- **Caching**: Keeps fetched service data in a lightweight in-memory cache.
- **Typed data models**: Defines request and response schemas with Pydantic.
- **Tests**: Covers serialization of Pydantic models in SSE responses.

## Project structure

```text
yatra-app/
├── .env.example                  # Environment variable template
├── .gitignore                    # Excludes local secrets and generated files
├── requirements.txt              # Python dependencies
├── app/
│   ├── main.py                   # FastAPI application and router registration
│   ├── model.py                  # Request and response models
│   ├── routes/
│   │   ├── planner.py            # Aggregated travel-plan endpoint
│   │   └── stream.py             # SSE travel-plan endpoint
│   └── services/
│       ├── cache.py              # In-memory cache
│       ├── currency.py           # Currency exchange-rate service
│       ├── places.py             # Built-in place recommendations
│       └── weather.py            # Weather forecast service
└── tests/
    └── test_stream_serialization.py
```

## Getting started

### Prerequisites

- Python 3.10 or newer
- API keys for [WeatherAPI](https://www.weatherapi.com/) and
  [ExchangeRate-API](https://www.exchangerate-api.com/)

### Install dependencies

From the project directory, create and activate a virtual environment.

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
notepad .env
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp -n .env.example .env
${EDITOR:-nano} .env
```

Set these variables in `.env`:

```env
WEATHERAPI_API_KEY=your_weatherapi_key
EXCHANGERATE_API_KEY=your_exchangerate_api_key
```

Keep your real API keys private. `.env` is excluded from Git; only the
placeholder `.env.example` should be committed.

## Run the application

Start the development server from the project directory:

```bash
python -m uvicorn app.main:app --reload
```

The API is available at <http://127.0.0.1:8000>. Interactive documentation
is available at:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## API endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Application information and endpoint list |
| `POST` | `/plan/` | Aggregate weather, places, and currency data |
| `POST` | `/stream/plan` | Stream plan data as server-sent events |

Both plan endpoints accept a JSON body like:

```json
{
  "destination": "Jaipur",
  "start_date": "2026-12-01",
  "end_date": "2026-12-03",
  "base_currency": "INR"
}
```

The date range must be at least one night and no more than 14 calendar days.
The destination must also be supported by the weather service's forecast
window. The places catalog currently has entries for Manali, Goa, and Jaipur.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## License

No license file is currently included in this repository. Add a `LICENSE` file
if you intend to distribute the project under a specific license.
