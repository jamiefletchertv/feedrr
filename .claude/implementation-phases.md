# feedrr - Implementation Phases

## Phase 1: Project Setup & Architecture ✓

### Objectives
- Set up project structure
- Configure Python environment
- Create configuration files
- Initialize git repository

### Tasks
- [x] Create directory structure
- [ ] Create `pyproject.toml` with dependencies
- [ ] Create configuration files (`feeds.yaml`, `config.yaml`)
- [ ] Create Python package structure with `__init__.py` files
- [ ] Create `.gitignore`
- [ ] Update README with setup instructions

### Deliverables
- Complete project skeleton
- Dependency management configured
- Initial configuration files

---

## Phase 2: Core RSS Feed Processing

### Objectives
- Implement RSS feed fetching
- Parse and extract article data
- Store articles in database

### Tasks
- [ ] Create database models (SQLAlchemy)
  - Articles table
  - Sources table
  - Topics table
  - ArticleTopics junction table
- [ ] Implement RSS feed fetcher
  - Multi-feed support
  - Error handling and retry logic
  - Rate limiting
- [ ] Create database operations
  - Insert new articles
  - Check for existing articles (by URL/GUID)
  - Update source metadata
- [ ] Build CLI command for manual feed fetching
- [ ] Add logging and monitoring

### Deliverables
- Functional RSS fetcher
- Database populated with articles
- CLI tool for testing: `feedrr fetch`

### Testing
- Test with 2-3 diverse RSS feeds
- Verify duplicate URL handling
- Check error handling with invalid feeds

---

## Phase 3: LLM Integration (Tagging & Deduplication)

### Objectives
- Implement topic tagging using LLM
- Implement content deduplication
- Optimize for performance

### Tasks

#### Topic Tagging
- [ ] Download and load sentence-transformers model (all-MiniLM-L6-v2)
- [ ] Define topic taxonomy
- [ ] Implement zero-shot classification or clustering
- [ ] Store topic associations in database
- [ ] Add confidence scores

#### Content Deduplication
- [ ] Generate embeddings for article content
- [ ] Implement cosine similarity calculation
- [ ] Set similarity threshold (0.85)
- [ ] Mark duplicate articles
- [ ] Keep earliest article as canonical

#### Optimization
- [ ] Cache embeddings to avoid recomputation
- [ ] Batch process articles
- [ ] Lazy load model (only when needed)

### Deliverables
- Articles tagged with topics
- Duplicate articles identified and marked
- CLI tool for testing: `feedrr process`

### Testing
- Test topic accuracy on sample articles
- Verify deduplication with known duplicates
- Benchmark processing speed

---

## Phase 4: Static Site Generation

### Objectives
- Create Jinja2 templates
- Generate static HTML pages
- Organize content for easy navigation

### Tasks
- [ ] Design template structure
  - `base.html` - Base layout
  - `index.html` - Homepage with recent articles
  - `article.html` - Individual article page
  - `topic.html` - Topic listing page
- [ ] Implement static site generator
  - Query database for articles
  - Render templates with article data
  - Generate index pages
  - Generate topic pages
  - Generate individual article pages
  - Copy static assets (CSS, JS)
- [ ] Create pagination for large article lists
- [ ] Generate RSS feed for aggregated content
- [ ] Add sitemap.xml for SEO

### Deliverables
- Complete static site in `/docs` folder
- All pages properly linked
- CLI tool for testing: `feedrr generate`

### Testing
- Verify all links work
- Test with large number of articles
- Check mobile responsiveness

---

## Phase 5: Web UI (feeed-style)

### Objectives
- Create clean, minimal, readable UI
- Mobile-first responsive design
- Fast loading and good UX

### Tasks
- [ ] Design CSS framework decision (Tailwind vs custom)
- [ ] Create homepage layout
  - Article cards with previews
  - Date and source information
  - Topic tags
- [ ] Implement topic filtering
  - Filter by topic
  - Multiple topic selection
  - Clear filters button
- [ ] Add dark/light mode toggle
  - CSS variables for theming
  - localStorage for preference
  - System preference detection
- [ ] Optimize for mobile
  - Touch-friendly UI
  - Readable font sizes
  - Proper spacing
- [ ] Add minimal JavaScript
  - Theme switcher
  - Topic filter
  - Progressive enhancement
- [ ] Performance optimization
  - Minimize CSS/JS
  - Optimize images
  - Lazy loading

### Deliverables
- Beautiful, functional web UI
- Mobile-responsive design
- Dark/light mode support
- Fast page loads

### Testing
- Test on multiple devices (mobile, tablet, desktop)
- Test in different browsers
- Verify accessibility (WCAG compliance)
- Performance testing (Lighthouse score)

---

## Phase 6: GitHub Pages Deployment

### Objectives
- Set up GitHub Actions workflow
- Automate feed fetching and site generation
- Deploy to GitHub Pages

### Tasks
- [ ] Create GitHub Actions workflow file
  - Schedule: every 30-60 minutes
  - Install Python dependencies
  - Fetch RSS feeds
  - Process with LLM
  - Generate static site
  - Commit changes
  - Deploy to GitHub Pages
- [ ] Configure GitHub Pages
  - Set source to `/docs` folder or `gh-pages` branch
  - Custom domain support (optional)
- [ ] Database versioning strategy
  - Git LFS for database file, OR
  - Separate branch for data, OR
  - Rebuild database from scratch each time
- [ ] Add workflow status badge to README
- [ ] Set up notifications for failed builds

### Deliverables
- Fully automated pipeline
- Live site on GitHub Pages
- Regular updates (every 30-60 minutes)

### Testing
- Test workflow runs successfully
- Verify site updates automatically
- Check error handling in workflow

---

## Post-MVP Enhancements

### Bionic Reader Mode
- [ ] Implement bold first-half-of-word logic
- [ ] Add toggle button in UI
- [ ] Store preference in localStorage

### Enhanced Versioning
- [ ] Implement database snapshots
- [ ] Add rollback functionality
- [ ] Create version history UI

### Deduplication Enhancements
- [ ] Article stacking view for duplicates
  - Group duplicate/similar articles together
  - Show all sources covering the same story
  - Expandable stack to view alternative perspectives
  - Display canonical article with "X other sources" indicator
- [ ] Trending topics detection
  - Flag topics covered by multiple sources as "trending"
  - Calculate trending score based on number of duplicate sources
  - Highlight trending articles in UI with badge/indicator
  - Sort option to show trending articles first
  - Time-based trending (last 24h, 48h, week)

### Additional Features
- [ ] Search functionality
- [ ] Article bookmarking
- [ ] Export to PDF/EPUB
- [ ] Email digest subscription
- [ ] Social sharing buttons
- [ ] Reading time estimates
- [ ] Article recommendations
- [ ] Web scraping for article images (for feeds that don't include images in RSS)
  - Fetch article page when RSS feed lacks images
  - Extract image from og:image meta tags or article content
  - Cache to avoid repeated fetches

---

## Milestone Tracking

| Phase | Status | Completion Date |
|-------|--------|----------------|
| Phase 1: Setup | In Progress | TBD |
| Phase 2: RSS Processing | Not Started | TBD |
| Phase 3: LLM Integration | Not Started | TBD |
| Phase 4: Site Generation | Not Started | TBD |
| Phase 5: Web UI | Not Started | TBD |
| Phase 6: Deployment | Not Started | TBD |
