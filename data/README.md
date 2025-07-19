# Data Processing Documentation

## Data Pipeline
1. Raw data from Qloo API → `/data/raw/`
2. Cleaned and normalized data → `/data/processed/`
3. Temporary files → `/data/temp/` (auto-cleaned weekly)
4. Schema definitions → `/data/schemas/`

## File Structure
- `raw/`: Original API responses (JSON format)
- `processed/`: 
  - `affinities.csv`: Normalized cultural affinity scores
  - `demand_forecasts.parquet`: Prediction outputs
- `schemas/`:
  - `affinity_schema.json`: Data structure for cultural insights
  - `prediction_schema.json`: Output format for forecasts

## Processing Guidelines
1. Always validate data against schemas before processing
2. Maintain data lineage through filename conventions:
   - `{source}_{date}_{version}.ext`
3. Never modify raw files - create new processed versions

## Schema Examples
```json
// affinity_schema.json
{
  "market": "string",
  "category": "string",
  "affinities": [
    {
      "trait": "string",
      "score": "float",
      "percentile": "float"
    }
  ]
}