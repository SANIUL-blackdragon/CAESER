# Frontend Documentation

## Application Architecture
The frontend is built with Streamlit and organized into:
- `/src`: Main application logic
- `/public`: Static assets (images, fonts)
- `/components`: Reusable UI components
- `/styles`: Global styles and themes

## Main Components
1. `MarketSelector`: Choose target market and category
2. `InsightVisualizer`: Display cultural affinity data
3. `PredictionDashboard`: Show demand forecasts
4. `StrategyGenerator`: Create marketing recommendations

## Development Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run development server: `streamlit run src/main.py`
3. Access at: `http://localhost:8501`

## Styling Guidelines
- Use CSS variables for colors in `/styles/theme.css`
- Follow BEM naming convention for component classes
- Mobile-first responsive design
- Dark/light theme support

## Component Structure Example
```python
# components/MarketSelector.py
class MarketSelector:
    """Dropdown for selecting target market"""
    
    def __init__(self):
        self.markets = ["NYC", "London", "Tokyo"]
        
    def render(self):
        return st.selectbox("Select Market", self.markets)