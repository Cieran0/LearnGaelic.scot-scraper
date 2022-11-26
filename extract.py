#!/usr/bin/python
from requests_html import HTMLSession

def printRow(rows, i):
    row = rows[i]
    g = row.split(' ')[3].split('>')[1].split('<')[0]
    a = row.split('src=\"')[3].split('\"')[0]
    e = row.split('<td>')[2].split('<')[0]
    if(e == ""):
        e = []
        b = row.split('<td>')[2].split('</span> ')
        for x in b:
            y = (x.split('</'))
            if(len(y) > 1):
                e.append(y[0].strip())
    print(row.split('<div class=\"dictionary_item-term headword\">')[1].split('<')[0])
    print(e)
    print(a)
    return



session = HTMLSession()
addrs = "https://www.learngaelic.scot/dictionary/index.jsp?abairt=|&slang=both&wholeword=true"
abairt = "person"
r = session.get(addrs.replace('|',abairt))
r.html.render()
rows = []
for i in range(0,100):
    row = r.html.find('#' + str(i), first=True)
    if(row == None): 
        break
    rows.append(row.html)

if(len(rows) == 0):
    print("Request failed, the Scottish Goverment can fuck off!")
    exit(-1)

q = 1
print("["+str(q)+"]")
printRow(rows, q)