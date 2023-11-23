from importlib.metadata import version as get_version
from pathlib import Path

import typer
from turbofan import command, project

package_name = "airboss"
app = typer.Typer(add_completion=False, help=project.summary(package_name))


@app.command()
def version():
    """
    Shows the current version.
    """
    typer.echo(get_version(package_name))


projects_app = typer.Typer()
app.add_typer(projects_app, name="projects", help="Project management commands.")


@projects_app.command(
    help="Cleans all projects found in the specified path, acconrding to the project Makefile."
)
def clean(path: Path = typer.Argument(".", help="The path to the projects.")):
    """
    Run clean executes 'make clean' in all subdirectories from the execution
    of the command.
    """

    for path in Path(path).glob("*/Makefile"):
        typer.echo(f"Running make clean in {path.parent}")
        command.Command(["make", "-C", path.parent, "clean"]).run()


if __name__ == "__main__":
    app()
