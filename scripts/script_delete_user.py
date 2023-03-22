from config.config import Config

x = Config.col_users.delete_one({"name": 'Admin'})
print(f'user: Admin has been deleted ', x)
x = Config.col_users.delete_one({"name": 'Username'})
print(f'user: Username has been deleted ', x)
