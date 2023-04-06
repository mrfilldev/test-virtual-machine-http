import json
from datetime import datetime
from types import SimpleNamespace

from bson import json_util
from flask import session

from configuration.config import Config
from main import oauth_via_yandex
from db import database
from . import login


users = database.col_users


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


class User:

    def __init__(self, username, email, isActive, role):
        self.username = username
        self.email = email
        self.isActive = isActive
        self.role = role
        self.timestamp = datetime.now()


    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @login.user_loader
    def load_user(self):
        user = oauth_via_yandex.get_user(session['ya-token'])

        u = users.find_one({"login": user['login']})

        if not u:
            return None
        return User(
            username=u['Name'],
            email=u['email'],
            isActive=u['isActive'],
            role=u['role'],
        )

    # # @login_manager.user_loader
    # # def load_user(user_id):
    # #     return User.get_id(user_id)
