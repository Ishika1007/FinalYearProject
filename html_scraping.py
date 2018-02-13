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

# for loop here..............
#url = input("Enter a website to extract the URL's from: ")
x = True
while(x):
    host = "www.webscantest.com"
    URL = "www.webscantest.com/jsmenu/auto_osrun.php"
    #requestMethod,url,host,referer,origin,csrfToken,form,sensitiveParameters,statusCode,contentType,
     #    server,x_frame_options,x_xss,content_length,comments
    outgoingUrl = []
    r = ''
    Request = namedtuple('Request', fields)
    Main = []
    req1 = requests.get("http://" +URL, allow_redirects = False)
    req = requests.Request('GET',"http://" +URL, headers={'host':host})
    s = req.prepare()
    sessions = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    sessions.mount('http://', adapter)
    sessions.mount('https://', adapter)

    try:
        r = sessions.get("http://" +URL)
        url = s.path_url #url
        data = r.text
        requestMethod = r.request.method #request method
        host = s.headers['host'] #host name
        statusCode = r.status_code
        server = r.headers['Server']
        #print(server)
        soup = BeautifulSoup(data)
        form = False      # form tag
        #print(r.history)
        #print("HREFs:")
        for link in soup.find_all('a'):
            if link.get('href'):
                print(link.get('href'))
                outgoingUrl.append(link.get('href'))
        #print("SCRIPT SOURCE:")
        for link in soup.find_all('script'):
            if link.get('src'):
                print(link.get('src'))
                outgoingUrl.append(link.get('src'))
        #print("IMAGE SOURCE:")
        for link in soup.find_all('img'):
            if link.get('src'):
                print(link.get('src'))
                outgoingUrl.append(link.get('src'))
        #print("FORM ELEEMENT:")
        for link in soup.find_all('form'):
            if link.get('action'):
                print(link.get('action'))
                form = True
                outgoingUrl.append(link.get('action'))
        for link in soup.find_all('meta'):
            if link.get('URL'):
                print(link.get('URL'))
                outgoingUrl.append(link.get('URL'))
         # LINK HREF LEFT..............


    except requests.exceptions.ConnectionError as exc:
        print(exc)
        sleep(5)
    x = False