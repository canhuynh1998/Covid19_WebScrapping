'''
Database class,
We are not going to create many instance of different database so everything will be static

'''
import pymongo 
from pymongo import MongoClient
from Scrapper import Scrapper
import time
start_time = time.time()
class Database:
    CONNECTION = "mongodb+srv://canhuynh:can1234@cluster0.dehxw.mongodb.net/Covid19?retryWrites=true&w=majority"
    #CONNECTION = "mongodb+srv://canhuynh:<password>@cluster0.dehxw.mongodb.net/<dbname>?retryWrites=true&w=majority"
    DATABASE = None

    @staticmethod
    def initialize():
        '''
        Initialize the Database
        '''
        cluster = MongoClient(Database.CONNECTION)
        Database.DATABASE = cluster['Covid19']

    @staticmethod
    def insert(collection, data):
        '''
        Insert 1 document to the collection at a time
        '''
        Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def find_one(collection, data):
        '''
        Return the desired document type dictionary
        '''
        return Database.DATABASE[collection].find_one(data)
    
    @staticmethod
    def update(collection, data):
        '''
        Update document to the most recent data
        '''

        def updateHelper(data, key, existing):
            '''
            Calculate data that was deleted from the original web page
            '''
            if type(data[key]) is str or type(existing[key]) is str:
                return
            if key == "newCases":
                return data["totalCases"] - existing["totalCases"]
            else:
                return data["totalDeath"] - existing["totalDeath"]
                
        currentCollection = Database.DATABASE[collection]
        collectionLength = len(list(currentCollection.find()))  #length of the collection

        index = 0
    
        while index < collectionLength:
            existing = currentCollection.find_one({'_id': index})
            currentValue = data[index]
            for key, value in currentValue.items():
                if key == "newCases" or key == "newDeaths":
                    value = updateHelper(currentValue, key, existing)
                if key == "_id" or key == "county" or key == "state":
                    continue
                currentCollection.update_one({'_id':index},{"$set":{key:value}})
            index += 1




# Database.initialize()

# # # # Insert 
# scrapper = Scrapper()
# print(len(scrapper.counties))
#states = scrapper.states
# # # #print(states)
# # # counties = scrapper.counties
# # #print(counties)
# Database.DATABASE['Counties'].delete_many({})
# Database.DATABASE['States'].delete_many({})
# for county in scrapper.counties:
#     print(county)
#     Database.insert('Counties', county)
# for state in scrapper.states:
#     Database.insert('States',state)
# Database.update('States', scrapper.states)
# Database.update('Counties', scrapper.counties)
# print("--- %s seconds ---" % (time.time() - start_time))
