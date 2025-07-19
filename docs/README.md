# Documentation Guidelines

## Documentation Structure
- `/md`: Markdown documentation files
  - Technical specifications
  - Architecture decisions
  - User guides
- `/txt`: Plain text files
  - Changelogs
  - Meeting notes
  - Raw documentation sources

## Writing Standards
1. Use Markdown for all new documentation
2. Follow the Diátaxis framework:
   - Tutorials (how-to guides)
   - How-to guides (problem-oriented)
   - Explanation (background context)
   - Reference (technical details)
3. Include version metadata in headers

## Version Control
- Major versions in filenames (v1.0, v2.0)
- Changes documented in CHANGELOG.md
- Deprecated docs moved to `/archive`

## Contribution Process
1. Create a new branch for docs changes
2. Update relevant documentation files
3. Update CHANGELOG.md
4. Submit pull request for review

## Example Documentation
```markdown
# API v1.2 Reference
## Last Updated: 2025-07-19

### Authentication
All endpoints require JWT authentication:
`Authorization: Bearer <token>`

### Rate Limits
- 100 requests/minute
- 1000 requests/day