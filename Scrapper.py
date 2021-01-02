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
    ('utah','usa/utah/'), ('kentucky','usa/kentucky/'), ('washington','usa/washington/'),('nevada','usa/nevada/') ,('arkansas','usa/arkansas/'),
    ('kansas','usa/kansas/'), ('mississippi','usa/mississippi/'), ('connecticut','usa/connecticut/'), ('nebraska','usa/nebraska/') , ('new-mexico','usa/new-mexico/'),
    ('idaho','usa/idaho/'),('oregon','usa/oregon/'), ('south-dakota','usa/south-dakota/'), ('north-dakota','usa/north-dakota/'), ('rhode-island','usa/rhode-island/'),
    ('west-virginia','usa/west-virginia/'),('montana','usa/montana/'), ('delaware','usa/delaware/'),('alaska','usa/alaska/'), ('wyoming','usa/wyoming/'),
    ('usa/new-hampshire/','new-hampshire'),('district-of-columbia','usa/district-of-columbia/') ,('maine','usa/maine/'), ('hawaii','usa/hawaii/'),
    ('vermont','usa/vermont/')
]

class Scrapper:
    
    def __init__(self):
        self.counties = self.formatCounties()
        #print(self.counties)
        self.states = self.formatStates()
        print('Everything is ready!!')
        
    
    def scrap(self, isUSA, state=''):
        URL = 'https://www.worldometers.info/coronavirus/'
        if isUSA:
            URL += 'country/us'
        else:
            URL += state
            #print(URL)
        html = requests.get(URL)
        soup = BeautifulSoup(html.text, 'lxml')                                       
        table = soup.find("table", attrs={"id" : "usa_table_countries_today"})
        if table is None:
            #print('There is no available information!')
            return []
        head = table.tbody.find_all("tr")
        return head
    

    def getCounties(self):
        '''
        Scrapping data publicly available for all counties of USA
        Traverse through the statelookup global list to access URL for each state.
        Return a list of tuple as tuple will protect data from accidentally modifying 
        Each tuple contains important data for each state.
        (Name, Total Cases, New Cases, Total Death, New Death, Active Case )
        '''
        headings = []
        print('Generating data')
        states = 0
        for idx in range(len(statelookup)):
            county = statelookup[idx][1]
            head = self.scrap(False, county)
            state = statelookup[idx][0]
            if '-' in state:
                state = state.replace('-',' ')
            state = state.title()
            states += 1
            for i in range(1,len(head)):
                row = []
                td = head[i].find_all('td')
                #print(td[0].text.replace('\n','').strip())
                for i, th in enumerate(td):
                    if i == 6:
                        break
                    value = th.text.replace('\n','').strip()
                    if value == '' or value == 'N/A':
                        value = 0   #Default Value
                    
                    #This block is to convert all numeric data from String into integer
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
                row.append(state)
                headings.append(tuple(row))
        return headings

    
    def getUSA(self):
        '''
        Scrapping data for all states of USA
        Return a list of tuple as tuple will protect data from accidentally modifying 
        Each tuple contains important data for each state.
        (Name, Total Cases, New Cases, Total Death, New Death, Active Case )
        '''
        head = self.scrap(True)
        headings= []
        print('Loading')
        for i in range(len(head)):
            row = []
            td = head[i].find_all('td') #find all td tags
            for i, th in enumerate(td):
                if i == 8 :
                    break
                if i == 6:
                    continue
                value = th.text.replace('\n','').strip() #eliminate all the white space
                if value == "" or value == 'N/A':
                    value = 0   # Default Value
                
                #This block is to convert all numeric data from String into integer
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
        return headings


    def formatStates(self):
        '''
        Reformat the instance list self.states to have the same format with MongoDB
        Return a list of dictionaries since MongoDB requires dictionary formatted
        Keys for these dictionaries are also keys for searching in MongoDB
        '''
        results = []
        print('Generating data')
        for state in self.getUSA():
            result = {  "_id":None,
                        "states":None,
                        "totalCases":None,
                        "newCases": None,
                        "totalDeath":None,
                        "newDeaths":None,
                        "activeCases":None 
                        }
            i = 0
            #Assign the correct value to the correct key
            while i < len(state):
                if i == 0:
                    result['_id'] = int(state[i])
                elif i == 1:
                    result['states'] = state[i]
                elif i == 2:
                    result['totalCases'] = state[i]
                elif i == 3:
                    result["newCases"] = state[i]
                elif i == 4:
                    result["totalDeath"] = state[i]
                elif i == 5:
                    result["newDeaths"] =state[i]
                else:
                    result["activeCases"] = state[i]
                i += 1
            results.append(result)
        #print(results)
        return results

    def formatCounties(self):
        '''
        Reformat the instance list self.states to have the same format with MongoDB
        Return a list of dictionaries since MongoDB requires dictionary formatted
        Keys for these dictionaries are also keys for searching in MongoDB
        '''
        results = []
        print('Loading')
        for index, state in enumerate(self.getCounties()):
            result = {  "_id":index,
                        "county":None,
                        "state" : None,
                        "totalCases":None,
                        "newCases": None,
                        "totalDeath":None,
                        "newDeaths":None,
                        "activeCases":None 
                        }
            i = 0
            #Assign the correct value to the correct key
            while i < len(state):
                if i == 0:
                    result['county'] = state[i]
                elif i == 1:
                    result['totalCases'] = state[i]
                elif i == 2:
                    result["newCases"] = state[i]
                elif i == 3:
                    result["totalDeath"] = state[i]
                elif i == 4:
                    result["newDeaths"] =state[i]
                elif i == 5:
                    result["activeCases"] = state[i]
                else:
                    result["state"] = state[i]
                i += 1
            results.append(result)
      
        return results

#scrapper = Scrapper()
#print(len(statelookup))
#print("--- %s seconds ---" % (time.time() - start_time))
    