import requests
import re
import wget
from bs4 import BeautifulSoup
import os

# UC of Irvine
url = "https://archive.ics.uci.edu/ml/"
r = requests.get(url + "datasets.php")

soup = BeautifulSoup(r.content, 'html.parser') 
table = soup.body.find_all("table", limit = 2)[1]

# get the web page dataset by img tags
for elem in table.find_all('img'):

    # get a tag parent of img tag
    a = elem.find_parent()
    dataset_name = a['href'][len('datasets')+1:]

    # get dataset url web page
    r2 = requests.get(url + a['href'])
    soup2 = BeautifulSoup(r2.content, 'html.parser')

    # find the web paf link in html
    table2 = soup2.body.find_all("table",limit = 3)[2]
    a2 = table2.find_all('a')[0]
    data_path = a2['href']

    # check if every data_path are write in a good format
    if data_path[len(data_path)-1] != "/":
        data_path = data_path + "/"

    # get the dataset files
    r3 = requests.get(url + data_path[3:])
    soup3 = BeautifulSoup(r3.content, 'html.parser')

    for tag in soup3.body.ul.find_all('li')[1:]:
        if tag.a['href'] != 'Index':
            path = "data/" + dataset_name
            try:
                os.makedirs(path)
            except FileExistsError:
                # directory already exists
                pass
            source = url + data_path[3:] + tag.a['href']
            dest = path + "/" + tag.a['href']
            wget.download(source, dest) # download the data


# raise error if number of dataset is not good
local_path = 'data'
folder_count = sum(1 for folders in os.listdir(local_path)
    if os.path.isdir(os.path.join(local_path, folders)))

class DirNumber(Exception):
    def __init__(self, message = "File number is not 622"):
        super.__init__(message)


if folder_count != 622:
    raise DirNumber