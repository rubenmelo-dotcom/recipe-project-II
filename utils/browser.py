from pathlib import Path
import selenium
import selenium.webdriver
from selenium.webdriver.edge.service import Service
from time import sleep


ROOT_DIR = Path(__file__).parent.parent
EDGEDRIVER_NAME = 'msedgedriver'
EDGEDRIVER_DIR = ROOT_DIR / 'bin' / EDGEDRIVER_NAME


def make_browser(*options):
    edge_options = selenium.webdriver.EdgeOptions()

    if options is not None:
        for option in options:
            edge_options.add_argument(option)

    edge_service = Service(executable_path=str(EDGEDRIVER_DIR))
    browser = selenium.webdriver.Edge(
        edge_options,
        edge_service
    )
    return browser


if __name__ == '__main__':
    browser = make_browser()
    browser.get('https://www.google.com/')
