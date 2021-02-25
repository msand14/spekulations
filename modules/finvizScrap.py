from modules.loadingConfigurations import getWebsConfig, getSoupConfig
from modules.scrappingActions import getSoup
import logging

def GetFinvizTableFor(stock: str):
    """
    Gets a stock ticker and returns a bs4.element.Tag, which contains all the news froma company
    :param stock: Ticker of the company
    :return: table Tag
    """
    logging.info('Getting the table tag for ' + stock)
    link = getWebsConfig(obj='newsFinviz')

    conf = getSoupConfig(obj='headers')
    conf_user = conf['agent']
    conf_web = conf['browser']
    headers = {conf_user: conf_web}
    soup = getSoup(link=link + stock, headers=headers)
    news_table = soup.find(id='news-table')
    return news_table


def getFinviz_todayNews(stock: str, today: str) -> list:
    """
    Gets a Stock name, scraps finviz stock news (FROM TODAY) and returns it in list form
    :param today: String that represents the actual date
    :param stock: name of the company ( Ticker)
    :return: list of news related to the stock
    """

    all_news = []
    news_table = GetFinvizTableFor(stock)
    date = ''
    for tr in news_table.find_all('tr'):
        text = tr.a.get_text()
        url = tr.a['href']
        date_scrape = tr.td.text.split()
        logging.info(date_scrape)
        if len(date_scrape) == 1:
            logging.info('1 --- time: ' + date_scrape[0])
            time = date_scrape[0]
            date = date
        else:
            date = date_scrape[0]
            logging.info('2 --- date: ' + date_scrape[0])
            logging.info('3 : ---time' + date_scrape[1])
            time = date_scrape[1]
        if date == today:
            all_news.append([stock, date, time, text, url])
        else:
            return all_news
    return all_news


def getFinvizStockNames(url: str):
    """
        get the Names of the Penny Stocks we want to analyse
        :return: list of stock names
        """
    link = getWebsConfig(obj='pennysPool')['web']

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko)" +
                             "Chrome/50.0.2661.102 Safari/537.36"}
    soup = getSoup(link=url, headers=headers)
    nPages = int(soup.find("select", {"id": "pageSelect"}).find('option').text.replace('\n', '').replace(' ', '')[-2:].
                 replace('/',''))
    current_page = link
    stocks = []
    root_url = 'https://finviz.com/'
    for page in range(1, nPages + 1, 1):
        if page != 1:
            soup = getSoup(current_page, headers)
        div1 = soup.find("div", {"id": "screener-content"})
        table = div1.find_all('table')[3]
        for tr in table.find_all('tr'):
            if 'Ticker' in tr.text:
                continue
            td = tr.find_all('td')
            stocks.append(td[1].text)
        if page != nPages + 1:
            next_pages = soup.find("td", {"class": "body-table screener_pagination"}) \
                .find_all("a", {"class": "tab-link"})[-1].attrs['href']
            current_page = root_url + next_pages
    return stocks
