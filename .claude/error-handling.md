# Error Handling Strategy

## Overview

feedrr is designed to be resilient to common RSS feed issues. The MVP prioritizes continued operation over failing completely when individual feeds have problems.

## RSS Feed Fetching Errors

### Common Issues Handled

1. **Rate Limiting (HTTP 420)**
   - Some feeds (e.g., The Verge) implement aggressive rate limiting
   - Returns HTTP 420 "X-Forbidden" errors when limits are exceeded
   - **Handling**: Error is logged, feed is skipped, other feeds continue processing

2. **HTTP Errors (4xx, 5xx)**
   - 404 Not Found: Feed moved or deleted
   - 500 Server Error: Temporary server issues
   - 503 Service Unavailable: Maintenance mode
   - **Handling**: All HTTP errors are caught, logged, and skipped

3. **Network Timeouts**
   - Slow or unresponsive feed servers
   - Default timeout: 30 seconds
   - **Handling**: Timeout exceptions caught, feed skipped

4. **Parse Errors**
   - Malformed XML/RSS
   - Encoding issues
   - **Handling**: Parse errors caught, feed skipped

### Implementation

Error handling is implemented in `src/feedrr/fetcher/rss.py:69-71`:

```python
except Exception as e:
    print(f"Error fetching {feed_url}: {e}")
    return []
```

The CLI layer (`src/feedrr/cli.py:85-96`) handles the empty response:

```python
articles_data = fetch_feed(source.feed_url)

if articles_data:
    # Save to database
    new_count = save_articles(session, source, articles_data)
    total_new += new_count
    console.print(f"    [green]✓[/green] Found {len(articles_data)} articles, {new_count} new")
else:
    console.print(f"    [yellow]![/yellow] No articles found")
```

### Error Output Example

```
Fetching from 3 sources...

  Fetching: Hacker News
    ✓ Found 30 articles, 30 new
  Fetching: TechCrunch
    ✓ Found 20 articles, 20 new
  Fetching: The Verge
Error fetching https://www.theverge.com/rss/index.xml: 420 Client Error: X-Forbidden for url: https://www.theverge.com/rss/index.xml
    ! No articles found

✓ Fetch complete! Added 50 new articles
```

## Topic Processing Errors

### Handled Cases

1. **Empty Articles**
   - Articles with no title or content
   - **Handling**: Assigned 'general' topic by default

2. **Model Loading Failures**
   - sentence-transformers model download/load issues
   - **Handling**: Exception propagates, process command fails (intentional - critical error)

3. **Unknown Topics**
   - Topic slugs not in config
   - **Handling**: Assignment skipped (except 'general' which auto-creates)

4. **Duplicate Assignments**
   - Same topic assigned multiple times
   - **Handling**: Database constraint prevents duplicates silently

## Database Errors

### Handled Cases

1. **Duplicate Articles**
   - Same URL fetched multiple times
   - **Handling**: Checked before insert, duplicates skipped (`src/feedrr/storage/db.py:48-51`)

2. **Integrity Constraint Violations**
   - Race conditions in multi-fetch scenarios
   - **Handling**: Transaction rolled back, error caught (`src/feedrr/storage/db.py:67-72`)

```python
try:
    session.commit()
except IntegrityError:
    session.rollback()
    # Some duplicates might have been added between queries
    pass
```

## Philosophy

The MVP error handling follows these principles:

1. **Fail Gracefully**: Individual feed failures don't stop the entire pipeline
2. **Log and Continue**: Errors are logged but processing continues
3. **Fail Fast for Critical Errors**: Database/model loading failures are critical and should fail
4. **User Visibility**: Users see which feeds failed in the output
5. **Idempotency**: Re-running commands is safe (duplicates are skipped)

## Future Improvements (Post-MVP)

- Retry logic with exponential backoff
- Feed health tracking (mark feeds as unhealthy after N failures)
- Automatic feed URL updates (detect redirects)
- Email/webhook notifications for persistent failures
- Detailed error logs to file (currently just console)
- Metrics dashboard showing feed reliability
