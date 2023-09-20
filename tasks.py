from invoke import task
import platform
from src.build import initialize_db


pty = True
python = "python3"
if platform.system() == "Windows":
    pty = False
    python = "python"


@task
def dev(ctx):
    print("PTY", pty)
    ctx.run("flask --app ./src/app.py run --debug", pty=pty)


@task
def build(ctx):
    initialize_db()
