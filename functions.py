import pandas as pd
import requests
import random
from bs4 import BeautifulSoup
import re



def scrapper(ticker_list):

    """
    This function takes a list of tickers (such as ['AAPL', 'META']) as input and scraps the related data from yahoo finance. 
    More specifically, the data come from the "financials" tab of yahoo finance and therefore the scrapper gathers some fundamentals data about those companies.
    The resulting data are stored in a dictionary of dictionaries and can then be easily put into a pandas dataframe (or something else)
    """

    all_results = dict()

    for ticker in ticker_list:

        # define some user agents to be used to avoid detection and blocking
        user_agents = [ 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
        ]
        
        # randomly choose an agent
        user_agent = random.choice(user_agents)
        headers = {'User-Agent': user_agent}

        # construct the URL using the ticker passed as argument to the function
        URL = f"https://finance.yahoo.com/quote/{ticker}/financials/"

        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        soup_str = str(soup)

        # get the time data
        soup_str = str(soup)
        start = soup_str.find('Breakdown')
        end = soup_str.find('Total Revenue')
        substr = soup_str[start:end]
        year = re.findall('\\d+/\\d+/\\d+', substr)
        year.insert(0, 'TTM')

        # Isolate the table from the rest of the content
        soup_str = str(soup)
        start = soup_str.find('Breakdown')
        end = soup_str.find('Related Tickers')
        substr = soup_str[start:end]

        # each company's data are stored in a dictionary
        results = dict()
        # here we use regular expressions (regex) to target the specific bits we are interested in
        for i in re.findall("column sticky(.*?)<div class=\"row lv-0", substr):
            title = re.findall('title=\"(.*?)\"', i)[0]
            data = re.findall('<div(.*?)</div>', i)[1:]
            data_ = [re.findall('>(.*) ', d)[0] for d in data if re.findall('>(.*) ', d)[0] not in title]
            results[title] = data_
        results['year'] = year

        # finaly we add the data scrapped for the current ticker into the another dictionary.
        all_results[ticker] = results
        
    
    return all_results



def create_dataframe(financial_data_dic):

    """
    This function loops through the scrapped data dictionary and put everything into a dataframe.
    The input data is a dictionary of dictionaries with the main key being a comapnie's ticker.
    The output is a dataframe.
    """

    all_df = []
    
    for ticker in financial_data_dic.keys():
        data = pd.DataFrame(financial_data_dic[ticker])
        data['ticker'] = ticker
        all_df.append(data)
    financials = pd.concat(all_df, axis=0)
    # moving ticker to first position
    col = financials.pop('ticker')
    financials.insert(0, col.name, col)
    # moving year to second postision
    col = financials.pop('year')
    financials.insert(1, col.name, col)

    return financials

