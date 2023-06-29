import pymongo
import os

from ..configuration.config import Config

# pymongo
url = Config.PYMONGO_URL
tlsCAFile = Config.tlsCAFile
client = pymongo.MongoClient(url, tlsCAFile=tlsCAFile)
db_production = client['test_database']

col_orders = db_production["test_orders"]
col_owners = db_production["test_owners"]
col_carwashes_admins = db_production["test_carwashes_admins"]
col_carwashes = db_production["test_carwashes"]
col_prices = db_production["test_prices"]
col_sets_of_prices = db_production["sets_of_prices"]
col_companies = db_production["test_companies"]
col_networks = db_production["test_networks"]
col_users = db_production["test_users"]

