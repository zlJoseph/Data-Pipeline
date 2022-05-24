import logging
import sys
logging.basicConfig(level=logging.INFO)
import subprocess
import pathlib

logger = logging.getLogger(__name__)
news_sites_uids = ['records']

def main():
    _extract()
    _transform()
    _load()

def _extract():
    """
        Proceso de extracción de datos
    """
    logger.info('Starting extract process')
    subprocess.Popen([sys.executable,f'{pathlib.Path(__file__).parent.absolute()}/Extract/main.py']).communicate()
    #subprocess.run(['python', 'main.py'], cwd=f'{pathlib.Path(__file__).parent.absolute()}/Extract')


def _transform():
    """
        Proceso de transformación de datos
    """
    logger.info('Starting transform process')
    subprocess.Popen([sys.executable,f'{pathlib.Path(__file__).parent.absolute()}/Transform/main.py']).communicate()


def _load():
    """
        Proceso de carga de datos
    """
    logger.info('Starting load process')
    subprocess.Popen([sys.executable,f'{pathlib.Path(__file__).parent.absolute()}/Load/main.py']).communicate()


if __name__ == '__main__':
    """
        Ejecuta el proceso de ETL
    """
    main()
