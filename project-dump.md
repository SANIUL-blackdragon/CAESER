# Project Dump: D:\LAPTOP\TO_EARN\AI\CAESER
Generated: 2025-07-28 04:47:47
Max File Size: 10MB

---


## File: .env

```$language

# API Keys
QLOO_API_KEY=Ed8qH8iz9GVhxRR2JVkVjVpwcxx1vy_at3TQPxIekkY
OPENROUTER_API_KEY=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
# Database Configuration
DB_PATH=./data/caeser.db

# API Base URL for deployment
API_BASE_URL=http://your-deployment-url.com

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENT=recipient@example.com
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy/zzz

# Google Sheets Configuration
GOOGLE_SHEETS_API_KEY=AIzaSyD-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_SHEETS_CREDENTIALS={"type":"service_account",...} # JSON credentials
SPREADSHEET_ID=your_spreadsheet_id
SALESFORCE_CLIENT_ID=your_client_id
SALESFORCE_CLIENT_SECRET=your_client_secret
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
SALESFORCE_TOKEN=your_security_token
SALESFORCE_INSTANCE_URL=https://your_instance.salesforce.com

# Twitter API Configuration
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
PROXY_LIST=proxy1,proxy2,proxy3
```


## File: alembic.ini

```$language

# A generic, single database configuration.

[alembic]
# path to migration scripts.
# this is typically a path given in POSIX (e.g. forward slashes)
# format, relative to the token %(here)s which refers to the location of this
# ini file
script_location = %(here)s/migrations

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.  for multiple paths, the path separator
# is defined by "path_separator" below.
prepend_sys_path = .


# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python>=3.9 or backports.zoneinfo library and tzdata library.
# Any required deps can installed by adding `alembic[tz]` to the pip requirements
# string value is passed to ZoneInfo()
# leave blank for localtime
# timezone =

# max length of characters to apply to the "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to <script_location>/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "path_separator"
# below.
# version_locations = %(here)s/bar:%(here)s/bat:%(here)s/alembic/versions

# path_separator; This indicates what character is used to split lists of file
# paths, including version_locations and prepend_sys_path within configparser
# files such as alembic.ini.
# The default rendered in new alembic.ini files is "os", which uses os.pathsep
# to provide os-dependent path splitting.
#
# Note that in order to support legacy alembic.ini files, this default does NOT
# take place if path_separator is not present in alembic.ini.  If this
# option is omitted entirely, fallback logic is as follows:
#
# 1. Parsing of the version_locations option falls back to using the legacy
#    "version_path_separator" key, which if absent then falls back to the legacy
#    behavior of splitting on spaces and/or commas.
# 2. Parsing of the prepend_sys_path option falls back to the legacy
#    behavior of splitting on spaces, commas, or colons.
#
# Valid values for path_separator are:
#
# path_separator = :
# path_separator = ;
# path_separator = space
# path_separator = newline
#
# Use os.pathsep. Default configuration used for new projects.
path_separator = os

# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

# database URL.  This is consumed by the user-maintained env.py script only.
# other means of configuring database URLs may be customized within the env.py
# file.
sqlalchemy.url = sqlite:///./data/caeser.db

[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the module runner, against the "ruff" module
# hooks = ruff
# ruff.type = module
# ruff.module = ruff
# ruff.options = check --fix REVISION_SCRIPT_FILENAME

# Alternatively, use the exec runner to execute a binary found on your PATH
# hooks = ruff
# ruff.type = exec
# ruff.executable = ruff
# ruff.options = check --fix REVISION_SCRIPT_FILENAME

# Logging configuration.  This is also consumed by the user-maintained
# env.py script only.
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

```


## File: caeser_visuals.html

```$language

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
```


## File: tree.ps1

```$language

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
```
## TREE

+-- api/
|   +-- controllers/
|   +-- models/
|   +-- routes/
|   +-- services/
|   |   |-- data_quality_service.py
|   |   |-- discord_service.py
|   |   |-- hype_engine.py
|   |   |-- integrations_service.py
|   |   |-- llm_service.py
|   |   |-- qloo_service.py
|   +-- utils/
|   |   |-- logging.py
|   |-- cron.py
|   |-- main.py
+-- bin/
|   +-- sqlite/
|   |   |-- sqldiff.exe
|   |   |-- sqlite3.exe
|   |   |-- sqlite3_analyzer.exe
|   |   |-- sqlite3_rsync.exe
+-- data/
|   +-- processed/
|   +-- raw/
|   +-- schemas/
|   +-- temp/
|   |-- caeser.db
|   |-- init_db.py
+-- docs/
|   +-- img/
|   |   |-- mermaid_diagram_2025207-1.png
|   |   |-- mermaid_diagram_2025207-2.png
|   +-- md/
|   |   |-- architecture.md
|   |   |-- CAESER_MVP_Day1_Day1,5_Plan.markdown
|   |   |-- CAESER_MVP_Day2_Day2,5_Plan.markdown
|   |   |-- CAESER_MVP_Day3_Day3,5_Plan.markdown
|   |   |-- CAESER_MVP_Day4_Day4,5_Plan.markdown
|   |   |-- CAESER_MVP_Day5_Day5_0_Plan.markdown
|   |   |-- CAESER_MVP_Development_Plan.markdown
|   |   |-- Discord_Webhook_Integration.md
|   |   |-- naming-conventions.md
|   |   |-- OPENROUTER_LLM_INTEGRATION.md
|   |   |-- Qloo-Insights-API-Guide.markdown
|   +-- txt/
|   |   |-- draft-main.txt
|   |   |-- draft.txt
|   |   |-- feature_draft.txt
|   |   |-- future-upgrades.md
|   |   |-- mvp-future-upgrades.md
|   |   |-- qloo-draft.txt
|   |   |-- summary-of-alpha_comp.md
+-- frontend/
|   +-- components/
|   +-- public/
|   +-- src/
|   |   |-- main.py
|   |   |-- outcome_form.py
|   +-- styles/
+-- notebooks/
+-- scrapers/
|   |-- affiliate_purchases.py
|   |-- credit_card_spending.py
|   |-- dark_web.py
|   |-- google_trends.py
|   |-- social_media_spider.py
+-- tests/
|-- .env
|-- .gitignore
|-- caeser_visuals.html
|-- eslint.config.mjs
|-- package-lock.json
|-- package.json
|-- project-dump.md
|-- ProjectDumper - Copy.ps1
|-- ProjectDumper.ps1
|-- requirements.txt
|-- tree.ps1


## File: api\cron.py

```$language

import asyncio, requests, sqlite3
from datetime import datetime, timedelta
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def health_check_loop():
    while True:
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
            conn = sqlite3.connect("./data/caeser.db")
            conn.execute("INSERT INTO error_logs(endpoint, error_msg, timestamp) VALUES (?,?,?)",
                         ("/health", "UP" if ok else "DOWN", datetime.utcnow().isoformat()))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            # Log the database error
            logger.error(f"Failed to log health check result in the database: {str(e)}")

        try:
            # Check for prediction drift and send Discord suggestion if necessary
            conn = sqlite3.connect("./data/caeser.db")
            cur = conn.execute("SELECT COUNT(*) FROM predictions WHERE predicted_uplift > 90")
            if cur.fetchone()[0] > 5:
                try:
                    requests.post("https://discord.com/api/webhooks/...", json={
                        "content": "🤖 Consider adding Google Trends to reduce high-score drift."
                    })
                except requests.RequestException as e:
                    logger.error(f"Failed to send Discord alert: {str(e)}")
            conn.close()
        except sqlite3.Error as e:
            logger.error(f"Failed to check prediction drift: {str(e)}")

        # Sleep for 5 minutes before the next health check
        await asyncio.sleep(300)

# Add this to run the health check loop when executed as a module
if __name__ == "__main__":
    print("Starting health monitoring service...")
    print("Press Ctrl+C to stop")
    try:
        asyncio.run(health_check_loop())
    except KeyboardInterrupt:
        print("\nHealth monitoring stopped")
        sys.exit(0)
```


## File: api\main.py

```$language

from api.utils.logging import setup_logging
logger = setup_logging()
from fastapi import FastAPI
from .services import qloo_service, llm_service, discord_service, hype_engine, integrations_service, data_quality_service
import logging
import sqlite3
import os
import pytz
from datetime import datetime
import math
from pydantic import BaseModel
from typing import Optional
import subprocess
import random
from pydantic import BaseModel
import time, traceback, json

# ➜ 1. Added at top with other imports
import time, json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

# Global variable for historical forecasts
historical_forecasts = []

class AnalyzeInput(BaseModel):
    product_name: str
    description: str
    tags: str
    target_area: Optional[str] = None
    locations: Optional[str] = None
    gender: Optional[str] = None
    
class FeedbackIn(BaseModel):
    user_id: str
    product_name: str
    category: str
    feedback_text: str
    sentiment_weight: float = 1.0

class RetrainOut(BaseModel):
    success: bool
    message: str
    new_weights: dict

@app.on_event("startup")
async def startup_event():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create system_events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            timestamp TEXT,
            details TEXT
        )
    """)
    
    # Create predictions and outcomes tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            category TEXT,
            predicted_uplift REAL,
            confidence REAL,
            timestamp TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outcomes (
            prediction_id INTEGER,
            actual_uplift REAL,
            timestamp TEXT,
            FOREIGN KEY(prediction_id) REFERENCES predictions(id)
        )
    """)
    
    # Log startup time in UTC
    utc_time = datetime.now(pytz.utc).isoformat()
    cursor.execute("""
        INSERT INTO system_events (event_type, timestamp)
        VALUES (?, ?)
    """, ("startup", utc_time))
    
    # Load historical forecasts
    cursor.execute("""
        SELECT score, timestamp FROM hype_scores 
        ORDER BY timestamp DESC LIMIT 100
    """)
    global historical_forecasts
    historical_forecasts = cursor.fetchall()
    
    conn.commit()
    conn.close()
    logger.info(f"System started at {utc_time}, loaded {len(historical_forecasts)} historical forecasts")

# ➜ 2. Wrapped all endpoints with logging
@app.post("/analyze")
async def analyze(input: AnalyzeInput):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/analyze", json.dumps(input.dict()), datetime.now(pytz.utc).isoformat()))
    conn.commit()
    conn.close()
    try:
        """Endpoint to trigger analysis pipeline"""
        try:
            # Parse inputs
            keywords = [kw.strip() for kw in input.tags.split(",")]
            locations = [loc.strip() for loc in input.locations.split(",")] if input.locations else []
            gender = input.gender
            
            # Build command for scraping
            cmd = [
                "scrapy", "crawl", "social_media", 
                "-a", f"keywords={','.join(keywords)}"
            ]
            
            if locations:
                cmd.extend(["-a", f"locations={','.join(locations)}"])
            if gender:
                cmd.extend(["-a", f"gender={gender}"])
            
            # Run scraping process
            logger.info(f"Running scraping command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Scraping failed: {result.stderr}")
                return {"success": False, "hype_score": 0.0, "message": f"Scraping failed: {result.stderr}"}
            
            logger.info(f"Scraping completed: {result.stdout}")
            
            # Simulate data processing and analysis (MVP: mock data)
            # In a real implementation, this would call the analysis pipeline
            hype_score = random.uniform(0, 100)  # Mock hype score for MVP
            
            return {
                "success": True, 
                "hype_score": hype_score, 
                "message": "Analysis completed successfully"
            }
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return {
                "success": False, 
                "hype_score": 0.0, 
                "message": f"Analysis failed: {str(e)}"
            }
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/analyze", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/insights/{location}/{category}")
async def get_insights(location: str, category: str, insight_type: str = "brand"):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        (f"/insights/{location}/{category}", json.dumps({"insight_type": insight_type}), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        logger.info(f"Fetching insights for {location}/{category}/{insight_type}")
        return qloo_service.get_cultural_insights(location, category, insight_type)
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            (f"/insights/{location}/{category}", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/llm_data_quality")
async def get_llm_data_quality():
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/llm_data_quality", None, datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        logger.info("Fetching LLM data quality metrics")
        return llm_service.get_llm_data_quality()
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/llm_data_quality", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/data_quality")
async def get_data_quality():
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/data_quality", None, datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        logger.info("Fetching general data quality metrics")
        return data_quality_service.check_data_quality()
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/data_quality", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.post("/predict/demand")
async def predict_demand(data: dict):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/predict/demand", json.dumps(data), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        product = data.get("product")
        insights = data.get("insights")
        logger.info(f"Generating prediction for product: {product.get('name', 'Unknown')}")
        prediction = llm_service.get_prediction(product, insights)
        
        # Save prediction to database
        if prediction and prediction.get("success"):
            prediction_data = prediction["data"]
            predicted_uplift = prediction_data.get("uplift", 0.0)
            confidence = prediction_data.get("confidence", 0.5)
            timestamp = datetime.now(pytz.utc).isoformat()
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO predictions (product_name, category, predicted_uplift, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (product["name"], product["category"], predicted_uplift, confidence, timestamp))
            conn.commit()
            conn.close()
            logger.info(f"Saved prediction for {product['name']} to database")
        
        return prediction
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/predict/demand", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.post("/hype/score")
async def calculate_hype_score(data: dict):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/hype/score", json.dumps(data), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        insights = data.get("insights")
        category = data.get("category")
        location = data.get("location")
        threshold = data.get("threshold", 20.0)
        logger.info("Calculating hype score")
        return hype_engine.calculate_hype_score(insights, category, location, threshold)
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/hype/score", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.post("/discord/alert")
async def send_discord_alert(data: dict):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/discord/alert", json.dumps(data), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        prediction = data.get("prediction")
        hype_data = data.get("hype_data")
        logger.info(f"Sending Discord alert for {prediction.get('product', {}).get('name', 'Unknown')}")
        return discord_service.send_alert(prediction, hype_data)
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/discord/alert", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.post("/integrations/send")
async def send_integrations(data: dict):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/integrations/send", json.dumps(data), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        prediction = data.get("prediction")
        hype_data = data.get("hype_data")
        logger.info(f"Sending data to integrations for {prediction.get('product', {}).get('name', 'Unknown')}")
        return integrations_service.send_integrations(prediction, hype_data)
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/integrations/send", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/hype/history/{location}/{category}")
async def get_hype_history(location: str, category: str):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        (f"/hype/history/{location}/{category}", None, datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT score, created_at FROM hype_scores 
                WHERE category = ? AND location = ?
                ORDER BY created_at ASC
            """, (category, location))
            rows = cursor.fetchall()
            conn.close()
            return {"success": True, "data": [{"score": row[0], "timestamp": row[1]} for row in rows], "message": "History retrieved"}
        except Exception as e:
            logger.error(f"Failed to retrieve hype history: {str(e)}")
            return {"success": False, "data": [], "message": f"Failed to retrieve hype history: {str(e)}"}
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            (f"/hype/history/{location}/{category}", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.post("/submit_outcome")
async def submit_outcome(data: dict):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/submit_outcome", json.dumps(data), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        prediction_id = data.get("prediction_id")
        actual_uplift = data.get("actual_uplift")

        # Validate prediction_id and actual_uplift
        if not prediction_id or not isinstance(prediction_id, int) or prediction_id <= 0:
            return {"success": False, "message": "Invalid prediction_id. It must be a positive integer."}
        
        if actual_uplift is None or not isinstance(actual_uplift, (int, float)):
            return {"success": False, "message": "Invalid actual_uplift. It must be a number."}

        timestamp = datetime.now(pytz.utc).isoformat()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if the prediction_id exists in the predictions table
        cursor.execute("SELECT COUNT(*) FROM predictions WHERE id = ?", (prediction_id,))
        if cursor.fetchone()[0] == 0:
            conn.close()
            return {"success": False, "message": f"No prediction found with ID {prediction_id}"}

        cursor.execute("""
            INSERT INTO outcomes (prediction_id, actual_uplift, timestamp)
            VALUES (?, ?, ?)
        """, (prediction_id, actual_uplift, timestamp))
        conn.commit()
        conn.close()
        logger.info(f"Submitted outcome for prediction ID {prediction_id}")
        return {"success": True, "message": "Outcome submitted successfully"}
    except Exception as e:
        logger.error(f"Failed to submit outcome: {str(e)}")
        return {"success": False, "message": f"Failed to submit outcome: {str(e)}"}
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/submit_outcome", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/calculate_loss")
async def calculate_loss(threshold: float = 80.0):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/calculate_loss", json.dumps({"threshold": threshold}), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.predicted_uplift, p.confidence, o.actual_uplift
                FROM predictions p
                JOIN outcomes o ON p.id = o.prediction_id
                ORDER BY p.timestamp DESC LIMIT 10
            """)
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                return {"success": False, "message": "No predictions with outcomes available"}
            
            losses = []
            for row in rows:
                predicted_class = 1 if row[1] >= threshold else 0  # predicted_uplift >= threshold%
                actual_class = 1 if row[3] >= threshold else 0     # actual_uplift >= threshold%
                p_i = row[2] if predicted_class == 1 else 1 - row[2]  # confidence for predicted class
                
                # Calculate cross-entropy loss
                if actual_class == 1:
                    loss = -math.log(p_i) if p_i > 0 else float('inf')
                else:
                    loss = -math.log(1 - p_i) if p_i < 1 else float('inf')
                losses.append(loss)
            
            average_loss = sum(losses) / len(losses)
            logger.info(f"Calculated average loss: {average_loss:.4f}")
            return {"success": True, "average_loss": average_loss, "message": "Loss calculated successfully"}
        
        except Exception as e:
            logger.error(f"Failed to calculate loss: {str(e)}")
            return {"success": False, "message": f"Failed to calculate loss: {str(e)}"}
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/calculate_loss", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

# ➜ 3. Replaced existing /feedback endpoint
@app.post("/feedback")
async def feedback_endpoint(body: FeedbackIn):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO feedback_log
           (user_id, product_name, category, feedback_text, sentiment_weight, timestamp)
           VALUES (?,?,?,?,?,?)""",
        (body.user_id, body.product_name, body.category,
         body.feedback_text, body.sentiment_weight,
         datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    await retrain_endpoint()          # auto-trigger
    return {"success": True, "message": "Feedback stored & model retrained"}

@app.post("/retrain")
async def retrain_endpoint():
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/retrain", None, datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h.sentiment, o.actual_uplift
            FROM hype_scores h
            JOIN outcomes o ON o.prediction_id = h.id
            ORDER BY h.created_at DESC LIMIT 100
        """)
        rows = cursor.fetchall()
        if not rows:
            conn.close()
            return {"success": False, "message": "Need ≥1 outcome to retrain"}
        sentiments = [r[0] for r in rows]
        actuals = [r[1] for r in rows]
        new_weight = sum(actuals) / (sum(sentiments) + 1e-9)
        cursor.execute("INSERT OR REPLACE INTO model_weights(key,value) VALUES('sentiment_weight',?)", (new_weight,))
        conn.commit()
        conn.close()
        return RetrainOut(success=True, message="Weights updated", new_weights={"sentiment_weight": new_weight})
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/retrain", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/runtime_estimates")
async def runtime_estimates():
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/runtime_estimates", None, datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(duration_ms) FROM api_calls ORDER BY id DESC LIMIT 50")
        avg = cursor.fetchone()[0] or 0
        conn.close()
        return {"average_duration_ms": avg, "estimate": f"≈ {avg/1000:.1f}s"}
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/runtime_estimates", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/error_logs")
async def error_logs(limit: int = 50):
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/error_logs", json.dumps({"limit": limit}), datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM error_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
        logs = cursor.fetchall()
        conn.close()
        return {"logs": [dict(row) for row in logs]}
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/error_logs", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

@app.get("/health")
async def health_check():
    start = time.time()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO request_state(endpoint, payload, ts) VALUES (?,?,?)",
        ("/health", None, datetime.now(pytz.utc).isoformat())
    )
    conn.commit()
    conn.close()
    try:
        logger.info("Health check endpoint called")
        return {"status": "ok"}
    finally:
        dur = (time.time() - start) * 1000
        sqlite3.connect(DB_PATH).execute(
            "INSERT INTO api_calls(endpoint, duration_ms, timestamp) VALUES (?,?,?)",
            ("/health", dur, datetime.now(pytz.utc).isoformat())
        ).commit()

# 🔚 5. Appended new endpoints at bottom
@app.get("/export_model")
async def export_model():
    return {"script": "def score(hype, sent): return hype*sentiment_weight + sent*popularity_weight"}

@app.post("/custom_score")
async def custom_score(py_code: str):
    exec(py_code, globals())   # ⚠️ naive — sandbox later
    return {"success": True, "message": "Custom scorer uploaded"}

@app.get("/backtest")
async def backtest():
    return {"mock_2023_campaign": {"predicted": 15, "actual": 12, "error": 3}}

@app.get("/competitors")
async def competitors():
    return {"nike": {"hype": 78}, "adidas": {"hype": 65}} ##This is example, use the dynamic data that has been used till now

logger.info('API initialized successfully')
```


## File: api\services\data_quality_service.py

```$language

import sqlite3
import os
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

def log_data_quality(metric: str, value: float, source: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO data_quality (metric, value, source, timestamp)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    """, (metric, value, source))
    conn.commit()
    conn.close()
    logger.info(f"Logged data quality: {metric} = {value} for {source}")

def check_data_quality():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    metrics = {}
    
    # Check missing values in social_data
    cursor.execute("SELECT COUNT(*) FROM social_data WHERE text IS NULL OR text = ''")
    missing_values = cursor.fetchone()[0]
    metrics['missing_values'] = {'value': missing_values, 'source': 'social_data'}
    log_data_quality('missing_values', missing_values, 'social_data')
    
    # Check feed freshness
    cursor.execute("SELECT MAX(timestamp) FROM social_data")
    latest_timestamp = cursor.fetchone()[0]
    freshness = 0 if not latest_timestamp else (datetime.now() - datetime.fromisoformat(latest_timestamp)).total_seconds() / 3600
    metrics['freshness'] = {'value': freshness, 'source': 'social_data'}
    log_data_quality('freshness', freshness, 'social_data')
    
    # Check API errors (from llm_data_quality for now)
    cursor.execute("SELECT COUNT(*) FROM llm_data_quality WHERE metric = 'errors' AND value = 1.0")
    api_errors = cursor.fetchone()[0]
    metrics['api_errors'] = {'value': api_errors, 'source': 'llm_service'}
    log_data_quality('api_errors', api_errors, 'llm_service')
    
    conn.close()
    return {
        "success": True,
        "data": metrics,
        "message": "Data quality metrics retrieved"
    }
```


## File: api\services\discord_service.py

```$language

import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import logging
import sqlite3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = os.getenv("EMAIL_PORT", 587)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

def is_product_marked(product_name, category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM marked_products 
        WHERE product_name = ? AND category = ?
    """, (product_name, category))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def send_discord_alert(prediction, hype_data):
    if not DISCORD_WEBHOOK_URL:
        logger.error("DISCORD_WEBHOOK_URL not configured")
        return {"success": False, "message": "DISCORD_WEBHOOK_URL not configured"}
    
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')
    
    if not is_product_marked(product_name, category):
        logger.info(f"Product {product_name} not marked, skipping Discord alert")
        return {"success": True, "message": "Product not marked, alert skipped"}
    
    embed = {
        "title": f"New Prediction for {product_name}",
        "description": (
            f"**Category**: {category}\n"
            f"**Uplift**: {prediction['uplift']:.2f}%\n"
            f"**Confidence**: {prediction['confidence']:.2f}\n"
            f"**Strategy**: {prediction['strategy']}\n"
            f"**Hype Score**: {hype_data['averageScore']:.2f}\n"
            f"**Hourly Sentiment Change**: {hype_data['hourly_sentiment_change']:.2f}%"
        ),
        "color": 0x667eea if not hype_data.get("change_detected") else 0xff0000,
        "footer": {"text": "CÆSER System"}
    }
    
    if hype_data.get("change_detected", False):
        embed["description"] += f"\n**Alert**: Hype score changed by {hype_data['change_percent']:.2f}%!"
    
    payload = {"embeds": [embed]}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        return {"success": True, "message": "Discord alert sent successfully"}
    except requests.RequestException as e:
        logger.error(f"Failed to send Discord alert: {str(e)}")
        return {"success": False, "message": f"Failed to send Discord alert: {str(e)}"}

def send_email_alert(prediction, hype_data):
    if not all([EMAIL_HOST, EMAIL_USER, EMAIL_PASSWORD, EMAIL_RECIPIENT]):
        logger.error("Email configuration missing")
        return {"success": False, "message": "Email configuration missing"}
    
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')
    
    if not is_product_marked(product_name, category):
        logger.info(f"Product {product_name} not marked, skipping email alert")
        return {"success": True, "message": "Product not marked, alert skipped"}
    
    subject = f"CÆSER Alert: {product_name}"
    body = (
        f"Category: {category}\n"
        f"Demand Uplift: {prediction['uplift']:.2f}%\n"
        f"Confidence: {prediction['confidence']:.2f}\n"
        f"Strategy: {prediction['strategy']}\n"
        f"Hype Score: {hype_data['averageScore']:.2f}\n"
        f"Hourly Sentiment Change: {hype_data['hourly_sentiment_change']:.2f}%"
    )
    if hype_data.get("change_detected", False):
        body += f"\nAlert: Hype score changed by {hype_data['change_percent']:.2f}%!"
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_RECIPIENT
    
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        logger.info("Email alert sent successfully")
        return {"success": True, "message": "Email alert sent successfully"}
    except Exception as e:
        logger.error(f"Failed to send email alert: {str(e)}")
        return {"success": False, "message": f"Failed to send email alert: {str(e)}"}

def send_slack_alert(prediction, hype_data):
    if not SLACK_WEBHOOK_URL:
        logger.error("SLACK_WEBHOOK_URL not configured")
        return {"success": False, "message": "SLACK_WEBHOOK_URL not configured"}
    
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')
    
    if not is_product_marked(product_name, category):
        logger.info(f"Product {product_name} not marked, skipping Slack alert")
        return {"success": True, "message": "Product not marked, alert skipped"}
    
    text = (
        f"*New Prediction for {product_name}*\n"
        f"Category: {category}\n"
        f"Demand Uplift: {prediction['uplift']:.2f}%\n"
        f"Confidence: {prediction['confidence']:.2f}\n"
        f"Strategy: {prediction['strategy']}\n"
        f"Hype Score: {hype_data['averageScore']:.2f}\n"
        f"Hourly Sentiment Change: {hype_data['hourly_sentiment_change']:.2f}%"
    )
    if hype_data.get("change_detected", False):
        text += f"\n*Alert*: Hype score changed by {hype_data['change_percent']:.2f}%!"
    
    payload = {"text": text}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        return {"success": True, "message": "Slack alert sent successfully"}
    except requests.RequestException as e:
        logger.error(f"Failed to send Slack alert: {str(e)}")
        return {"success": False, "message": f"Failed to send Slack alert: {str(e)}"}

def send_alert(prediction, hype_data):
    results = [
        send_discord_alert(prediction, hype_data),
        send_email_alert(prediction, hype_data),
        send_slack_alert(prediction, hype_data)
    ]
    successes = [r["success"] for r in results]
    messages = [r["message"] for r in results]
    return {"success": any(successes), "message": "; ".join(messages)}
```


## File: api\services\hype_engine.py

```$language

import random
from typing import Dict
import logging
import re
from collections import defaultdict
# Enhanced emoji mapping with fallback
EMOJI_MAP = defaultdict(lambda: 0.0, {
    "😊": 0.8, "😢": -0.8, "😍": 0.9, "😠": -0.9, "😐": 0.0,
    "👍": 0.7, "👎": -0.7, "🔥": 0.85, "💯": 0.9, "👀": 0.3
})
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
import sqlite3
import os
from textblob import TextBlob
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

category_keywords = {
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

def save_hype_score(score: float, category: str, location: str, sentiment: float, product_name: str = None) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO hype_scores (score, category, location, sentiment, product_name, created_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (score, category, location, sentiment, product_name))
    conn.commit()
    conn.close()

def get_previous_hype_score(category: str, location: str, product_name: str = None) -> tuple:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT score, sentiment FROM hype_scores 
        WHERE category = ? AND location = ?
    """
    params = [category, location]
    if product_name:
        query += " AND product_name = ?"
        params.append(product_name)
    query += " ORDER BY created_at DESC LIMIT 1 OFFSET 1"
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None)

def get_hourly_sentiment_change(category: str, location: str, product_name: str = None) -> float:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
        SELECT sentiment, created_at FROM hype_scores 
        WHERE category = ? AND location = ? AND created_at > ?
    """
    params = [category, location, (datetime.now() - timedelta(hours=1)).isoformat()]
    if product_name:
        query += " AND product_name = ?"
        params.append(product_name)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    if len(rows) < 2:
        return 0.0
    latest_sentiment, prev_sentiment = rows[-1][0], rows[0][0]
    return ((latest_sentiment - prev_sentiment) / prev_sentiment * 100) if prev_sentiment != 0 else 0.0

def get_social_data(category: str, days: int = 7) -> list:
    keywords = category_keywords.get(category.lower(), [category])
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = f"""
        SELECT text 
        FROM social_data 
        WHERE ({' OR '.join(['text LIKE ?' for _ in keywords])})
        AND timestamp > datetime('now', '-{days} days')
    """
    cursor.execute(query, tuple(f"%{kw}%" for kw in keywords))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def emoji_to_sentiment(text: str) -> float:
    scores = [EMOJI_MAP[ch] for ch in text if ch in EMOJI_MAP]
    return sum(scores) / (len(scores) or 1)

def scrub_pii(text: str) -> str:
    return EMAIL_REGEX.sub('', text)

def calculate_hype_score(insights: Dict, category: str, location: str, threshold: float = 20.0, product_name: str = None) -> Dict:
    validate_insights(insights)
    
    try:
        entities = insights["data"].get("entities", [])
        popularity = sum(entity["properties"].get("popularity", 0.5) for entity in entities) / len(entities) if entities else 0.5
        trend_factor = insights["data"].get("trend", 1.0)
        base_score = popularity * 100 * trend_factor
        
        # Use real data or a sophisticated model instead of random noise
        # For example, we can use historical data to simulate the noise
        # Here, we assume we have a function `get_historical_noise` that returns noise based on historical data
        historical_noise = get_historical_noise(category, location, product_name)
        hype_score = max(0.0, min(100.0, base_score + historical_noise))
        
        social_texts = get_social_data(category)
        if social_texts:
            sentiment_score = sum(
                TextBlob(scrub_pii(text)).sentiment.polarity + emoji_to_sentiment(text)
                for text in social_texts
            ) / len(social_texts) if social_texts else 0.0
            logger.info(f"Analyzed {len(social_texts)} social posts for sentiment")
        else:
            sentiment_score = 0.0
            logger.warning("No social data found for sentiment analysis")
        
        # Apply sentiment adjustment
        hype_score = min(100.0, hype_score * (1 + sentiment_score * 0.2))
        
        # Enhanced scoring components
        cultural_bonus = sum(1 for k in CULTURAL_KEYWORDS if k in " ".join(social_texts).lower()) * 2
        psychographic = PSYCHO_VEC["enthusiasm"](sentiment_score)
        hype_score = min(100.0, hype_score + cultural_bonus + psychographic)
        
        # Calculate additional metrics
        scenario = {"price_drop": min(100.0, hype_score * 1.05)}
        cycle_phase = "growth" if hype_score > 50 else "decline"
        confidence_weight = min(1.0, (entities[0]["properties"].get("confidence", 0.5) if entities else 0.5) * 0.8 + 0.2)
        
        previous_score, previous_sentiment = get_previous_hype_score(category, location, product_name)
        save_hype_score(hype_score, category, location, sentiment_score, product_name)
        
        change_detected = False
        change_percent = 0.0
        if previous_score is not None:
            change_percent = ((hype_score - previous_score) / previous_score) * 100
            change_detected = abs(change_percent) > threshold
        
        hourly_sentiment_change = get_hourly_sentiment_change(category, location, product_name)
        
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

def get_historical_noise(category: str, location: str, product_name: str = None) -> float:
    """
    Fetch historical noise data based on category, location, and product name.
    This function should be implemented to fetch real historical data.
    For now, it returns a placeholder value.
    """
    # Placeholder implementation
    # In a real scenario, this function would fetch historical data and compute the noise
    return 0.0  # Replace with actual historical noise calculation
```


## File: api\services\integrations_service.py

```$language

import os
import requests
import logging
import sqlite3
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SALESFORCE_CLIENT_ID = os.getenv("SALESFORCE_CLIENT_ID")
SALESFORCE_CLIENT_SECRET = os.getenv("SALESFORCE_CLIENT_SECRET")
SALESFORCE_USERNAME = os.getenv("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD = os.getenv("SALESFORCE_PASSWORD")
SALESFORCE_TOKEN = os.getenv("SALESFORCE_TOKEN")
SALESFORCE_INSTANCE_URL = os.getenv("SALESFORCE_INSTANCE_URL")

DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

def get_google_sheets_service():
    try:
        creds = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))
        service = build('sheets', 'v4', credentials=creds)
        logger.info("Google Sheets service initialized successfully")
        return service
    except Exception as e:
        logger.error(f"Failed to initialize Google Sheets service: {str(e)}")
        return None

def append_to_google_sheets(prediction, hype_data):
    if not GOOGLE_SHEETS_CREDENTIALS or not SPREADSHEET_ID:
        logger.error("Google Sheets configuration missing")
        return {"success": False, "message": "Google Sheets configuration missing"}
    
    service = get_google_sheets_service()
    if not service:
        return {"success": False, "message": "Failed to initialize Google Sheets service"}
    
    values = [
        [
            prediction['product'].get('name', 'Unknown'),
            prediction['product'].get('category', 'Unknown'),
            prediction.get('uplift', 0.0),
            prediction.get('confidence', 0.0),
            prediction.get('strategy', 'Unknown'),
            hype_data.get('averageScore', 0.0),
            hype_data.get('change_percent', 0.0) if hype_data.get('change_detected') else 0.0
        ]
    ]
    
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

def get_salesforce_access_token():
    if not all([SALESFORCE_CLIENT_ID, SALESFORCE_CLIENT_SECRET, SALESFORCE_USERNAME, SALESFORCE_PASSWORD, SALESFORCE_TOKEN, SALESFORCE_INSTANCE_URL]):
        logger.error("Salesforce configuration missing")
        return None
    
    auth_url = f"{SALESFORCE_INSTANCE_URL}/services/oauth2/token"
    payload = {
        'grant_type': 'password',
        'client_id': SALESFORCE_CLIENT_ID,
        'client_secret': SALESFORCE_CLIENT_SECRET,
        'username': SALESFORCE_USERNAME,
        'password': SALESFORCE_PASSWORD + SALESFORCE_TOKEN
    }
    try:
        response = requests.post(auth_url, data=payload, timeout=5)
        response.raise_for_status()
        access_token = response.json().get('access_token')
        if not access_token:
            logger.error("Failed to get Salesforce access token: No access token in response")
            return None
        logger.info("Salesforce access token obtained successfully")
        return access_token
    except requests.RequestException as e:
        logger.error(f"Failed to get Salesforce access token: {str(e)}")
        return None

def create_salesforce_record(prediction, hype_data):
    access_token = get_salesforce_access_token()
    if not access_token:
        return {"success": False, "message": "Failed to get Salesforce access token"}
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'Name': prediction['product'].get('name', 'Unknown Product'),
        'Category__c': prediction['product'].get('category', 'Unknown'),
        'Demand_Uplift__c': prediction.get('uplift', 0.0),
        'Confidence__c': prediction.get('confidence', 0.0),
        'Strategy__c': prediction.get('strategy', 'Unknown'),
        'Hype_Score__c': hype_data.get('averageScore', 0.0),
        'Hype_Change_Percent__c': hype_data.get('change_percent', 0.0) if hype_data.get('change_detected') else 0.0
    }
    try:
        response = requests.post(
            f"{SALESFORCE_INSTANCE_URL}/services/data/v52.0/sobjects/Opportunity",
            headers=headers,
            json=data,
            timeout=5
        )
        response.raise_for_status()
        logger.info("Salesforce record created successfully")
        return {"success": True, "message": "Salesforce record created successfully"}
    except requests.RequestException as e:
        logger.error(f"Failed to create Salesforce record: {str(e)}")
        return {"success": False, "message": f"Failed to create Salesforce record: {str(e)}"}

def send_integrations(prediction, hype_data):
    results = [
        append_to_google_sheets(prediction, hype_data),
        create_salesforce_record(prediction, hype_data)
    ]
    successes = [r["success"] for r in results]
    messages = [r["message"] for r in results]
    return {"success": any(successes), "message": "; ".join(messages)}
```


## File: api\services\llm_service.py

```$language

import os
import sqlite3
from openai import OpenAI
from retrying import retry
import logging
import json
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL = "https://caeser.example.com"
SITE_NAME = "CÆSER"
DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

def sanitize_input(input_data):
    if isinstance(input_data, str):
        return input_data.strip().replace(r'[^\w\s,.-]', '')
    return input_data

def log_llm_data_quality(metric: str, value: float):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO llm_data_quality (metric, value, timestamp)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    """, (metric, value))
    conn.commit()
    conn.close()
    logger.info(f"Logged LLM data quality: {metric} = {value}")

@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=5000)
def get_prediction(product, insights):
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY not configured")
        raise ValueError("OPENROUTER_API_KEY not configured")
    
    if not isinstance(product, dict) or not all(key in product for key in ["name", "category", "description"]):
        logger.error("Invalid product data: must include name, category, description")
        raise ValueError("Invalid product data")
    if not isinstance(insights, dict) or not insights.get("data"):
        logger.error("Invalid insights data")
        raise ValueError("Invalid insights data")
    
    product_name = sanitize_input(product["name"])
    product_category = sanitize_input(product["category"])
    product_description = sanitize_input(product["description"])
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    prompt = f"""
    Analyze the following product and cultural insights to predict demand uplift and suggest a marketing strategy.
    Product: {product_name} ({product_category})
    Description: {product_description}
    Cultural Insights: {insights['data']}
    Provide a response in JSON format with 'uplift' (percentage, float), 'strategy' (string), 'confidence' (float between 0 and 1), and 'trend' (list of dicts with 'time' and 'demand').
    """
    
    try:
        start_time = time.time()
        logger.info(f"Generating prediction for {product_name}")
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}]
        )
        result = completion.choices[0].message.content.strip()
        parsed_result = json.loads(result)
        if not all(key in parsed_result for key in ["uplift", "strategy", "confidence", "trend"]):
            logger.error("Invalid LLM response format")
            raise ValueError("Invalid LLM response format")
        
        # Log data quality metrics
        confidence = parsed_result.get("confidence", 0.0)
        response_time = time.time() - start_time
        log_llm_data_quality("confidence", confidence)
        log_llm_data_quality("response_time", response_time)
        
        logger.info(f"Prediction generated successfully for {product_name}")
        parsed_result["cpc"] = 1.0   # TikTok mock CPC ($1)
        parsed_result["cpm"] = 5.0   # TikTok mock CPM ($5)
        return {"success": True, "data": parsed_result, "message": "Prediction generated successfully"}
    except Exception as e:
        log_llm_data_quality("errors", 1.0)  # Log error occurrence
        logger.error(f"LLM request failed: {str(e)}")
        return {"success": False, "data": None, "message": f"LLM request failed: {str(e)}"}

def get_llm_data_quality():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT metric, AVG(value) as avg_value, COUNT(*) as count
        FROM llm_data_quality
        GROUP BY metric
    """)
    rows = cursor.fetchall()
    conn.close()
    metrics = {row[0]: {"avg_value": row[1], "count": row[2]} for row in rows}
    return {
        "success": True,
        "data": metrics,
        "message": "LLM data quality metrics retrieved"
    }
```


## File: api\services\qloo_service.py

```$language

import os
import requests
import logging
from retrying import retry
from cachetools import TTLCache
from typing import Dict, Optional

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize cache (TTL of 1 hour)
cache = TTLCache(maxsize=100, ttl=3600)

QLOO_API_KEY = os.getenv("QLOO_API_KEY")
BASE_URL = "https://hackathon.api.qloo.com/v2/insights"

def sanitize_input(input_str: str) -> str:
    return input_str.strip().replace(r"[^a-zA-Z0-9\s,.-]", "")

@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=5000)
def get_cultural_insights(location: str, category: str, insight_type: str = "brand") -> Dict:
    """Fetch cultural insights from Qloo API for a given location and category.
    
    Args:
        location (str): Geographic location (e.g., 'New York, NY').
        category (str): Product category (e.g., 'sneakers').
        insight_type (str): Type of insight ('brand', 'demographics', 'heatmap'). Defaults to 'brand'.
    
    Returns:
        Dict: Response with success status, data, and message.
              Example: {
                  "success": bool,
                  "data": {...},
                  "message": str
              }
    
    Raises:
        ValueError: If API key or inputs are invalid.
        requests.RequestException: If API call fails after retries.
    """
    if not QLOO_API_KEY:
        logger.error("QLOO_API_KEY not configured")
        raise ValueError("QLOO_API_KEY not configured")
    if not location or not isinstance(location, str) or not location.strip():
        logger.error("Invalid location provided")
        raise ValueError("Invalid location")
    if not category or not isinstance(category, str) or not category.strip():
        logger.error("Invalid category provided")
        raise ValueError("Invalid category")
    
    location = sanitize_input(location)
    category = sanitize_input(category)
    
    # Check cache
    cache_key = f"{insight_type}:{location}:{category}"
    if cache_key in cache:
        logger.info(f"Returning cached insights for {cache_key}")
        return cache[cache_key]
    
    headers = {
        "X-Api-Key": QLOO_API_KEY,
        "Content-Type": "application/json"
    }
    
    params = {}
    if insight_type == "brand":
        params = {
            "filter.type": "urn:entity:brand",
            "signal.location.query": location,
            "filter.tags": f"urn:tag:keyword:brand:{category.lower()}"
        }
    elif insight_type == "demographics":
        params = {
            "filter.type": "urn:demographics",
            "signal.location.query": location,
            "signal.interests.tags": f"urn:tag:keyword:brand:{category.lower()}"
        }
    elif insight_type == "heatmap":
        params = {
            "filter.type": "urn:heatmap",
            "filter.location.query": location,
            "signal.interests.tags": f"urn:tag:keyword:brand:{category.lower()}"
        }
    else:
        logger.error(f"Unsupported insight type: {insight_type}")
        raise ValueError(f"Unsupported insight type: {insight_type}")
    
    try:
        logger.info(f"Fetching {insight_type} insights for {location}/{category}")
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data.get("success"):
            logger.error(f"Invalid API response: {data.get('message', 'Unknown error')}")
            raise ValueError(f"Invalid API response: {data.get('message', 'Unknown error')}")
        
        result = {"success": True, "data": data["results"], "message": f"{insight_type.capitalize()} insights retrieved successfully"}
        cache[cache_key] = result
        logger.info(f"Cached insights for {cache_key}")
        return result
    except requests.RequestException as e:
        logger.error(f"Qloo API request failed: {str(e)}")
        return {"success": False, "data": None, "message": f"Qloo API request failed: {str(e)}"}
```


## File: api\utils\logging.py

```$language

import logging
from logging.handlers import RotatingFileHandler

def setup_logging(name: str = __name__, level: int = logging.INFO, log_file: str = None) -> logging.Logger:
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
```

## File: data\init_db.py

```$language

from alembic import config

def init_db():
    alembic_cfg = config.Config("alembic.ini")
    alembic.command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    init_db()
```


## File: frontend\src\main.py

```$language

import streamlit as st
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
import openpyxl
from io import BytesIO
import logging
from api.utils.logging import setup_logging
import sqlite3
import os
import sys
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Add scrapers directory to path for Google Trends import
sys.path.append('../scrapers')
from google_trends import get_google_trends, store_trend

logger = setup_logging()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")
st.set_page_config(page_title="CÆSER Dashboard", layout="wide")

st.markdown("""
    <style>
        .market-selector__dropdown { margin-bottom: 1rem; }
        .insight-visualizer__chart { max-width: 100%; }
        .prediction-dashboard__container { padding: 1rem; background-color: #f9f9f9; border-radius: 8px; }
        .product-keywords__input { width: 100%; }
        .product-description__textarea { width: 100%; min-height: 100px; }
        .data-quality__widget { background-color: #f0f0f0; padding: 1rem; border-radius: 8px; }
        .tabs-container { margin-top: 2rem; }
        @media (max-width: 768px) {
            .market-selector__dropdown { font-size: 14px; }
            .insight-visualizer__chart { height: 300px; }
        }
        :root {
            --primary-color: #667eea;
            --text-color: #333;
        }
        .stButton>button { background-color: var(--primary-color); color: white; }
    </style>
""", unsafe_allow_html=True)

def init_store_table():
    """Initialize the store_data table if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS store_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            sales REAL,
            date TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def user_provided_store_data():
    """Widget for uploading store data via CSV"""
    st.subheader("Upload Store Data")
    uploaded_file = st.file_uploader("Choose a CSV file (product, sales, date)", type="csv")
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            if not all(col in df.columns for col in ['product', 'sales', 'date']):
                st.error("CSV must contain columns: product, sales, date")
                return
                
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO store_data (product, sales, date, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (row['product'], row['sales'], row['date'], datetime.now().isoformat()))
                
            conn.commit()
            conn.close()
            st.success(f"Successfully uploaded {len(df)} store records")
            
            # Display uploaded data
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def fetch_and_display_trends():
    """Widget for Google Trends search"""
    st.subheader("Google Trends Search")
    keywords_input = st.text_input("Enter keywords (comma-separated, e.g., sneakers, boots):")
    
    if st.button("Fetch Trends"):
        if not keywords_input:
            st.error("Please enter at least one keyword")
            return
            
        keywords = [kw.strip() for kw in keywords_input.split(",")]
        with st.spinner("Fetching Google Trends data..."):
            try:
                trends = get_google_trends(keywords)
                if not trends:
                    st.warning("No trends data found")
                    return
                    
                # Store trends in database
                for keyword, interest in trends.items():
                    store_trend(keyword, interest)
                
                st.success("Trends fetched and stored successfully")
                
                # Display trends data
                trends_df = pd.DataFrame({
                    "Keyword": list(trends.keys()),
                    "Interest": list(trends.values()),
                    "Source": "google_trends",
                    "Timestamp": datetime.now().isoformat()
                })
                st.dataframe(trends_df)
                
            except Exception as e:
                st.error(f"Error fetching trends: {str(e)}")

def market_selector():
    st.subheader("Select Market and Category")
    col1, col2, col3 = st.columns(3)
    with col1:
        location = st.selectbox("Location", ["New York, NY", "London", "Tokyo"], key="location")
    with col2:
        category = st.selectbox("Category", ["sneakers", "electronics", "fashion"], key="category")
    with col3:
        threshold = st.number_input("Hype Change Threshold (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0)
    insight_type = st.selectbox("Insight Type", ["brand", "demographics", "heatmap"], key="insight_type")
    return location, category, insight_type, threshold

def product_keywords():
    st.subheader("Product Keywords")
    keywords = st.text_input("Enter keywords (comma-separated)", help="e.g., sneakers, streetwear")
    return [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []

def product_description():
    st.subheader("Product Description")
    description = st.text_area("Enter product description")
    return description.strip() if description else ""

def insight_visualizer(insights, insight_type, location, category):
    st.subheader("Cultural Insights")
    if not insights or not insights.get("success"):
        st.error("Failed to fetch cultural insights. Please try again.")
        return None
    
    try:
        entities = insights["data"].get("entities", [])
        if insight_type == "brand":
            df = pd.DataFrame([
                {"trait": entity["name"], "score": entity["properties"].get("popularity", 0.5)}
                for entity in entities
            ])
            fig = px.bar(df, x="trait", y="score", title="Cultural Affinity Scores",
                         color_discrete_sequence=["#667eea"])
            st.plotly_chart(fig, use_container_width=True)
            return df
        
        elif insight_type == "demographics":
            df = pd.DataFrame([
                {"age_group": entity.get("age_group", "Unknown"), "affinity": entity.get("affinity_score", 0.5)}
                for entity in entities
            ])
            fig = px.bar(df, x="age_group", y="affinity", title="Demographic Affinity",
                         color_discrete_sequence=["#764ba2"])
            st.plotly_chart(fig, use_container_width=True)
            return df
        
        elif insight_type == "heatmap":
            heatmap_data = insights["data"].get("heatmap", {})
            if not heatmap_data:
                st.warning("No heatmap data available.")
                return None
            z = heatmap_data.get("z", [])
            x = heatmap_data.get("x", [])
            y = heatmap_data.get("y", [])
            fig = go.Figure(data=go.Heatmap(z=z, x=x, y=y, colorscale="Viridis"))
            fig.update_layout(title="Regional Affinity Heatmap")
            st.plotly_chart(fig, use_container_width=True)
            return pd.DataFrame(z, columns=x, index=y)
        
        history_response = requests.get(f"{API_BASE_URL}/hype/history/{location}/{category}", timeout=10)
        history = history_response.json() if history_response.status_code == 200 else {"data": []}
        if history["data"]:
            df_history = pd.DataFrame(history["data"])
            fig_history = px.line(df_history, x="timestamp", y="score", title="Hype Score Trends",
                                  color_discrete_sequence=["#667eea"])
            st.plotly_chart(fig_history, use_container_width=True)
            return df_history
    except Exception as e:
        logger.error(f"Error rendering insights: {str(e)}")
        st.error(f"Error rendering insights: {str(e)}")
        return None

def prediction_dashboard(predictions, hype_score):
    st.subheader("Demand Predictions and Strategies")
    if not predictions or not predictions.get("success"):
        st.error("Failed to generate predictions. Please try again.")
        return None
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Demand Uplift", f"{predictions['data'].get('uplift', 'Unknown')}%")
        st.metric("Confidence Score", f"{predictions['data'].get('confidence', 'Unknown')}")
        st.metric("Hype Score", f"{hype_score.get('averageScore', 'Unknown')}")
        if hype_score.get("change_detected", False):
            st.warning(f"Significant change detected: {hype_score['change_percent']}%")
    with col2:
        st.write("**Recommended Strategy**")
        st.write(predictions["data"].get("strategy", "Unknown"))
    
    trend_data = predictions["data"].get("trend", [])
    if trend_data:
        df = pd.DataFrame(trend_data)
        fig = px.line(df, x="time", y="demand", title="Demand Trends",
                      color_discrete_sequence=["#667eea"])
        st.plotly_chart(fig, use_container_width=True)
        return df
    else:
        st.warning("No trend data available.")
    
    return pd.DataFrame({
        "Metric": ["Demand Uplift", "Confidence Score", "Hype Score", "Strategy"],
        "Value": [f"{predictions['data'].get('uplift', 'Unknown')}%",
                  f"{predictions['data'].get('confidence', 'Unknown')}",
                  f"{hype_score.get('averageScore', 'Unknown')}",
                  predictions["data"].get("strategy", "Unknown")]
    })

def export_report(insights_df, predictions_df, format_type):
    if insights_df is not None and predictions_df is not None:
        report_df = pd.concat([insights_df, predictions_df], axis=1, keys=["Insights", "Predictions"])
        if format_type == "PDF":
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            data = [report_df.columns.tolist()] + report_df.values.tolist()
            table = Table(data)
            doc.build([table])
            buffer.seek(0)
            return buffer, "caeser_report.pdf", "application/pdf"
        elif format_type == "Excel":
            buffer = BytesIO()
            report_df.to_excel(buffer, index=False, engine="openpyxl")
            buffer.seek(0)
            return buffer, "caeser_report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif format_type == "CSV":
            buffer = BytesIO()
            report_df.to_csv(buffer, index=False, encoding='utf-8')
            buffer.seek(0)
            return buffer, "caeser_report.csv", "text/csv"
    return None, None, None

def data_quality_widget():
    st.subheader("Data Quality Report")
    try:
        response = requests.get(f"{API_BASE_URL}/data_quality", timeout=5)
        metrics = response.json() if response.status_code == 200 else {}
        if metrics.get("success"):
            st.markdown('<div class="data-quality__widget">', unsafe_allow_html=True)
            st.write(f"**Missing Values**: {metrics['data'].get('missing_values', {}).get('value', 0)}")
            st.write(f"**API Errors**: {metrics['data'].get('api_errors', {}).get('value', 0)}")
            st.write(f"**Freshness**: {metrics['data'].get('freshness', {}).get('value', 'Unknown'):.2f} hours")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No data quality metrics available.")
    except Exception as e:
        logger.error(f"Error fetching data quality: {str(e)}")
        st.error(f"Error fetching data quality: {str(e)}")

def llm_data_quality_widget():
    st.subheader("LLM Data Quality Report")
    try:
        response = requests.get(f"{API_BASE_URL}/llm_data_quality", timeout=5)
        metrics = response.json() if response.status_code == 200 else {}
        if metrics.get("success"):
            st.markdown('<div class="data-quality__widget">', unsafe_allow_html=True)
            confidence = metrics['data'].get('confidence', {})
            st.write(f"**Average Confidence**: {confidence.get('avg_value', 'N/A'):.2f}")
            errors = metrics['data'].get('errors', {})
            st.write(f"**Error Count**: {errors.get('count', 0)}")
            response_time = metrics['data'].get('response_time', {})
            st.write(f"**Average Response Time**: {response_time.get('avg_value', 'N/A'):.2f} seconds")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No LLM data quality metrics available.")
    except Exception as e:
        logger.error(f"Error fetching LLM data quality: {str(e)}")
        st.error(f"Error fetching LLM data quality: {str(e)}")

def mark_product(user_id, product_name, category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO marked_products (user_id, product_name, category)
        VALUES (?, ?, ?)
    """, (user_id, product_name, category))
    conn.commit()
    conn.close()

def get_marked_products(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_name, category FROM marked_products WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"product_name": row[0], "category": row[1]} for row in rows]

def main():
    st.title("CÆSER: Cultural Affinity Simulation Engine for Retail")
    
    # Initialize store data table
    init_store_table()
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Main Dashboard", "Store Data", "Google Trends"])
    
    with tab1:
        user_id = st.text_input("User ID", help="Enter your user ID", key="user_id")
        location, category, insight_type, threshold = market_selector()
        keywords = product_keywords()
        description = product_description()
        export_format = st.selectbox("Export Format", ["PDF", "Excel", "CSV"], key="export_format")
        
        if user_id:
            marked_products = get_marked_products(user_id)
            if marked_products:
                st.subheader("Marked Products")
                for product in marked_products:
                    st.write(f"{product['product_name']} ({product['category']})")
        
        if st.button("Generate Insights and Predictions", key="submit"):
            with st.spinner("Fetching insights and predictions..."):
                try:
                    insights_response = requests.get(
                        f"{API_BASE_URL}/insights/{location}/{category}?insight_type={insight_type}",
                        timeout=10
                    )
                    insights = insights_response.json() if insights_response.status_code == 200 else {}
                    
                    product = {
                        "name": ", ".join(keywords) or category,
                        "category": category,
                        "description": description or f"{category} product"
                    }
                    
                    if st.checkbox("Mark this product for sentiment tracking", key="mark_product"):
                        mark_product(user_id, product["name"], category)
                    
                    prediction_payload = {"product": product, "insights": insights}
                    prediction_response = requests.post(
                        f"{API_BASE_URL}/predict/demand",
                        json=prediction_payload,
                        timeout=10
                    )
                    predictions = prediction_response.json() if prediction_response.status_code == 200 else {}
                    
                    hype_payload = {"insights": insights, "category": category, "location": location, "threshold": threshold, "product_name": product["name"]}
                    hype_response = requests.post(
                        f"{API_BASE_URL}/hype/score",
                        json=hype_payload,
                        timeout=10
                    )
                    hype_score = hype_response.json()
                    
                    insights_df = insight_visualizer(insights, insight_type, location, category)
                    predictions_df = prediction_dashboard(predictions, hype_score)
                    
                    if hype_score.get("hourly_sentiment_change"):
                        st.metric("Hourly Sentiment Change", f"{hype_score['hourly_sentiment_change']}%")
                    
                    data_quality_widget()
                    llm_data_quality_widget()
                    
                    buffer, filename, mime = export_report(insights_df, predictions_df, export_format)
                    if buffer:
                        st.download_button(
                            label=f"Download Report as {export_format}",
                            data=buffer,
                            file_name=filename,
                            mime=mime
                        )
                    
                    discord_payload = {"prediction": {"product": product, **predictions.get("data", {})}, "hype_data": hype_score}
                    requests.post(f"{API_BASE_URL}/discord/alert", json=discord_payload, timeout=5)
                    
                    integrations_payload = {"prediction": {"product": product, **predictions.get("data", {})}, "hype_data": hype_score}
                    requests.post(f"{API_BASE_URL}/integrations/send", json=integrations_payload, timeout=5)
                    
                except requests.RequestException as e:
                    logger.error(f"API request failed: {str(e)}")
                    st.error(f"API request failed: {str(e)}")
                except Exception as e:
                    logger.error(f"An error occurred: {str(e)}")
                    st.error(f"An error occurred: {str(e)}")
    
    with tab2:
        st.header("Store Data Management")
        user_provided_store_data()
        
        # Show existing store data
        st.subheader("Existing Store Data")
        conn = sqlite3.connect(DB_PATH)
        store_df = pd.read_sql_query("SELECT product, sales, date FROM store_data", conn)
        conn.close()
        
        if not store_df.empty:
            st.dataframe(store_df)
            st.download_button(
                label="Download Store Data as CSV",
                data=store_df.to_csv(index=False).encode('utf-8'),
                file_name="store_data.csv",
                mime="text/csv"
            )
        else:
            st.info("No store data available")
    
    with tab3:
        st.header("Google Trends Integration")
        fetch_and_display_trends()
        
        # Show existing trends data
        st.subheader("Existing Trends Data")
        conn = sqlite3.connect(DB_PATH)
        trends_df = pd.read_sql_query(
            "SELECT text AS keyword, likes AS interest, timestamp FROM social_data WHERE source='google_trends'", 
            conn
        )
        conn.close()
        
        if not trends_df.empty:
            st.dataframe(trends_df)
            st.download_button(
                label="Download Trends Data as CSV",
                data=trends_df.to_csv(index=False).encode('utf-8'),
                file_name="trends_data.csv",
                mime="text/csv"
            )
        else:
            st.info("No trends data available")

if __name__ == "__main__":
    main()
logger.info('Streamlit app initialized successfully')
```


## File: frontend\src\outcome_form.py

```$language

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

# Calculate ROI based on hype score and budget
roi = budget * 0.1 * (hype_score / 100)
st.metric("Est. ROI", f"${roi:.0f}", delta_color="inverse" if roi < budget else "normal")

if st.button("Submit"):
    if pid <= 0 or actual < 0:
        st.error("Please enter valid values for Prediction ID and Actual uplift %.")
    else:
        try:
            r = requests.post("http://localhost:8000/submit_outcome", json={"prediction_id": pid, "actual_uplift": actual})
            st.json(r.json())
        except requests.RequestException as e:
            st.error(f"Failed to submit outcome: {str(e)}")
```


## File: migrations\env.py

```$language

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```


## File: migrations\README

```$language

Generic single-database configuration.
```


## File: migrations\script.py.mako

```$language

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

```


## File: migrations\versions\4c0ff554c6e2_initial_migration.py

```$language

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
```


## File: scrapers\affiliate_purchases.py

```$language

# In scrapers/affiliate_purchases.py
import json
import sqlite3
import os
from datetime import datetime
import requests

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")

def init_affiliate_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS affiliate_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            clicks INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def fetch_affiliate_data(platform: str):
    # Example: Fetch data from a hypothetical affiliate API
    url = f"https://api.{platform}.com/v1/data"
    headers = {"Authorization": f"Bearer {os.getenv(f'{platform.upper()}_API_KEY')}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch data from {platform}: {str(e)}")
        return []

def store_affiliate_data():
    platforms = ["instagram", "facebook", "twitter"]  # Example platforms
    for platform in platforms:
        data = fetch_affiliate_data(platform)
        if not data:
            continue
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for item in data:
            cursor.execute("""
                INSERT INTO affiliate_data (platform, clicks, timestamp)
                VALUES (?, ?, ?)
            """, (platform, item.get('clicks', 0), datetime.now().isoformat()))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    init_affiliate_table()
    store_affiliate_data()
```


## File: scrapers\credit_card_spending.py

```$language

# In scrapers/credit_card_spending.py
import pandas as pd
import sqlite3
import os
from datetime import datetime
import requests

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")

def init_spending_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spending_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            spend_total REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def fetch_credit_card_data():
    # Example: Fetch data from a hypothetical credit card API
    url = "https://api.creditcard.com/v1/transactions"
    headers = {"Authorization": f"Bearer {os.getenv('CREDIT_CARD_API_KEY')}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch credit card data: {str(e)}")
        return []

def store_spending_data():
    data = fetch_credit_card_data()
    if not data:
        return
    df = pd.DataFrame(data)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO spending_data (category, spend_total, timestamp)
            VALUES (?, ?, ?)
        """, (row['category'], row['spend_total'], datetime.now().isoformat()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_spending_table()
    store_spending_data()
```


## File: scrapers\dark_web.py

```$language

# In scrapers/dark_web.py
import json
import sqlite3
import os
from datetime import datetime
import requests

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")

def init_dark_web_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dark_web_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            likes INTEGER,
            source TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def fetch_dark_web_data():
    # Example: Fetch data from a hypothetical dark web API
    url = "https://api.darkweb.com/v1/posts"
    headers = {"Authorization": f"Bearer {os.getenv('DARK_WEB_API_KEY')}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch dark web data: {str(e)}")
        return []

def store_dark_web_data():
    data = fetch_dark_web_data()
    if not data:
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for item in data:
        cursor.execute("""
            INSERT INTO dark_web_data (text, likes, source, timestamp)
            VALUES (?, ?, ?, ?)
        """, (item['text'], item['likes'], "dark_web", datetime.now().isoformat()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_dark_web_table()
    store_dark_web_data()
```


## File: scrapers\google_trends.py

```$language

# In scrapers/google_trends.py
import requests
import sqlite3
import os
from datetime import datetime
from time import sleep

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")

def get_google_trends(keywords):
    results = []
    url = f"https://trends.google.com/trends/api/dailytrends?hl=en-US&tz=300&geo=US&cat=all&ed={datetime.now().strftime('%Y%m%d')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            trends = data['default']['trendingSearchesDays'][0]['trendingSearches']
            for keyword in keywords:
                keyword = keyword.strip().lower()
                interest = 0
                for trend in trends:
                    if keyword in trend['title']['query'].lower():
                        interest = int(trend['formattedTraffic'].replace('K', '000').replace('M', '000000')) or 0
                        break
                results.append((keyword, interest))
            return results
        except requests.RequestException as e:
            logger.error(f"Failed to fetch Google Trends data (attempt {attempt + 1}/{retries}): {str(e)}")
            sleep(2 ** attempt)  # Exponential backoff
    return results

def store_trend(keyword, interest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO social_data (text, likes, source, timestamp)
        VALUES (?, ?, ?, ?)
    """, (keyword, interest, "google_trends", datetime.now().isoformat()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    keywords = input("Enter keywords (comma-separated): ").split(",")
    trends = get_google_trends(keywords)
    for keyword, interest in trends:
        store_trend(keyword, interest)
```


## File: scrapers\social_media_spider.py

```$language

# In scrapers/social_media_spider.py
import scrapy
import sqlite3
import requests
import json
from datetime import datetime
import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
import os
import random
from fake_useragent import UserAgent
import time

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
PROXY_LIST = os.getenv("PROXY_LIST", "").split(",") if os.getenv("PROXY_LIST") else []

class SqlitePipeline:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO social_data (text, likes, source, timestamp)
            VALUES (?, ?, ?, ?)
        """, (item['text'], item['likes'], item['source'], item['timestamp']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()

class SocialMediaSpider(scrapy.Spider):
    name = "social_media"
    custom_settings = {
        'ITEM_PIPELINES': {'__main__.SqlitePipeline': 1},
        'DOWNLOAD_DELAY': random.uniform(1, 3),
        'ROTATING_PROXY_LIST': PROXY_LIST,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [429, 500, 502, 503, 504]
    }
    ua = UserAgent()

    def __init__(self, sources='reddit,twitter,tiktok,imdb,ebay', target='sneakers', keywords='', *args, **kwargs):
        super(SocialMediaSpider, self).__init__(*args, **kwargs)
        self.sources = [s.strip().lower() for s in sources.split(',')]
        self.target = target
        self.keywords = [kw.strip().lower() for kw in keywords.split(',')] if keywords else []
        self.start_urls = []
        
        if 'reddit' in self.sources:
            self.start_urls.append(f"https://reddit.com/r/{self.target}")
        if 'tiktok' in self.sources:
            self.start_urls.append(f"https://www.tiktok.com/search?q={self.target}")
        if 'instagram' in self.sources:
            self.start_urls.append(f"https://www.instagram.com/explore/tags/{self.target}/")
        if 'imdb' in self.sources:
            self.start_urls.append(f"https://www.imdb.com/search/title/?title_type=feature&genres={self.target}&sort=user_rating,desc")
        if 'ebay' in self.sources:
            self.start_urls.append(f"https://www.ebay.com/sch/i.html?_nkw={self.target}&_sacat=0")
        if 'twitter' not in self.sources:
            return
        
        self.twitter_headers = {
            'Authorization': f'Bearer {TWITTER_API_KEY}',
            'Content-Type': 'application/json'
        }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers={'User-Agent': self.ua.random}, callback=self.parse)
        
        if 'twitter' in self.sources:
            query = f"{self.target} {' '.join(self.keywords)}" if self.keywords else self.target
            twitter_url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=100"
            yield Request(twitter_url, headers=self.twitter_headers, callback=self.parse_twitter, method='GET')

    def parse(self, response):
        source = 'reddit' if 'reddit' in response.url else 'tiktok' if 'tiktok' in response.url else 'instagram' if 'instagram' in response.url else 'imdb' if 'imdb' in response.url else 'ebay'
        
        if source == 'reddit':
            for post in response.css("div.Post"):
                text = post.css("h3::text").get(default="").strip().lower()
                if not self.keywords or any(kw in text for kw in self.keywords):
                    likes = post.css("div._1rZYMD_4xY3gRcSS3p8ODO::text").get(default="0")
                    yield {
                        "text": text,
                        "likes": int(likes.split()[0]) if likes.isdigit() else 0,
                        "source": source,
                        "timestamp": datetime.now().isoformat()
                    }
            next_page = response.css("a[rel='nofollow next']::attr(href)").get()
            if next_page:
                yield response.follow(next_page, self.parse, headers={'User-Agent': self.ua.random})
        
        elif source == 'tiktok':
            count = 0
            for video in response.css("div.tiktok-x6y88p-DivItemContainerV2"):
                if count >= 50:
                    break
                text = video.css("div.tiktok-1qb12g8-DivThreeColumnContainer p::text").get(default="").strip().lower()
                comments = video.css("div.tiktok-1qb12g8-DivCommentContent p::text").getall()
                if not self.keywords or any(kw in text for kw in self.keywords):
                    likes = video.css("strong.tiktok-1p7xrbz-StrongText::text").get(default="0")
                    # Append first 5 comments to text
                    comment_text = " | Comments: " + " ".join(comments[:5]) if comments else ""
                    yield {
                        "text": text + comment_text,
                        "likes": int(likes.replace('K', '000').replace('M', '000000')) if likes else 0,
                        "source": source,
                        "timestamp": datetime.now().isoformat()
                    }
                count += 1
            next_page = response.css("a.tiktok-1p7xrbz-AButton::attr(href)").get()
            if next_page:
                time.sleep(random.uniform(2, 5))
                yield response.follow(next_page, self.parse, headers={'User-Agent': self.ua.random})
        
        elif source == 'instagram':
            for post in response.css("article"):
                text = post.css("div._a9zs span::text").get(default="").strip().lower()
                if not self.keywords or any(kw in text for kw in self.keywords):
                    likes = post.css("div.Nm9FK span::text").get(default="0")
                    yield {
                        "text": text,
                        "likes": int(likes.replace(',', '')) if likes.replace(',', '').isdigit() else 0,
                        "source": source,
                        "timestamp": datetime.now().isoformat()
                    }
        
        elif source == 'imdb':
            count = 0
            for movie in response.css("div.lister-item"):
                if count >= 50:
                    break
                title = movie.css("h3 a::text").get(default="").strip().lower()
                rating = movie.css("div.ratings-bar strong::text").get(default="0")
                if not self.keywords or any(kw in title for kw in self.keywords):
                    yield {
                        "text": title,
                        "likes": float(rating) if rating.replace('.', '').isdigit() else 0.0,
                        "source": source,
                        "timestamp": datetime.now().isoformat()
                    }
                    count += 1
            next_page = response.css("a.next-page::attr(href)").get()
            if next_page and count < 50:
                yield response.follow(next_page, self.parse, headers={'User-Agent': self.ua.random})
        
        elif source == 'ebay':
            count = 0
            for item in response.css("li.s-item"):
                if count >= 50:
                    break
                title = item.css("h3.s-item__title::text").get(default="").strip().lower()
                price = item.css("span.s-item__price::text").get(default="0").replace("$", "").replace(",", "").strip()
                if not self.keywords or any(kw in title for kw in self.keywords):
                    yield {
                        "text": title,
                        "likes": float(price) if price.replace('.', '').isdigit() else 0.0,
                        "source": source,
                        "timestamp": datetime.now().isoformat()
                    }
                    count += 1
            next_page = response.css("a.pagination__next::attr(href)").get()
            if next_page and count < 50:
                yield response.follow(next_page, self.parse, headers={'User-Agent': self.ua.random})

    def parse_twitter(self, response):
        try:
            data = json.loads(response.text)
            tweets = data.get('data', [])
            for tweet in tweets:
                text = tweet.get('text', '').lower()
                if not self.keywords or any(kw in text for kw in self.keywords):
                    yield {
                        "text": text,
                        "likes": tweet.get('public_metrics', {}).get('like_count', 0),
                        "source": "twitter",
                        "timestamp": datetime.now().isoformat()
                    }
        except json.JSONDecodeError:
            self.logger.error("Failed to parse Twitter response")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Social Media Spider")
    parser.add_argument("--sources", default="reddit,twitter,tiktok,instagram,imdb,ebay", help="Comma-separated sources (e.g., reddit,twitter)")
    parser.add_argument("--target", default="sneakers", help="Target subreddit or query")
    parser.add_argument("--keywords", default="", help="Comma-separated keywords")
    args = parser.parse_args()
    
    process = CrawlerProcess()
    process.crawl(SocialMediaSpider, sources=args.sources, target=args.target, keywords=args.keywords)
    process.start()
`


---
## Summary
Total files processed: 26
Completed: 2025-07-28 04:48:01
