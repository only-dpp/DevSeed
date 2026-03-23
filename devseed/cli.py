import typer

from devseed.commands.init import app as init_app
from devseed.commands.doctor import app as doctor_app
from devseed.commands.setup import app as setup_app
from devseed.commands.run import app as run_app

app = typer.Typer(
    help="DevSeed - CLI para bootstrap e workflow de projetos Python backend.",
    no_args_is_help=True,
    add_completion=False,
)

app.add_typer(init_app, name="init")
app.add_typer(doctor_app, name="doctor")
app.add_typer(setup_app, name="setup")
app.add_typer(run_app, name="run")