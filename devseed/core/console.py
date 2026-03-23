from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

console = Console()


def info(message: str) -> None:
    console.print(f"[bold cyan]→[/] {message}")


def success(message: str) -> None:
    console.print(f"[bold green]✓[/] {message}")


def warning(message: str) -> None:
    console.print(f"[bold yellow]⚠[/] {message}")


def error(message: str) -> None:
    console.print(f"[bold red]✖[/] {message}")


def abort(message: str, exit_code: int = 1) -> None:
    import typer
    error(message)
    raise typer.Exit(code=exit_code)


def title(message: str) -> None:
    console.print()
    console.print(
        Panel.fit(
            f"[bold white]{message}[/]",
            border_style="cyan",
            padding=(0, 2),
        )
    )


def section(message: str) -> None:
    console.print()
    console.print(Rule(f"[bold blue]{message}[/]"))


def plain(message: str = "") -> None:
    console.print(message)

def next_step(command: str, description: str | None = None) -> None:
    console.print()
    console.print("[bold]Próximo passo sugerido:[/]")
    if description:
        console.print(f"[cyan]{command}[/]  → {description}")
    else:
        console.print(f"[cyan]{command}[/]")