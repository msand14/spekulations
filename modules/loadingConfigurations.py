import json
import os


def getWebsConfig(path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs\webs.json')), obj=''):
    """
    Loads the configuration needed to scrap the different webs
    :param path: Location where the configuration is  stored
    :param obj: Name of the web (key of a dictionary)
    :return: Full Url of the web to scrap (value of the dictionary)
    """
    with open(path) as json_file:
        data = json.load(json_file)
        return data[obj]


def getSoupConfig(path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs\/beautifulSoup.json')),
                  obj=''):
    """
    Loads the configuration needed to create the Beautiful Soup
    :param path: Location where the configuration is  stored
    :param obj: Key contained in the confiuguration whose value we are interested in
    :return: value of the obj
    """
    with open(path) as json_file:
        data = json.load(json_file)
        return data[obj]
