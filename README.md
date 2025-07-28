# CAESER Project

## Overview
CAESER is a full-stack application combining data processing, API services, and frontend visualization. The system includes:
- Python backend services
- Web frontend
- Data scrapers and processors
- Database integration

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- SQLite (included)
- Docker (optional)

### Installation
1. Clone the repository
2. Install backend dependencies:
```bash
pip install -r requirements.txt
```
3. Install frontend dependencies:
```bash
cd frontend
npm install
```

### Configuration
1. Copy `.env.example` to `.env` and configure environment variables
2. Initialize database:
```bash
python data/init_db.py
```

## Project Structure

```
├── api/               # Backend services
├── data/              # Data processing and storage
├── frontend/          # Frontend application  
├── migrations/        # Database migrations
├── notebooks/         # Jupyter notebooks
├── scrapers/          # Data collection scripts
├── tests/             # Test cases
```

## Usage

### Running the Application
Start backend:
```bash
python api/main.py
```

Start frontend:
```bash
cd frontend
npm run dev
```

### Docker
```bash
docker-compose up --build
```

## Contributing

### Code of Conduct
- Be respectful and inclusive
- Keep discussions professional
- No harassment of any kind

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with:
   - Clear description of changes
   - Relevant tests
   - Updated documentation

## Troubleshooting

### Common Issues
- **Database connection errors**: Verify `.env` configuration
- **Missing dependencies**: Run `pip install -r requirements.txt` and `npm install`
- **Frontend not loading**: Check console for errors

## License
This project is licensed under the [MIT License](LICENSE) for personal and non-commercial use only.