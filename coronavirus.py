import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


url = 'https://www.worldometers.info/coronavirus/'

r = requests.get(url)
# parsing to bs4
html = r.text
soup = BeautifulSoup(html,'html.parser')


print(soup.title.text)
print()
live_data = soup.find_all('div',id='maincounter-wrap')
for i in live_data:
    print(i.text)

print()
print('Analisis berdasarkan per-negara')
print()
# ekstrak tabel
table_body = soup.find('tbody')
table_rows = table_body.find_all('tr')

countries = []
cases = []
todays = []
deaths = []
recovered = []

for tr in table_rows:
    td = tr.find_all('td')
    countries.append(td[0].text)
    cases.append(td[1].text)
    todays.append(td[2].text.strip())
    deaths.append(td[3].text.strip())
    recovered.append(td[5].text.strip())

indices = [i for i in range(1,len(countries)+1)]
headers = ['Countries','Total Cases','Todays Cases','Deaths','Total Recovered']
df = pd.DataFrame(list(zip(countries,cases,todays,deaths,recovered)),columns=headers,index=indices)
df.to_csv('analisiscorona.csv')
print(df)

# plotting graph
y_pos = list(range(len(countries)))

plt.bar(y_pos,cases[::-1],align='center',alpha=0.5)
plt.xticks(y_pos,countries[::-1],rotation=80)
plt.ylabel('Total Cases')
plt.title('Persons affected by Corona Virus slurrr')
plt.savefig('analisiscorona.png',dpi=600)
plt.show()