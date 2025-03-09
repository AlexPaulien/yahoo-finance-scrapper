from functions import *

def main(ticker_list=['NVDA', 'AAPL', 'MSFT']):
    results = create_dataframe(scrapper(ticker_list))
    print(results)



if __name__ == "__main__":
    main()