# Yahoo Finance Scrapper
*Scrapping financial data from Yahoo finance.*

## Goal

This script parses the financial data page from yahoo finance for a list of tickers and put them all in a dictionary (of dictionaries). The data we are targeting comes from the url 'https://finance.yahoo.com/quote/AAPL/financials/' (exemple from Apple's ticker) are shown in the two screenshots below:

![data we want to scrap](assets/img/yahoo_finance_screenshot_1.png)
![other data we want to scrap](assets/img/yahoo_finance_screenshot_2.png)
*the data this script is scrapping*

Another function (provided) transforms the scrapped data into a Pandas dataframe for further analysis and work.

## Methodology

The code iterates through the list of tickers provided and requests the corresponding url page using the Requests method and BeautifulSoup. We use a list of web browser agents (please refer to the code file) in order to avoid detection and blocking.

```      
    # randomly choose an agent
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}

    # construct the URL using the ticker passed as argument to the function
    URL = f"https://finance.yahoo.com/quote/{ticker}/financials/"

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    soup_str = str(soup)
```

## Results


## Future work