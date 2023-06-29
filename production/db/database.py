import pymongo
import os

from ..configuration.config import Config

# pymongo
url = Config.PYMONGO_URL
tlsCAFile = Config.tlsCAFile
client = pymongo.MongoClient(url, tlsCAFile=tlsCAFile)
db_test = client['test_database']

db_production = client['production_db']

col_orders = db_production["production_orders"]
col_owners = db_production["production_owners"]
col_carwashes_admins = db_production["production_carwashes_admins"]
col_carwashes = db_production["production_carwashes"]
col_prices = db_production["production_prices"]
col_sets_of_prices = db_production["production_sets_of_prices"]
col_companies = db_production["production_companies"]
col_networks = db_production["production_networks"]
col_users = db_production["production_users"]

