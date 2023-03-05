import sys
import click as c


@c.group()
def util():
    pass


@c.command()
def info():
    c.echo("in click")


if __name__ == "__main__":
    util()
