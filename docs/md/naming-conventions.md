# CÆSER Naming Conventions

## General Principles
- Be descriptive but concise
- Follow language-specific conventions
- Maintain consistency across codebase

## File Naming
- Python: `snake_case.py`
- JavaScript: `camelCase.js`
- Markdown: `kebab-case.md`
- Tests: `test_*.py` or `*.test.js`

## Variables
- Python/JavaScript: `snake_case`
- Private variables: `_prefix_with_underscore`
- Constants: `ALL_CAPS`

## Functions/Methods
- Python: `snake_case()`
- JavaScript: `camelCase()`
- Async functions: suffix with `_async` (Python) or `Async` (JS)

## Classes
- Python/JavaScript: `PascalCase`
- Abstract classes: prefix with `Abstract`

## Examples
```python
# Good
def calculate_demand_forecast():
    MAX_RETRIES = 3
    _internal_cache = {}

class DemandPredictor:
    async def predict_async(self):
        pass
```

```javascript
// Good
const maxRetries = 3;
const _internalCache = {};

class DemandPredictor {
    async predictAsync() {}
}
```

## Database
- Tables: `plural_snake_case`
- Columns: `snake_case`
- Foreign keys: `related_table_id`

## API Endpoints
- REST: `/kebab-case`
- Query params: `camelCase`