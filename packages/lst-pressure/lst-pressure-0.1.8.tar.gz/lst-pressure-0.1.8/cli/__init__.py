import argparse
import logging
import os
from conf import Conf, LogLevel
from .apps import __all__ as app_lib

conf = Conf()


def configure_logging(log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    logging.basicConfig(level=numeric_level)


def cli():
    prog = "NRF SARAO"
    description = "LST Pressure"
    version = os.getenv("LST_VERSION", "development")

    parser = argparse.ArgumentParser(prog=prog, description=description, usage=argparse.SUPPRESS)
    parser.add_argument("-v", "--version", action="version", version=version)
    parser.add_argument("--debug", action="store_true", help='Show logs of "DEBUG" level or higher')
    parser.add_argument("--info", action="store_true", help='Show logs of "INFO" level or higher')
    parser.add_argument(
        "--warn", action="store_true", help='Show logs of "WARN" level or higher (default)'
    )

    # Build the CLI
    apps = {app.id: app(parser) for app in app_lib}
    args = parser.parse_args()
    cmd = args.command

    # Override environment configuration
    if args.warn:
        conf.LOG_LEVEL = LogLevel.WARN
    if args.info:
        conf.LOG_LEVEL = LogLevel.INFO
    if args.debug:
        conf.LOG_LEVEL = LogLevel.DEBUG

    if not cmd:
        parser.print_help()
        return

    # Execute the CLI
    app = apps.get(cmd, None)
    if not app:
        parser.print_help()

    app.parse(args).exe()
