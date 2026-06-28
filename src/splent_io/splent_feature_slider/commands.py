"""
CLI commands contributed by splent_feature_slider.

These commands are auto-discovered by the framework and exposed in the
SPLENT CLI under the ``feature:slider`` group.

Usage::

    splent feature:slider hello
"""

import click


@click.command("hello")
def hello():
    """Example command — replace with your own."""
    click.echo("  Hello from splent_feature_slider!")


cli_commands = [hello]
