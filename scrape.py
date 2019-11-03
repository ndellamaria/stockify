import requests
from bs4 import BeautifulSoup
import io
import urllib
from PIL import Image
import string
import json
import sys
import fileinput


def writerows(rows, filename):
    with open(filename, 'a', encoding='utf-8') as toWrite:
        writer = csv.writer(toWrite)
        writer.writerows(rows)

def grabSite(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        exit()




    # for rows in soup.find_all("tr"):
    #     if("oddrow" in rows["class"]) or ("evenrow" in rows["class"]):
    #         open =
    #         high =
    #         low =
    #         close =
    #         adj =
    #
    #         listings.append([open,high,low,close,adj])


if __name__ == '__main__':
    txtFile = open('data.csv', 'w')
    stockTkrs = {'TSLA', 'MSFT', 'NFLX','FB','AMZN','GOOG','AAPL'}
    baseurl = 'https://finance.yahoo.com/quote/'
    parturl = '/history?p='
    data = {}
    data['stocks'] = []

    for a in stockTkrs:
        print(a)
        fullurl = baseurl + a + parturl + a
        response = grabSite(fullurl)

        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find("tbody")
        open = soup.table.find('span', attrs={'data-reactid': '55'}).text
        high = soup.table.find('span', attrs={'data-reactid': '57'}).text
        low = soup.table.find('span', attrs={'data-reactid': '59'}).text
        close = soup.table.find('span', attrs={'data-reactid': '61'}).text


        data['stocks'].append({
            'TCKR': a,
            'Open': float(open.replace(',','')),
            'High': float(high.replace(',','')),
            'Low': float(low.replace(',','')),
            'Close': float(close.replace(',',''))
        })

    json.dump(data, txtFile)
