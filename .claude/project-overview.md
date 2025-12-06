# feedrr - Project Overview

## Vision
RSS/News Aggregator (MVP) with AI-powered features for content curation and reading enhancement.

## Core Requirements

### Must-Have Features (MVP)
1. **RSS Feed Processing**
   - Support for multiple RSS sources
   - Reliable fetching and parsing
   - Error handling and retry logic

2. **Web Interface**
   - Mobile/Web view similar to iOS app "feeed"
   - Clean, minimal, readable layout
   - Mobile-responsive design

3. **LLM-Powered Features**
   - Context/topic tagging using lightweight LLM
   - Content deduplication using lightweight LLM
   - Local processing (no API costs)

4. **Static Site Hosting**
   - GitHub Pages deployment
   - Static site generation (similar to osmos:feed or FreshRSS)
   - Automated builds via GitHub Actions

5. **Data Management**
   - Local database with records
   - Rollback or versioning support

### Post-MVP Features
- Bionic reader mode (bold first half of words for faster reading)
- Enhanced versioning and rollback capabilities

## Technical Decisions

### Language & Framework
- **Python 3.11+** - Great ecosystem for LLM integration, faster development
- Modern tooling with pyproject.toml

### Architecture
- **Static Site Generator** - Runs periodically via GitHub Actions
- **SQLite Database** - Local storage with version control
- **Lightweight LLM** - sentence-transformers (all-MiniLM-L6-v2, ~80MB)

### Hosting Strategy
- **GitHub Pages** - Static site hosting
- **Pre-generation** - HTML pages generated periodically
- **Client-side enhancement** - Progressive enhancement with minimal JS

## Success Criteria
- [ ] Successfully fetch and parse RSS feeds from multiple sources
- [ ] Accurate topic tagging on articles
- [ ] Effective content deduplication (>85% similarity threshold)
- [ ] Clean, mobile-friendly UI similar to "feeed" app
- [ ] Automated deployment to GitHub Pages
- [ ] Build runs successfully every 30-60 minutes
- [ ] Database versioning working correctly

## Timeline
- Phase 1: Project Setup & Architecture ✓
- Phase 2: Core RSS Feed Processing
- Phase 3: LLM Integration
- Phase 4: Static Site Generation
- Phase 5: Web UI Development
- Phase 6: GitHub Pages Deployment
