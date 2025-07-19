# CÆSER (Cultural Affinity Simulation Engine for Retail)

## Project Overview
CÆSER is an AI system designed to predict, simulate, and strategize market behavior for e-commerce merchants through cultural intelligence and predictive analytics. The system integrates Qloo's Taste AI™ API for cultural insights and DeepSeek/Kimi models via OpenRouter.ai for predictive analytics.

## Key Features
- Cultural affinity analysis
- Demand forecasting
- Marketing strategy recommendations
- Synthetic buyer modeling

## Directory Structure
- `/api` - Backend API code (FastAPI)
  - `/routes` - API endpoints
  - `/controllers` - Business logic
  - `/models` - Data models
  - `/services` - External service integrations
- `/data` - Data processing and storage
  - `/raw` - Raw data files
  - `/processed` - Cleaned/processed data
  - `/schemas` - Data schemas/definitions
- `/frontend` - Streamlit dashboard
  - `/src` - Source code
  - `/public` - Static assets
  - `/components` - Reusable components
- `/tests` - Unit and integration tests
- `/docs` - Project documentation
  - `/md` - Markdown files
  - `/txt` - Text files

## Setup Instructions
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see `.env.example`)
4. Run the API: `uvicorn api.main:app --reload`
5. Run the frontend: `streamlit run frontend/src/main.py`

## Usage
1. Configure your merchant profile
2. Select target market and product category
3. View cultural insights and predictions
4. Generate marketing strategies

## Contribution Guidelines
- Follow PEP 8 style guide for Python
- Write unit tests for new features
- Document all public interfaces
- Create pull requests to the `develop` branch