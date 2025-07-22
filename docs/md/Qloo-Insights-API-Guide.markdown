# Qloo Insights API Guide

## Introduction

Welcome to the Qloo Insights API Guide! This documentation provides everything you need to harness the power of the Qloo Insights API, a robust tool for generating AI-driven recommendations and insights. Whether you're a beginner integrating your first API or an advanced developer exploring complex use cases, this guide will walk you through setup, usage, and advanced features.

The Qloo Insights API leverages billions of signals to deliver taste-based insights across categories like movies, books, brands, and more. With flexible input/output options, extensive filtering, and versatile applications, it’s designed to unlock deep cultural intelligence about user preferences and behaviors.

Let’s dive in and get started!

---

## Getting Started

### Accessing the API

To use the Qloo Insights API, you’ll need an API key. Contact the Qloo team at [support@qloo.com](mailto:support@qloo.com) to request your key, and it will be generated for you promptly (typically within one business day).

### Authentication

Authenticate your API requests by including your API key in the request headers. Below are examples in different languages:

#### cURL
```bash
curl --location --request GET 'https://staging.api.qloo.com/v2/insights?query=audi' \
--header 'Content-Type: application/json' \
--header 'X-Api-Key: <your-api-key>'
```

#### JavaScript
```javascript
const fetch = require('node-fetch');

const url = 'https://staging.api.qloo.com/v2/insights?query=audi';
const headers = {
  'Content-Type': 'application/json',
  'X-Api-Key': '<your-api-key>'
};

fetch(url, { headers })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

#### Python
```python
import requests

url = 'https://staging.api.qloo.com/v2/insights?query=audi'
headers = {
  'Content-Type': 'application/json',
  'X-Api-Key': '<your-api-key>'
}

response = requests.get(url, headers=headers)
print(response.text)
```

Replace `<your-api-key>` with the key provided by Qloo.

### Making Your First API Call

Let’s make a simple request to retrieve a list of comedy movies. This example includes:

- The API endpoint URL
- A filter for movie entity types
- A tag filter for the "comedy" genre
- Your API key for authentication

#### Example Request
```bash
curl --location 'https://staging.api.qloo.com/v2/insights/?filter.type=urn:entity:movie&filter.tags=urn:tag:genre:media:comedy' \
--header 'x-api-key: <your-api-key>'
```

For more details on basic requests, see the [Basic Insights](#basic-insights) section.

---

## Understanding Responses

API responses provide detailed data about entities matching your query. Here’s an example response for the comedy movie request above:

#### Example Response
```json
{
  "success": true,
  "results": {
    "entities": [
      {
        "name": "Django Unchained",
        "entity_id": "369D1544-628B-4C21-95A0-1488117A308A",
        "type": "urn:entity",
        "subtype": "urn:entity:movie",
        "properties": {
          "release_year": 2012,
          "release_date": "2012-12-25",
          "description": "With the help of a German bounty-hunter, a freed slave sets out to rescue his wife from a brutal plantation owner in Mississippi.",
          "content_rating": "R",
          "duration": 165,
          "image": {
            "url": "https://staging.images.qloo.com/i/369D1544-628B-4C21-95A0-1488117A308A-420x-outside.jpg"
          },
          "akas": [
            {"value": "Django Unchained", "languages": ["fy"]},
            {"value": "被解放的姜戈", "languages": ["zh"]}
          ],
          "filming_location": "Evergreen Plantation - 4677 Highway 18, Edgard, Louisiana, USA",
          "production_companies": ["The Weinstein Company", "Columbia Pictures"],
          "release_country": ["United States"],
          "popularity": 0.9998529346882951,
          "tags": [
            {"id": "urn:tag:keyword:media:ex_slave", "name": "Ex Slave", "type": "urn:tag:keyword:media"},
            {"id": "urn:tag:keyword:media:historical_fiction", "name": "Historical Fiction", "type": "urn:tag:keyword:media"}
          ]
        }
      }
    ]
  },
  "duration": 22
}
```

Key fields include:
- `name`: Entity name
- `entity_id`: Unique identifier
- `properties`: Metadata like release year, description, and tags
- `popularity`: A score between 0 and 1 indicating relative popularity

Understanding this structure is essential for parsing and utilizing the data effectively.

---

## Key Features

The Qloo Insights API offers:

- **Flexible Input and Output**: Supports diverse data types (entities, tags, demographics, locations) for tailored results.
- **Extensive Filtering**: Fine-tune queries with filters for genres, demographics, locations, and more.
- **Versatile Applications**: Ideal for personalization, market analysis, content discovery, and beyond.

These capabilities make it a powerful tool for unlocking user insights.

---

## Common Use Cases

- **Personalized Recommendations**: Suggest content based on user interests.
- **Market Analysis**: Identify trends and preferences for strategic decisions.
- **Content Discovery**: Help users explore new entities aligned with their tastes.
- **Location-Based Insights**: Deliver recommendations tied to geographic data.

Explore these in detail in the [Advanced Usage](#advanced-usage) section.

---

## API System Status

Check the operational status of Qloo services:

- **Qloo API Version 2.0**: Operational (Last Checked: 7/20/2025, 1:22:22 PM)
- **Qloo API Version 1.0**: Operational (Last Checked: 7/20/2025, 1:22:23 PM)
- **Qloo Search API Version 1.0**: Operational (Last Checked: 7/20/2025, 1:22:23 PM)

Regularly verify status to ensure uninterrupted integration.

---

## Qloo LLM Hackathon Developer Guide

For hackathon participants, this section provides tailored guidance.

### Hackathon Environment
Use the base URL: `https://hackathon.api.qloo.com`. Note: Hackathon API keys are exclusive to this environment and won’t work in staging or production.

### Available Endpoints
All Qloo API endpoints are accessible, with `/v2/insights` as the primary endpoint for insights and recommendations.

### Supported Entity Types
Specify `filter.type` in every request. Options include:
- `urn:entity:artist`
- `urn:entity:book`
- `urn:entity:brand`
- `urn:entity:destination`
- `urn:entity:movie`
- `urn:entity:person`
- `urn:entity:place`
- `urn:entity:podcast`
- `urn:entity:tv_show`
- `urn:entity:video_game`

### Quick Start
1. Use `/search` to find entity IDs by name.
2. Use `/v2/tags` for tag IDs.
3. Use `/v2/audiences` for audience IDs.
4. Pass IDs into `/v2/insights` as signals or filters.

### Common Issues
- **Missing Endpoint**: Ensure URLs include an endpoint (e.g., `/v2/insights`).
- **Invalid Tags**: Verify tags via `/v2/tags`.
- **Wrong Environment**: Use `hackathon.api.qloo.com`.

### Resources
- [Hackathon Sign-Up](https://example.com/signup)
- [Qloo API Docs](https://example.com/docs)
- Discord: #qloo-hackathon channel

---

## Insights API Deep Dive

The `/v2/insights` endpoint is the core of Qloo’s offering, providing taste-based insights.

### Key Parameters
- `filter.type` (required): Entity category (e.g., `urn:entity:movie`).
- `bias.trends`: Adjusts trending entity influence.
- `filter.location`: Filters by geographic data (WKT or Qloo ID).
- `signal.demographics.age`: Weights results by age ranges.

See the [Parameter Reference](#parameter-reference) for a full list.

### Entity Types
Supported types include Artist, Book, Brand, Destination, Movie, Person, Place, Podcast, TV Show, and Video Game. Each has specific parameters detailed in the [Entity Type Parameter Guide](#entity-type-parameter-guide).

---

## Advanced Usage

### Basic Insights
Retrieve recommendations by entity type:
```bash
curl --location 'https://staging.api.qloo.com/v2/insights/?filter.type=urn:entity:movie&filter.tags=urn:tag:genre:media:comedy&filter.release_year.min=2022' \
--header 'x-api-key: <your-api-key>'
```

### Demographic Insights
Get demographic affinity scores:
```bash
curl --location 'https://staging.api.qloo.com/v2/insights?filter.type=urn:demographics&signal.interests.tags=urn:tag:genre:media:action' \
--header 'x-api-key: <your-api-key>'
```

### Heatmaps
Generate location-based heatmap data:
```bash
curl --location 'https://staging.api.qloo.com/v2/insights/?filter.type=urn:heatmap&filter.location.query=NYC&signal.interests.tags=urn:tag:genre:media:non_fiction' \
--header 'x-api-key: <your-api-key>'
```

### Location Insights
Recommendations by location:
```bash
curl --location 'https://staging.api.qloo.com/v2/insights/?filter.type=urn:entity:movie&signal.location.query=Lower%20East%20Side' \
--header 'x-api-key: <your-api-key>'
```

### Taste Analysis
Retrieve tag metadata:
```bash
curl --location 'https://staging.api.qloo.com/v2/insights?filter.type=urn:tag&filter.tag.types=urn:tag:keyword:media&filter.parents.types=urn:entity:movie' \
--header 'x-api-key: <your-api-key>'
```

---

## API Reference

### Endpoints
- **Insights**: `GET /v2/insights`
- **Audiences**: `GET /v2/audiences`
- **Trends**: `GET /trends/category`
- **Geospatial**: `GET /geospatial`
- **Recommendations**: `GET /recommendations`

### Parameter Reference
A comprehensive list is available in the [Parameter Reference](#parameter-reference) section (placeholder for detailed external link or appendix).

### Entity Type Parameter Guide
Details on parameters per entity type are in the [Entity Type Parameter Guide](#entity-type-parameter-guide) section (placeholder for detailed external link or appendix).

---

## Conclusion

You’re now equipped to leverage the Qloo Insights API for powerful insights and recommendations. Start by experimenting with basic calls, then explore advanced features to suit your needs. For further assistance, reach out to [support@qloo.com](mailto:support@qloo.com) or join our developer community on Discord.

Happy coding!