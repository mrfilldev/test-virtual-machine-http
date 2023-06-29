import pymongo
import os

from ..configuration.config import Config


# pymongo
url = Config.PYMONGO_URL
tlsCAFile = Config.tlsCAFile
client = pymongo.MongoClient(url, tlsCAFile=tlsCAFile)
db_test = client['test_database']

col_orders = db_test["test_orders"]
col_owners = db_test["test_owners"]
col_carwashes_admins = db_test["test_carwashes_admins"]
col_carwashes = db_test["test_carwashes"]
col_prices = db_test["test_prices"]
col_sets_of_prices = db_test["sets_of_prices"]
col_companies = db_test["test_companies"]
col_networks = db_test["test_networks"]
col_users = db_test["test_users"]
