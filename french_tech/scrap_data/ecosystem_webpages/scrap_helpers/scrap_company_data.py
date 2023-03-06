# import requests
from urllib import request

from bs4 import BeautifulSoup as bs

web_request = request.urlopen(url="https://ecosystem.lafrenchtech.com/companies/holiworking")
web_soup = bs(web_request, 'lxml')

print(web_soup.prettify())
