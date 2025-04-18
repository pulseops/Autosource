#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime
from sim.engine import stream_story
from rich.console import Console
from rich.table import Table
from rich import print as rprint

def format_event_data(data: dict) -> str:
    """Format event data for display."""
    return json.dumps(data, indent=2)

def create_event_table(event) -> Table:
    """Create a rich table for event display."""
    table = Table(show_header=False, box=None)
    
    # Add event metadata
    table.add_row("[bold blue]Source:[/bold blue]", event.source)
    table.add_row("[bold blue]Event:[/bold blue]", event.event)
    table.add_row("[bold blue]Org ID:[/bold blue]", event.org_id)
    table.add_row("[bold blue]Timestamp:[/bold blue]", event.timestamp)
    
    # Add formatted data
    table.add_row("[bold blue]Data:[/bold blue]", format_event_data(event.data))
    
    return table

def stream_story_events(story_path: str):
    """Stream and display events from a story file."""
    console = Console()
    
    console.print(f"\n[bold green]🚀 Streaming events from {story_path}[/bold green]\n")
    
    try:
        for i, event in enumerate(stream_story(story_path), 1):
            # Print event separator
            console.print(f"\n[bold yellow]Event #{i}[/bold yellow]")
            console.print("=" * 50)
            
            # Create and print event table
            table = create_event_table(event)
            console.print(table)
            
            # Print separator
            console.print("-" * 50)
            
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        return 1
    
    console.print("\n[bold green]✨ Stream completed successfully[/bold green]\n")
    return 0

def list_available_stories():
    """List all available example stories."""
    console = Console()
    stories_dir = Path(__file__).parent.parent / "stories"
    
    console.print("\n[bold]Available Example Stories:[/bold]")
    for story_file in stories_dir.glob("**/*.yaml"):
        relative_path = story_file.relative_to(stories_dir)
        console.print(f"- {relative_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: stream_events.py <story_file>")
        print("\nExample story files:")
        list_available_stories()
        return 1
    
    story_path = sys.argv[1]
    return stream_story_events(story_path)

if __name__ == "__main__":
    # Add rich as a requirement
    try:
        import rich
    except ImportError:
        print("Installing required package: rich")
        import subprocess
        subprocess.check_call(["pip", "install", "rich"])
    
    exit(main()) 