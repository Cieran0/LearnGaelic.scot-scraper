#!/usr/bin/python
from requests_html import HTMLSession

def getRows(abairt): 
    session = HTMLSession()
    addrs = "https://www.learngaelic.scot/dictionary/index.jsp?abairt=|&slang=both&wholeword=true"
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
    return rows

def getData(rows, i):
    row = rows[i].replace('<i>','').replace('</i>','').replace('&amp;','&')
    g = row.split('<div class=\"dictionary_item-term headword\">')[1].split('<')[0]
    a = ""
    try:
        a = row.split('src=\"')[3].split('\"')[0]
    except:
        pass
    e = []
    e = row.split('<td>')[2].split('<')
    if(e[0] == ""):
        e = []
        b = row.split('<td>')[2].split('</span> ')
        for x in b:
            y = (x.split('</'))
            if(len(y) > 1):
                e.append(y[0].strip())
    else:
        e = [e[0]]
    return g,a,combine(e)

def combine(s):
    concat = s[0]
    for i in range(1, len(s)):
        concat = concat + ' / ' + s[i]
    return concat

def displayData(rows, start, count):
    nRows = []
    if count > len(rows):
        count = len(rows)

    for i in range(start,count):
        g,a,e = getData(rows,i)
        nRows.append((f'{[i]}' ,g, e))
    lens = []
    for col in zip(*nRows):
        lens.append(max([len(v) for v in col]))
    format = "  ".join(["{:<" + str(l) + "}" for l in lens])
    for row in nRows:
        print(format.format(*row))

def getAbairt():
    return input('Enter word in Gàidhlig or English: ')

def saveWord(rows,i):
    print('Saving...')
    g,a,e = getData(rows,i)
    with open("gàidhlig.txt", "a") as myfile:
        myfile.write(g)
        myfile.write('\n')
    with open("english.txt", "a") as myfile:
        myfile.write(e)
        myfile.write('\n')
    with open("audio.txt", "a") as myfile:
        myfile.write(a)
        myfile.write('\n')
    
def isFirstWordCorrect():
    if input('Is this correct? y/n : ').lower() == "y":
        return True
    else:
        return False

def main():
    abairt = getAbairt()
    rows = getRows(abairt)
    displayData(rows,0,1)
    if isFirstWordCorrect() == True:
        saveWord(rows,0)
        print('Goodbye!')
        exit(0)
    else:
        displayData(rows,0,len(rows))
        index = input('Type the number of the correct row: ')
        try:
            saveWord(rows,int(index))
        except:
            print('Invalid row')
            print('Goodbye!')
            exit(-1)
    print('Goodbye!')

main()