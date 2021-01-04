from Database import Database
from Scrapper import Scrapper
import os.path, time
# millis = int(time.time())
# print(millis)
# print((os.path.getatime("main.py")))
# print(os.path.getmtime("main.py"))
# print("last modified: %s" % time.ctime(os.path.getatime("main.py")))
# print("created: %s" % time.ctime(os.path.getctime("main.py")))


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

def isUpdating():
    lastAccessTime = os.path.getatime("main.py")
    currentAccessTime = time.time()
    return int(currentAccessTime - lastAccessTime) > 43200
    
def displayData(collection, data):
    
    if collection == 'States':
        print('{} state has total {} cases and {} total death cases'.format(str(data['state']), str(data["totalCases"]), str(data['totalDeath'])))
        print('There have been {} new cases and {} new deaths since the last look up'.format(str(data['newCases']), str(data["newDeaths"])))
    else:
        print('{} county of {} state has total {} cases and {} total death cases'.format(str(data['county']) ,str(data['state']), str(data["totalCases"]), str(data['totalDeath'])))
        print('There have been {} new cases and {} new deaths since the last look up'.format(str(data['newCases']), str(data["newDeaths"])))       
    print('\n')

def stringProcessing(string):
    string = string.lower()
    string = string.title()
    return string

if __name__ == "__main__":
    Welcome()
    Database.initialize() 
    
    if isUpdating():
        scrapper = Scrapper()
        Database.update('States', scrapper.states)
        Database.update('Counties', scrapper.counties)
        print('Everything is up to date!!')
    
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
