from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Mapping

import requests
from plumbum import local, FG
import click

PLUGINS = [
    'izhangzhihao.rainbow.brackets',  # https://plugins.jetbrains.com/plugin/10080-rainbow-brackets
    'com.mallowigi',  # https://plugins.jetbrains.com/plugin/10044-atom-material-icons
]
BUILD = '232.8660.197'
URL = 'https://plugins.jetbrains.com/pluginManager?action=download&id={plugin_xml_id}&build={build}'

wget = local['wget']


def get_plugin_latest_version(plugin_xml_id: str) -> str:
    root = ET.fromstring(requests.get(f'https://plugins.jetbrains.com/plugins/list?pluginId={plugin_xml_id}').text)
    for node in root.iter('version'):
        return node.text
    raise Exception('failed to get latest version')


def download(plugin_xml_id: str, output: Path, build: str = BUILD) -> None:
    wget[URL.format(plugin_xml_id=plugin_xml_id, build=build), '-O', output, '--no-clobber'] & FG


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
