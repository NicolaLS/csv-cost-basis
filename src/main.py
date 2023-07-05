import time
import sys
import requests
import pandas as pd

# TODO: Put a 'you can't sue me if you mess up your taxes with this' in the README


url = 'https://api.coingecko.com/api/v3/coins/bitcoin/history/'
params = {'date': None, 'localization': 'en'}


def fetch_open_price(date, currency='usd'):
    str_date = date.strftime('%d-%m-%Y')
    params['date'] = str_date
    resp = requests.get(url, params=params)

    # check rate limit
    if resp.status_code == 429:
        # wait one minute
        print('Rate Limit reached, waiting 60 seconds...')
        time.sleep(60)
        resp = requests.get(url, params=params)

    resp_json = resp.json()

    price = (resp_json.get('market_data').get(
        'current_price').get(currency))
    print(f'Price on {str_date}: {price:.2f} {currency.upper()}')
    return price


def main(currency, file_path):
    # TODO: Document in readme: you need to export the CSV to data/history.csv
    history_df = pd.read_csv(file_path,
                             index_col=0, parse_dates=True)

    date_and_price = {date: fetch_open_price(
        date) for date in history_df.index}

    currency_upper = currency.upper()
    price_col = f'Price {currency_upper}'
    value_col = f'Value {currency_upper}'

    history_df[price_col] = history_df.index.map(
        date_and_price)

    history_df[price_col].round(2)

    history_df[value_col] = ((
        history_df['Amount'] * history_df[price_col]) / 100_000_000).round(2)

    print('All transactions:')
    print(history_df)

    recv_history_df = history_df.loc[history_df['Type'] == 'received']
    total_recv_btc = sum(recv_history_df['Amount']) / 100_000_000
    total_recv_fiat = sum(recv_history_df[value_col])

    print('saving result in data/result.csv')
    history_df.to_csv('./data/result.csv')

    print(
        f'Received BTC: {total_recv_btc} {currency_upper}: {total_recv_fiat:.2f}')
    print('Price is not accurrate it represents UTC 00:00 for that date')
    print('There might be rounding errors.')
    print('the publisher of this software assumes no liability if this data is not accurate')


if __name__ == '__main__':
    # init args
    arg_len = len(sys.argv)

    currency = 'usd' if arg_len == 1 else str(sys.argv[1])
    print(f'using currency: {currency}')

    file_path = './data/history.csv' if arg_len != 3 else str(sys.argv[2])
    print(f'using data from: {file_path}')

    main(currency, file_path)
