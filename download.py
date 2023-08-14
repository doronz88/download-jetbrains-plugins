import xml.etree.ElementTree as ET
from pathlib import Path

import click
import requests
from plumbum import local, FG

PLUGINS = [
    # https://plugins.jetbrains.com/plugin/10080-rainbow-brackets
    'izhangzhihao.rainbow.brackets',

    # https://plugins.jetbrains.com/plugin/10044-atom-material-icons
    'com.mallowigi',

    # https://plugins.jetbrains.com/plugin/15635-diagrams-net-integration
    'de.docs_as_co.intellij.plugin.diagramsnet',

    # https://plugins.jetbrains.com/plugin/12255-visual-studio-code-dark-plus-theme
    'com.samdark.intellij-visual-studio-code-dark-plus',

    # https://plugins.jetbrains.com/plugin/11938-one-dark-theme
    'com.markskelton.one-dark-theme',

    # https://plugins.jetbrains.com/plugin/164-ideavim
    'IdeaVIM',
]
BUILD = '232.8660.197'
DOWNLOAD_URL = 'https://plugins.jetbrains.com/pluginManager?action=download&id={plugin_xml_id}&build={build}'
DETAILS_URL = 'https://plugins.jetbrains.com/plugins/list?pluginId={plugin_xml_id}'

wget = local['wget']


def get_plugin_latest_version(plugin_xml_id: str) -> str:
    root = ET.fromstring(requests.get(DETAILS_URL.format(plugin_xml_id=plugin_xml_id)).text)
    for node in root.iter('version'):
        return node.text
    raise Exception('failed to get latest version')


def download(plugin_xml_id: str, output: Path, build: str = BUILD) -> None:
    wget[DOWNLOAD_URL.format(plugin_xml_id=plugin_xml_id, build=build), '-O', output, '--no-clobber'] & FG


@click.command()
@click.argument('output', type=click.Path(file_okay=False))
def cli(output: str):
    output = Path(output)
    output.mkdir(exist_ok=True, parents=True)
    for plugin in PLUGINS:
        latest_version = get_plugin_latest_version(plugin)
        output_file = output / f'{plugin}_{latest_version}.zip'
        if output_file.exists():
            continue
        download(plugin, output_file)


if __name__ == '__main__':
    cli()
