# Testing Documentation

## Testing Strategy
- Unit tests: Test individual functions/components
- Integration tests: Test module interactions
- API contract tests: Verify API specifications
- UI snapshot tests: Visual regression testing

## Test Organization
- `/unit`: Isolated unit tests
- `/integration`: Cross-module tests
- `/api`: API endpoint tests
- `/e2e`: End-to-end scenarios

## Running Tests
1. Run all tests: `pytest`
2. Run specific test suite: `pytest tests/unit`
3. Generate coverage report: `pytest --cov=./ --cov-report=html`

## Coverage Requirements
- Minimum 80% coverage for all new code
- Critical paths must have 100% coverage
- Document any excluded code with `# pragma: no cover`

## Example Test
```python
# tests/unit/test_predictions.py
def test_demand_prediction():
    """Test demand prediction logic"""
    test_data = {"market": "NYC", "category": "sneakers"}
    result = predict_demand(test_data)
    assert isinstance(result, dict)
    assert "forecast" in result
    assert "confidence" in result