from html.parser import HTMLParser
from bs4 import BeautifulSoup
from time import sleep
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import csv
import xml.etree.ElementTree as ET
import re
import networkx as nx
import matplotlib.pyplot as plt
from collections import namedtuple

fields = ['requestMethod','url','host','referer','origin','csrfToken','form','sensitiveParameters','statusCode','contentType',
         'outgoingUrl','server','x_frame_options','x_xss','content_length','comments']

#url = input("Enter a website to extract the URL's from: ")
host = "www.webscantest.com"
url = "www.webscantest.com/jsmenu/auto_osrun.php"
r = ''
Request = namedtuple('Request', fields)
Main = []
req1 = requests.get("http://" +url, allow_redirects = False)
req = requests.Request('GET',"http://" +url, headers={'host':host})
s = req.prepare()
sessions = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
sessions.mount('http://', adapter)
sessions.mount('https://', adapter)

try:
    r = sessions.get("http://" +url)
    print(s.path_url)
    data = r.text
    print("REQUEST METHOD: "+r.request.method)
    print(s.headers['host'])
    print("STATUS CODE:" + str(r.status_code))
    soup = BeautifulSoup(data)
    print(r.history)
    print("HREFs:")
    for link in soup.find_all('a'):
        if link.get('href'):
            print(link.get('href'))
    print("SCRIPT SOURCE:")
    for link in soup.find_all('script'):
        if link.get('src'):
            print(link.get('src'))
    print("IMAGE SOURCE:")
    for link in soup.find_all('img'):
        if link.get('src'):
            print(link.get('src'))
    print("FORM ELEEMENT:")
    for link in soup.find_all('form'):
        if link.get('action'):
            print(link.get('action'))


except requests.exceptions.ConnectionError as exc:
    print(exc)
    sleep(5)
