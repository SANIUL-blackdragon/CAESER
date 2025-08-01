# Project Dump: D:\LAPTOP\TO_EARN\AI\CAESER
Generated: 2025-08-01 08:58:14
Max File Size: 10MB

---


## File: .env

``$language

# .env  (overwrite existing file)
STARTUP_MESSAGE="CÆSER API is live and ready 🚀"

# --- API Keys ---
QLOO_API_KEY=
OPENROUTER_API_KEY=

# --- Database (PostgreSQL) ---
# .env
DB_PATH=postgresql+asyncpg://caeser_user:caeser_pass@localhost:5432/caeser

# --- Redis ---
REDIS_URL=redis://redis:6379/0

# --- API Configuration ---
API_BASE_URL=http://localhost:8000

# --- Discord ---
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1400641359064596553/qbMMf4rebXmD0IcWHgqXW-30n5FeL2-zjSk3em-RxTA_csEJ4zAr6hIFSCr0CBW4FaAq

# --- Email (optional) ---
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENT=recipient@example.com

# --- Google Sheets (optional) ---
GOOGLE_SHEETS_API_KEY=your_google_sheets_api_key
GOOGLE_SHEETS_CREDENTIALS={"type": "service_account", "project_id": "your_project_id"}
SPREADSHEET_ID=your_spreadsheet_id

# --- Salesforce (optional) ---
SALESFORCE_CLIENT_ID=your_client_id
SALESFORCE_CLIENT_SECRET=your_client_secret
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
SALESFORCE_TOKEN=your_security_token
SALESFORCE_INSTANCE_URL=https://your_instance.salesforce.com

# --- Default behaviour ---
DEFAULT_FORECAST_DAYS=90
MIN_TREND_DATA_POINTS=3
DEFAULT_CONFIDENCE_THRESHOLD=0.85
DEFAULT_KEYWORDS=sneakers,boots
DEFAULT_GENDER_OPTIONS=All,Male,Female
DEFAULT_INSIGHT_TYPES=brand,demographics,heatmap
`


## File: .env.example

``$language

# .env  (overwrite existing file)
STARTUP_MESSAGE="CÆSER API is live and ready 🚀"

# --- API Keys ---
QLOO_API_KEY=your_qloo_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# --- Database (PostgreSQL) ---
DB_PATH=postgresql://caeser_user:caeser_pass@postgres:5432/caeser

# --- Redis ---
REDIS_URL=redis://redis:6379/0

# --- API Configuration ---
API_BASE_URL=http://localhost:8000

# --- Discord ---
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_STRING

# --- Email (optional) ---
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENT=recipient@example.com

# --- Google Sheets (optional) ---
GOOGLE_SHEETS_API_KEY=your_google_sheets_api_key
GOOGLE_SHEETS_CREDENTIALS={"type": "service_account", "project_id": "your_project_id"}
SPREADSHEET_ID=your_spreadsheet_id

# --- Salesforce (optional) ---
SALESFORCE_CLIENT_ID=your_client_id
SALESFORCE_CLIENT_SECRET=your_client_secret
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
SALESFORCE_TOKEN=your_security_token
SALESFORCE_INSTANCE_URL=https://your_instance.salesforce.com

# --- Default behaviour ---
DEFAULT_FORECAST_DAYS=90
MIN_TREND_DATA_POINTS=3
DEFAULT_CONFIDENCE_THRESHOLD=0.85
DEFAULT_KEYWORDS=sneakers,boots
DEFAULT_GENDER_OPTIONS=All,Male,Female
DEFAULT_INSIGHT_TYPES=brand,demographics,heatmap
`


## File: alembic.ini

``$language

# alembic.ini
[alembic]
script_location = %(here)s/migrations
sqlalchemy.url = postgresql+asyncpg://caeser_user:caeser_pass@localhost:5432/caeser
# Logging configuration
# This section configures the logging for Alembic and SQLAlchemy.
# It uses a simple console handler that outputs to stderr.
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
`


## File: caeser_visuals.html

``$language

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CÆSER System Visualizations</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .glass-effect {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .hover-scale { transition: transform 0.3s ease; }
        .hover-scale:hover { transform: scale(1.02); }
        .animate-fade-in { animation: fadeIn 0.6s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .section-divider {
            background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
            height: 1px;
            margin: 2rem 0;
        }

        /* Dark mode styles */
        .dark body { background-color: #0f172a; color: #e2e8f0; }
        .dark .bg-white { background-color: #1e293b !important; color: #e2e8f0 !important; }
        .dark .text-gray-800 { color: #e2e8f0 !important; }
        .dark .text-gray-600 { color: #94a3b8 !important; }
        .dark .shadow-lg { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4); }
        .dark .section-divider { background: linear-gradient(90deg, transparent, #475569, transparent); }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="gradient-bg text-white p-4 shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold flex items-center">
                <i data-lucide="activity" class="mr-2"></i>
                CÆSER System Visualizations
            </h1>
            <button id="darkModeToggle" class="p-2 rounded-lg glass-effect hover:scale-110 transition-transform">
                <i data-lucide="moon" id="darkIcon"></i>
                <i data-lucide="sun" id="lightIcon" class="hidden"></i>
            </button>
        </div>
    </nav>

    <!-- Hero Section -->
    <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="gradient-bg text-white rounded-2xl p-8 mb-8 hover-scale">
            <h2 class="text-3xl font-bold mb-4">Cultural Affinity Simulation Engine for Retail</h2>
            <p class="text-lg opacity-90">
                Comprehensive visual representation of the CÆSER system. Each visualization helps developers understand 
                architecture, data flow, and key insights from cultural affinity analysis, demand forecasting, marketing strategies, and synthetic buyer modeling.
            </p>
        </div>

        <!-- System Architecture Section -->
        <section class="mb-12 animate-fade-in">
            <h2 class="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                <i data-lucide="layout-dashboard" class="mr-3 text-indigo-600"></i>
                Overall System Architecture
            </h2>
            <p class="text-gray-600 mb-6">
                The architecture visualizations illustrate how the CÆSER system is structured and how data flows between modules. 
                Understanding the architecture is crucial for developers to grasp system interactions.
            </p>

            <div class="grid md:grid-cols-2 gap-8">
                <div class="bg-white rounded-xl shadow-lg p-6 hover-scale">
                    <h3 class="text-xl font-semibold mb-4 text-gray-800">System Flow Chart</h3>
                    <p class="text-sm text-gray-600 mb-4">
                        High-level data flow between main modules - from user interaction to final insights
                    </p>
                    <div class="mermaid">
                        graph TD
                            A[👤 User] --> B[🎨 Frontend]
                            B --> C[⚙️ API Gateway]
                            C --> D[📊 Data Processing]
                            D --> E[🎯 Qloo API]
                            D --> F[🤖 OpenRouter API]
                            D --> G[💾 Database]
                            C --> H[🔔 Services]
                            H --> I[💬 Discord Bot]
                            B --> J[📈 Dashboard]
                    </div>
                </div>

                <div class="bg-white rounded-xl shadow-lg p-6 hover-scale">
                    <h3 class="text-xl font-semibold mb-4 text-gray-800">Sequence Diagram</h3>
                    <p class="text-sm text-gray-600 mb-4">
                        Detailed view of processing steps and component interactions
                    </p>
                    <div class="mermaid">
                        sequenceDiagram
                            participant U as 👤 User
                            participant F as 🎨 Frontend
                            participant A as ⚙️ API
                            participant D as 📊 Data Processing
                            participant Q as 🎯 Qloo
                            participant O as 🤖 OpenRouter
                            participant DB as 💾 Database
                            participant DS as 💬 Discord

                            U->>F: Select market/product
                            F->>A: Request insights
                            A->>D: Process request
                            D->>Q: Fetch cultural data
                            Q-->>D: Return affinity scores
                            D->>O: Generate predictions
                            O-->>D: Return predictions
                            D->>DB: Store data
                            D-->>A: Send processed data
                            A-->>F: Return insights
                            F-->>U: Display results
                            A->>DS: Send Discord alert
                    </div>
                </div>
            </div>
        </section>

        <div class="section-divider"></div>

        <!-- Cultural Affinity Analysis -->
        <section class="mb-12 animate-fade-in">
            <h2 class="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                <i data-lucide="users" class="mr-3 text-green-600"></i>
                Cultural Affinity Analysis
            </h2>
            <p class="text-gray-600 mb-6">
                Identify market preferences based on cultural insights from Qloo API. These visualizations help understand 
                how affinity scores are distributed across traits, regions, and categories.
            </p>

            <div class="grid lg:grid-cols-3 gap-6 mb-8">
                <div class="bg-white rounded-xl shadow-lg p-6 hover-scale">
                    <h4 class="text-lg font-semibold mb-3">Affinity Scores</h4>
                    <canvas id="affinityBarChart" width="400" height="200"></canvas>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-6 hover-scale lg:col-span-2">
                    <h4 class="text-lg font-semibold mb-3">Regional Heat Map</h4>
                    <div id="affinityHeatMap" class="w-full h-64"></div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-lg p-6">
                <h4 class="text-lg font-semibold mb-3">Trait Relationships</h4>
                <div class="mermaid">
                    graph LR
                        A[🎭 Arts & Culture] --> B[🛍️ Shopping]
                        A --> C[🍽️ Food & Drink]
                        B --> D[💰 Luxury Goods]
                        C --> D
                        B --> E[🎯 Targeted Marketing]
                        C --> E
                </div>
            </div>
        </section>

        <div class="section-divider"></div>

        <!-- Demand Forecasting -->
        <section class="mb-12 animate-fade-in">
            <h2 class="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                <i data-lucide="trending-up" class="mr-3 text-blue-600"></i>
                Demand Forecasting
            </h2>
            <p class="text-gray-600 mb-6">
                Predict sales uplift based on cultural insights. Visualize demand trends, cumulative growth, and forecast distributions.
            </p>

            <div class="grid lg:grid-cols-2 gap-6 mb-8">
                <div class="bg-white rounded-xl shadow-lg p-6 hover-scale">
                    <h4 class="text-lg font-semibold mb-3">Demand Trends</h4>
                    <canvas id="demandLineChart" width="400" height="200"></canvas>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-6 hover-scale">
                    <h4 class="text-lg font-semibold mb-3">Cumulative Growth</h4>
                    <canvas id="demandAreaChart" width="400" height="200"></canvas>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-lg p-6">
                <h4 class="text-lg font-semibold mb-3">Demand Distribution</h4>
                <div id="demandBoxPlot" class="w-full h-64"></div>
            </div>
        </section>

        <div class="section-divider"></div>

        <!-- Marketing Strategies -->
        <section class="mb-12 animate-fade-in">
            <h2 class="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                <i data-lucide="target" class="mr-3 text-purple-600"></i>
                Marketing Strategies
            </h2>
            <p class="text-gray-600 mb-6">
                Generate actionable recommendations based on insights. Track resource allocation, strategy effectiveness, and decision trees.
            </p>

            <div class="grid md:grid-cols-2 gap-8">
                <div class="bg-white rounded-xl shadow-lg p-6 hover-scale">
                    <h4 class="text-lg font-semibold mb-3">Resource Allocation</h4>
                    <div class="mermaid">
                        pie title Marketing Budget Distribution
                            "📱 Social Media" : 40
                            "📧 Email Campaign" : 30
                            "🤳 Influencer Marketing" : 30
                    </div>
                </div>

                <div class="bg-white rounded-xl shadow-lg p-6 hover-scale">
                    <h4 class="text-lg font-semibold mb-3">Strategy Flow</h4>
                    <div class="mermaid">
                        sankey-beta
                            Social Media,Engagement,100
                            Email Campaign,Conversions,50
                            Influencer Marketing,Awareness,80
                            Engagement,Sales,60
                            Conversions,Sales,40
                            Awareness,Sales,20
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-lg p-6 mt-6">
                <h4 class="text-lg font-semibold mb-3">Decision Tree</h4>
                <div class="mermaid">
                    graph TD
                        A[🎯 Start] --> B{💰 Budget > $10k?}
                        B -->|Yes| C[🤳 Influencer Marketing]
                        B -->|No| D{👥 Young Audience?}
                        D -->|Yes| E[📱 Social Media]
                        D -->|No| F[📧 Email Campaign]
                </div>
            </div>
        </section>

        <div class="section-divider"></div>

        <!-- Synthetic Buyer Modeling -->
        <section class="mb-12 animate-fade-in">
            <h2 class="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                <i data-lucide="user-cog" class="mr-3 text-orange-600"></i>
                Synthetic Buyer Modeling
            </h2>
            <p class="text-gray-600 mb-6">
                Simulate consumer behavior to generate hype scores. Analyze buyer personas and demographic distributions.
            </p>

            <div class="grid lg:grid-cols-3 gap-6">
                <div class="bg-white rounded-xl shadow-lg p-6 hover-scale">
                    <h4 class="text-lg font-semibold mb-3">Persona Radar</h4>
                    <canvas id="buyerRadarChart" width="400" height="400"></canvas>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-6 hover-scale">
                    <h4 class="text-lg font-semibold mb-3">Demographics</h4>
                    <canvas id="buyerScatterPlot" width="400" height="200"></canvas>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-6 hover-scale">
                    <h4 class="text-lg font-semibold mb-3">Hype Distribution</h4>
                    <canvas id="hypeHistogram" width="400" height="200"></canvas>
                </div>
            </div>
        </section>

        <!-- Project Timeline -->
        <section class="mb-12 animate-fade-in">
            <h2 class="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                <i data-lucide="calendar-clock" class="mr-3 text-red-600"></i>
                Project Timeline
            </h2>
            <div class="bg-white rounded-xl shadow-lg p-6">
                <div class="mermaid">
                    gantt
                        title CÆSER Development Timeline
                        dateFormat  YYYY-MM-DD
                        section 🚀 Setup
                        API Keys & Environment    :a1, 2025-07-19, 1d
                        Qloo Integration        :after a1, 1d
                        section 💻 Development
                        LLM Integration       :2025-07-21, 1d
                        Buyer Modeling        :after a2, 1d
                        Forecasting Engine    :after a3, 1d
                        section 🎯 Deployment
                        Testing & QA          :2025-07-24, 1d
                        Production Release    :2025-07-25, 1d
                </div>
            </div>
        </section>
    </div>

    <script>
        // Initialize Mermaid
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            themeVariables: {
                primaryColor: '#667eea',
                primaryTextColor: '#fff',
                primaryBorderColor: '#764ba2',
                lineColor: '#374151',
                secondaryColor: '#f3f4f6',
                tertiaryColor: '#e5e7eb'
            }
        });

        // Initialize Lucide Icons
        lucide.createIcons();

        // Dark Mode Toggle
        const darkModeToggle = document.getElementById('darkModeToggle');
        const darkIcon = document.getElementById('darkIcon');
        const lightIcon = document.getElementById('lightIcon');
        let isDark = false;

        darkModeToggle.addEventListener('click', () => {
            isDark = !isDark;
            document.documentElement.classList.toggle('dark', isDark);
            darkIcon.classList.toggle('hidden', isDark);
            lightIcon.classList.toggle('hidden', !isDark);
        });

        // Chart configurations
        Chart.defaults.font.family = 'Inter';
        Chart.defaults.color = '#374151';
        Chart.defaults.borderColor = '#e5e7eb';

        // Affinity Bar Chart
        const ctxBar = document.getElementById('affinityBarChart').getContext('2d');
        new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: ['🎭 Arts', '🛍️ Shopping', '🍽️ Food', '🏃 Sports', '🎮 Gaming'],
                datasets: [{
                    label: 'Affinity Score',
                    data: [0.8, 0.6, 0.9, 0.7, 0.85],
                    backgroundColor: ['rgba(102, 126, 234, 0.8)', 'rgba(118, 75, 162, 0.8)', 'rgba(255, 99, 132, 0.8)', 'rgba(54, 162, 235, 0.8)', 'rgba(255, 206, 86, 0.8)'],
                    borderColor: ['rgba(102, 126, 234, 1)', 'rgba(118, 75, 162, 1)', 'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)'],
                    borderWidth: 2,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, max: 1 } }
            }
        });

        // Heat Map
        const heatData = [{
            z: [[0.8, 0.6, 0.9], [0.7, 0.85, 0.75], [0.9, 0.8, 0.95]],
            x: ['🇺🇸 North America', '🇪🇺 Europe', '🇦🇺 Asia Pacific'],
            y: ['Fashion', 'Electronics', 'Home & Garden'],
            type: 'heatmap',
            colorscale: 'Viridis',
            showscale: true
        }];
        Plotly.newPlot('affinityHeatMap', heatData, { responsive: true, margin: { t: 20 } });

        // Demand Line Chart
        const ctxLine = document.getElementById('demandLineChart').getContext('2d');
        new Chart(ctxLine, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Weekly Demand',
                    data: [120, 190, 300, 500, 200, 300],
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } }
            }
        });

        // Area Chart
        const ctxArea = document.getElementById('demandAreaChart').getContext('2d');
        new Chart(ctxArea, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Cumulative Sales',
                    data: [120, 310, 610, 1110, 1310, 1610],
                    fill: true,
                    backgroundColor: 'rgba(167, 139, 250, 0.2)',
                    borderColor: 'rgba(167, 139, 250, 1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } }
            }
        });

        // Box Plot
        const boxData = [{
            y: [10, 15, 25, 35, 50, 60, 75, 85, 100],
            type: 'box',
            name: 'Demand Distribution',
            boxpoints: 'all',
            jitter: 0.3,
            pointpos: -1.8
        }];
        Plotly.newPlot('demandBoxPlot', boxData, { responsive: true, margin: { t: 20 } });

        // Radar Chart
        const ctxRadar = document.getElementById('buyerRadarChart').getContext('2d');
        new Chart(ctxRadar, {
            type: 'radar',
            data: {
                labels: ['Excitement', 'Loyalty', 'Engagement', 'Trust', 'Innovation'],
                datasets: [{
                    label: 'Tech Enthusiast',
                    data: [90, 70, 85, 80, 95],
                    backgroundColor: 'rgba(167, 139, 250, 0.2)',
                    borderColor: 'rgba(167, 139, 250, 1)',
                    pointBackgroundColor: 'rgba(167, 139, 250, 1)'
                }]
            },
            options: {
                responsive: true,
                scales: { r: { beginAtZero: true, max: 100 } }
            }
        });

        // Scatter Plot
        const ctxScatter = document.getElementById('buyerScatterPlot').getContext('2d');
        new Chart(ctxScatter, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Buyer Personas',
                    data: [
                        {x: 25, y: 50000}, {x: 35, y: 75000}, {x: 45, y: 100000},
                        {x: 28, y: 60000}, {x: 32, y: 85000}, {x: 40, y: 95000}
                    ],
                    backgroundColor: 'rgba(167, 139, 250, 0.5)',
                    borderColor: 'rgba(167, 139, 250, 1)'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: { title: { display: true, text: 'Age' } },
                    y: { title: { display: true, text: 'Income ($)' } }
                }
            }
        });

        // Histogram
        const ctxHistogram = document.getElementById('hypeHistogram').getContext('2d');
        new Chart(ctxHistogram, {
            type: 'bar',
            data: {
                labels: ['0.0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1.0'],
                datasets: [{
                    label: 'Buyer Count',
                    data: [15, 25, 45, 35, 20],
                    backgroundColor: 'rgba(167, 139, 250, 0.8)',
                    borderColor: 'rgba(167, 139, 250, 1)',
                    borderWidth: 2,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } }
            }
        });

        // Smooth scroll for internal links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Add intersection observer for animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                }
            });
        }, observerOptions);

        document.querySelectorAll('section').forEach(section => {
            observer.observe(section);
        });
    </script>
</body>
</html>
`


## File: demo_loader.py

``$language

#!/usr/bin/env python3
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.sql import text
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_URL = os.getenv("DB_PATH", "postgresql+asyncpg://caeser_user:caeser_pass@localhost:5432/caeser")

async def load_demo_data():
    engine = create_async_engine(DB_URL)
    demo_rows = [
        # Google Trends
        ("sneakers", 78, "google_trends"),
        ("boots", 62, "google_trends"),
        ("electronics", 95, "google_trends"),
        # Affiliate
        ("Nike Air Max 90", 120, "affiliate"),
        ("Adidas Ultraboost 22", 95, "affiliate"),
        # Credit Card
        ("Footwear", 250, "credit_card"),
        ("Electronics", 500, "credit_card"),
        # Dark Web
        ("Limited drop on darknet", 88, "dark_web"),
    ]
    
    async with AsyncSession(engine) as session:
        for i, (text_val, likes, source) in enumerate(demo_rows, 1):
            await session.execute(
                text("""
                    INSERT INTO social_data(id, platform, post_content, sentiment_score, created_at)
                    VALUES (:id, :platform, :post_content, :sentiment_score, :created_at)
                """),
                {
                    "id": i,
                    "platform": source,
                    "post_content": text_val,
                    "sentiment_score": float(likes),
                    "created_at": datetime.fromisoformat("2025-08-01T02:12:10.651398")
                }
            )
        await session.commit()
    
    print("✅ Demo data loaded into PostgreSQL")

if __name__ == "__main__":
    asyncio.run(load_demo_data())
`


## File: docker-compose.yml

``$language

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: caeser_user
      POSTGRES_PASSWORD: caeser_pass
      POSTGRES_DB: caeser
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U caeser_user -d caeser"]
      interval: 30s
      timeout: 5s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 5s
      retries: 3

  caeser-api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - postgres
      - redis
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  caeser-frontend:
    image: python:3.11-slim
    working_dir: /app
    command: >
      sh -c "
        pip install streamlit requests python-dotenv plotly openpyxl reportlab &&
        streamlit run frontend/src/main.py --server.port=8501 --server.address=0.0.0.0
      "
    ports:
      - "8501:8501"
    env_file: .env
    depends_on:
      - caeser-api
    volumes:
      - .:/app
    restart: unless-stopped

volumes:
  pgdata:
`


## File: Dockerfile

``$language

FROM python:3.11-slim as builder
WORKDIR /app
RUN apt-get update && apt-get install -y gcc g++ git curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
# Removed: apt-get install sqlite3
COPY --from=builder /usr/local /usr/local
COPY . .
# Removed: python data/init_db.py  (Alembic handles it)
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
`


## File: LICENSE

``$language

Modified MIT License with Commercial Use Restriction

Summary: This license allows you to use, modify, and distribute the software for personal and non-commercial purposes. If you want to use the software for commercial purposes, you need to get written permission from the author.

Full License Text:

Copyright (c) 2025 SANIUL-blackdragon (mdalifsaniul@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

2. The Software may not be used for commercial purposes without explicit written permission from the author. "Commercial purposes" means any use of the Software that is intended to generate profit or revenue, whether directly or indirectly, such as using the Software in a business setting, selling the Software, or incorporating it into a revenue-generating product or service.

To request permission for commercial use, please contact the author at mdalifsaniul@gmail.com.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
`


## File: tree.ps1

``$language

function Show-Tree {
    param (
        [string]$Path = ".",
        [string]$Indent = "",
        [string[]]$Exclude = @('venv', 'node_modules', '.git', '.vscode', 'dist', 'build', '__pycache__', '__MACOSX', '.DS_Store')
    )

    # Get all items (directories and files), excluding specified directories
    $items = Get-ChildItem -Path $Path | Where-Object { $_.PSIsContainer -or $Exclude -notcontains $_.Name }
    foreach ($item in $items) {
        if ($item.PSIsContainer) {
            # Directory
            if ($Exclude -notcontains $item.Name) {
                Write-Output "$Indent+-- $($item.Name)/"
                Show-Tree -Path $item.FullName -Indent "$Indent|   " -Exclude $Exclude
            }
        } else {
            # File
            Write-Output "$Indent|-- $($item.Name)"
        }
    }
}

# Run the function
Show-Tree
`
+-- .continue/
|   +-- mcpServers/
|   |   |-- new-mcp-server.yaml
+-- .pytest_cache/
|   +-- v/
|   |   +-- cache/
|   |   |   |-- lastfailed
|   |   |   |-- nodeids
|   |   |   |-- stepwise
|   |   |   |-- __init__.py
|   |   |-- __init__.py
|   |-- .gitignore
|   |-- CACHEDIR.TAG
|   |-- README.md
|   |-- __init__.py
+-- api/
|   +-- controllers/
|   |   |-- __init__.py
|   +-- models/
|   |   |-- __init__.py
|   +-- routes/
|   |   |-- __init__.py
|   +-- services/
|   |   |-- data_quality_service.py
|   |   |-- discord_service.py
|   |   |-- hype_engine.py
|   |   |-- integrations_service.py
|   |   |-- llm_service.py
|   |   |-- predict_trend.py
|   |   |-- qloo_service.py
|   |   |-- __init__.py
|   +-- utils/
|   |   |-- logging.py
|   |   |-- __init__.py
|   |-- cron.py
|   |-- main.py
|   |-- __init__.py
+-- bin/
|   +-- sqlite/
|   |   |-- sqldiff.exe
|   |   |-- sqlite3.exe
|   |   |-- sqlite3_analyzer.exe
|   |   |-- sqlite3_rsync.exe
|   |   |-- __init__.py
|   |-- __init__.py
+-- data/
|   +-- processed/
|   |   |-- __init__.py
|   +-- raw/
|   |   |-- __init__.py
|   +-- schemas/
|   |   |-- __init__.py
|   +-- temp/
|   |   |-- __init__.py
|   |-- caeser.db
|   |-- init_db.py
|   |-- __init__.py
+-- docs/
|   +-- img/
|   |   |-- mermaid_diagram_2025207-1.png
|   |   |-- mermaid_diagram_2025207-2.png
|   |   |-- __init__.py
|   +-- md/
|   |   |-- architecture.md
|   |   |-- CAESER_MVP_Day1_Day1,5_Plan.markdown
|   |   |-- CAESER_MVP_Day2_Day2,5_Plan.markdown
|   |   |-- CAESER_MVP_Day3_Day3,5_Plan.markdown
|   |   |-- CAESER_MVP_Day4_Day4,5_Plan.markdown
|   |   |-- CAESER_MVP_Day5_Day5_0_Plan.markdown
|   |   |-- CAESER_MVP_Development_Plan.markdown
|   |   |-- Discord_Webhook_Integration.md
|   |   |-- mvp-future-upgrades.md
|   |   |-- naming-conventions.md
|   |   |-- OPENROUTER_LLM_INTEGRATION.md
|   |   |-- Qloo-Insights-API-Guide.markdown
|   |   |-- __init__.py
|   +-- txt/
|   |   |-- draft-main.txt
|   |   |-- draft.txt
|   |   |-- feature_draft.txt
|   |   |-- future-upgrades.md
|   |   |-- qloo-draft.txt
|   |   |-- __init__.py
|   |-- __init__.py
+-- frontend/
|   +-- components/
|   |   |-- __init__.py
|   +-- public/
|   |   |-- __init__.py
|   +-- src/
|   |   |-- main.py
|   |   |-- outcome_form.py
|   |   |-- __init__.py
|   +-- styles/
|   |   |-- __init__.py
|   |-- __init__.py
+-- migrations/
|   +-- versions/
|   |   |-- 20250729_add_categories.py
|   |   |-- 20250729_add_competitors.py
|   |   |-- 20250730_pg_indexes.py
|   |   |-- 4c0ff554c6e2_initial_migration.py
|   |   |-- a9772e6a7448_merge_categories_and_competitors.py
|   |   |-- __init__.py
|   |-- env.py
|   |-- README
|   |-- script.py.mako
|   |-- __init__.py
+-- notebooks/
|   |-- __init__.py
+-- scrapers/
|   |-- affiliate_purchases.py
|   |-- credit_card_spending.py
|   |-- dark_web.py
|   |-- demo_affiliate.csv
|   |-- demo_credit.csv
|   |-- demo_dark.csv
|   |-- google_trends.py
|   |-- scraper_config.json
|   |-- social_media_spider.py
|   |-- __init__.py
+-- tests/
|   |-- conftest.py
|   |-- test_api.py
|   |-- test_predict_trend.py
|   |-- __init__.py
|-- .env
|-- .env.example
|-- .gitignore
|-- alembic.ini
|-- caeser_visuals.html
|-- demo_loader.py
|-- docker-compose.yml
|-- Dockerfile
|-- error.txt
|-- eslint.config.mjs
|-- LICENSE
|-- package-lock.json
|-- package.json
|-- project-dump.md
|-- ProjectDumper.ps1
|-- README.md
|-- requirements.txt
|-- tree.ps1
|-- __init__.py

## File: __init__.py

``$language

# CAESER/__init__.py
"""
Root package marker for the CÆSER project.
"""
__version__ = "0.1.0"
`


## File: .continue\mcpServers\new-mcp-server.yaml

``$language

name: New MCP server
version: 0.0.1
schema: v1
mcpServers:
  - name: New MCP server
    command: npx
    args:
      - -y
      - <your-mcp-server>
    env: {}

`


## File: api\cron.py

``$language

import asyncio
import requests
from datetime import datetime, timedelta
import sys
import logging
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def health_check_loop():
    while True:
        ok = False
        try:
            # Perform the health check
            r = requests.get("http://localhost:8000/health", timeout=5)
            ok = r.status_code == 200
        except requests.RequestException as e:
            # Log the exception if the request fails
            logger.error(f"Health check request failed: {str(e)}")
            ok = False
        except Exception as e:
            # Log any other unexpected exceptions
            logger.error(f"Unexpected error during health check: {str(e)}")
            ok = False

        try:
            # Log the health check result in the database
            db_url = os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser")
            engine = create_async_engine(db_url, echo=False)
            async with AsyncSession(engine) as session:
                try:
                    await session.execute(
                        text("INSERT INTO error_logs(endpoint, error_msg, timestamp) VALUES (:endpoint, :msg, :ts)"),
                        {"endpoint": "/health", "msg": "UP" if ok else "DOWN", "ts": datetime.utcnow().isoformat()}
                    )
                    await session.commit()
                except Exception as e:
                    logger.error(f"Failed to log health check result in the database: {str(e)}")
                    await session.rollback()
        except Exception as e:
            # NEW: guard around db_url / engine creation
            logger.error(f"Could not build DB URL or engine: {str(e)}")
            # Continue loop; no return here so the cron keeps running

        try:
            # Check for prediction drift and send Discord suggestion if necessary
            db_url = os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser")
            engine = create_async_engine(db_url, echo=False)
            async with AsyncSession(engine) as session:
                try:
                    result = await session.execute(
                        text("SELECT COUNT(*) FROM predictions WHERE predicted_uplift > 90")
                    )
                    count = result.scalar() or 0
                    if count > 5:
                        try:
                            requests.post("https://discord.com/api/webhooks/...", json={
                                "content": "🤖 Consider adding Google Trends to reduce high-score drift."
                            })
                        except requests.RequestException as e:
                            logger.error(f"Failed to send Discord alert: {str(e)}")
                except Exception as e:
                    logger.error(f"Failed to check prediction drift: {str(e)}")
                    await session.rollback()
        except Exception as e:
            # NEW: guard around db_url / engine creation
            logger.error(f"Could not build DB URL or engine: {str(e)}")
            # Continue loop; no return here so the cron keeps running

        # Sleep for 5 minutes before the next health check
        await asyncio.sleep(300)

webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
if webhook_url:
    try:
        requests.post(webhook_url, json={
            "content": "🤖 Consider adding Google Trends to reduce high-score drift."
        }, timeout=5)
    except requests.RequestException as e:
        logger.error(f"Failed to send Discord alert: {str(e)}")

# Add this to run the health check loop when executed as a module
if __name__ == "__main__":
    print("Starting health monitoring service...")
    print("Press Ctrl+C to stop")
    try:
        asyncio.run(health_check_loop())
    except KeyboardInterrupt:
        print("\nHealth monitoring stopped")
        sys.exit(0)
`


## File: api\main.py

``$language

# api/main.py  –  v3 + semaphore + AWS Secrets Manager
import asyncio
import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Union

import boto3
import numpy as np
import pandas as pd
from celery import Celery
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, select, text, Table, MetaData, Column, String, Float, Integer, JSON, TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
import redis.asyncio as redis
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Import the unchanged service layer
from .services import (
    data_quality_service,
    discord_service,
    hype_engine,
    integrations_service,
    llm_service,
    qloo_service,
    init_qloo_service,
    init_data_quality_service,
    init_discord_service,
    init_hype_engine_service,
    init_llm_service,
    init_predict_trend_service,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---------- SECRETS ----------
secrets = boto3.client(
    "secretsmanager",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

def get_secret(name: str, fallback: Optional[str] = None) -> str: #type: ignore
    """Always return a string (never dict or None)."""
    try:
        val = json.loads(secrets.get_secret_value(SecretId=name)["SecretString"])
        if isinstance(val, dict):
            # if the secret itself is a JSON blob, stringify it
            return json.dumps(val)
        return str(val)
    except Exception:
        return str(os.getenv(name, fallback or ""))

DB_URL       = get_secret("caeser-db-url")
REDIS_URL    = get_secret("caeser-redis-url")
QLOO_API_KEY = get_secret("qloo-api-key")
OPENROUTER   = get_secret("openrouter-key")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# ---------- SERVICES ----------
engine = create_async_engine(
    DB_URL, pool_pre_ping=True, pool_size=10, max_overflow=20
)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# ---------- DATABASE TABLES ----------
metadata = MetaData()

competitors = Table(
    "competitors",
    metadata,
    Column("name", String, primary_key=True),
    Column("hype_score", Float, nullable=False),
)

categories = Table(
    "categories",
    metadata,
    Column("category_name", String, primary_key=True),
    Column("keywords", String),
)

# ---------- FASTAPI ----------
app = FastAPI(title="CÆSER API v3")

# ---------- CELERY SETUP ----------
celery_app = Celery(
    "caeser",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)
celery_app.conf.task_default_queue = "scraping"
celery_app.conf.task_routes = {
    "api.main.run_scrapy": {"queue": "scraping"}
}

# ---------- GLOBAL EXCEPTION HANDLER ----------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception at %s: %s", request.url, exc, exc_info=True
    )
    return JSONResponse(
        status_code=500, content={"detail": "Internal server error"}
    )

# ---------- MODELS ----------
class LogMessageIn(BaseModel):
    new_message: str

class CompetitorIn(BaseModel):
    name: str
    hype_score: float

class CategoryIn(BaseModel):
    category_name: str
    keywords: str  # comma-separated

class AnalyzeInput(BaseModel):
    product_name: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)
    tags: str = Field(..., min_length=1)
    target_area: Optional[str] = None
    locations: Optional[str] = None
    gender: Optional[str] = None
    sources: Optional[str] = None

class RetrainOut(BaseModel):
    success: bool
    message: str
    new_weights: dict

# ---------- UTIL ----------
async def init_db_indexes() -> None:
    async with engine.begin() as conn:
        await conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS competitors (
                    name TEXT PRIMARY KEY,
                    hype_score REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS predictions (
                    id SERIAL PRIMARY KEY,
                    product_name TEXT,
                    data JSONB
                );
                CREATE TABLE IF NOT EXISTS hype_scores (
                    id SERIAL PRIMARY KEY,
                    score REAL,
                    sentiment REAL,
                    category TEXT,
                    location TEXT,
                    product_name TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS outcomes (
                    id SERIAL PRIMARY KEY,
                    prediction_id INTEGER,
                    actual_uplift REAL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS model_weights (
                    key TEXT PRIMARY KEY,
                    value REAL
                );
                CREATE TABLE IF NOT EXISTS categories (
                    category_name TEXT PRIMARY KEY,
                    keywords TEXT
                );
                CREATE TABLE IF NOT EXISTS social_data (
                    id SERIAL PRIMARY KEY,
                    source TEXT,
                    text TEXT,
                    likes INTEGER,
                    timestamp TIMESTAMPTZ
                );
                """
            )
        )

# ---------- CACHED QLOO with granular key ----------
async def cached_qloo(
    location: str, tags: str, insight_type: str = "brand"
) -> Dict:
    tag_list = sorted(tags.split(","))
    key = f"qloo:{insight_type}:{location}:{tag_list}"
    cached = await redis_client.get(key)
    if cached:
        return json.loads(cached)

    result = await qloo_service.get_cultural_insights_async(
        location, tag_list, insight_type
    )
    await redis_client.setex(key, 3600, json.dumps(result))
    return result

# ---------- TREND PREDICTION ----------
async def predict_trend(product_name: str, tags: str) -> Dict:
    try:
        tag_list = tags.split(",")
        async with AsyncSessionLocal() as session:
            query = text(
                """
                SELECT likes, timestamp
                FROM social_data
                WHERE source='google_trends' AND text = ANY(:tags)
                ORDER BY timestamp
                """
            )
            rows = (
                await session.execute(query, {"tags": tag_list})
            ).fetchall()

        if len(rows) < 3:
            return {"success": False, "message": "Insufficient trend data"}

        df = pd.DataFrame(rows, columns=["likes", "timestamp"])
        df["likes"] = pd.to_numeric(df["likes"], errors="coerce").fillna(0)
        model = ExponentialSmoothing(
            df["likes"], trend="add", seasonal=None
        ).fit()
        forecast = model.forecast(90)
        peak_idx = int(np.argmax(forecast))
        peak_date = (
            pd.Timestamp.utcnow() + pd.Timedelta(days=peak_idx)
        ).strftime("%Y-%m-%d")

        return {
            "success": True,
            "predicted_peak_days": peak_idx + 1,
            "predicted_peak_date": peak_date,
            "confidence": max(
                0.0, 1 - model.sse / (df["likes"] ** 2).sum()
            ),
        }

    except Exception as e:
        logger.exception("Trend prediction failed")
        return {"success": False, "message": str(e)}

# ---------- STARTUP ----------
@app.on_event("startup")
async def startup_event():
    await init_db_indexes()
    await init_qloo_service()
    await init_data_quality_service()
    await init_discord_service()
    await init_hype_engine_service()
    await init_llm_service()
    await init_predict_trend_service()
    await FastAPILimiter.init(redis_client)
    Instrumentator().instrument(app).expose(app)
    logger.info(os.getenv("STARTUP_MESSAGE", "CÆSER API v3 live 🚀"))

# ---------- ENDPOINTS ----------
# ---------- CELERY TASK ----------
@celery_app.task(name="api.main.run_scrapy")
async def run_scrapy(
    product_name: str,
    sources: str,
    tags: str,
    locations: str = None, #type: ignore
    gender: str = None, #type: ignore
):
    cmd = [
        "scrapy",
        "crawl",
        "social_media",
        "-a",
        f"target={product_name}",
        "-a",
        f"sources={sources}",
        "-a",
        f"keywords={tags}",
    ]
    if locations:
        cmd.extend(["-a", f"locations={locations}"])
    if gender:
        cmd.extend(["-a", f"gender={gender}"])

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise Exception(f"Scraping failed: {stderr.decode()}")
    return stdout.decode()

@app.post(
    "/analyze",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
async def analyze_endpoint(inp: AnalyzeInput):
    start = time.time()
    try:
        # Queue the scraping task
        task = run_scrapy.delay(
            product_name=inp.product_name,
            sources=inp.sources or "reddit,tiktok,instagram,imdb,ebay",
            tags=inp.tags,
            locations=inp.locations,
            gender=inp.gender,
        )

        # Continue with other processing while scraping runs in background
        hype = await hype_engine.calculate_hype_score_async(
            {},
            inp.tags,
            inp.target_area or "global",
            20.0,
            inp.product_name,
        )

        trend = await predict_trend(inp.product_name, inp.tags)

        return {
            "success": True,
            "hype_score": hype.get("averageScore", 0),
            "trend_prediction": trend if trend.get("success") else None,
            "message": "Analysis completed (scraping queued)",
            "task_id": task.id,
        }

    except Exception as e:
        logger.exception("Unhandled error in /analyze")
        return {
            "success": False,
            "message": "Internal server error",
            "error": str(e),
        }
    finally:
        logger.info("/analyze took %.1f ms", (time.time() - start) * 1000)

# ---------- Legacy endpoints ----------
@app.post("/admin/log_message")
async def set_log_message(body: LogMessageIn):
    os.environ["STARTUP_MESSAGE"] = body.new_message
    return {"success": True, "message": "Next restart will use the new message"}

@app.get("/competitors")
async def competitors():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(competitors))
        rows = result.fetchall()
    return {r.name: {"hype": r.hype_score} for r in rows}

@app.post(
    "/competitors/add",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))]
)
async def add_competitor(body: CompetitorIn):
    async with AsyncSessionLocal() as session:
        stmt = insert(competitors).values(
            name=body.name, hype_score=body.hype_score
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["name"],
            set_=dict(hype_score=body.hype_score),
        )
        await session.execute(stmt)
        await session.commit()
    return {
        "success": True,
        "message": f"Competitor {body.name} saved/updated",
    }

@app.post(
    "/categories",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))]
)
async def add_or_update_category(body: CategoryIn):
    async with AsyncSessionLocal() as session:
        stmt = insert(categories).values(
            category_name=body.category_name, keywords=body.keywords
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["category_name"],
            set_=dict(keywords=body.keywords),
        )
        await session.execute(stmt)
        await session.commit()
    return {
        "success": True,
        "message": f"Category '{body.category_name}' saved",
    }

@app.get("/categories")
async def list_categories():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(categories))
        rows = result.fetchall()
    return {
        "success": True,
        "data": {r.category_name: r.keywords.split(",") for r in rows},
    }

@app.get("/insights/{location}")
async def get_insights(
    location: str, tags: str, insight_type: str = "brand"
):
    return await cached_qloo(location, tags, insight_type)

@app.get("/llm_data_quality")
async def get_llm_data_quality():
    return await llm_service.get_llm_data_quality_async()

@app.get("/data_quality")
async def get_data_quality():
    return await data_quality_service.check_data_quality_async()

@app.post("/predict/demand")
async def predict_demand(data: dict) -> dict:
    return await llm_service.get_prediction_async(
        data.get("product", {}),
        data.get("insights", {}),
        data.get("hype_score", 0),
    )

@app.post("/hype/score")
async def calculate_hype_score(data: dict) -> dict:
    return await hype_engine.calculate_hype_score_async(
        data.get("insights", {}),
        data.get("category", ""),
        data.get("location", ""),
        20.0,
    )

@app.post("/discord/alert")
async def send_discord_alert(data: dict):
    return await discord_service.send_alert_async(
        data.get("prediction"), data.get("hype_data")
    )

@app.post("/integrations/send")
async def send_integrations(data: dict):
    return await integrations_service.send_integrations_async(
        data.get("prediction"), data.get("hype_data")
    )

@app.get("/hype/history/{location}/{category}")
async def get_hype_history(location: str, category: str):
    async with AsyncSessionLocal() as session:
        rows = (
            await session.execute(
                text(
                    """
                    SELECT score, created_at
                    FROM hype_scores
                    WHERE category = :cat AND location = :loc
                    ORDER BY created_at
                    """
                ),
                {"cat": category, "loc": location},
            )
        ).fetchall()
    return {
        "success": True,
        "data": [{"score": r[0], "timestamp": r[1]} for r in rows],
    }

@app.post("/submit_outcome")
async def submit_outcome(data: dict):
    pid = data.get("prediction_id")
    uplift = data.get("actual_uplift")
    if not isinstance(pid, int) or pid <= 0:
        raise HTTPException(
            status_code=400, detail="Bad prediction_id"
        )
    if uplift is None or not isinstance(uplift, (int, float)):
        raise HTTPException(
            status_code=400, detail="Bad actual_uplift"
        )
    async with AsyncSessionLocal() as session:
        await session.execute(
            text(
                """
                INSERT INTO outcomes(prediction_id, actual_uplift, timestamp)
                VALUES (:pid, :uplift, :ts)
                """
            ),
            {"pid": pid, "uplift": uplift, "ts": datetime.utcnow()},
        )
        await session.commit()
    return {"success": True, "message": "Outcome submitted"}

@app.post("/retrain", response_model=RetrainOut)
async def retrain_endpoint():
    async with AsyncSessionLocal() as session:
        rows = (
            await session.execute(
                text(
                    """
                    SELECT h.sentiment, o.actual_uplift
                    FROM hype_scores h
                    JOIN outcomes o ON o.prediction_id = h.id
                    ORDER BY h.created_at DESC
                    LIMIT 100
                    """
                )
            )
        ).fetchall()
        if not rows:
            return RetrainOut(
                success=False,
                message="Need ≥1 outcome to retrain",
                new_weights={},
            )
        sentiments = [r[0] for r in rows]
        actuals = [r[1] for r in rows]
        new_weight = sum(actuals) / (sum(sentiments) + 1e-9)
        await session.execute(
            text(
                """
                INSERT INTO model_weights(key, value)
                VALUES ('sentiment_weight', :val)
                ON CONFLICT(key) DO UPDATE SET value=EXCLUDED.value
                """
            ),
            {"val": new_weight},
        )
        await session.commit()
    return RetrainOut(
        success=True,
        message="Weights updated",
        new_weights={"sentiment_weight": new_weight},
    )

@app.get("/health")
async def health_check():
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    return {"status": "ok"}

`


## File: api\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: api\controllers\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: api\models\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: api\routes\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: api\services\data_quality_service.py

``$language

import os
import logging
from datetime import datetime, timedelta
from typing import Optional

import asyncpg

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/caeser")
pg_pool: Optional[asyncpg.Pool] = None

async def _init_connections() -> None:
    global pg_pool
    try:
        pg_pool = await asyncpg.create_pool(POSTGRES_URL, min_size=1, max_size=10)
        async with pg_pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS data_quality (
                    metric TEXT NOT NULL,
                    value REAL NOT NULL,
                    source TEXT NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS llm_data_quality (
                    metric TEXT NOT NULL,
                    value REAL NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
        logger.info("PostgreSQL connected and data_quality table ensured.")
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL or create table: {e}")
        pg_pool = None

async def log_data_quality(metric: str, value: float, source: str):
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot log data quality.")
        return
    try:
        async with pg_pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO data_quality (metric, value, source, timestamp) VALUES ($1, $2, $3, NOW())",
                metric, value, source
            )
        logger.info(f"Logged data quality: {metric} = {value} for {source}")
    except Exception as e:
        logger.error(f"Failed to log data quality to PostgreSQL: {e}")

async def check_data_quality():
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot check data quality.")
        return {"success": False, "message": "Database not connected"}

    metrics = {}
    try:
        async with pg_pool.acquire() as conn:
            # Check missing values in social_data
            missing_values = await conn.fetchval("SELECT COUNT(*) FROM social_data WHERE text IS NULL OR text = ''")
            metrics['missing_values'] = {'value': missing_values, 'source': 'social_data'}
            await log_data_quality('missing_values', missing_values, 'social_data')
            
            # Check feed freshness
            latest_timestamp_str = await conn.fetchval("SELECT MAX(timestamp) FROM social_data")
            freshness = 0.0
            if latest_timestamp_str:
                latest_timestamp = datetime.fromisoformat(latest_timestamp_str.isoformat())
                freshness = (datetime.now() - latest_timestamp).total_seconds() / 3600
            metrics['freshness'] = {'value': freshness, 'source': 'social_data'}
            await log_data_quality('freshness', freshness, 'social_data')
            
            # Check API errors (from llm_data_quality for now)
            api_errors = await conn.fetchval("SELECT COUNT(*) FROM llm_data_quality WHERE metric = 'errors' AND value = 1.0")
            metrics['api_errors'] = {'value': api_errors, 'source': 'llm_service'}
            await log_data_quality('api_errors', api_errors, 'llm_service')
            
        return {
            "success": True,
            "data": metrics,
            "message": "Data quality metrics retrieved"
        }
    except Exception as e:
        logger.error(f"Failed to check data quality from PostgreSQL: {e}")
        return {"success": False, "message": f"Failed to retrieve data quality: {e}"}

async def check_data_quality_async():
    return await check_data_quality()

async def init_data_quality_service():
    await _init_connections()

`


## File: api\services\discord_service.py

``$language

import os
import boto3
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import logging
import asyncio
from typing import Optional
import asyncpg

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/caeser")
pg_pool: Optional[asyncpg.Pool] = None

# ------------------------------------------------------------------
def _get_secret(secret_id: str) -> str:
    """
    Get secret from AWS Secrets Manager with fallback to environment variables.
    Initializes boto3 client on demand to avoid issues during import.
    """
    secret_value = ""
    try:
        # First, try environment variables (often used in CI/CD or local dev)
        env_var_name = secret_id.upper().replace("-", "_")
        secret_value = os.getenv(env_var_name, "")
        if secret_value:
            return secret_value

        # If not in env, try AWS Secrets Manager
        secrets_client = boto3.client('secretsmanager', region_name=os.getenv("AWS_REGION", "us-east-1"))
        secret_value = secrets_client.get_secret_value(SecretId=secret_id)['SecretString']
        return secret_value
    except Exception as e:
        # This will catch botocore.exceptions.NoCredentialsError if AWS isn't configured
        logger.warning(f"Could not retrieve secret '{secret_id}'. Error: {e}. Service may be disabled.")
        return "" # Return empty string to signify failure

# ------------------------------------------------------------------
async def is_product_marked(product_name: str, category: str) -> bool:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot check if product is marked.")
        return False
    try:
        async with pg_pool.acquire() as conn:
            count = await conn.fetchval(
                "SELECT COUNT(*) FROM marked_products WHERE product_name = $1 AND category = $2",
                product_name, category
            )
            return count > 0
    except Exception as e:
        logger.error(f"Failed to check if product is marked in PostgreSQL: {e}")
        return False

# ------------------------------------------------------------------
# Batched alert queues
discord_alerts = []
slack_alerts   = []
email_alerts   = []

def _flush_discord():
    if not discord_alerts:
        return
    
    DISCORD_WEBHOOK_URL = _get_secret("discord_webhook")
    if not DISCORD_WEBHOOK_URL:
        logger.warning("DISCORD_WEBHOOK_URL not set. Cannot send Discord alerts.")
        discord_alerts.clear()
        return

    payload = {"content": "\n".join(discord_alerts)}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5).raise_for_status()
        logger.info("Discord batch sent (%d alerts)", len(discord_alerts))
    except Exception as e:
        logger.error("Failed Discord batch: %s", e)
    discord_alerts.clear()

def _flush_slack():
    if not slack_alerts:
        return

    SLACK_WEBHOOK_URL = _get_secret("slack_webhook")
    if not SLACK_WEBHOOK_URL:
        logger.warning("SLACK_WEBHOOK_URL not set. Cannot send Slack alerts.")
        slack_alerts.clear()
        return

    payload = {"text": "\n".join(slack_alerts)}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5).raise_for_status()
        logger.info("Slack batch sent (%d alerts)", len(slack_alerts))
    except Exception as e:
        logger.error("Failed Slack batch: %s", e)
    slack_alerts.clear()

def _flush_email():
    if not email_alerts:
        return

    EMAIL_HOST = _get_secret("email_host")
    EMAIL_PORT_STR = _get_secret("email_port")
    EMAIL_USER = _get_secret("email_user")
    EMAIL_PASSWORD = _get_secret("email_password")
    EMAIL_RECIPIENT = _get_secret("email_recipient")

    if not all([EMAIL_HOST, EMAIL_PORT_STR, EMAIL_USER, EMAIL_PASSWORD, EMAIL_RECIPIENT]):
        logger.warning("Email settings are incomplete. Cannot send email alerts.")
        email_alerts.clear()
        return
        
    try:
        EMAIL_PORT = int(EMAIL_PORT_STR)
    except (ValueError, TypeError):
        logger.error(f"Invalid EMAIL_PORT: {EMAIL_PORT_STR}. Must be an integer.")
        email_alerts.clear()
        return

    body = "\n\n".join(email_alerts)
    msg = MIMEText(body)
    msg["Subject"] = "CÆSER Alert Batch"
    msg["From"]    = EMAIL_USER
    msg["To"]      = EMAIL_RECIPIENT

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        logger.info("Email batch sent (%d alerts)", len(email_alerts))
    except Exception as e:
        logger.error("Failed email batch: %s", e)
    email_alerts.clear()

# ------------------------------------------------------------------
# The send_*_alert functions remain unchanged as they only append to lists
async def send_discord_alert(prediction, hype_data):
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')

    if not await is_product_marked(product_name, category):
        logger.info("Product %s not marked – skipping Discord", product_name)
        return {"success": True, "message": "Product not marked, alert skipped"}

    alert = (
        f"**{product_name}** ({category})\n"
        f"Uplift: {prediction['uplift']:.2f}% | "
        f"Confidence: {prediction['confidence']:.2f} | "
        f"Strategy: {prediction['strategy']} | "
        f"Hype: {hype_data['averageScore']:.2f} | "
        f"Sentiment Δ: {hype_data['hourly_sentiment_change']:.2f}%"
    )
    if hype_data.get("change_detected"):
        alert += f" ⚠️ Hype changed by {hype_data['change_percent']:.2f}%!"
    discord_alerts.append(alert)
    return {"success": True, "message": "Queued for Discord batch"}

async def send_slack_alert(prediction, hype_data):
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')

    if not await is_product_marked(product_name, category):
        logger.info("Product %s not marked – skipping Slack", product_name)
        return {"success": True, "message": "Product not marked, alert skipped"}

    alert = (
        f"*{product_name}* ({category})\n"
        f"Uplift: {prediction['uplift']:.2f}% | "
        f"Confidence: {prediction['confidence']:.2f} | "
        f"Strategy: {prediction['strategy']} | "
        f"Hype: {hype_data['averageScore']:.2f} | "
        f"Sentiment Δ: {hype_data['hourly_sentiment_change']:.2f}%"
    )
    if hype_data.get("change_detected"):
        alert += f" ⚠️ Hype changed by {hype_data['change_percent']:.2f}%!"
    slack_alerts.append(alert)
    return {"success": True, "message": "Queued for Slack batch"}

async def send_email_alert(prediction, hype_data):
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')

    if not await is_product_marked(product_name, category):
        logger.info("Product %s not marked – skipping Email", product_name)
        return {"success": True, "message": "Product not marked, alert skipped"}

    body = (
        f"Product: {product_name}\n"
        f"Category: {category}\n"
        f"Demand Uplift: {prediction['uplift']:.2f}%\n"
        f"Confidence: {prediction['confidence']:.2f}%\n"
        f"Strategy: {prediction['strategy']}\n"
        f"Hype Score: {hype_data['averageScore']:.2f}\n"
        f"Hourly Sentiment Change: {hype_data['hourly_sentiment_change']:.2f}%"
    )
    if hype_data.get("change_detected"):
        body += f"\n⚠️ Hype score changed by {hype_data['change_percent']:.2f}%!"
    email_alerts.append(body)
    return {"success": True, "message": "Queued for Email batch"}

# ------------------------------------------------------------------
async def send_alert(prediction, hype_data):
    await send_discord_alert(prediction, hype_data)
    await send_slack_alert(prediction, hype_data)
    await send_email_alert(prediction, hype_data)

    # Flush all queues
    _flush_discord()
    _flush_slack()
    _flush_email()

    # Summaries
    successes = [bool(discord_alerts), bool(slack_alerts), bool(email_alerts)]
    return {"success": any(successes),
            "message": "Alerts batched and flushed"}

# ------------------------------------------------------------------
# NEW ASYNC WRAPPER
# ------------------------------------------------------------------
async def send_alert_async(prediction, hype_data):
    return await send_alert(prediction, hype_data)

async def init_discord_service():
    global pg_pool
    try:
        pg_pool = await asyncpg.create_pool(POSTGRES_URL, min_size=1, max_size=10)
        async with pg_pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS marked_products (
                    product_name TEXT PRIMARY KEY,
                    category TEXT NOT NULL
                );
                """
            )
        logger.info("PostgreSQL connected and marked_products table ensured.")
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL or create marked_products table: {e}")
        pg_pool = None
`


## File: api\services\hype_engine.py

``$language

import random
from typing import Dict, Optional, List
import logging
import re
from collections import defaultdict
import os
from textblob import TextBlob
from datetime import datetime, timedelta
import asyncio
import asyncpg

# Enhanced emoji mapping with fallback
EMOJI_MAP = defaultdict(lambda: 0.0, {
    "😊": 0.8, "😢": -0.8, "😍": 0.9, "😠": -0.9, "😐": 0.0,
    "👍": 0.7, "👎": -0.7, "🔥": 0.85, "💯": 0.9, "👀": 0.3
})
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/caeser")
pg_pool: Optional[asyncpg.Pool] = None

async def _init_connections() -> None:
    global pg_pool
    try:
        pg_pool = await asyncpg.create_pool(POSTGRES_URL, min_size=1, max_size=10)
        async with pg_pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS hype_scores (
                    id SERIAL PRIMARY KEY,
                    score REAL,
                    sentiment REAL,
                    category TEXT,
                    location TEXT,
                    product_name TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS social_data (
                    id SERIAL PRIMARY KEY,
                    source TEXT,
                    text TEXT,
                    likes INTEGER,
                    timestamp TIMESTAMPTZ
                );
                CREATE TABLE IF NOT EXISTS categories (
                    category_name TEXT PRIMARY KEY,
                    keywords TEXT
                );
                """
            )
        logger.info("PostgreSQL connected and hype_scores, social_data, categories tables ensured.")
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL or create tables: {e}")
        pg_pool = None

async def get_categories_async() -> Dict[str, List[str]]:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot fetch categories.")
        return {
            "sneakers": ["sneakers", "shoes", "footwear", "kicks"],
            "electronics": ["electronics", "gadgets", "tech", "devices"],
            "fashion": ["fashion", "clothing", "apparel", "style"]
        }
    try:
        async with pg_pool.acquire() as conn:
            rows = await conn.fetch("SELECT category_name, keywords FROM categories")
            if not rows:
                return {
                    "sneakers": ["sneakers", "shoes", "footwear", "kicks"],
                    "electronics": ["electronics", "gadgets", "tech", "devices"],
                    "fashion": ["fashion", "clothing", "apparel", "style"]
                }
            return {row["category_name"]: [kw.strip() for kw in row["keywords"].split(",")] for row in rows}
    except Exception as e:
        logger.error(f"Database error while fetching categories: {e}")
        return {
            "sneakers": ["sneakers", "shoes", "footwear", "kicks"],
            "electronics": ["electronics", "gadgets", "tech", "devices"],
            "fashion": ["fashion", "clothing", "apparel", "style"]
        }

# Cultural keywords for bonus scoring
CULTURAL_KEYWORDS = ["hype", "trend", "viral", "drop", "exclusive", "limited", "collab"]
# Psychographic vectors
PSYCHO_VEC = {
    "enthusiasm": lambda s: abs(s),
    "virality": lambda s: s * 1.2 if s > 0.5 else s,
    "controversy": lambda s: abs(s) * 0.8 if s < -0.3 else 0
}

def validate_insights(insights: Dict) -> None:
    if not isinstance(insights, dict) or not insights.get("data"):
        logger.error("Invalid insights data")
        raise ValueError("Invalid insights data")
    if not isinstance(insights["data"], dict):
        logger.error("Insights data must be a dictionary")
        raise ValueError("Insights data must be a dictionary")

async def save_hype_score(score: float, category: str, location: str, sentiment: float, product_name: str | None = None) -> None:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot save hype score.")
        return
    try:
        async with pg_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO hype_scores (score, category, location, sentiment, product_name, created_at)
                VALUES ($1, $2, $3, $4, $5, NOW())
            """, score, category or "", location or "", sentiment, product_name or "")
    except Exception as e:
        logger.error(f"Failed to save hype score to PostgreSQL: {e}")

async def get_previous_hype_score(category: str, location: str, product_name: str | None = None) -> tuple:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot get previous hype score.")
        return (None, None)
    try:
        async with pg_pool.acquire() as conn:
            query = """
                SELECT score, sentiment FROM hype_scores 
                WHERE category = $1 AND location = $2
            """
            params = [category or "", location or ""]
            if product_name:
                query += " AND product_name = $3"
                params.append(product_name or "")
            query += " ORDER BY created_at DESC LIMIT 1 OFFSET 1"
            
            # Adjust parameter indexing for asyncpg
            if product_name:
                row = await conn.fetchrow(query, params[0], params[1], params[2])
            else:
                row = await conn.fetchrow(query, params[0], params[1])
            
            return (row["score"], row["sentiment"]) if row else (None, None)
    except Exception as e:
        logger.error(f"Failed to get previous hype score from PostgreSQL: {e}")
        return (None, None)

async def get_hourly_sentiment_change(category: str, location: str, product_name: str | None = None) -> float:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot get hourly sentiment change.")
        return 0.0
    try:
        async with pg_pool.acquire() as conn:
            query = """
                SELECT sentiment, created_at FROM hype_scores 
                WHERE category = $1 AND location = $2 AND created_at > NOW() - INTERVAL '1 hour'
            """
            params = [category or "", location or ""]
            if product_name:
                query += " AND product_name = $3"
                params.append(product_name or "")
            
            if product_name:
                rows = await conn.fetch(query, params[0], params[1], params[2])
            else:
                rows = await conn.fetch(query, params[0], params[1])
            
            if len(rows) < 2:
                return 0.0
            
            # Sort by created_at to ensure correct latest/oldest sentiment
            rows.sort(key=lambda r: r["created_at"])
            latest_sentiment = rows[-1]["sentiment"]
            oldest_sentiment = rows[0]["sentiment"]
            
            return ((latest_sentiment - oldest_sentiment) / oldest_sentiment * 100) if oldest_sentiment != 0 else 0.0
    except Exception as e:
        logger.error(f"Failed to get hourly sentiment change from PostgreSQL: {e}")
        return 0.0

async def get_social_data(category: str, days: int = 7) -> List[str]:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot get social data.")
        return []
    try:
        category_keywords = await get_categories_async() # Fetch categories asynchronously
        keywords = category_keywords.get(category.lower() if category else "", [category or ""])
        
        async with pg_pool.acquire() as conn:
            # Constructing dynamic WHERE clause for keywords
            where_clauses = [f"text ILIKE '%{kw}%'" for kw in keywords]
            query = f"""
                SELECT text 
                FROM social_data 
                WHERE ({' OR '.join(where_clauses)})
                AND timestamp > NOW() - INTERVAL '{days} days'
            """
            rows = await conn.fetch(query)
            return [row["text"] for row in rows]
    except Exception as e:
        logger.error(f"Failed to get social data from PostgreSQL: {e}")
        return []

def emoji_to_sentiment(text: str) -> float:
    scores = [EMOJI_MAP[ch] for ch in text if ch in EMOJI_MAP]
    return sum(scores) / (len(scores) or 1)

def scrub_pii(text: str) -> str:
    return EMAIL_REGEX.sub('', text or "")

async def calculate_hype_score(insights: Dict, category: str, location: str, threshold: float = 20.0, product_name: str | None = None) -> Dict:
    validate_insights(insights)
    
    try:
        entities = insights["data"].get("entities", [])
        popularity = sum(entity["properties"].get("popularity", 0.5) for entity in entities) / len(entities) if entities else 0.5
        trend_factor = insights["data"].get("trend", 1.0)
        base_score = popularity * 100 * trend_factor
        
        historical_noise = await get_historical_noise(category, location, product_name) # Make this async
        hype_score = max(0.0, min(100.0, base_score + historical_noise))
        
        social_texts = await get_social_data(category) # Make this async
        if social_texts:
            sentiment_score = sum(
                TextBlob(scrub_pii(text)).sentiment.polarity + emoji_to_sentiment(text) # type: ignore
                for text in social_texts
            ) / len(social_texts) if social_texts else 0.0
            logger.info(f"Analyzed {len(social_texts)} social posts for sentiment")
        else:
            sentiment_score = 0.0
            logger.warning("No social data found for sentiment analysis")
        
        hype_score = min(100.0, hype_score * (1 + sentiment_score * 0.2))
        
        cultural_bonus = sum(1 for k in CULTURAL_KEYWORDS if k in " ".join(social_texts).lower()) * 2
        psychographic = PSYCHO_VEC["enthusiasm"](sentiment_score)
        hype_score = min(100.0, hype_score + cultural_bonus + psychographic)
        
        scenario = {"price_drop": min(100.0, hype_score * 1.05)}
        cycle_phase = "growth" if hype_score > 50 else "decline"
        confidence_weight = min(1.0, (entities[0]["properties"].get("confidence", 0.5) if entities else 0.5) * 0.8 + 0.2)
        
        previous_score, previous_sentiment = await get_previous_hype_score(category, location, product_name) # Make this async
        await save_hype_score(hype_score, category, location, sentiment_score, product_name) # Make this async
        
        change_detected = False
        change_percent = 0.0
        if previous_score is not None:
            change_percent = ((hype_score - previous_score) / previous_score) * 100
            change_detected = abs(change_percent) > threshold
        
        hourly_sentiment_change = await get_hourly_sentiment_change(category, location, product_name) # Make this async
        
        logger.info(f"Calculated hype score: {hype_score:.2f}, Sentiment: {sentiment_score:.2f}, Change: {change_percent:.2f}%, Hourly Sentiment Change: {hourly_sentiment_change:.2f}%")
        return {
            "success": True,
            "averageScore": round(hype_score, 2),
            "sentiment": round(sentiment_score, 2),
            "change_detected": change_detected,
            "change_percent": round(change_percent, 2),
            "hourly_sentiment_change": round(hourly_sentiment_change, 2),
            "scenario": scenario,
            "cycle_phase": cycle_phase,
            "confidence_weight": round(confidence_weight, 2),
            "message": "Enhanced hype score calculated with cultural and psychographic factors"
        }
    except Exception as e:
        logger.error(f"Failed to calculate hype score: {str(e)}")
        return {
            "success": False, 
            "averageScore": 0.0, 
            "sentiment": 0.0, 
            "change_detected": False, 
            "change_percent": 0.0, 
            "hourly_sentiment_change": 0.0,
            "scenario": {},
            "cycle_phase": "unknown",
            "confidence_weight": 0.0,
            "message": f"Failed to calculate hype score: {str(e)}"
        }

async def get_historical_noise(category: str, location: str, product_name: str | None = None) -> float:
    """
    Fetch historical noise data based on category, location, and product name.
    This function should be implemented to fetch real historical data.
    For now, it returns a placeholder value.
    """
    return 0.0

async def calculate_hype_score_async(insights, category, location, threshold=20.0, product_name: str | None = None):
    return await calculate_hype_score(insights, category or "", location or "", threshold, product_name or "")

async def init_hype_engine_service():
    await _init_connections()
`


## File: api\services\integrations_service.py

``$language

import os
import json
import requests
import logging
import sqlite3
import backoff
import boto3
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from functools import lru_cache
import asyncio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# 0. Secrets Manager helper
# ------------------------------------------------------------------
_secrets_client = boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION", "us-east-1"))

def _get_secret(secret_name: str, default=None):
    """
    Fetch secret from AWS Secrets Manager; fall back to env var if not found.
    """
    try:
        return _secrets_client.get_secret_value(SecretId=secret_name)["SecretString"]
    except Exception as e:
        logger.warning(f"Could not pull secret '{secret_name}' from AWS: {e}")
        return os.getenv(secret_name, default)

# ------------------------------------------------------------------
# 1. Configuration
# ------------------------------------------------------------------
GOOGLE_SHEETS_CREDENTIALS = _get_secret("GOOGLE_SHEETS_CREDENTIALS")
SPREADSHEET_ID          = _get_secret("SPREADSHEET_ID")
SALESFORCE_CLIENT_ID    = _get_secret("SALESFORCE_CLIENT_ID")
SALESFORCE_CLIENT_SECRET= _get_secret("SALESFORCE_CLIENT_SECRET")
SALESFORCE_USERNAME     = _get_secret("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD     = _get_secret("SALESFORCE_PASSWORD")
SALESFORCE_TOKEN        = _get_secret("SALESFORCE_TOKEN")
SALESFORCE_INSTANCE_URL = _get_secret("SALESFORCE_INSTANCE_URL")
DISCORD_WEBHOOK_SECRET_NAME = "discord_webhook"   # AWS secret name
DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

# ------------------------------------------------------------------
# 2. Google Sheets helpers
# ------------------------------------------------------------------
@lru_cache(maxsize=1)
def get_google_sheets_service():
    """
    Returns a cached Google Sheets service object.
    """
    try:
        creds_json = GOOGLE_SHEETS_CREDENTIALS
        if not creds_json:
            raise ValueError("Google Sheets credentials are not set.")
        creds = Credentials.from_service_account_info(json.loads(creds_json))
        service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
        logger.info("Google Sheets service initialized successfully")
        return service
    except (ValueError, json.JSONDecodeError, HttpError) as e:
        logger.error(f"Failed to initialize Google Sheets service: {str(e)}")
        return None

@backoff.on_exception(backoff.expo, HttpError, max_tries=5)
def append_to_google_sheets(prediction, hype_data):
    if not GOOGLE_SHEETS_CREDENTIALS or not SPREADSHEET_ID:
        logger.error("Google Sheets configuration missing")
        return {"success": False, "message": "Google Sheets configuration missing"}

    service = get_google_sheets_service()
    if not service:
        return {"success": False, "message": "Failed to initialize Google Sheets service"}

    values = [[
        prediction.get('product', {}).get('name', 'Unknown'),
        prediction.get('product', {}).get('category', 'Unknown'),
        prediction.get('uplift', 0.0),
        prediction.get('confidence', 0.0),
        prediction.get('strategy', 'Unknown'),
        hype_data.get('averageScore', 0.0),
        hype_data.get('change_percent', 0.0) if hype_data.get('change_detected') else 0.0
    ]]

    body = {'values': values}
    try:
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="Sheet1!A:G",
            valueInputOption="RAW",
            body=body
        ).execute()
        logger.info("Data appended to Google Sheets successfully")
        return {"success": True, "message": "Data appended to Google Sheets successfully"}
    except HttpError as e:
        logger.error(f"Failed to append to Google Sheets: {str(e)}")
        return {"success": False, "message": f"Failed to append to Google Sheets: {str(e)}"}

# ------------------------------------------------------------------
# 3. Salesforce helpers
# ------------------------------------------------------------------
@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
def get_salesforce_access_token():
    required = [SALESFORCE_CLIENT_ID, SALESFORCE_CLIENT_SECRET, SALESFORCE_USERNAME,
                SALESFORCE_PASSWORD, SALESFORCE_TOKEN, SALESFORCE_INSTANCE_URL]
    if not all(required):
        logger.error("Salesforce configuration missing")
        return None

    auth_url = f"{SALESFORCE_INSTANCE_URL}/services/oauth2/token"
    password = (SALESFORCE_PASSWORD or "") + (SALESFORCE_TOKEN or "")
    payload = {
        'grant_type': 'password',
        'client_id': SALESFORCE_CLIENT_ID,
        'client_secret': SALESFORCE_CLIENT_SECRET,
        'username': SALESFORCE_USERNAME,
        'password': password
    }
    response = requests.post(auth_url, data=payload, timeout=10)
    response.raise_for_status()
    access_token = response.json().get("access_token")
    if not access_token:
        logger.error("No access token in Salesforce response")
        return None
    logger.info("Salesforce access token obtained successfully")
    return access_token

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
def create_salesforce_record(prediction, hype_data):
    access_token = get_salesforce_access_token()
    if not access_token:
        return {"success": False, "message": "Failed to get Salesforce access token"}

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'Name': prediction.get('product', {}).get('name', 'Unknown Product'),
        'Category__c': prediction.get('product', {}).get('category', 'Unknown'),
        'Demand_Uplift__c': prediction.get('uplift', 0.0),
        'Confidence__c': prediction.get('confidence', 0.0),
        'Strategy__c': prediction.get('strategy', 'Unknown'),
        'Hype_Score__c': hype_data.get('averageScore', 0.0),
        'Hype_Change_Percent__c': hype_data.get('change_percent', 0.0) if hype_data.get('change_detected') else 0.0
    }
    response = requests.post(
        f"{SALESFORCE_INSTANCE_URL}/services/data/v58.0/sobjects/Opportunity",
        headers=headers,
        json=data,
        timeout=10
    )
    response.raise_for_status()
    logger.info("Salesforce record created successfully")
    return {"success": True, "message": "Salesforce record created successfully"}

# ------------------------------------------------------------------
# 4. Discord helper (new) – batched alerts
# ------------------------------------------------------------------
_discord_alerts_buffer = []

def queue_discord_alert(message: str):
    """
    Add message to the in-memory buffer for Discord.
    """
    _discord_alerts_buffer.append(message)

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
def flush_discord_alerts():
    """
    Send all queued alerts in one batched POST.
    """
    global _discord_alerts_buffer
    if not _discord_alerts_buffer:
        return

    webhook_url = _get_secret(DISCORD_WEBHOOK_SECRET_NAME)
    if not webhook_url:
        logger.warning("Discord webhook URL not found; skipping alerts.")
        _discord_alerts_buffer.clear()
        return

    payload = {"content": "\n".join(_discord_alerts_buffer)}
    response = requests.post(webhook_url, json=payload, timeout=10)
    response.raise_for_status()
    logger.info(f"Sent {len(_discord_alerts_buffer)} Discord alerts")
    _discord_alerts_buffer.clear()

# ------------------------------------------------------------------
# 5. Main orchestrator
# ------------------------------------------------------------------
def send_integrations(prediction, hype_data):
    """
    Push data to Google Sheets, Salesforce, and queue Discord alerts.
    """
    # Queue a short Discord message for each prediction
    product_name = prediction.get('product', {}).get('name', 'Unknown')
    uplift = prediction.get('uplift', 0.0)
    queue_discord_alert(f"📈 {product_name}: predicted uplift {uplift:.2%}")

    results = [
        append_to_google_sheets(prediction, hype_data),
        create_salesforce_record(prediction, hype_data)
    ]
    flush_discord_alerts()  # send batched alerts

    successes = [r["success"] for r in results]
    messages = [r["message"] for r in results]
    return {"success": any(successes), "message": "; ".join(messages)}

# ------------------------------------------------------------------
# NEW ASYNC WRAPPER
# ------------------------------------------------------------------
async def send_integrations_async(prediction, hype_data):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, send_integrations, prediction, hype_data)

`


## File: api\services\llm_service.py

``$language

import os
import json
import time
import logging
import asyncio
import redis.asyncio as redis  # async-first client
import asyncpg

from openai import AsyncOpenAI
from typing import Dict, Optional

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/caeser")
pg_pool: Optional[asyncpg.Pool] = None
REDIS_URL          = os.getenv("REDIS_URL", "redis://localhost:6379/0")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL           = "http://localhost:8000"
SITE_NAME          = "CAESER"

logger = logging.getLogger(__name__)

# async Redis client
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# Async OpenAI client
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    http_client=None,
)

async def _init_connections() -> None:
    global pg_pool
    try:
        pg_pool = await asyncpg.create_pool(POSTGRES_URL, min_size=1, max_size=10)
        async with pg_pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS llm_data_quality (
                    metric TEXT NOT NULL,
                    value REAL NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
        logger.info("PostgreSQL connected and llm_data_quality table ensured.")
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL or create table: {e}")
        pg_pool = None

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def sanitize_input(s: str) -> str:
    return s.strip()

async def log_llm_data_quality(metric: str, value: float):
    """Persist metric in PostgreSQL asynchronously."""
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot log LLM data quality.")
        return
    try:
        async with pg_pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO llm_data_quality (metric, value, timestamp) VALUES ($1, $2, NOW())",
                metric, value
            )
    except Exception as e:
        logger.error(f"Failed to log LLM data quality to PostgreSQL: {e}")

# -----------------------------------------------------------------------------
# Core async function (upgraded & minimal)
# -----------------------------------------------------------------------------
async def _get_prediction_async(product: Dict, insights: Dict, hype_score: float) -> Dict:
    """
    Ultra-lean async variant that performs the LLM call and caching logic.
    """
    cache_key = f"llm:{product.get('name','')}:{hash(json.dumps(product, sort_keys=True))}"

    # Try cache first
    if (cached := await redis_client.get(cache_key)):
        return json.loads(cached)

    # Build prompt
    prompt = f"""
    Analyze the following product and cultural insights to predict demand uplift and suggest a marketing strategy.
    Product: {sanitize_input(product.get('name',''))}
    Tags: {', '.join([sanitize_input(t) for t in product.get('tags',[])])}
    Description: {sanitize_input(product.get('description',''))}
    Target Market: {sanitize_input(product.get('location','Global'))}
    Age: {sanitize_input(product.get('age_range','All'))}
    Gender: {sanitize_input(product.get('gender','All'))}
    Cultural Insights: {insights.get('data',{})}
    Hype Score: {hype_score}
    Provide a response in JSON format with 'uplift' (percentage, float), 'strategy' (string), 'confidence' (float 0-1), and 'trend' (list of dicts with 'time' and 'demand').
    """

    try:
        start = time.time()
        resp = await client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}],
            timeout=30,
        )
        content = resp.choices[0].message.content
        if content is None:
            raise ValueError("LLM response content is None")
        data = json.loads(content.strip())

        # Validate required keys
        required = {"uplift", "strategy", "confidence", "trend"}
        if not required.issubset(data):
            raise ValueError("Invalid LLM response format")

        # Add mock TikTok costs (backward compatibility)
        data["cpc"] = 1.0
        data["cpm"] = 5.0

        # Cache for 1 hour
        await redis_client.setex(cache_key, 3600, json.dumps({"success": True, "data": data}))

        # Log quality metrics
        await log_llm_data_quality("confidence", data.get("confidence", 0.0))
        await log_llm_data_quality("response_time", time.time() - start)

        return {"success": True, "data": data, "message": "Prediction generated successfully"}

    except Exception as e:
        logger.error("LLM request failed: %s", e)
        await log_llm_data_quality("errors", 1.0)
        return {"success": False, "data": None, "message": f"LLM request failed: {e}"}

# -----------------------------------------------------------------------------
# Public async prediction endpoint
# -----------------------------------------------------------------------------
async def get_prediction_async(product: Dict, insights: Dict, hype_score: float) -> Dict:
    """Public async wrapper for the prediction logic."""
    return await _get_prediction_async(product, insights, hype_score)

# -----------------------------------------------------------------------------
# Sync wrapper (100 % backward-compatible)
# -----------------------------------------------------------------------------
def get_prediction(product: Dict, insights: Dict, hype_score: float) -> Dict:
    """
    Legacy synchronous entry-point for all existing callers.
    Internally delegates to the async implementation.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:  # no loop in current thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(_get_prediction_async(product, insights, hype_score))

# -----------------------------------------------------------------------------
# Data-quality endpoint (unchanged)
# -----------------------------------------------------------------------------
async def get_llm_data_quality() -> Dict:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot get LLM data quality.")
        return {"success": False, "message": "Database not connected"}
    try:
        async with pg_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT metric, AVG(value) as avg_value, COUNT(*) as count
                FROM llm_data_quality
                GROUP BY metric
                """
            )
            metrics = {row["metric"]: {"avg_value": row["avg_value"], "count": row["count"]} for row in rows}
            return {
                "success": True,
                "data": metrics,
                "message": "LLM data quality metrics retrieved",
            }
    except Exception as e:
        logger.error(f"Failed to retrieve LLM data quality from PostgreSQL: {e}")
        return {"success": False, "message": f"Failed to retrieve LLM data quality: {e}"}

# ------------------------------------------------------------------
# NEW ASYNC WRAPPER
# ------------------------------------------------------------------
async def get_llm_data_quality_async():
    return await get_llm_data_quality()

async def init_llm_service():
    await _init_connections()
`


## File: api\services\predict_trend.py

``$language

import os
from datetime import datetime, timedelta
import logging
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from typing import Dict, Optional, List
import asyncpg

# Optional Prophet import (graceful fallback)
try:
    from prophet import Prophet
    HAS_PROPHET = True
except ImportError:
    HAS_PROPHET = False

POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/caeser")
pg_pool: Optional[asyncpg.Pool] = None

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def _init_connections() -> None:
    global pg_pool
    try:
        pg_pool = await asyncpg.create_pool(POSTGRES_URL, min_size=1, max_size=10)
        async with pg_pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS social_data (
                    id SERIAL PRIMARY KEY,
                    source TEXT,
                    text TEXT,
                    likes INTEGER,
                    timestamp TIMESTAMPTZ
                );
                CREATE TABLE IF NOT EXISTS trend_predictions (
                    id SERIAL PRIMARY KEY,
                    product_name TEXT,
                    tags TEXT,
                    predicted_peak_days INTEGER,
                    predicted_peak_date TEXT,
                    confidence REAL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS idx_trend_lookup ON social_data(source, text);
                """
            )
        logger.info("PostgreSQL connected and trend_predictions, social_data tables ensured.")
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL or create tables: {e}")
        pg_pool = None

# ------------------------------------------------------------------
async def predict_trend(product_name: str, tags: str) -> Dict:
    """
    Predict trend peak using Holt-Winters or Prophet (if available and data is large).
    """
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot predict trend.")
        return {"success": False, "message": "Database not connected"}

    try:
        async with pg_pool.acquire() as conn:
            tags_list = [tag.strip() for tag in tags.split(",")]
            # Use ILIKE for case-insensitive search and ANY for array matching
            query = """
                SELECT likes, timestamp FROM social_data
                WHERE source='google_trends' AND (text ILIKE $1 OR text = ANY($2::text[]))
                ORDER BY timestamp ASC
            """
            rows = await conn.fetch(query, f"%{product_name}%", tags_list)

            if not rows:
                logger.warning("No trend data for %s (%s)", product_name, tags)
                return {"success": False, "message": "No trend data"}

            likes = np.array([r["likes"] for r in rows], dtype=float)
            timestamps = [r["timestamp"] for r in rows]

            if len(likes) < 3:
                logger.warning("Insufficient data points")
                return {"success": False, "message": "Insufficient data"}

            # --- Model choice ---
            if HAS_PROPHET and len(likes) > 30:
                import pandas as pd # Import pandas here if only used in this branch
                # Prophet for longer series
                df = pd.DataFrame({
                    "ds": timestamps,
                    "y": likes
                })
                m = Prophet()
                m.fit(df)
                future = m.make_future_dataframe(periods=90)
                forecast = m.predict(future)
                peak_row = forecast.loc[forecast["yhat"].idxmax()]
                peak_date = peak_row["ds"].strftime("%Y-%m-%d")
                peak_days = (peak_row["ds"] - timestamps[-1]).days # type: ignore
                confidence = 0.9  # Prophet gives intervals; simplified here
            else:
                # Holt-Winters (faster for short series)
                model = ExponentialSmoothing(likes, trend="add", seasonal=None)
                fit = model.fit()
                fcast = fit.forecast(90)
                peak_idx = int(np.argmax(fcast))
                peak_days = peak_idx + 1
                peak_date = (timestamps[-1] + timedelta(days=peak_days)).strftime("%Y-%m-%d")
                confidence = min(0.95, 1.0 - fit.sse / np.sum(likes ** 2))

            await conn.execute("""
                INSERT INTO trend_predictions
                (product_name, tags, predicted_peak_days, predicted_peak_date, confidence, timestamp)
                VALUES ($1, $2, $3, $4, $5, NOW())
            """, product_name, tags, int(peak_days), peak_date, confidence)

            logger.info("Trend for %s: peak in %d days on %s (%.2f conf)",
                        product_name, peak_days, peak_date, confidence)
            return {
                "success": True,
                "predicted_peak_days": int(peak_days),
                "predicted_peak_date": peak_date,
                "confidence": confidence
            }

    except Exception as e:
        logger.error("Trend prediction failed: %s", e)
        return {"success": False, "message": f"Prediction failed: {e}"}

# ------------------------------------------------------------------
async def init_predict_trend_service():
    await _init_connections()

# ------------------------------------------------------------------
if __name__ == "__main__":
    import asyncio
    async def main():
        await init_predict_trend_service()
        result = await predict_trend("Wireless Headphones", "electronics, audio")
        print(result)
    asyncio.run(main())

`


## File: api\services\qloo_service.py

``$language

# api/services/qloo_service.py
import os
import json
import asyncio
import aiohttp
import logging
import re
from typing import Dict, List, Optional
import asyncpg
import redis.asyncio as redis
from cachetools import TTLCache

# -------------------- Logging --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------- Redis (primary cache) --------------------
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client: Optional[redis.Redis] = None

# -------------------- PostgreSQL (second-level cache) ----------
POSTGRES_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/postgres"
)
pg_pool: Optional[asyncpg.Pool] = None

# -------------------- In-Memory fallback ------------------------
memory_cache = TTLCache(maxsize=100, ttl=3600)

# -------------------- Constants ---------------------------------
QLOO_API_KEY = os.getenv("QLOO_API_KEY")
BASE_URL = "https://hackathon.api.qloo.com/v2/insights"

# -------------------- Helpers ----------------------------------
def sanitize_input(input_str: str) -> str:
    """Remove any non-alphanumeric characters except space, comma, period, hyphen."""
    return re.sub(r"[^a-zA-Z0-9\s,.-]", "", input_str.strip())

# >>>>> GRANULAR CACHE KEY (already deterministic) <<<<<
def _build_cache_key(insight_type: str, location: str, tags: List[str]) -> str:
    tag_csv = ",".join(sorted(tags))  # keep it deterministic
    return f"qloo:{insight_type}:{location}:{tag_csv}"

def _build_params(insight_type: str, location: str, tags: List[str]) -> Dict[str, Optional[str]]:
    filter_tags = ",".join([f"urn:tag:keyword:brand:{tag.lower()}" for tag in tags])
    params: Dict[str, Optional[str]] = {}

    if insight_type == "brand":
        params.update({
            "filter.type": "urn:entity:brand",
            "signal.location.query": location if location != "global" else None,
            "filter.tags": filter_tags
        })
    elif insight_type == "demographics":
        params.update({
            "filter.type": "urn:demographics",
            "signal.location.query": location if location != "global" else None,
            "signal.interests.tags": filter_tags
        })
    elif insight_type == "heatmap":
        params.update({
            "filter.type": "urn:heatmap",
            "filter.location.query": location if location != "global" else None,
            "signal.interests.tags": filter_tags
        })
    else:
        raise ValueError(f"Unsupported insight type: {insight_type}")
    return params

# -------------------- Async retry wrapper ----------------------
async def _retry_async(coro, max_attempts: int = 3, base_delay: float = 1.0):
    attempt = 0
    while True:
        try:
            return await coro
        except Exception as e:
            attempt += 1
            if attempt >= max_attempts:
                raise
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning("Retrying in %.1fs after failure: %s", delay, e)
            await asyncio.sleep(delay)

# -------------------- Cache helpers -----------------------------
async def _get_cache(key: str) -> Optional[Dict]:
    """Redis → PostgreSQL → memory fall-through."""
    # 1. Redis
    if redis_client:
        try:
            cached = await redis_client.get(key)
            if cached:
                logger.info("Cache hit (Redis) for %s", key)
                return json.loads(cached)
        except Exception as e:
            logger.warning("Redis read failed: %s", e)

    # 2. PostgreSQL
    if pg_pool:
        try:
            async with pg_pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT value FROM qloo_cache WHERE key = $1", key
                )
                if row:
                    logger.info("Cache hit (PostgreSQL) for %s", key)
                    return json.loads(row["value"])
        except Exception as e:
            logger.warning("PostgreSQL read failed: %s", e)

    # 3. In-memory
    if key in memory_cache:
        logger.info("Cache hit (memory) for %s", key)
        return memory_cache[key]

    return None

async def _set_cache(key: str, value: Dict, ttl: int = 3600) -> None:
    """Write-through to Redis, PostgreSQL and memory."""
    payload = json.dumps(value)

    # 1. Redis
    if redis_client:
        try:
            await redis_client.setex(key, ttl, payload)
        except Exception as e:
            logger.warning("Redis write failed: %s", e)

    # 2. PostgreSQL
    if pg_pool:
        try:
            async with pg_pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO qloo_cache(key, value, expires_at)
                    VALUES ($1, $2, NOW() + INTERVAL '1 hour')
                    ON CONFLICT (key) DO UPDATE
                    SET value = EXCLUDED.value,
                        expires_at = EXCLUDED.expires_at
                    """,
                    key, payload
                )
        except Exception as e:
            logger.warning("PostgreSQL write failed: %s", e)

    # 3. Memory
    memory_cache[key] = value

# -------------------- Connection initializers -------------------
async def _init_connections() -> None:
    """Called once at startup (see bottom)."""
    global redis_client, pg_pool

    # Redis
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        await redis_client.ping()
        logger.info("Redis connected")
    except Exception as e:
        logger.warning("Redis unavailable: %s", e)
        redis_client = None

    # PostgreSQL
    try:
        pg_pool = await asyncpg.create_pool(POSTGRES_URL, min_size=1, max_size=10)
        # ensure table exists
        async with pg_pool.acquire() as conn: #type: ignore
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS qloo_cache (
                    key TEXT PRIMARY KEY,
                    value JSONB NOT NULL,
                    expires_at TIMESTAMPTZ NOT NULL
                )
                """
            )
        logger.info("PostgreSQL connected")
    except Exception as e:
        logger.warning("PostgreSQL unavailable: %s", e)
        pg_pool = None

# -------------------- Main service call -------------------------
async def get_cultural_insights(
    location: str,
    tags: List[str],
    insight_type: str = "brand"
) -> Dict:
    # ---------- Validation ----------
    if not QLOO_API_KEY:
        raise ValueError("QLOO_API_KEY not configured")

    if not location or not isinstance(location, str) or not location.strip():
        raise ValueError("Invalid location provided")

    if not tags or not isinstance(tags, list) or not all(isinstance(t, str) and t.strip() for t in tags):
        raise ValueError("Invalid tags provided")

    location = sanitize_input(location)
    tags = [sanitize_input(tag) for tag in tags]

    cache_key = _build_cache_key(insight_type, location, tags)

    # >>>>> ASYNC TWEAK: immediate cache return <<<<<
    cached = await _get_cache(cache_key)
    if cached:
        return cached

    # ---------- Build Request ----------
    params = _build_params(insight_type, location, tags)
    headers = {
        "X-Api-Key": QLOO_API_KEY,
        "Content-Type": "application/json"
    }

    # ---------- Async HTTP Call with Retry ----------
    async def _fetch():
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10)
        ) as session:
            async with session.get(BASE_URL, headers=headers, params=params) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise ValueError(f"Qloo API error {resp.status}: {text}")
                data = await resp.json()
                if not data.get("success"):
                    raise ValueError(f"Invalid API response: {data.get('message', 'Unknown error')}")
                return data

    try:
        data = await _retry_async(_fetch())
    except Exception as e:
        logger.error("Qloo API request failed: %s", e)
        return {"success": False, "data": None, "message": str(e)}

    # ---------- Cache & Return ----------
    result = {
        "success": True,
        "data": data.get("results"),
        "message": f"{insight_type.capitalize()} insights retrieved successfully"
    }

    await _set_cache(cache_key, result, ttl=3600)
    logger.info("Cached insights for %s", cache_key)
    return result

# -------------------- Module-level startup hook -----------------
# If you have an ASGI lifespan-handler (FastAPI/Starlette),
# call _init_connections() there instead.
async def init_qloo_service():
    await _init_connections()

# ------------------------------------------------------------------
# NEW ASYNC WRAPPER
# ------------------------------------------------------------------
async def get_cultural_insights_async(location, tags, insight_type="brand"):
    return await get_cultural_insights(location, tags, insight_type)
`


## File: api\services\__init__.py

``$language

from .data_quality_service import check_data_quality_async, init_data_quality_service
from .discord_service import send_alert_async, init_discord_service
from .hype_engine import calculate_hype_score_async, init_hype_engine_service
from .integrations_service import send_integrations_async
from .llm_service import get_prediction_async, get_llm_data_quality_async, init_llm_service
from .qloo_service import get_cultural_insights_async, init_qloo_service
from .predict_trend import predict_trend, init_predict_trend_service

`


## File: api\utils\logging.py

``$language

import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(name: str = __name__, level: int = logging.INFO, log_file: str | None = os.getenv("LOG_FILE")) -> logging.Logger:
    """Configure and return a logger instance.
    Args:
        name (str): Logger name (defaults to module name).
        level (int): Logging level (defaults to INFO).
        log_file (str): Path to log file (optional).
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log file is specified
    if log_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger
`


## File: api\utils\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: bin\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: bin\sqlite\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: data\caeser.db

``$language

SQLite format 3   @                                                                     .v�
� 

� 
�
��
h�s
�z                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                �	33�5tableaffiliate_platformsaffiliate_platforms
CREATE TABLE affiliate_platforms (id INTEGER PRIMARY KEY, platform_name TEXT UNIQUE)E
Y3 indexsqlite_autoindex_affiliate_platforms_1affiliate_platforms�/##�%tablecompetitorscompetitorsCREATE TABLE competitors (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	hype_score FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
)5I# indexsqlite_autoindex_competitors_1competitors	�;!!�AtablecategoriescategoriesCREATE TABLE categories (
	id INTEGER NOT NULL, 
	category_name VARCHAR NOT NULL, 
	keywords TEXT NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (category_name)
)3G! indexsqlite_autoindex_categories_1categoriesm%/�indexidx_insightscultural_insightsCREATE INDEX idx_insights ON cultural_insights (location, category)�~//�+tablecultural_insightscultural_insightsCREATE TABLE cultural_insights (
	id INTEGER NOT NULL, 
	location TEXT NOT NULL, 
	category TEXT NOT NULL, 
	data TEXT NOT NULL, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	PRIMARY KEY (id)
)�)++�	tablealembic_versionalembic_versionCREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
)=Q+ indexsqlite_autoindex_alembic_version_1alembic_version       
   � ��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             =20250729_add_competitors   2025072%a9772e6a7448
   � ��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            =20250729_add_competitors   202507%a9772e6a7448
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
   � ���                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
 twitter facebook instagram
   � ���                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            twitterfacebook	instagram
`


## File: data\init_db.py

``$language

# data/init_db.py
"""
PostgreSQL + SQLAlchemy bootstrap (ORM edition).
Keeps Alembic first, then falls back to ORM for anything missing.
"""
import os
import logging
from datetime import datetime, timedelta

from sqlalchemy import (
    create_engine, MetaData, Column,
    Integer, String, Float, DateTime, Text, CheckConstraint
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from alembic import config, command

# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# PostgreSQL connection
# ------------------------------------------------------------------
DB_URL = "postgresql+asyncpg://caeser_user:caeser_pass@localhost:5432/caeser"

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)
Base = declarative_base()

# ------------------------------------------------------------------
# ORM Models
# ------------------------------------------------------------------
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    category_name = Column(String, index=True)


class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True)
    product_name = Column(String, index=True)
    category = Column(String)
    predicted_uplift = Column(Float)
    confidence = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class SocialData(Base):
    __tablename__ = "social_data"
    __table_args__ = (
        {"postgresql_partition_by": "RANGE (timestamp)"}
    )
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    likes = Column(Integer)
    source = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class CulturalInsight(Base):
    __tablename__ = "cultural_insights"
    id = Column(Integer, primary_key=True)
    location = Column(String, index=True)
    insight_type = Column(String)
    value = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class Competitor(Base):
    __tablename__ = "competitors"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    website = Column(String)
    hype_score = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "hype_score >= 0 AND hype_score <= 100",
            name="hype_range"
        ),
    )


class InsightType(Base):
    __tablename__ = "insight_types"
    id = Column(Integer, primary_key=True)
    type_name = Column(String, unique=True, nullable=False)


# ------------------------------------------------------------------
# Utility: create missing tables via ORM
# ------------------------------------------------------------------
def create_missing_tables():
    """Create tables that Alembic has not produced yet."""
    Base.metadata.create_all(engine, checkfirst=True)
    logger.info("ORM tables ensured.")


# ------------------------------------------------------------------
# Utility: seed insight_types defaults
# ------------------------------------------------------------------
def seed_insight_types():
    defaults = ["brand", "demographics", "heatmap"]
    with SessionLocal() as session:
        for t in defaults:
            session.merge(InsightType(type_name=t))
        session.commit()
    logger.info("Insight types seeded.")


# ------------------------------------------------------------------
# Utility: create extra objects if Alembic skipped them
# ------------------------------------------------------------------
def create_post_migration_objects():
    with engine.begin() as conn:
        # 2025 partition
        conn.execute(sa.text("""
            CREATE TABLE IF NOT EXISTS social_data_2025
            PARTITION OF social_data
            FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
        """))

        # View
        conn.execute(sa.text("""
            CREATE OR REPLACE VIEW avg_hype_per_category AS
            SELECT category, AVG(predicted_uplift) AS avg_hype
            FROM predictions
            GROUP BY category;
        """))

        # Validate constraints after ensuring data is clean
        conn.execute(sa.text("""
            ALTER TABLE competitors VALIDATE CONSTRAINT hype_range;
        """))
    logger.info("Post-migration objects created and constraints validated.")


# ------------------------------------------------------------------
# Main entry point
# ------------------------------------------------------------------
def init_db():
    try:
        # 1. Alembic first
        alembic_cfg = config.Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Alembic migrations complete.")

        # 2. ORM fallback
        create_missing_tables()

        # 3. Seed data
        seed_insight_types()

        # 4. Post-migration objects (view, partition, etc.)
        create_post_migration_objects()

    except SQLAlchemyError as e:
        logger.exception("Database bootstrap failed: %s", e)
        raise


if __name__ == "__main__":
    init_db()
`


## File: data\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: data\processed\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: data\raw\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: data\schemas\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: docs\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: frontend\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: frontend\components\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: frontend\public\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: frontend\src\main.py

``$language

# frontend/src/main.py – v2 + helpers + validator
import asyncio, os, json, logging, re
from datetime import datetime
import streamlit as st
import requests, pandas as pd, plotly.express as px, plotly.graph_objects as go
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
st.set_page_config(page_title="CÆSER Dashboard v2", layout="wide")

# ---------- THEMING & DARK MODE ----------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
st.sidebar.button(
    "🌗 Toggle Dark",
    on_click=lambda: st.session_state.__setitem__(
        "dark_mode", not st.session_state.dark_mode
    ),
)
st.markdown(
    f"""<style> :root {{ --p:{os.getenv("PRIMARY_COLOR","#667eea")};}}
.dark body{{background:#0f172a;color:#e2e8f0}}</style>""",
    unsafe_allow_html=True,
)

# ---------- ASYNC / VALID ----------
async def async_post(endpoint, payload):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=payload,
            timeout=60,
        ).json(),
    )

def validate_inputs(n, d):
    return bool(n.strip() and d.strip())

# ---------- SIDEBAR ----------
with st.sidebar.expander("🛠 Manage"):
    for t, lbl in (("categories", "Category"), ("competitors", "Competitor")):
        st.subheader(f"{lbl}")
        name = st.text_input(f"{lbl} Name", key=f"{t}_name")
        extra = (
            st.number_input("Hype Score", 0.0, 100.0, 50.0, key=f"{t}_score")
            if t == "competitors"
            else st.text_area("Keywords (comma)", key=f"{t}_kw")
        )
        if st.button("Save", key=f"{t}_save"):
            payload = (
                {"name": name, "hype_score": extra}
                if t == "competitors"
                else {"category_name": name, "keywords": extra}
            )
            st.success(
                requests.post(
                    f"{API_BASE_URL}/{t}",
                    json=payload,
                    timeout=5,
                )
                .json()
                .get("message", "Saved")
            )

# ---------- HELPERS ----------
@st.cache_data(ttl=300)
def _get_insights(location, tags, insight_type):
    """Cached wrapper for /insights endpoint."""
    url = f"{API_BASE_URL}/insights/{location or 'global'}"
    params = {"tags": tags or "", "insight_type": insight_type}
    return requests.get(url, params=params, timeout=30).json()

@st.cache_data(ttl=300)
def _get_trend_prediction(location, tags):
    url = f"{API_BASE_URL}/trend_prediction"
    payload = {"location": location or "global", "tags": tags or ""}
    return requests.post(url, json=payload, timeout=30).json()

def insight_chart(data, itype):
    if not data or not data.get("success"):
        return None
    ents = data["data"].get("entities", [])
    if itype == "brand":
        df = pd.DataFrame(
            [
                {"trait": e["name"], "score": e["properties"].get("popularity", 0.5)}
                for e in ents
            ]
        )
        fig = px.bar(df, x="trait", y="score", title="Cultural Affinity")
    elif itype == "demographics":
        df = pd.DataFrame(
            [
                {"age": e.get("age_group", "?"), "affinity": e.get("affinity_score", 0.5)}
                for e in ents
            ]
        )
        fig = px.bar(df, x="age", y="affinity", title="Demographic Affinity")
    elif itype == "heatmap":
        h = data["data"].get("heatmap", {})
        fig = go.Figure(
            go.Heatmap(
                z=h.get("z", []),
                x=h.get("x", []),
                y=h.get("y", []),
                colorscale="Viridis",
            )
        )
        fig.update_layout(title="Regional Heatmap")
    else:
        return None
    st.plotly_chart(fig, use_container_width=True)
    return df

def pred_chart(p, hype, t):
    if not p or not p.get("success"):
        return None
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Uplift %", f"{p['data'].get('uplift', '-')}")
        st.metric("Confidence", f"{p['data'].get('confidence', '-')}")
        st.metric("Hype", f"{hype}")
        if t and t.get("success"):
            st.metric("Peak in", f"{t['predicted_peak_days']} days")
    with c2:
        st.write("**Strategy**", p["data"].get("strategy", "-"))
    trend = p["data"].get("trend", [])
    if trend:
        st.plotly_chart(
            px.line(
                pd.DataFrame(trend),
                x="time",
                y="demand",
                title="Demand Trend",
            ),
            use_container_width=True,
        )
    return pd.DataFrame([{"Metric": "Uplift", "Value": p["data"].get("uplift")}])

def export_report(df1, df2, fmt):
    if df1 is None or df2 is None:
        return None, None, None
    report = pd.concat([df1, df2], axis=1)
    buf = BytesIO()
    if fmt == "PDF":
        SimpleDocTemplate(buf, pagesize=letter).build(
            [Table([report.columns.tolist()] + report.values.tolist())]
        )
    elif fmt == "Excel":
        report.to_excel(buf, index=False)
    else:
        report.to_csv(buf, index=False)
    buf.seek(0)
    return (
        buf,
        f"report.{fmt.lower()}",
        (
            "application/pdf"
            if fmt == "PDF"
            else (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                if fmt == "Excel"
                else "text/csv"
            )
        ),
    )

def dq_widget():
    try:
        m = requests.get(f"{API_BASE_URL}/data_quality", timeout=5).json()
        if m.get("success"):
            st.subheader("Data Quality")
            for k, v in m["data"].items():
                st.write(f"**{k}**: {v.get('value', '-')}")
    except Exception:
        pass

# ---------- LIGHTWEIGHT VALIDATOR ----------
def validate_frontend_inputs(pn, desc, tags, loc, age, gender):
    """Return (ok: bool, error_msg: str)"""
    if not pn.strip():
        return False, "Product Name is required."
    if len(pn) > 120:
        return False, "Product Name ≤ 120 chars."
    if not desc.strip():
        return False, "Description is required."
    if len(desc) > 1000:
        return False, "Description ≤ 1000 chars."
    if tags and not re.match(r'^[\w\s,]+$', tags):
        return False, "Tags may only contain letters, numbers, spaces & commas."
    if age and not age.isdigit():
        return False, "Age must be a number."
    return True, ""

# ---------- MAIN ----------
tab1, tab2, tab3 = st.tabs(["Dashboard", "Store Data", "Google Trends"])
with tab1:
    st.subheader("Product Details")
    pn = st.text_input("Product Name*")
    desc = st.text_area("Description*")
    tags = st.text_input("Tags")
    loc = st.text_input("Location")
    age = st.text_input("Age")
    gender = st.selectbox("Gender", ["All", "Male", "Female"])
    itype = st.selectbox("Insight", ["brand", "demographics", "heatmap"])
    if st.button("Analyze", use_container_width=True):
        ok, err = validate_frontend_inputs(pn, desc, tags, loc, age, gender)
        if not ok:
            st.error(err)
        elif validate_inputs(pn, desc):
            with st.spinner("Analyzing…"):
                res = asyncio.run(
                    async_post(
                        "/analyze",
                        {
                            "product_name": pn,
                            "description": desc,
                            "tags": tags,
                            "locations": loc,
                            "gender": gender,
                        },
                    )
                )
                hype = res.get("hype_score", 0)
                with st.spinner("Fetching trend prediction…"):
                    trend = asyncio.run(
                        async_post(
                            "/predict/trend",
                            {"product_name": pn, "tags": tags},
                        )
                    )
                with st.spinner("Fetching insights…"):
                    ins = _get_insights(loc, tags, itype)
                with st.spinner("Predicting demand…"):
                    pred = asyncio.run(
                        async_post(
                            "/predict/demand",
                            {
                                "product": {"name": pn, "tags": tags},
                                "insights": ins,
                                "hype_score": hype,
                            },
                        )
                    )
                df_ins = insight_chart(ins, itype)
                df_pred = pred_chart(pred, hype, trend)
                dq_widget()
                buf, fn, mime = export_report(
                    df_ins,
                    df_pred,
                    st.selectbox("Export", ["CSV", "Excel", "PDF"]),
                )
                if buf:
                    st.download_button("Download Report", data=buf, file_name=fn, mime=mime)

with tab2:
    st.subheader("Store Data")
    up = st.file_uploader("CSV (product,sales,date)", type="csv")
    if up:
        df = pd.read_csv(up)
        st.dataframe(df.head())
        if st.button("Upload"):
            with st.spinner("Uploading…"):
                for _, row in df.iterrows():
                    asyncio.run(async_post("/store_data", dict(row)))
            st.success("Uploaded!")
        st.download_button(
            "Download existing store data",
            data=requests.get(f"{API_BASE_URL}/store_data").content,
            file_name="store.csv",
        )

with tab3:
    kw = st.text_input("Google Trends Keywords")
    if st.button("Fetch"):
        with st.spinner("Fetching Google Trends…"):
            r = requests.post(
                f"{API_BASE_URL}/google_trends",
                json={"keywords": kw.split(",")},
            )
        st.dataframe(pd.json_normalize(r.json()))
`


## File: frontend\src\outcome_form.py

``$language

import streamlit as st
import requests

st.title("Report Actual Uplift")

# Input fields with validation
pid = st.number_input("Prediction ID", min_value=1, value=1, step=1)
actual = st.number_input("Actual uplift %", min_value=0.0, value=0.0, step=0.1)

# New gamified slider section
st.subheader("Marketing Simulation")
budget = st.slider("Marketing Budget ($)", 1000, 50000, 10000)
hype_score = st.slider("Estimated Hype Score", 0, 100, 70)

# Calculate ROI based on hype score and budget (capped at 50 % of budget)
roi = min(budget * 0.1 * (hype_score / 100), budget * 0.5)
st.metric("Est. ROI", f"${roi:.0f}", delta_color="inverse" if roi < budget else "normal")

if st.button("Submit"):
    if pid <= 0 or actual < 0:
        st.error("Please enter valid values for Prediction ID and Actual uplift %.")
    else:
        try:
            r = requests.post(
                f"{os.getenv('API_BASE_URL', 'http://localhost:8000')}/submit_outcome",
                json={"prediction_id": pid, "actual_uplift": actual}
            )
            st.json(r.json())
        except requests.RequestException as e:
            st.error(f"Failed to submit outcome: {str(e)}")
`


## File: frontend\src\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: frontend\styles\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: migrations\env.py

``$language

import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
DB_URL = os.getenv("DB_PATH", "postgresql+asyncpg://caeser_user:caeser_pass@localhost:5432/caeser")

# Alembic Config object
config = context.config
config.set_main_option('sqlalchemy.url', DB_URL)

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate support
target_metadata = None

async def run_migrations_online():
    """Run migrations in 'online' mode using async engine."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata
            )
        )
        await connection.run_sync(
            lambda sync_conn: context.run_migrations()
        )

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
`


## File: migrations\README

``$language

Generic single-database configuration.
`


## File: migrations\script.py.mako

``$language

"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade schema."""
    ${downgrades if downgrades else "pass"}

`


## File: migrations\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: migrations\versions\20250729_add_categories.py

``$language

"""Add flexible categories table

Revision ID: 20250729_add_categories
Revises: 4c0ff554c6e2
Create Date: 2025-07-29 08:00:00

"""
from alembic import op
import sqlalchemy as sa

revision = "20250729_add_categories"
down_revision = "4c0ff554c6e2"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("category_name", sa.String(), nullable=False, unique=True),
        sa.Column("keywords", sa.Text(), nullable=False)  # comma-separated
    )

def downgrade() -> None:
    op.drop_table("categories")
`


## File: migrations\versions\20250729_add_competitors.py

``$language

"""Add competitors table

Revision ID: 20250729_add_competitors
Revises: 4c0ff554c6e2
Create Date: 2025-07-29 08:05:00
"""
from alembic import op
import sqlalchemy as sa

revision = "20250729_add_competitors"
down_revision = "4c0ff554c6e2"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "competitors",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False, unique=True),
        sa.Column("hype_score", sa.Float, nullable=False, default=0.0)
    )

def downgrade() -> None:
    op.drop_table("competitors")
`


## File: migrations\versions\20250730_pg_indexes.py

```python
from alembic import op
import sqlalchemy as sa

revision = "20250730_pg_indexes"
down_revision = "a9772e6a7448"
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create a new partitioned table
    op.execute("""
        CREATE TABLE social_data_new (
            id SERIAL,
            platform TEXT,
            post_content TEXT,
            sentiment_score REAL,
            created_at TIMESTAMPTZ,
            PRIMARY KEY (id, created_at)
        ) PARTITION BY RANGE (created_at);
    """)
    
    # Create partitions for 2025 and 2026
    op.execute("""
        CREATE TABLE social_data_2025 PARTITION OF social_data_new
        FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
    """)
    op.execute("""
        CREATE TABLE social_data_2026 PARTITION OF social_data_new
        FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
    """)
    
    # Copy data from the old table
    op.execute("""
        INSERT INTO social_data_new (id, platform, post_content, sentiment_score, created_at)
        SELECT id, platform, post_content, sentiment_score, created_at FROM social_data;
    """)
    
    # Drop the old table and rename the new one
    op.execute("DROP TABLE social_data;")
    op.execute("ALTER TABLE social_data_new RENAME TO social_data;")
    
    # Create indexes
    op.create_index("idx_categories_name", "categories", ["name"])
    op.create_index("idx_predictions_product", "predictions", ["product_name"])
    op.create_index("idx_social_data_platform", "social_data", ["platform"])
    op.create_index("idx_social_data_platform_created_at", "social_data", ["platform", "created_at"])
    op.create_index("idx_social_data_post_content", "social_data", ["post_content"])
    
    # Create view
    op.execute("""
        CREATE OR REPLACE VIEW avg_trend_per_category AS
        SELECT category_id, AVG(trend_score) AS avg_trend
        FROM predictions
        GROUP BY category_id;
    """)
    
    # Add hype_score column and constraint
    op.add_column("competitors", sa.Column("hype_score", sa.Float))
    op.execute("""
        ALTER TABLE competitors
        ADD CONSTRAINT hype_range
        CHECK (hype_score >= 0 AND hype_score <= 100)
        NOT VALID;
    """)

def downgrade() -> None:
    # Reverse constraints
    op.drop_constraint("hype_range", "competitors")
    op.drop_column("competitors", "hype_score")
    
    # Reverse view
    op.execute("DROP VIEW IF EXISTS avg_trend_per_category")
    
    # Reverse indexes
    op.drop_index("idx_social_data_post_content", table_name="social_data")
    op.drop_index("idx_social_data_platform_created_at", table_name="social_data")
    op.drop_index("idx_social_data_platform", table_name="social_data")
    op.drop_index("idx_predictions_product", table_name="predictions")
    op.drop_index("idx_categories_name", table_name="categories")
    
    # Recreate the original non-partitioned table
    op.execute("""
        CREATE TABLE social_data_old AS SELECT * FROM social_data;
    """)
    op.execute("DROP TABLE social_data;")
    op.execute("ALTER TABLE social_data_old RENAME TO social_data;")
    ```


## File: migrations\versions\4c0ff554c6e2_initial_migration.py

``$language

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4c0ff554c6e2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    inspector = sa.inspect(op.get_bind())
    tables = inspector.get_table_names()

    if 'cultural_insights' not in tables:
        op.create_table('cultural_insights',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location', sa.Text(), nullable=False),
        sa.Column('category', sa.Text(), nullable=False),
        sa.Column('data', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index('idx_insights', 'cultural_insights', ['location', 'category'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_insights', table_name='cultural_insights')
    op.drop_table('cultural_insights')
    # ### end Alembic commands ###
`


## File: migrations\versions\a9772e6a7448_merge_categories_and_competitors.py

``$language

"""merge categories and competitors

Revision ID: a9772e6a7448
Revises: 20250729_add_categories, 20250729_add_competitors
Create Date: 2025-07-29 17:25:26.581468
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "a9772e6a7448"
down_revision: Union[str, Sequence[str], None] = ("20250729_add_categories", "20250729_add_competitors")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Previous files already added the tables; nothing to merge
    pass

def downgrade() -> None:
    pass
`


## File: migrations\versions\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: notebooks\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


## File: scrapers\affiliate_purchases.py

``$language

"""
affiliate_purchases.py – real APIs + demo fallback
"""
import asyncio, json, os, logging, csv, aiohttp
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
async def last_scraped() -> datetime:
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT MAX(timestamp) FROM social_data WHERE source='affiliate'")
        )
        ts = result.scalar()
        return datetime.fromisoformat(ts) if ts else datetime.utcnow() - timedelta(days=7)

# ------------------------------------------------------------------
async def init_affiliate_table():
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        await session.execute(text("""
            CREATE TABLE IF NOT EXISTS affiliate_platforms (
                id SERIAL PRIMARY KEY,
                platform_name TEXT UNIQUE NOT NULL
            )
        """))
        defaults = ["instagram", "facebook", "twitter"]
        for p in defaults:
            await session.execute(
                text("INSERT INTO affiliate_platforms(platform_name) VALUES (:name) ON CONFLICT DO NOTHING"),
                {"name": p}
            )
        await session.commit()

# ------------------------------------------------------------------
async def fetch_affiliate_data(platform: str):
    api_key = os.getenv(f"{platform.upper()}_API_KEY")
    if not api_key:
        logger.warning("No API key for %s – using demo CSV", platform)
        return []
    url = f"https://api.{platform}.com/v1/data"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=15) as response:
                response.raise_for_status()
                return await response.json()
    except Exception as e:
        """Always return [] so demo CSV is used."""
        return []
# ------------------------------------------------------------------
async def load_demo_csv():
    demo_path = pathlib.Path(__file__).with_name("demo_affiliate.csv")
    if not demo_path.exists():
        return []
    with open(demo_path, newline="", encoding="utf-8") as f:
        return [{"title": row["title"], "clicks": int(row["clicks"]), "timestamp": row["timestamp"]}
                for row in csv.DictReader(f)]

# ------------------------------------------------------------------
async def store_affiliate_data():
    await init_affiliate_table()
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        result = await session.execute(text("SELECT platform_name FROM affiliate_platforms"))
        platforms = [row[0] for row in result.fetchall()]

        last = await last_scraped()
        fresh_rows = []

        for platform in platforms:
            data = await fetch_affiliate_data(platform)
            if not data:
                data = await load_demo_csv()
            for row in data:
                try:
                    if datetime.fromisoformat(row["timestamp"]) > last:
                        fresh_rows.append(row)
                except (KeyError, ValueError):
                    continue

        if fresh_rows:
            for item in fresh_rows:
                await session.execute(
                    text("""
                        INSERT INTO social_data(text, likes, source, timestamp)
                        VALUES (:text, :likes, :source, :timestamp)
                    """),
                    {
                        "text": f"{platform}:{item.get('title','')}",
                        "likes": item.get("clicks", 0),
                        "source": "affiliate",
                        "timestamp": item["timestamp"],
                    }
                )
            await session.commit()
            logger.info("Stored %d fresh affiliate rows.", len(fresh_rows))

# ------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(init_affiliate_table())
    asyncio.run(store_affiliate_data())
`


## File: scrapers\credit_card_spending.py

``$language

"""
credit_card_spending.py – real API + demo CSV fallback
"""
import asyncio, csv, os, logging, aiohttp
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
import pathlib

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
async def last_scraped() -> datetime:
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT MAX(timestamp) FROM social_data WHERE source='credit_card'")
        )
        ts = result.scalar()
        return datetime.fromisoformat(ts) if ts else datetime.utcnow() - timedelta(days=7)

# ------------------------------------------------------------------
async def init_spending_table():
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        await session.execute(text("""
            CREATE TABLE IF NOT EXISTS spending_data (
                id SERIAL PRIMARY KEY,
                category TEXT,
                spend_total REAL,
                timestamp TEXT
            )
        """))
        await session.commit()

# ------------------------------------------------------------------
async def fetch_credit_card_data():
    api_key = os.getenv("CREDIT_CARD_API_KEY")
    if not api_key:
        return []
    url = "https://api.creditcard.com/v1/transactions"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=15) as response:
                response.raise_for_status()
                return await response.json()
    except Exception as e:
        """Always return [] so demo CSV is used."""
        return []

# ------------------------------------------------------------------
async def load_demo_csv():
    demo_path = pathlib.Path(__file__).with_name("demo_credit.csv")
    if not demo_path.exists():
        return []
    with open(demo_path, newline="", encoding="utf-8") as f:
        return [{"category": row["category"], "spend_total": float(row["spend_total"]), "timestamp": row["timestamp"]}
                for row in csv.DictReader(f)]

# ------------------------------------------------------------------
async def store_spending_data():
    data = await fetch_credit_card_data()
    if not data:
        data = await load_demo_csv()
    last = await last_scraped()
    fresh = [r for r in data if datetime.fromisoformat(r["timestamp"]) > last]
    if not fresh:
        logger.info("No fresh credit-card data.")
        return

    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        await session.execute(
            text("""
                INSERT INTO social_data(text, likes, source, timestamp)
                VALUES (:text, :likes, :source, :timestamp)
            """),
            [{"text": row["category"], "likes": int(row["spend_total"]), "source": "credit_card", "timestamp": row["timestamp"]}
             for row in fresh]
        )
        await session.commit()
    logger.info("Stored %d fresh credit-card rows.", len(fresh))

# ------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(init_spending_table())
    asyncio.run(store_spending_data())
`


## File: scrapers\dark_web.py

``$language

"""
dark_web.py – async + proxy + demo fallback + NLP filter
"""
import asyncio, csv, os, random, logging, pathlib
from datetime import datetime
from typing import List, Tuple
import spacy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text

nlp = spacy.load("en_core_web_sm")

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
PROXY_LIST = os.getenv("PROXY_LIST", "").split(",") if os.getenv("PROXY_LIST") else []
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
async def fetch_dark(session, query: str) -> List[Tuple[str, int]]:
    api_key = os.getenv("DARK_WEB_API_KEY")
    if not api_key:
        return []
    url = f"https://darkweb.example.com/search?q={query}&key={api_key}"
    proxy = random.choice(PROXY_LIST) if PROXY_LIST else None
    try:
        async with session.get(url, proxy=proxy) as resp:
            if resp.status != 200:
                return []
            data = await resp.json()
        query_doc = nlp(query)
        posts = []
        for post in data.get("items", []):
            text_raw = post.get("text", "").strip()
            if not text_raw or len(text_raw.split()) < 3:
                continue
            if nlp(text_raw).similarity(query_doc) < 0.5:
                continue
            posts.append((text_raw, int(post.get("likes", 0))))
        return posts
    except Exception as e:
        """Always return [] so demo CSV is used."""
        return []

# ------------------------------------------------------------------
async def load_demo_csv():
    demo_path = pathlib.Path(__file__).with_name("demo_dark.csv")
    if not demo_path.exists():
        return []
    with open(demo_path, newline="", encoding="utf-8") as f:
        return [(row["text"], int(row["likes"])) for row in csv.DictReader(f)]

# ------------------------------------------------------------------
async def store_dark(posts: List[Tuple[str, int]]) -> None:
    if not posts:
        return
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        await session.execute(
            text("""
                INSERT INTO social_data(text, likes, source, timestamp)
                VALUES (:text, :likes, :source, :timestamp)
            """),
            [
                {"text": text, "likes": likes, "source": "dark_web", "timestamp": datetime.utcnow().isoformat()}
                for text, likes in posts
            ]
        )
        await session.commit()

# ------------------------------------------------------------------
async def main(keywords: List[str]) -> None:
    keywords = [k.strip() for k in keywords if k.strip()]
    if not keywords:
        logger.info("No keywords supplied.")
        return
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
        tasks = [fetch_dark(session, kw) for kw in keywords]
        results = await asyncio.gather(*tasks)
    flat = [item for sublist in results for item in sublist]
    if not flat:
        flat = await load_demo_csv()
    await store_dark(flat)
    logger.info("Dark-web scrape complete: %d posts stored", len(flat))

# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        kw_input = input("Dark-web keywords (comma-separated): ")
        asyncio.run(main(kw_input.split(",")))
    except KeyboardInterrupt:
        logger.info("Aborted.")
`


## File: scrapers\demo_affiliate.csv

``$language

title,clicks,timestamp
"Nike Air Max 90",120,"2025-07-30T12:00:00"
"Adidas Ultraboost 22",95,"2025-07-30T12:05:00"
"New Balance 550",80,"2025-07-30T12:10:00"
"Jordan 1 Retro",200,"2025-07-30T12:15:00"
"Puma RS-X",65,"2025-07-30T12:20:00"
"Reebok Club C",50,"2025-07-30T12:25:00"
"Converse Chuck 70",110,"2025-07-30T12:30:00"
"Vans Old Skool",90,"2025-07-30T12:35:00"
"Asics Gel-Kayano",75,"2025-07-30T12:40:00"
"Salomon XT-6",135,"2025-07-30T12:45:00"
`


## File: scrapers\demo_credit.csv

``$language

category,spend_total,timestamp
"Footwear",250.75,"2025-07-30T12:00:00"
"Electronics",499.99,"2025-07-30T12:05:00"
"Apparel",125.50,"2025-07-30T12:10:00"
"Accessories",89.95,"2025-07-30T12:15:00"
"Groceries",67.30,"2025-07-30T12:20:00"
"Home & Garden",310.00,"2025-07-30T12:25:00"
"Beauty",55.25,"2025-07-30T12:30:00"
"Sports",180.00,"2025-07-30T12:35:00"
"Toys",42.10,"2025-07-30T12:40:00"
"Automotive",220.40,"2025-07-30T12:45:00"
`


## File: scrapers\demo_dark.csv

``$language

text,likes
"Limited drop on darknet",88
"Rare sneaker leak confirmed",72
"Underground hype collab",95
"Secret restock tonight",61
"Stealth release discovered",110
"Back-door pair secured",47
"Hidden marketplace link",83
"Off-grid sellers active",69
"Exclusive batch incoming",76
"Unreleased colorway spotted",92
`


## File: scrapers\google_trends.py

``$language

"""
google_trends.py – upgraded with pytrends & static fallback
"""
import asyncio
import aiohttp
import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Tuple
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text

try:
    from pytrends.request import TrendReq
    HAS_PYTRENDS = True
except ImportError:
    HAS_PYTRENDS = False

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
def fetch_trend(keyword: str) -> Tuple[str, int, bool]:
    """
    Use official pytrends if available, else static demo.
    Returns (keyword, score, success_flag).
    """
    if HAS_PYTRENDS:
        try:
            pytrend = TrendReq(hl="en-US", tz=360)
            pytrend.build_payload([keyword], timeframe="today 12-m")
            df = pytrend.interest_over_time()
            score = int(df[keyword].iloc[-1]) if not df.empty else 0
            return keyword, score, True
        except Exception as e:
            logger.error("pytrends failed for %s: %s", keyword, e)
            return keyword, 0, False
    else:
        # static demo fallback
        demo = {"sneakers": 78, "boots": 62, "electronics": 95}
        return keyword, demo.get(keyword.lower(), 50), True

# ------------------------------------------------------------------
async def last_scraped() -> datetime:
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT MAX(timestamp) FROM social_data WHERE source='google_trends'")
        )
        ts = result.scalar()
        return datetime.fromisoformat(ts) if ts else datetime.utcnow() - timedelta(days=7)

# ------------------------------------------------------------------
async def needs_refresh(keyword: str, since: datetime) -> bool:
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT MAX(timestamp) FROM social_data WHERE source='google_trends' AND text=:keyword"),
            {"keyword": keyword}
        )
        ts = result.scalar()
        if not ts:
            return True
        return datetime.fromisoformat(ts) < datetime.utcnow() - timedelta(hours=12)

# ------------------------------------------------------------------
async def store_trends(rows: List[Tuple[str, int]]) -> None:
    engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
    async with AsyncSession(engine) as session:
        await session.execute(
            text("""
                INSERT INTO social_data(text, likes, source, timestamp)
                VALUES (:text, :likes, :source, :timestamp)
            """),
            [
                {"text": kw, "likes": interest, "source": "google_trends", "timestamp": datetime.utcnow().isoformat()}
                for kw, interest in rows
            ]
        )
        await session.commit()

# ------------------------------------------------------------------
async def main(keywords: List[str]) -> None:
    keywords = [k.strip() for k in keywords if k.strip()]
    if not keywords:
        logger.info("No keywords supplied.")
        return

    since = await last_scraped()
    to_fetch = [kw for kw in keywords if await needs_refresh(kw, since)]
    if not to_fetch:
        logger.info("All keywords are fresh (< 12 h). Nothing to fetch.")
        return

    logger.info("Fetching %d keywords: %s", len(to_fetch), to_fetch)
    results = [fetch_trend(kw) for kw in to_fetch]

    new_rows = [(kw, score) for kw, score, ok in results if ok and score > 0]
    if new_rows:
        await store_trends(new_rows)
        logger.info("Stored %d new trend scores.", len(new_rows))
    else:
        logger.info("No new data returned.")

# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        kw_input = input("Keywords (comma-separated): ")
        kw_list = kw_input.split(",")
        asyncio.run(main(kw_list))
    except KeyboardInterrupt:
        logger.info("Aborted.")
`


## File: scrapers\social_media_spider.py

``$language

import scrapy, asyncio, aiohttp, json, os, random, time, logging, pathlib
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

DB_PATH          = os.getenv("DB_PATH", "../data/caeser.db")
PROXY_LIST       = os.getenv("PROXY_LIST", "").split(",") if os.getenv("PROXY_LIST") else []
TWITTER_CREDS    = {
    "bearer": os.getenv("TWITTER_BEARER")
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
class SqlitePipeline:
    async def open_spider(self, spider):
        self.engine = create_async_engine(os.getenv("DB_PATH", "postgresql+asyncpg://postgres:postgres@localhost:5432/caeser"))
        async with AsyncSession(self.engine) as session:
            await session.execute(text("""
                CREATE TABLE IF NOT EXISTS social_data(
                    id SERIAL PRIMARY KEY,
                    text TEXT,
                    likes INTEGER,
                    source TEXT,
                    timestamp TEXT
                )
            """))
            await session.commit()

    async def close_spider(self, spider):
        await self.engine.dispose()

    async def process_item(self, item, spider):
        async with AsyncSession(self.engine) as session:
            await session.execute(
                text("""
                    INSERT INTO social_data(text, likes, source, timestamp)
                    VALUES (:text, :likes, :source, :timestamp)
                """),
                {
                    "text": item["text"],
                    "likes": item["likes"],
                    "source": item["source"],
                    "timestamp": item["timestamp"]
                }
            )
            await session.commit()
        return item

# ------------------------------------------------------------------
class DynamicProxyMiddleware:
    """Rotate proxy per request."""
    def process_request(self, request, spider):
        if PROXY_LIST:
            request.meta["proxy"] = random.choice(PROXY_LIST)
        return None

# ------------------------------------------------------------------
class SocialMediaSpider(scrapy.Spider):
    name = "social_media"
    ua = UserAgent()

    custom_settings = {
        "ITEM_PIPELINES": {"__main__.SqlitePipeline": 1},
        "DOWNLOADER_MIDDLEWARES": {
            "__main__.Retry429Middleware": 550,
            "__main__.AdaptiveBackoffMiddleware": 560
        },
        "DOWNLOAD_DELAY": 1.2,
        "CONCURRENT_REQUESTS": 8,
        "RETRY_TIMES": 3,
    }

    def __init__(
        self,
        sources="",
        target="",
        keywords="",
        locations="",
        gender="",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.sources = [s.strip().lower() for s in sources.split(",") if s.strip()]
        self.target = target.strip()
        self.keywords = [k.strip().lower() for k in keywords.split(",") if k.strip()]
        self.locations = [loc.strip().lower() for loc in locations.split(",") if loc.strip()]
        self.gender = gender.strip().lower()

        cfg_path = pathlib.Path(__file__).with_name("scraper_config.json")
        if cfg_path.exists():
            with open(cfg_path, encoding="utf-8") as f:
                self.cfg = json.load(f)
        else:
            self.cfg = {}

        self.start_urls = []
        for src in self.sources:
            if src in self.cfg:
                self.start_urls.append(self.cfg[src]["url"].format(target=self.target))

    # ------------------------------------------------------------------
    def start_requests(self):
        headers = {"User-Agent": self.ua.random}
        for url in self.start_urls:
            yield Request(url, headers=headers, callback=self.parse, dont_filter=True)

        if "twitter" in self.sources and TWITTER_CREDS["bearer"]:
            query = f"{self.target} {' '.join(self.keywords)} {' '.join(self.locations)}"
            yield Request(
                f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=100",
                headers={"Authorization": f"Bearer {TWITTER_CREDS['bearer']}"},
                callback=self.parse_twitter,
                dont_filter=True,
            )

    # ------------------------------------------------------------------
    def parse(self, response):
        source = "reddit" if "reddit" in response.url else "tiktok" if "tiktok" in response.url else "instagram" if "instagram" in response.url else "ebay" if "ebay" in response.url else "imdb"
        parser_map = {
            "reddit": self._parse_reddit,
            "tiktok": self._parse_tiktok,
            "instagram": self._parse_instagram,
            "ebay": self._parse_ebay,
            "imdb": self._parse_imdb,
        }
        yield from parser_map[source](response)

    # ------------------------------------------------------------------
    def _filter_text(self, text):
        if not text or len(text.split()) < 3:
            return None
        return text

    def _parse_reddit(self, response):
        for post in response.css("div.Post"):
            text = post.css("h3::text").get(default="").strip()
            text = self._filter_text(text)
            if not text:
                continue
            likes = int(post.css("div._1rZYMD_4xY3gRcSS3p8ODO::text").get(default="0").split()[0])
            yield {"text": text, "likes": likes, "source": "reddit", "timestamp": datetime.utcnow().isoformat()}

        next_page = response.css("a[rel='nofollow next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def _parse_tiktok(self, response):
        for video in response.css("div.tiktok-x6y88p-DivItemContainerV2"):
            text = video.css("div.tiktok-1qb12g8-DivThreeColumnContainer p::text").get(default="").strip()
            text = self._filter_text(text)
            if not text:
                continue
            likes_str = video.css("strong.tiktok-1p7xrbz-StrongText::text").get(default="0")
            likes = int(likes_str.replace("K", "000").replace("M", "000000")) if likes_str else 0
            yield {"text": text, "likes": likes, "source": "tiktok", "timestamp": datetime.utcnow().isoformat()}

    def _parse_instagram(self, response):
        for post in response.css("article"):
            text = post.css("div._a9zs span::text").get(default="").strip()
            text = self._filter_text(text)
            if not text:
                continue
            likes = int(post.css("div.Nm9FK span::text").get(default="0").replace(",", ""))
            yield {"text": text, "likes": likes, "source": "instagram", "timestamp": datetime.utcnow().isoformat()}

    def _parse_ebay(self, response):
        for item in response.css("li.s-item"):
            text = item.css("h3.s-item__title::text").get(default="").strip()
            text = self._filter_text(text)
            if not text:
                continue
            price = float(
                item.css("span.s-item__price::text")
                .get(default="0")
                .replace("$", "")
                .replace(",", "")
            )
            yield {"text": text, "likes": int(price), "source": "ebay", "timestamp": datetime.utcnow().isoformat()}

    def _parse_imdb(self, response):
        for movie in response.css("div.lister-item"):
            text = movie.css("h3 a::text").get(default="").strip()
            text = self._filter_text(text)
            if not text:
                continue
            rating = float(movie.css("div.ratings-bar strong::text").get(default="0"))
            yield {"text": text, "likes": int(rating * 10), "source": "imdb", "timestamp": datetime.utcnow().isoformat()}

    def parse_twitter(self, response):
        try:
            data = json.loads(response.text)
            for tweet in data.get("data", []):
                text = self._filter_text(tweet.get("text", ""))
                if not text:
                    continue
                yield {
                    "text": text,
                    "likes": tweet.get("public_metrics", {}).get("like_count", 0),
                    "source": "twitter",
                    "timestamp": datetime.utcnow().isoformat(),
                }
        except json.JSONDecodeError:
            logger.error("Invalid Twitter JSON response")

# ------------------------------------------------------------------
class Retry429Middleware(RetryMiddleware):
    def _retry(self, request, reason, spider):
        response = reason.value.response if hasattr(reason, "value") else None
        if response and response.status == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            spider.logger.info(f"429 received, retrying after {retry_after}s")
            time.sleep(retry_after)
        return super()._retry(request, reason, spider)

# Append right after the existing Retry429Middleware class in social_media_spider.py
class AdaptiveBackoffMiddleware(RetryMiddleware):
    """429/503 aware with exponential back-off and jitter."""
    def __init__(self, settings, *args, **kwargs):
        super().__init__(settings, *args, **kwargs)
        self.backoff_base = self.settings.getfloat("BACKOFF_BASE", 1.0)

    def process_response(self, request, response, spider):
        if response.status in {429, 503}:
            retry_after = int(response.headers.get("Retry-After", 60))
            jitter = random.uniform(0.5, 1.5)
            delay = retry_after * jitter
            spider.logger.info("AdaptiveBackoff: sleeping %.1fs", delay)
            time.sleep(delay)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

# ------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", default="reddit,twitter,tiktok,instagram,ebay,imdb")
    parser.add_argument("--target", required=True)
    parser.add_argument("--keywords", default="")
    parser.add_argument("--locations", default="")
    parser.add_argument("--gender", default="")
    args = parser.parse_args()

    process = CrawlerProcess()
    process.crawl(
        SocialMediaSpider,
        sources=args.sources,
        target=args.target,
        keywords=args.keywords,
        locations=args.locations,
        gender=args.gender,
    )
    process.start()
`


## File: scrapers\__init__.py

``$language

# Autogenerated marker file – keeps dir importable

`


---
## Summary
Total files processed: 63
Completed: 2025-08-01 08:58:42
