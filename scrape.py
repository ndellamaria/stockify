import requests
from bs4 import BeautifulSoup
import io
import urllib
from PIL import Image
import string

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

category_url = ['https://www.tractorsupply.com/tsc/catalog/farm-ranch?cm_sp=Farm_Ranch',
    'https://www.tractorsupply.com/tsc/catalog/livestock?cm_sp=Fly_Livestock-_-Category-_-All',
    'https://www.tractorsupply.com/tsc/catalog/lawn-garden?cm_sp=Fly_Lawn_Garden-_-Category-_-All',
    'https://www.tractorsupply.com/tsc/catalog/truck-trailer?cm_sp=Fly_Truck_Trailer-_-Category-_-All',
    'https://www.tractorsupply.com/tsc/catalog/hardware-tools?cm_sp=Fly_Hardware_Tools-_-Category-_-All',
    'https://www.tractorsupply.com/tsc/catalog/heating-cooling?cm_sp=Heating_Cooling',
    'https://www.tractorsupply.com/tsc/catalog/sporting-goods?cm_sp=Sporting_Goods',
    'https://www.tractorsupply.com/tsc/catalog/outdoor-living?cm_sp=Outdoor_Living']

def grabSite(url):
    return requests.get(url, headers=headers)

if __name__ == '__main__':
    txtFile = open('categories.txt', 'w')
    for a in category_url:
        quote_page = grabSite(a)
        body = quote_page.text
        soup = BeautifulSoup(body, 'html.parser')
        soup.prettify()

        dic = { }
        for a in soup.findAll('div', attrs={'class': 'col-md-4 category col-lg-3 py-1 py-md-5 category-border text-center'}):
            name_box = a.find('h4', attrs={'class': 'text-center font-stymie'})
            name = name_box.text.strip()

            img_box = a.find('img', attrs={'id': 'img1'})
            img_url = img_box.get('data-blzsrc')
            img_url = 'https:' + img_url
            file = urllib.request.urlopen(img_url)
            im = io.BytesIO(file.read())
            img = Image.open(im)
            img_name = name + '.jpg'
            img.save(img_name)

            link_box = a.find('a')
            link_url = link_box.get('href')
            link_url = 'https://wwww.tractorsupply.com' + link_url
            print(link_url)
            txtFile.write(name + '\n')
            dic[name] = link_url
