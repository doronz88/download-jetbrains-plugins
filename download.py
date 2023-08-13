from pathlib import Path
from plumbum import local, FG
import click

PLUGINS = [
    'izhangzhihao.rainbow.brackets',  # https://plugins.jetbrains.com/plugin/10080-rainbow-brackets
    'com.mallowigi',  # https://plugins.jetbrains.com/plugin/10044-atom-material-icons
]
BUILD = '232.8660.197'
URL = 'https://plugins.jetbrains.com/pluginManager?action=download&id={plugin_xml_id}&build={build}'

wget = local['wget']


def download(plugin_xml_id: str, output: Path, build: str = BUILD) -> None:
    wget[URL.format(plugin_xml_id=plugin_xml_id, build=build), '-O', output, '--no-clobber'] & FG


@click.command()
@click.argument('output', type=click.Path(file_okay=False))
def cli(output: str):
    output = Path(output)
    output.mkdir(exist_ok=True, parents=True)
    for plugin in PLUGINS:
        download(plugin, output / f'{plugin}.zip')


if __name__ == '__main__':
    cli()
