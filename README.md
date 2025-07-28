# CÆSER - Cultural Affinity Simulation Engine for Retail

## Overview
CÆSER is an AI system designed to predict, simulate, and strategize market behavior for e-commerce merchants through cultural intelligence and predictive analytics. The system integrates:
- Qloo's Taste AI™ API for cultural insights
- DeepSeek/Kimi models via OpenRouter.ai for predictive analytics
- Discord webhooks for alerts
- Streamlit for dashboard visualization

## Project Structure
```
.
├── api/                  # FastAPI backend
│   ├── main.py           # Main API routes and logic
│   ├── services/         # Service layer implementations
│   └── utils/            # Utility functions
├── frontend/             # Streamlit dashboard
│   └── src/main.py       # Main dashboard implementation
├── data/                 # Data storage and processing
├── docs/                 # Documentation
├── migrations/           # Database migrations
├── scrapers/             # Data scraping utilities
├── tests/                # Test cases
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Multi-container setup
├── package.json          # Frontend dependencies
└── requirements.txt      # Python dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js (for frontend)
- Docker (optional)

### Installation
1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   npm install
   ```

### Configuration
1. Create a `.env` file with required API keys:
   ```
   QLOO_API_KEY=your_qloo_key
   OPENROUTER_API_KEY=your_openrouter_key
   DISCORD_WEBHOOK_URL=your_webhook_url
   ```

### Running Locally
1. Start the backend:
   ```bash
   uvicorn api.main:app --reload
   ```
2. Start the frontend:
   ```bash
   streamlit run frontend/src/main.py
   ```

### Docker Deployment
```bash
docker-compose up --build
```

## API Endpoints
Key endpoints include:
- `/analyze` - Trigger analysis pipeline
- `/insights/{location}/{category}` - Get cultural insights
- `/predict/demand` - Generate demand predictions
- `/hype/score` - Calculate hype scores
- `/discord/alert` - Send Discord alerts

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
ISC