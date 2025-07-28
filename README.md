# CAESER Project

## Overview

CAESER (Cultural Affinity Simulation Engine for Retail) is a full-stack application designed to empower retailers with AI-driven insights into cultural trends and product demand across various markets. By integrating data from multiple sources—such as the Qloo Insights API for cultural affinity data and OpenRouter for large language model (LLM) predictions—CAESER delivers actionable recommendations to optimize marketing strategies, forecast demand, and manage inventory effectively.

## What is CAESER?
CAESER is a tool that helps retailers:

Analyze Cultural Affinities: Understand how cultural preferences vary by region, demographics, and product categories.
Predict Demand: Forecast potential sales uplift for products using AI and cultural data.
Generate Marketing Strategies: Receive AI-generated suggestions tailored to market trends and consumer behavior.
Simulate Buyer Behavior: Model synthetic buyers to estimate product hype and engagement.
Integrate External Data: Combine insights from Google Trends, social media, and other sources for a holistic view.

The project leverages a Python-based FastAPI backend, a Streamlit-powered frontend, data scrapers for real-time information, and a SQLite database for storage, making it a robust solution for retail analytics.
Key Features

Cultural Insights: Fetches affinity data via the Qloo API to identify market preferences.
Demand Forecasting: Uses LLMs through OpenRouter to predict sales trends.
Hype Score Calculation: Evaluates product popularity with a custom engine.
Interactive Dashboard: Visualizes insights and predictions via Streamlit.
Modular Design: Supports additional integrations like Salesforce and Twitter.

## API Keys
CAESER relies on several external APIs, requiring specific API keys for full functionality. Below is a guide to obtaining and configuring them:
Required API Keys

### Qloo Insights API

Purpose: Provides cultural affinity data critical to CAESER’s core functionality.
How to Obtain: Contact the Qloo team at support@qloo.com to request an API key (typically issued within one business day).
Documentation: See Qloo Insights API Guide for detailed usage instructions.


### OpenRouter API

Purpose: Enables access to LLMs for demand predictions and strategy generation.
How to Obtain: Sign up at openrouter.ai and generate an API key from your account dashboard.
Documentation: Refer to OpenRouter LLM Integration Guide for integration examples.



### Optional API Keys

#### Google Sheets API

Purpose: Allows data import/export with Google Sheets.
How to Obtain: Set up a Google Cloud project, enable the Sheets API, and download credentials from Google Developers.
Usage: Configure GOOGLE_SHEETS_API_KEY, GOOGLE_SHEETS_CREDENTIALS, and SPREADSHEET_ID in .env.


#### Twitter API

Purpose: Enables social media scraping for additional data.
How to Obtain: Apply for a Twitter Developer account at developer.twitter.com and generate API keys and tokens.
Usage: Set TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, and TWITTER_ACCESS_TOKEN_SECRET in .env.


#### Salesforce API

Purpose: Integrates with Salesforce for CRM data.
How to Obtain: Create a connected app in Salesforce and obtain credentials from Salesforce Developer Guide.
Usage: Configure SALESFORCE_CLIENT_ID, SALESFORCE_CLIENT_SECRET, SALESFORCE_USERNAME, SALESFORCE_PASSWORD, SALESFORCE_TOKEN, and SALESFORCE_INSTANCE_URL in .env.


## Proxy List

Purpose: Supports proxy usage for scraping tasks.
How to Obtain: Provide a comma-separated list of proxy URLs (e.g., proxy1,proxy2,proxy3).
Usage: Set PROXY_LIST in .env.



## Configuration

Copy the .env.example file to .env:cp .env.example .env


Open .env in a text editor and insert your API keys:QLOO_API_KEY=your_qloo_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Add optional keys as needed


Save the file. CAESER will load these variables at runtime.

Note: The core functionality requires only Qloo and OpenRouter keys. Optional keys enhance features but are not mandatory.
Setup Instructions
Prerequisites

Python 3.9+: For backend and frontend services.
SQLite: Included by default for database storage.
Docker: Optional, for containerized deployment.

## Installation

Clone the Repository:
git clone: https://github.com/SANIUL-blackdragon/CAESER.git
cd caeser


## Install Dependencies:

pip install -r requirements.txt

This installs all necessary Python packages, including FastAPI, Streamlit, and Scrapy.

## Configure Environment Variables:

Follow the API Keys section to set up .env.


## Initialize the Database:
python data/init_db.py

This runs Alembic migrations to set up the SQLite database (caeser.db).


## Project Structure
├── api/               # Backend FastAPI services
├── data/              # Database and data processing scripts
├── frontend/          # Streamlit frontend application
├── migrations/        # Alembic database migrations
├── notebooks/         # Jupyter notebooks for analysis
├── scrapers/          # Web scraping scripts (e.g., social_media_spider.py)
├── tests/             # Unit and integration tests
├── docs/              # Documentation files
├── .env               # Environment variables (create from .env.example)
├── docker-compose.yml # Docker configuration
├── README.md          # This file

## Usage
Running Locally

### Start the Backend:
uvicorn api.main:app --host 0.0.0.0 --port 8000

The FastAPI server will be available at http://localhost:8000.

### Start the Frontend:
streamlit run frontend/src/main.py

Access the dashboard at http://localhost:8501.


### Running with Docker

Build and Run:docker-compose up --build


Backend: http://localhost:8000
Frontend: http://localhost:8501



## How It Works
CAESER operates through a modular pipeline:

### Data Collection:

Scrapers (e.g., social_media_spider.py) gather data from sources like Twitter and Google Trends.
Stored in the SQLite database (caeser.db).


### Cultural Insights:

The Qloo API (api/services/qloo_service.py) fetches affinity data based on location and category inputs.


### Prediction Generation:

OpenRouter’s LLM (api/main.py:/predict/demand) processes data and insights to forecast demand and suggest strategies.


### Hype Score Calculation:

A custom engine (api/services/hype_engine.py) computes a hype score reflecting product buzz.


### Visualization:

The Streamlit frontend (frontend/src/main.py) displays insights, predictions, and charts in an interactive dashboard.



For a detailed system overview, see CAESER System Visualizations, which includes architecture diagrams and data flows.

## Contributing Code of Conduct

Be respectful and inclusive.
Maintain professional discussions.
No harassment tolerated.

## Guidelines

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes with clear messages.
Submit a pull request with:
Description of changes.
Relevant tests.
Updated documentation.



## Troubleshooting Common Issues

Database Errors: Ensure DB_PATH in .env points to data/caeser.db and run python data/init_db.py.
API Key Issues: Verify keys in .env match those from providers.
Frontend Not Loading: Check Streamlit logs for errors and ensure the backend is running.

## License

CAESER is distributed under a modified MIT License that balances open-source accessibility with specific restrictions to protect the project's intent. Here's what you need to know:

What You Can Do





Personal Use: You are free to download, use, modify, and share CAESER for personal projects, experimentation, or learning purposes.



Non-Commercial Use: You can use CAESER in non-profit or educational settings, such as academic research or community projects, without any additional permission.

What You Cannot Do Without Permission





Commercial Use: Using CAESER for any profit-making activities—such as in a business, for paid services, or to generate revenue—is prohibited unless you obtain explicit written permission from the author. Examples include:





Running CAESER in a commercial retail environment.



Selling products or services derived from CAESER.



Incorporating CAESER into a paid application or tool.



To request permission for commercial use, contact the author, SANIUL-blackdragon, at mdalifsaniul@gmail.com.

Additional Responsibilities





API Compliance: CAESER integrates with external APIs like Qloo and OpenRouter. If you use these services, you must comply with their respective terms of service. Check their documentation for details:





Qloo API Terms



OpenRouter Terms



No Warranty: CAESER is provided "as is," meaning there are no guarantees about its performance or suitability for your needs. Use it at your own risk—see the full disclaimer in the LICENSE file.

Full License Text

For the complete legal terms, including the copyright notice and detailed disclaimer, please refer to the LICENSE file in the project repository.

Why This License?

The modified MIT License ensures CAESER remains freely available for personal and non-commercial exploration while allowing the author to retain control over its commercial applications. This approach supports the open-source community while safeguarding the project's integrity.

If you have questions about what’s allowed or need clarification, feel free to reach out to the author!

Third-Party API Compliance
Users must comply with the terms of service of integrated APIs (e.g., Qloo, OpenRouter). Review their respective documentation for obligations.