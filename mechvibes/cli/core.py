import click

# from mechvibes.runner import run as run_mechvibes


class ConfigDefinition(click.ParamType):
    def convert(self, value, param, ctx):
        # TODO: Parse this.
        return value


@click.group()
def main():
    pass


@main.command()
@click.option("--with", "-w", multiple=True, type=ConfigDefinition())
def run(**kwargs):
    print(repr(kwargs))


#    run_mechvibes()
