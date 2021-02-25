import time
import requests
from bs4 import BeautifulSoup
from modules.loadingConfigurations import *
from modules.loggingSettings import *


def getSoup(link, headers={'User-Agent': 'Chrome'}):
    """
    Gets the Soup for scrapping
    :param link: URL where the information is located on the Internet
    :param headers: Useful for the permission settings
    :return: The BeautifulSoup object represents the parsed document as a whole.
    """
    time.sleep(3) #By default, in order not to get blocked by a webpage
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko)' +
                             'Chrome/50.0.2661.102 Safari/537.36'}

    page = requests.get(link, headers=headers)
    if page.status_code != 200:
        logging.error('ERROR ' + getSoup.__name__ + ': Error de conexión')
        logging.error(link)
        logging.error(str(page))
        return None
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup