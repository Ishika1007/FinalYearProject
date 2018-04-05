
import csv
import xml.etree.ElementTree as ET
import re
import nltk
import networkx as nx
import scipy as sp
import matplotlib.pyplot as plt
from collections import namedtuple
import networkx as nx
from bs4 import BeautifulSoup
from time import sleep
import numpy as np
import requests
from nltk.tokenize import word_tokenize
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import csv
from nltk.stem import PorterStemmer
import openpyxl
from openpyxl import load_workbook
wbnew = openpyxl.Workbook()
wbnew.save('new_excel.xlsx')
ws2 = wbnew.active
wbnew2 = openpyxl.Workbook()
wbnew2.save('data_excel.xlsx')
ws3 = wbnew2.active

mydata = set()
G=nx.DiGraph()
mycount = 0
myglobal = {}
ps = PorterStemmer()
form_dict = {}
def parseXML(xmlfile):

    initialize_fields()
    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    # create empty list for news items
    data = []
    outgoingUrl = []

    max = ws2.max_row + 1
    for item in root.findall('./Request'):
        # empty news dictionary
        request = {}
        ownPath = ""
        URL,host, host1,contentType = "", "","",""
        statusCode=100
        # iterate child elements of item
        for child in item:
            script=0
            request[child.tag] = child.text
            if child.tag == "Hostname":
                host = child.text
                host = host.strip()
                print(host)
                host1 = "http://"+host+":80"
            if child.tag == "Url":
                URL = child.text
                # parameters as input from user... symbols "="
                req1 = requests.get(URL, allow_redirects=False)
                sessions = requests.Session()
                retry = Retry(connect=3, backoff_factor=0.5)
                adapter = HTTPAdapter(max_retries=retry)
                r = sessions.get(URL)
                if 'X-Powered-By' in r.headers:
                    print(URL)
                    x_powered_by = r.headers['X-Powered-By']
                else:
                    x_powered_by = ""

                requestMethod = r.request.method
                server = ""#r.headers['Server']
                contentType = ""#r.headers['Content-Type']
                contentLength = ""#r.headers['content-length']
                URL = URL.strip()
                URL = URL[len(host1):]
                URL = check_both(URL)
                if not check_file_type(URL):
                    break
            if child.tag == "RequestHeader":
                referer = processRequestHeaderReferer(child.text,host)
            if child.tag == "ResponseHeader":
                child.text = child.text.strip()
                statusCode = child.text[9:12]
                print(statusCode)
            if child.tag ==
            if child.tag == "ResponseData":
                if not child.text:
                    continue
                count_pay = textprocessing(child.text)
                form = 0
                count_session = sessionprocessing(child.text)
                soup = BeautifulSoup(child.text, 'html.parser')
                for link in soup.find_all('a'):
                    if link.get('href'):
                        a=link.get('href')
                        a = check_both(a)
                        if not check_file_type(a):
                            continue
                        append_new(max, URL, a, requestMethod,host,statusCode,server, referer,0,contentType,contentLength,x_powered_by,count_pay,count_session)
                        max += 1
                for link in soup.find_all('script'):
                    script = 1
                    if link.get('src'):
                        a=link.get('src')
                        a = check_both(a)
                        if not check_file_type(a):
                            continue
                        append_new(max, URL, a, requestMethod,host,statusCode,server, referer,0,contentType,contentLength,x_powered_by,count_pay,count_session)
                        max += 1
                for link in soup.find_all('form'):
                    if link.get('action'):
                        a=link.get('action')
                        a = check_both(a)
                        if not check_file_type(a):
                            continue
                        append_new(max, URL, a, requestMethod,host,statusCode,server, referer,1,contentType,contentLength,x_powered_by,count_pay,count_session)
                        max += 1
                for link in soup.find_all('meta'):
                    if link.get('URL'):
                        a=link.get('URL')
                        a = check_both(a)
                        if not check_file_type(a):
                            continue
                        append_new(max, URL, a, requestMethod,host,statusCode,server, referer,0,contentType,contentLength,x_powered_by,count_pay,count_session)
                        max += 1
            # special checking for namespace object content:media

        # append news dictionary to news items list

def textprocessing(child):
    text_translated = re.sub(r'[^a-z]', ' ', child.lower())
    text_translated = word_tokenize(text_translated)
    fileObj  = open("nlp", "r")
    fileObj = list(fileObj)
    count = 0

    for i, j in enumerate(fileObj):
        fileObj[i] = j[:-1]

    for i in fileObj:
        if i in text_translated:
            count += 1
    return count

def sessionprocessing(child):
    text_translated = re.sub(r'[^a-z]', ' ', child.lower())
    text_translated = word_tokenize(text_translated)
    fileObj  = open("session", "r")

    fileObj = list(fileObj)
    count = 0
    for i, j in enumerate(fileObj):
        fileObj[i] = j[:-1]


    for i in fileObj:
        if i in text_translated:
            count += 1
    return count

def processRequestHeaderReferer(child,hostname):
    referer = re.findall(r'Referer: http://', child)
    if len(referer)==0:
        return ""
    referer = referer[0]+ hostname
    refererString = (re.findall(r'Referer: http://.*',child))
    if len(refererString)==0:
        return ""
    refererString = refererString[0]
    return check_both(refererString[len(referer):])

def initialize_fields():

    ws2.cell(row=1, column=1).value = "Source URL"
    ws2.cell(row=1, column=2).value = "Outgoing URL"
    ws2.cell(row=1, column=3).value = "Request Method"
    ws2.cell(row=1, column=4).value = "Host Name"
    ws2.cell(row=1, column=5).value = "Status Code"
    ws2.cell(row=1, column=6).value = "Server"
    ws2.cell(row=1, column=7).value = "Referer"
    ws2.cell(row=1, column=8).value = "Form"
    ws2.cell(row=1, column=9).value = "Content-type"
    ws2.cell(row=1, column=10).value = "Content-length"
    ws2.cell(row=1, column=11).value = "X-Powered-by:"
    ws2.cell(row=1, column=12).value = "Payment words:"
    ws2.cell(row=1, column=13).value = "Session words:"
    ws3.cell(row=1, column=1).value = "Page:"
    ws3.cell(row=1, column=2).value = "Outgoing:"
    ws3.cell(row=1, column=3).value = "Incoming:"
    ws3.cell(row=1, column=4).value = "Indegree Centrality"
    ws3.cell(row=1, column=5).value = "Outdegree Centrality"
    ws3.cell(row=1, column=6).value = "Closeness Centrality"
    ws3.cell(row=1, column=7).value = "Betweeness Centrality"
    ws3.cell(row=1, column=8).value = "EigenVector Centrality"
    ws3.cell(row=1, column=9).value = "PageRank Score"
    ws3.cell(row=1, column=10).value = "Payment words:"
    ws3.cell(row=1, column=11).value = "Session words:"
    ws3.cell(row=1, column=12).value = "Number of form tags:"
    ws3.cell(row=1, column=13).value = "Method:"
    ws3.cell(row=1, column=14).value = "Referer:"

def append_new(max,URL,a,requestMethod,Host,statusCode,server, referer,form,ct,cl,xpb,cnt1,cnt2):
    URL = check_parameters(URL)
    a = check_parameters(a)
    G.add_node(URL)
    G.add_node(a)
    G.add_edge(URL,a)

    mydata.add((URL,a,requestMethod,Host,statusCode,server, referer,form,ct,cl,xpb,cnt1,cnt2))

def check_parameters(link):
    if "?" in link:
        myindex = link.find("?")
        return check_suffix(link[:myindex])
    else:
        return link

def check_file_type(a):
    if ".css" in a or ".png" in a or ".ico" in a or ".woff" in a or ".woff2" in a or ".gif" in a or ".txt" in a:
        return False
    else:
        return True
def check_path(a):
    if a[0]=='/':
        return a
    else:
        return "/"+a
def check_suffix(a):
    if a[-1]=='/':
        return a
    else:
        return a+"/"
def check_both(a):
    a = check_path(a)
    a = check_suffix(a)
    return a

def check_request_method(a):
    if a=="POST" or a=="PUT" or a=="PATCH":
        return 1
    else:
        return 0
def main():

    # parse xml file
    parseXML('test123.xml')
    ics = nx.in_degree_centrality(G)
    # Gt = most_important(G) # trimming

    ocs = nx.out_degree_centrality(G)

    # Gt = most_important(G) # trimming

    cns = nx.closeness_centrality(G)


    pns = nx.betweenness_centrality(G)

    ens = nx.eigenvector_centrality_numpy(G)
    pgs = nx.pagerank(G, alpha=0.85, personalization=None,
                      max_iter=5, tol=1.0e-2, nstart=None, weight='weight',
                    dangling=None)

    def pagerank(G, alpha=0.85, personalization=None,
                 max_iter=5, tol=1.0e-2, nstart=None, weight='weight',
                 dangling=None):
        if len(G) == 0:
            return {}

        if not G.is_directed():
            D = G.to_directed()
        else:
            D = G

            # Create a copy in (right) stochastic form
        W = nx.stochastic_graph(D, weight=weight)
        N = W.number_of_nodes()

        nx.draw(D, with_labels=True, font_weight='bold')
        plt.show()

        # Choose fixed starting vector if not given
        if nstart is None:
            x = dict.fromkeys(W, 1.0 / N)
        else:
            # Normalized nstart vector
            s = float(sum(nstart.values()))
            x = dict((k, v / s) for k, v in nstart.items())

        if personalization is None:

            # Assign uniform personalization vector if not given
            p = dict.fromkeys(W, 1.0 / N)
        else:
            missing = set(G) - set(personalization)
            if missing:
                raise NetworkXError('Personalization dictionary '
                                    'must have a value for every node. '
                                    'Missing nodes %s' % missing)
            s = float(sum(personalization.values()))
            p = dict((k, v / s) for k, v in personalization.items())

        if dangling is None:

            # Use personalization vector if dangling vector not specified
            dangling_weights = p
        else:
            missing = set(G) - set(dangling)
            if missing:
                raise NetworkXError('Dangling node dictionary '
                                    'must have a value for every node. '
                                    'Missing nodes %s' % missing)
            s = float(sum(dangling.values()))
            dangling_weights = dict((k, v / s) for k, v in dangling.items())
        dangling_nodes = [n for n in W if W.out_degree(n, weight=weight) == 0.0]

        # power iteration: make up to max_iter iterations
        for _ in range(max_iter):
            xlast = x
            x = dict.fromkeys(xlast.keys(), 0)
            danglesum = alpha * sum(xlast[n] for n in dangling_nodes)
            for n in x:

                # this matrix multiply looks odd because it is
                # doing a left multiply x^T=xlast^T*W
                for nbr in W[n]:
                    x[nbr] += alpha * xlast[n] * W[n][nbr][weight]
                x[n] += danglesum * dangling_weights[n] + (1.0 - alpha) * p[n]

            # check convergence, l1 norm
            err = sum([abs(x[n] - xlast[n]) for n in x])
            if err < N * tol:
                return x
        raise NetworkXError('pagerank: power iteration failed to converge '
                            'in %d iterations.' % max_iter)

    dc,cn,bc = "","",""
    outer,inner=1,0
    c1,c2,form=0,0,0
    referer = ""
    common = {}
    for i in sorted(mydata):
        outer+=1
        URL = i[0]
        a = i[1]
        # session,payment, method, form
        common[URL] = [i[-2], i[-1], i[2], i[6], i[7]]
        #number of form tags
        if URL in common:
            common[URL][4] += i[7]
        if URL in myglobal:
            list = myglobal[URL]
            list[0] += 1
        else:
            myglobal[URL] = [1, 0]
        if a in myglobal:
            list = myglobal[a]
            list[1] += 1
        else:
            myglobal[a] = [0, 1]
        for j,k in enumerate(i):
            inner+=1
            if inner==14:
                inner=1
            ws2.cell(row=outer, column=inner).value = k


    wbnew.save('new_excel.xlsx')
    maxm=2
    method=0
    print(myglobal)
    for i in myglobal:
        ws3.cell(row=maxm,column=1).value = i
        l = myglobal[i]
        ws3.cell(row=maxm,column=2).value = l[0]
        ws3.cell(row=maxm,column=3).value = l[1]
        ws3.cell(row=maxm, column=4).value = ics[i]
        ws3.cell(row=maxm, column=5).value = ocs[i]
        ws3.cell(row=maxm, column=6).value = cns[i]
        ws3.cell(row=maxm, column=7).value = pns[i]
        ws3.cell(row=maxm, column=8).value = ens[i]
        ws3.cell(row=maxm, column=9).value = pgs[i]
        if i in common:
            c1 = common[i][0]
            c2 = common[i][1]
            method = check_request_method(common[i][2])
            referer = common[i][3]
            form = common[i][4]
        ws3.cell(row=maxm, column=10).value = c1
        ws3.cell(row=maxm, column=11).value = c2
        ws3.cell(row=maxm, column=12).value = form
        ws3.cell(row=maxm, column=13).value = method
        ws3.cell(row=maxm, column=14).value = referer
        maxm+=1
    wbnew2.save('data_excel.xlsx')
    nx.draw(G, with_labels=True)
    plt.show()

if __name__ == "__main__":
    # calling main function
    main()