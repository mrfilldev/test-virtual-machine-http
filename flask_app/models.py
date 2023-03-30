import json
from types import SimpleNamespace

from bson import json_util
from flask import session
from flask_login import LoginManager, UserMixin
from config.config import Config
from flask_app import oauth_via_yandex

from flask_login import current_user, login_user, logout_user, login_required

from flask_app.urls import app

users = Config.col_users
login = LoginManager(app)



class Order:

    def __init__(self, _id, CarWashId, BoxNumber, ContractId, Sum, Status, DateCreate, SumCompleted,
                 SumPaidStationCompleted, ):
        self.Id = _id
        self.CarWashId = int(CarWashId)
        self.BoxNumber = BoxNumber
        self.ContractId = ContractId
        self.Sum = Sum
        self.Status = Status
        self.DateCreate = DateCreate
        self.SumPaidStationCompleted = SumCompleted
        self.SumCompleted = SumPaidStationCompleted


class Point:  # enum.Enum):
    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.lon = longitude

    def return_list(self):
        list_obj = [self.lat, self.lon]
        return list_obj


class Carwash:
    def __init__(self, _id, enable, name, address, Location: Point,
                 Type, stepCost, limitMinCost, Boxes, Price):
        self.Id = _id
        self.Enable = enable
        self.Name = name
        self.Address = address
        self.Location = Location
        self.Type = Type
        self.StepCost = stepCost
        self.LimitMinCost = limitMinCost
        self.Boxes = Boxes
        self.Price = Price


class Network:
    def __init__(self, _id, Name):
        self.Id = _id
        self.Name = Name


class User():
    def __init__(self, _id, Name, Login, Network_Id, Role):
        self.Id = _id
        self.Name = Name
        self.Login = Login
        self.Network_Id = Network_Id
        self.Role = Role

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    @staticmethod
    def get_id(self):
        return self.Name

    @login_manager.user_loader
    def load_user(self):
        user = oauth_via_yandex.get_user(session['ya-token'])

        u = users.find_one({"Login": user['login']})
        data = json.loads(json_util.dumps(u))
        data = json.dumps(data, default=lambda x: x.__dict__)
        u = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

        user['access_level'] = u['access_level']
        user['date_registered'] = u['date_registered']
        user['company_name'] = u['company_name']
        user['inn'] = u['inn']

        if not u:
            return None
        return user

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.get_id(user_id)
