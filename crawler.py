
import csv
import xml.etree.ElementTree as ET
import re
import networkx as nx
import matplotlib.pyplot as plt



def parseXML(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    # create empty list for news items
    data = []

    for item in root.findall('./{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        data.append(item.text)

    return data

### XML to python..................................
def savetoCSV(requestitems, filename):
    # specifying the fields for csv file

    # writing to csv file
    with open(filename, 'w',newline='') as csvfile:
        # creating a csv dict writer object
        writer = csv.writer(csvfile)
        for val in requestitems:
            writer.writerow([val])
def main():
    # parse xml file
    myxml = 'hv.xml'
    data=parseXML(myxml)
    savetoCSV(data,'myexcel.csv')

if __name__ == "__main__":
    # calling main function
    main()