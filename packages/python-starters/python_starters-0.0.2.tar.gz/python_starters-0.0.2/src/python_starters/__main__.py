"""Command-line interface."""
import click

from .starters_cli import add_starter as _add_starter
from .starters_cli import init_starter as _init_starter
from .starters_cli import list_starters as _list_starters
from .starters_cli import remove_starter as _remove_starter
from .starters_cli import resolve_conflicts as _resolve_conflicts
from .starters_cli import update_starter as _update_starter


@click.group()
@click.version_option()
def main() -> None:
    """Python Starters - A tool to manage and update project starters."""


@main.command()
def init() -> None:
    """Initialize Python Starters in the current project."""
    _init_starter()


@main.command()
@click.argument("starter_git_url")
def add(starter_git_url: str) -> None:
    """Add a new starter to the project."""
    _add_starter(starter_git_url)


@main.command()
@click.argument("starter_name")
def update(starter_name: str) -> None:
    """Update the specified starter."""
    _update_starter(starter_name)


@main.command()
@click.argument("starter_name")
def remove(starter_name: str) -> None:
    """Remove the specified starter."""
    _remove_starter(starter_name)


@main.command()
def list() -> None:
    """List all starters in the project."""
    _list_starters()


@main.command()
@click.argument("starter_name")
def resolve(starter_name: str) -> None:
    """Resolve merge conflicts for the specified starter."""
    _resolve_conflicts(starter_name)


if __name__ == "__main__":
    main()
