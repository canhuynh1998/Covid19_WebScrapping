'''
Database class,
We are not going to create many instance of different database so everything will be static

'''
import pymongo 
from pymongo import MongoClient
from Scrapper import Scrapper

class Database:
    CONNECTION = "mongodb+srv://canhuynh:can1234@cluster0.dehxw.mongodb.net/Covid19?retryWrites=true&w=majority"
    DATABASE = None

    @staticmethod
    def initialize():
        cluster = MongoClient(Database.CONNECTION)
        Database.DATABASE = cluster['Covid19']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert_one(data)
    
    @staticmethod
    def find(collection, data):
        return Database.DATABASE[collection].find(data)

    @staticmethod
    def find_one(collection, data):
        return Database.DATABASE[collection].find_one(data)


Database.initialize()

# Insert 
# scrapper = Scrapper()
# states = scrapper.USA

# for state in states:
#     Database.insert('States', state)

Database.DATABASE['States'].delete_many({})