"""feedrr CLI - Command Line Interface."""

import click
import yaml
from pathlib import Path
from rich.console import Console
from rich.table import Table

from feedrr.config import get_config_path, get_feeds_path, get_data_dir
from feedrr.storage.models import create_database, get_session
from feedrr.storage.db import (
    load_sources_from_config,
    get_enabled_sources,
    save_articles,
    get_article_count,
    get_source_count,
    load_topics_from_config,
    get_articles_without_topics,
    assign_topic_to_article
)
from feedrr.fetcher.rss import fetch_feed
from feedrr.processor.topics import assign_topics

console = Console()

__version__ = "0.1.0"


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """feedrr - RSS/News Aggregator with AI-powered features."""
    pass


@main.command()
def init_db() -> None:
    """Initialize the database."""
    try:
        # Get database path
        db_dir = get_data_dir()
        db_dir.mkdir(parents=True, exist_ok=True)
        db_path = db_dir / "feedrr.db"

        # Create database
        create_database(str(db_path))
        console.print(f"[green]✓[/green] Database created at: {db_path}")

        # Load sources from config
        feeds_path = get_feeds_path()
        with open(feeds_path) as f:
            feeds_config = yaml.safe_load(f)

        session = get_session(str(db_path))
        load_sources_from_config(session, feeds_config['sources'])

        # Load topics from config
        config_path = get_config_path()
        with open(config_path) as f:
            config = yaml.safe_load(f)

        load_topics_from_config(session, config['topics'])
        session.close()

        console.print(f"[green]✓[/green] Loaded {len(feeds_config['sources'])} sources from config")
        console.print(f"[green]✓[/green] Loaded {len(config['topics'])} topics from config")
        console.print("[bold green]Database initialized successfully![/bold green]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@main.command()
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all sources", default=True)
def fetch(fetch_all: bool) -> None:
    """Fetch RSS feeds."""
    try:
        # Get database path
        db_path = get_data_dir() / "feedrr.db"
        if not db_path.exists():
            console.print("[red]Error:[/red] Database not found. Run 'feedrr init-db' first")
            return

        session = get_session(str(db_path))

        # Get enabled sources
        sources = get_enabled_sources(session)
        if not sources:
            console.print("[yellow]No enabled sources found[/yellow]")
            session.close()
            return

        console.print(f"[cyan]Fetching from {len(sources)} sources...[/cyan]\n")

        total_new = 0
        for source in sources:
            console.print(f"  Fetching: [bold]{source.name}[/bold]")

            # Fetch articles
            articles_data = fetch_feed(source.feed_url)

            if articles_data:
                # Save to database
                new_count = save_articles(session, source, articles_data)
                total_new += new_count
                console.print(f"    [green]✓[/green] Found {len(articles_data)} articles, {new_count} new")
            else:
                console.print(f"    [yellow]![/yellow] No articles found")

        session.close()
        console.print(f"\n[bold green]✓ Fetch complete![/bold green] Added {total_new} new articles")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@main.command()
@click.option("--limit", type=int, help="Limit number of articles to process")
def process(limit: int | None) -> None:
    """Process articles with topic tagging."""
    try:
        # Get database path
        db_path = get_data_dir() / "feedrr.db"
        if not db_path.exists():
            console.print("[red]Error:[/red] Database not found. Run 'feedrr init-db' first")
            return

        session = get_session(str(db_path))

        # Load topic definitions from config
        config_path = get_config_path()
        with open(config_path) as f:
            config = yaml.safe_load(f)

        topic_definitions = config['topics']

        # Get articles without topics
        articles = get_articles_without_topics(session)

        if not articles:
            console.print("[green]All articles already tagged![/green]")
            session.close()
            return

        # Apply limit if specified
        if limit:
            articles = articles[:limit]

        console.print(f"[cyan]Processing {len(articles)} articles...[/cyan]\n")

        processed_count = 0
        for article in articles:
            # Combine title and content for topic assignment
            article_text = f"{article.title} {article.content or ''}"

            # Assign topics
            topic_slugs = assign_topics(article_text, topic_definitions)

            # Save topic assignments
            for slug in topic_slugs:
                assign_topic_to_article(session, article, slug)

            processed_count += 1

            if processed_count % 10 == 0:
                console.print(f"  Processed {processed_count}/{len(articles)} articles...")

        session.close()
        console.print(f"\n[bold green]✓ Processing complete![/bold green] Tagged {processed_count} articles")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        import traceback
        console.print(traceback.format_exc())


@main.command()
@click.option("--force", is_flag=True, help="Force regeneration of all pages")
@click.option("--output", default="site", help="Output directory")
def generate(force: bool, output: str) -> None:
    """Generate static site."""
    console.print("[yellow]Static site generation not yet implemented[/yellow]")
    console.print("Coming in Phase 4: Static Site Generation")


@main.command()
def build() -> None:
    """Run full pipeline: fetch → process → generate."""
    console.print("[bold cyan]feedrr build pipeline[/bold cyan]\n")

    # Step 0: Initialize database if needed
    db_path = get_data_dir() / "feedrr.db"
    if not db_path.exists():
        console.print("[bold]Step 0: Initializing database[/bold]")
        ctx = click.get_current_context()
        ctx.invoke(init_db)
        console.print()

    # Step 1: Fetch
    console.print("[bold]Step 1: Fetching RSS feeds[/bold]")
    ctx = click.get_current_context()
    ctx.invoke(fetch)
    console.print()

    # Step 2: Process
    console.print("[bold]Step 2: Processing articles[/bold]")
    ctx.invoke(process)
    console.print()

    # Step 3: Generate (not yet implemented)
    console.print("[bold]Step 3: Generating static site[/bold]")
    console.print("[yellow]Static site generation not yet implemented[/yellow]")
    console.print()

    console.print("[bold green]✓ Build pipeline complete![/bold green]")


@main.command()
def stats() -> None:
    """Show statistics about the database."""
    try:
        # Get database path
        db_path = get_data_dir() / "feedrr.db"
        if not db_path.exists():
            console.print("[red]Error:[/red] Database not found. Run 'feedrr init-db' first")
            return

        session = get_session(str(db_path))

        # Get counts
        source_count = get_source_count(session)
        article_count = get_article_count(session)

        # Create table
        table = Table(title="feedrr Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="green", justify="right")

        table.add_row("Sources", str(source_count))
        table.add_row("Articles", str(article_count))

        console.print(table)
        session.close()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@main.group()
def sources() -> None:
    """Manage RSS feed sources."""
    pass


@sources.command("list")
def sources_list() -> None:
    """List all configured sources."""
    console.print("[yellow]Source listing not yet implemented[/yellow]")


@sources.command("add")
@click.argument("name")
@click.argument("feed_url")
def sources_add(name: str, feed_url: str) -> None:
    """Add a new RSS feed source."""
    console.print(f"[yellow]Would add source: {name} ({feed_url})[/yellow]")


if __name__ == "__main__":
    main()
