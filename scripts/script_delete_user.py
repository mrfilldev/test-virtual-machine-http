from config.config import Config

x = Config.col_users.delete_one({"_id": 'namespace($oid="641aea4acdb05bc1a79167aa")'})
print(f'user: 641aea4acdb05bc1a79167ab has been deleted ', x)
x = Config.col_users.delete_one({"_id": 'namespace($oid="641aea4acdb05bc1a79167ab")'})
print(f'user: 641aea4acdb05bc1a79167ab has been deleted ', x)
