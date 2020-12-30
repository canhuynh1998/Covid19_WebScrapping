import requests
from bs4 import BeautifulSoup

global statelookup
statelookup = [
    ("california","usa/california/"), ("texas" ,"usa/texas/"), ("florida", 'usa/florida/'), ("illinois" ,"usa/illinois/"),
    ("newyork" ,"usa/new-york/"), ("ohio" ,"usa/ohio/"), ("georgia", "usa/georgia/"), ("pennsylvania", "usa/pennsylvania/"),
    ("tennessee", "usa/tennessee/"), ("michigan", "usa/michigan/"), ("northcarolina" ,"usa/north-carolina/") ,("indiana" ,"usa/indiana/"),
    ("arizona" ,"usa/arizona/"), ('wisconsin' ,'usa/wisconsin/'), ('newjersey' ,'usa/new-jersey/'),
    ('minnesota','usa/minnesota/'), ('missouri','usa/missouri/'), ('massachusetts' ,'usa/massachusetts/'),
    ('alabama','usa/alabama/'), ('virginia','usa/virginia/'), ('colorado','usa/colorado/'), ('louisiana','usa/louisiana/'),
    ('south-carolina','usa/south-carolina/'), ('iowa','usa/iowa/'), ('oklahoma','usa/oklahoma/'),('maryland','usa/maryland/'),
    ('utah','usa/utah/'), ('kentucky','usa/kentucky/'), ('washington','usa/washington/'),('nevada','usa/nevada/') ('arkansas','usa/arkansas/'),
    ('kansas','usa/kansas/'), ('mississippi','usa/mississippi/'), ('connecticut','usa/connecticut/'), ('nebraska','usa/nebraska/') , ('new-mexico','usa/new-mexico/'),
    ('',''),
]

class Scrapper:
    
    def __init__(self):
        
        self.counties = self.getCounties()
        self.USA = self.getUSA()
        
    
    def scrap(self, isUSA, state=''):
        URL = 'https://www.worldometers.info/coronavirus/'
        if isUSA:
            URL += 'country/us'
        else:
            URL += state
            print(URL)
        html = requests.get(URL)
       # print(state)
        soup = BeautifulSoup(html.text, 'lxml')
                                            # id="usa_table_countries_today"
        table = soup.find("table", attrs={"id" : "usa_table_countries_today"})
        # print(table)
        # # if not table.tbody():
        # #     return
        if table is None:
            print('There is no available information!')
            return []
        head = table.tbody.find_all("tr")
        return head
    

    def getCounties(self):
        headings = []
        for idx in range(len(statelookup)):
            county = statelookup[idx][1]
            head = self.scrap(False, county)
            

            for i in range(len(head)):
                #print('Hi')
                row = []
                td = head[i].find_all('td')
                for i, th in enumerate(td):
                    if i == 6:
                        break
                    value = th.text.replace('\n','').strip()
                    #print(value)
                    if value == '' or value == 'N/A':
                        value = 0
                    if i != 0 and type(value) is str:
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
        print(len(headings))
        print(headings)
        return headings

    
    def getUSA(self):
        head = self.scrap(True)
        headings= []

        for i in range(len(head)):
            row = []
            td = head[i].find_all('td') #find all td tags
            for i, th in enumerate(td):
                if i == 7 :
                    break
                value = th.text.replace('\n','').strip() #elimiate all the white space
                if value == "" or value == 'N/A':
                    value = 0
                if i != 1 and type(value) is str:
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
        print(len(headings))
        print(headings)
        return headings


scrapper = Scrapper()
    
    