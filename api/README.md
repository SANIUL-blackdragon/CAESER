# API Documentation

## Architecture Overview
The API is built using FastAPI and follows RESTful principles. It's organized into four main components:
- Routes: Define API endpoints and request/response models
- Controllers: Handle business logic and data processing
- Models: Define data structures and database schemas
- Services: Interface with external APIs (Qloo, OpenRouter)

## Endpoints
### Cultural Insights
- `GET /insights/{market}/{category}` - Get cultural affinity data
- `POST /insights/analyze` - Analyze custom data

### Predictions
- `POST /predict/demand` - Generate demand forecasts
- `POST /predict/strategies` - Generate marketing strategies

## Development Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables:
   - `QLOO_API_KEY`
   - `OPENROUTER_API_KEY`
3. Run locally: `uvicorn main:app --reload`

## Testing
Run tests with: `pytest tests/api/`