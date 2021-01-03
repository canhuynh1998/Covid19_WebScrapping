from Database import Database
from Scrapper import Scrapper

def Welcome():
    '''
    Greeting Message
    '''
    print('\t~~~~~~Welcome to My Program~~~~~~')

def GoodBye():
    '''
    Good bye Message
    '''
    print('\tThank You and Wear Your Mask!!!')

def LookUp(collection, data):
    return Database.find_one(collection,data)

def displayData(collection, data):
    
    if collection == 'States':
        print('{} state has total {} cases and {} total death cases'.format(str(data['state']), str(data["totalCases"]), str(data['totalDeath'])))
        print('There have been {} new cases and {} new deaths since the last look up"'.format(str(data['newCases']), str(data["newDeaths"])))
    else:
        print('{} county of {} state has total {} cases and {} total death cases"'.format(str(data['county']) ,str(data['state']), str(data["totalCases"]), str(data['totalDeath'])))
        print('There have been {} new cases and {} new deaths since the last look up'.format(str(data['newCases']), str(data["newDeaths"])))       
    print('\n')

def stringProcessing(string):
    string = string.lower()
    string = string.title()
    return string

if __name__ == "__main__":
    Welcome()
    scrapper = Scrapper()
    Database.initialize()
    # Database.update('States', scrapper.states)
    # Database.update('Counties', scrapper.counties)
    print('\n')
    run = True
    while run:
        customerOption= input("What kind of data do you want to search for? ")
        collection, key, value = None, None, None
        if customerOption == '1':
            collection = 'States'
            key = 'state'
            value = input("Which state?") 
        else:
            collection = 'Counties'
            key = 'county'
            value = input("Which county?")

        value = stringProcessing(value)
        returnData = LookUp(collection, {key:value})
        
        try:
            displayData(collection, returnData)
        except:
            returnData = LookUp('States', {'_id':0})
            displayData("States", returnData)
        
        keepSearching = input("Do you want to continue searching?(y/n)")
        if keepSearching.lower() != 'y':
            run = False
    GoodBye()
'''
FIND HOW TO TRACK WHEN IS THE LAST TIME THE PROGRAM RUN
'''