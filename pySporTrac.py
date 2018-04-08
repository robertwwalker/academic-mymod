#! /usr/bin/python
import pandas as pd
import bs4
import re
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
base_url = "http://www.spotrac.com/nfl/"
def get_page(url):
    page = urlopen(base_url)
    soup = BeautifulSoup(page, 'lxml')
    file = open("spotrac_urls.txt", 'w')
    file.write(str(soup))
    file.close()
def get_team_table(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
get_page(base_url)
with open("spotrac_urls.txt", 'r') as file:
    for line in file:
        line = line.strip()
from bs4 import BeautifulSoup
page = open("spotrac_urls.txt", 'r')
soup = BeautifulSoup(page, "lxml")
div = soup.find("div","subnav-posts")
import re
links = div.find_all('a')
for link in links:
    print(link.get('href'))
len(links)
from urllib.request import urlopen
def get_team_table(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
    data_rows = [row for row in soup.find("table", "datatable").find_all("tr")]
    return data_rows
# create an empty list
team_data = []

for link in links:
    team_data.append(get_team_table(link.get('href')))

len(team_data)

#data_rows = [row for row in soup.find("td", "center").find_all("tr")]
table_data = []

#soup = BeautifulSoup(team_data[0], 'lxml')

#This needs to be a nested for loop because inner items of the list are BeautifulSoup Elements
for row in team_data:
    for element in row:
        #print(type(element))
        if soup.find_all("td", attrs={"class":" right xs-hide "}) is not None:
            table_data.append(element.get_text())

player_data = []
for row in table_data:
    player_data.append(row.split("\n"))
    #print(player_data)

len(player_data)

import pandas as pd
df = pd.DataFrame(player_data)
df = df.drop(14, 1)
df = df.drop(0, 1)
df = df.drop(1, 1)


df = df.drop(df.index[[0]])
#df.set_index(1, inplace=True)
print(df.shape)
df.head()

players = []
for row in team_data[0]:
    if row.get_text("tr") is not None:
        players.append(row) 

column_headers = [col.get_text() for col in players[0].find_all("th") if col.get_text()]
len(column_headers)

df.columns = column_headers
df.head()

#The header repeated itself in the data.  This didn't reveal itself until the data type conversion step below
#but this fixes all occurrences of it.
rows_to_be_dropped = df.loc[df['Cap Hit'] == 'Cap %'].index
df = df.drop(rows_to_be_dropped)

#Apply a regex to convert the 'Cap Hit' column from a string to a float.  
# df['Cap Hit'] =(df['Cap Hit'].replace('[\$,)]', "", regex=True).replace( '[(]','-',   regex=True ).astype(float))

# My fix
df['Cap Hit'] = (df['Cap Hit'].replace('[\$,)]', "", regex=True).replace('[-,)]', "", regex=True).replace('\s\s.*', "", regex=True).astype(float))
df['Base Salary'] = (df['Base Salary'].replace('[\$,)]', "", regex=True).replace('[-,)]', "", regex=True).astype(float))
df['Signing Bonus'] = (df['Signing Bonus'].replace('[\$,)]', "", regex=True).replace('[-,)]', "", regex=True).astype(float))
df['Roster Bonus'] = (df['Roster Bonus'].replace('[\$,)]', "", regex=True).replace('[-,)]', "", regex=True).astype(float))
df['Option Bonus'] = (df['Option Bonus'].replace('[\$,)]', "", regex=True).replace('[-,)]', "", regex=True).astype(float))
df['Workout Bonus'] = (df['Workout Bonus'].replace('[\$,)]', "", regex=True).replace('[-,)]', "", regex=True).astype(float))
df['Restruc. Bonus'] = (df['Restruc. Bonus'].replace('[\$,)]', "", regex=True).replace('[-,)]', "", regex=True).astype(float))
df['Misc.'] = (df['Misc.'].replace('[\$,)]', "", regex=True).replace('[-,)]', "", regex=True).astype(float))
df['Dead Cap'] = (df['Dead Cap'].replace('\(',"",regex=True).replace('\)',"",regex=True).replace('[\$,)]', "", regex=True).replace('[-,)]', "", regex=True).astype(float))

#Sanity check to make sure it worked.
df['Cap Hit'].sum()

df.to_csv("NFLSalData.csv")

df2 = pd.DataFrame(rows_to_be_dropped)
df2.to_csv("NFLRowsD.csv")

