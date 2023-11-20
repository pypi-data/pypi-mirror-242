import importlib
from pathlib import Path

import typer

from fastapi_toolkit.generate import CodeGenerator

app = typer.Typer()


@app.command('g')
@app.command('generate')
def generate(metadata_path: Path = 'metadata', root_path: Path = 'inner_code',
             table: bool = True, router: bool = True, mock: bool = True):
    if not root_path.is_dir():
        typer.confirm(f'root_path: {root_path} is not a dir, do you want to create it?', abort=True)
        root_path.mkdir(parents=True)
    importlib.import_module(f'{metadata_path}.models')
    generator = CodeGenerator(root_path)
    generator.parse_models()
    if table:
        generator.generate_tables()
    if router:
        generator.generate_routers()
    if mock:
        generator.generate_mock()


@app.command('mock')
@app.command('m')
def mock(root_path: Path = 'inner_code'):
    main = importlib.import_module(f'{root_path}.mock').main
    main()


db_app = typer.Typer()


@db_app.command('init')
@db_app.command('i')
def db_init(root_path: Path = 'inner_code'):
    init = importlib.import_module(f'{root_path}.dev.db').init
    init(root_path)


@db_app.command('migrate')
@db_app.command('m')
def db_migrate(root_path: Path = 'inner_code', msg: str = None):
    migrate = importlib.import_module(f'{root_path}.dev.db').migrate
    migrate(msg)


@db_app.command('upgrade')
@db_app.command('u')
def db_upgrade(root_path: Path = 'inner_code'):
    upgrade = importlib.import_module(f'{root_path}.dev.db').upgrade
    upgrade()


app.add_typer(db_app, name="db")
