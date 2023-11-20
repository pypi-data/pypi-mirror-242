"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Python Starters."""


if __name__ == "__main__":
    main(prog_name="python-starters")  # pragma: no cover
