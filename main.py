from modules.finvizScrap import getFinviz_todayNews, getFinvizStockNames
from modules.email import setEmailCredentials, send_email
from datetime import date
from modules.loggingSettings import *
import time
import os
from datetime import timedelta

logging.basicConfig(level=logging.INFO)


def main():

    # Set the credentials needed for the email
    # In case you want to reuse this script many times, just hardcode the environment variables here
    os.environ['SENDER_EMAIL_USER'] = "example_sender@gmail.com"
    os.environ['EMAIL_PASSWORD'] = 'example_pass'
    os.environ['RECEIVER_EMAIL_USER'] = 'example_receiver@gmail.com'

    setEmailCredentials()
    start_time = time.monotonic()  # start counting the time

    # 1-.Get list of stock tickers
    logging.info('\n1-. We are analyzing the next stocks:')
    url = 'https://finviz.com/screener.ashx?v=111&f=sh_avgvol_o750,sh_price_u10,sh_relvol_o1&ft=4'
    stocks = getFinvizStockNames(url=url)
    for n, stock in enumerate(stocks):
        logging.info(stock)
    nStocks = len(stocks)
    logging.info('Total stocks: ' + str(nStocks))

    # 2-. Get today news from every stock
    logging.info('\n2-. Getting the stock news from today:')
    d_stock_news = []
    today = str(date.today().strftime("%b-%d-%y"))
    for n, stock in enumerate(stocks):
        try:
            logging.debug('News for ' + stock)
            news = getFinviz_todayNews(stock, today)
            if len(news) > 0:
                logging.info(stock + ' has actual news:')
                for new in news:
                    logging.info(new)
                    d_stock_news.append([new[0], new[2], new[3], new[4]])
            else:
                logging.info(stock + ' has No actual news')
        except Exception as e:
            logging.warning('Problem detected whit ' + stock)
            logging.warning(str(e))
            continue
    try:
        totalStockNews = len(d_stock_news)
        logging.info('Amount stocks with news: ')
        logging.info(str(totalStockNews))
    except Exception as e:
        logging.warning('Empty Dictionary totalStockNews : ' + str(e))
    bsendEmail = False
    if len(d_stock_news) > 0:
        try:
            logging.info(' Sending email')
            send_email(d_stock_news)
            bsendEmail = True
        except Exception as e:
            logging.warning('Problem sending the email')
            logging.warning(str(e))

    end_time = time.monotonic()
    finalMessage = """
            The programm exited succesfully!! 
            Stocks found   : """ + str(len(stocks)) + """
            News found     : """ + str(totalStockNews) + """
            Dedicated time : """ + str(timedelta(seconds=end_time - start_time)) + """
            Email Send     : """ + str(bsendEmail) + """ 
            """
    logging.info(finalMessage)
    print(finalMessage)

if __name__ == '__main__':
    main()
