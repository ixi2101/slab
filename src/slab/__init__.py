import typer
from . import builder
from .logging_config import setup_logging, get_logger

app = typer.Typer()
logger = get_logger(__name__)


@app.command()
def build(
    binary: str,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
    log_file: str = typer.Option(None, "--log-file", help="Log to file")
):
    """Build cross-compiled binaries."""
    # Setup logging
    log_level = "DEBUG" if verbose else "INFO"
    setup_logging(level=log_level, log_file=log_file)
    
    logger.info(f"Starting build for binary: {binary}")
    b = builder.Builder("./output") 
    match binary:
        case "strace":
            logger.info("Building strace")
            b.build_strace()
        case _:
            logger.error(f"Unknown binary: {binary}")
            raise typer.Exit(1)


def main() -> None:
    app()
