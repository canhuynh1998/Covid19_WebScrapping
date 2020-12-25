import requests
from bs4 import BeautifulSoup

global statelookup
statelookup = {
    "california" : "usa/california/", "texas" : "usa/texas/", "florida" : 'usa/florida/', "illinois":"usa/illinois/",
    "newyork" : "usa/new-york/", "ohio": "usa/ohio/", "georgia": "usa/georgia/", "pennsylvania": "usa/pennsylvania/",
    "tennessee": "usa/tennessee/", "michigan": "usa/michigan/", "northcarolina":"usa/north-carolina/" ,"indiana":"usa/indiana/",
    "arizona":"usa/arizona/"
    }


class ScrapperTesting():

    def __init__(self):
        self.URL = 'https://www.worldometers.info/coronavirus/'
        self.state = self._getState()
        self.format()


    def scrap(self):
        self.URL += self.state
        html = requests.get(self.URL)
        soup = BeautifulSoup(html.text, 'lxml')
        table = soup.find("table", attrs={"id" : "usa_table_countries_today"})
        head = table.tbody.find_all("tr")

        return head

    def _getState(self):
        checkState = input("Do you want to look up any specific state?(Y/N)")
        state = 'country/us/'
        if 'y' in checkState.lower():
            getState = input("What state do you want to look for?")
            getState = getState.replace(" ","")
            getState = getState.lower().strip()
            if getState in statelookup:
                state = statelookup[getState]
        return state
        
    def format(self):

        #get individual states
        head = self.scrap()
        headings= []

        for i in range(len(head)):
            row = []
            td = head[i].find_all('td') #find all td tags
            for i, th in enumerate(td):
                if i == 6 and self.state != 'country/us/':
                    break
                elif self.state == 'country/us/' and i == 7:
                    break

                value = th.text.replace('\n','').strip() #elimiate all the white space
                if value == "" or value == 'N/A':
                    value = 0
                
                if (i != 1 and self.state == 'country/us/') or (i != 0 and self.state != 'country/us/'):
                    if type(value) is str :
                    #this is for general useage
                        letter = ''
                        for char in value:
                            '''
                            strip the ',' from the number
                            '''
                            if char ==',':
                                continue
                            letter += char
                            letter = letter.strip()
                        value = float(letter)
                row.append(value)
            headings.append(tuple(row))

scaper = Scrapper()