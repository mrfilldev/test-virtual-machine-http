import enum
from datetime import datetime

from ..db import database

# from new_project.app import login


users = database.col_users


class Types(enum.IntEnum):
    SelfServiceFixPrice = 1  # автомойка самообслуживания Fix Price
    SelfService = 2  # автомойка самообслуживания
    Contactless = 3  # безконтактная
    Manual = 4  # ручная мойка
    Portal = 5  # портальная
    Tunnel = 6  # тунельная
    Dry = 7  # сухая


class StatusOrder(enum.IntEnum):
    OrderCreated = 10  # заказ создан и полностью оплачен
    Completed = 20  # заказа завершен успешно
    CarWashCanceled = 30  # заказ отменен интегрируемой системой
    UserCanceled = 40  # заказ отменен пользователем
    Expire = 50  # статус от интегрируемой системы не поступил в течение 3 часов
    SystemAggregator_Error = 60  # Внутренняя ошибка

    def StatusOrderToDispaly(self, category):
        if category == StatusOrder.OrderCreated:
            return 'Заказ создан'
        elif category == StatusOrder.Completed:
            return 'Заказ выполнен'
        elif category == StatusOrder.CarWashCanceled:
            return 'Заказ отменен мойкой'
        elif category == StatusOrder.UserCanceled:
            return 'Заказ отменен пользователем'
        elif category == StatusOrder.Expire:
            return 'Заказ не актуален'
        elif category == StatusOrder.SystemAggregator_Error:
            return 'Заказ не выполнен'
        else:
            return category


class CategoryAuto(enum.IntEnum):
    Compact = 10
    MiddleSize = 20
    Crossover = 30
    OffRoad = 40
    MicroBus = 50

    def CategoryAutoToDispaly(self, category):
        if category == CategoryAuto.Compact:
            return 'Кат.1'
        elif category == CategoryAuto.MiddleSize:
            return 'Кат.2'
        elif category == CategoryAuto.Crossover:
            return 'Кат.3'
        elif category == CategoryAuto.OffRoad:
            return 'Кат.4'
        elif category == CategoryAuto.MicroBus:
            return 'Кат.5'
        else:
            return category


class BoxStatus(enum.IntEnum):
    Free = 1  # – свободен
    Busy = 2  # - занят
    Unavailable = 3  # – недоступен(закрыт на ремонте)


class CostType(enum.IntEnum):
    Fix = 1  # – фиксированная
    PerMinute = 2  # – стоимость


class Boxes:
    def __init__(self, numbers, boxStatus):
        self.number = numbers
        self.status = boxStatus


class CostIdSum:
    def __init__(self, category, sum):
        self.category = category
        self.sum = sum


class Prices:
    def __init__(self, id, name, description, cost_id_sum, cost_type):
        self.Id = id
        self.name = name
        self.description = description
        self.categoryPrice = cost_id_sum
        self.costType = cost_type


class PricesCarWash:
    def __init__(self, id, category, cost):
        self.Id = id
        self.categoryPrice = category
        self.cost = cost


class Point:  # enum.Enum):
    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.lon = longitude

    def return_list(self):
        list_obj = [self.lat, self.lon]
        return list_obj


class Carwash:
    def __init__(self, id, enable, name, address, Location: Point,
                 Type, stepCost, limitMinCost, Boxes, Price, CarwashAdmin):
        self.Id = id
        self.Enable = enable
        self.Name = name
        self.Address = address
        self.Location = Location
        self.Type = Type
        self.StepCost = stepCost
        self.LimitMinCost = limitMinCost
        self.Boxes = Boxes
        self.Price = Price
        self.CarwashAdmin = CarwashAdmin


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


#
# class Point:  # enum.Enum):
#     def filters(self, latitude, longitude):
#         self.lat = latitude
#         self.lon = longitude
#
#     def return_list(self):
#         list_obj = [self.lat, self.lon]
#         return list_obj

#
# class Carwash:
#     def filters(self, _id, enable, name, address, Location: Point,
#                  Type, stepCost, limitMinCost, Boxes, Price):
#         self.Id = _id
#         self.Enable = enable
#         self.Name = name
#         self.Address = address
#         self.Location = Location
#         self.Type = Type
#         self.StepCost = stepCost
#         self.LimitMinCost = limitMinCost
#         self.Boxes = Boxes
#         self.Price = Price


class Network:
    def __init__(self, _id, network_name):
        self.Id = _id
        self.Name = network_name
        self.Carwashes = []


class User:
    def __init__(self, Id, email, role):
        self.Id = Id
        self.role = role
        self.email = email
        self.date = datetime.now()
        self.networks = []
        self.carwashes = []


class UserRole(enum.Enum):
    admin = 'Администратор'
    network_owner = 'Владелец Сети'
    worker = 'Сотрудник Мойки'

    # @staticmethod
    # def is_authenticated():
    #     return True
    #
    # @staticmethod
    # def is_active():
    #     return True
    #
    # @staticmethod
    # def is_anonymous():
    #     return False
    #
    # def get_id(self):
    #     return self.username

    # @login.user_loader
    # def load_user(self):
    #     user = oauth_via_yandex.get_user(session['ya-token'])
    #
    #     u = users.find_one({"login": user['login']})
    #
    #     if not u:
    #         return None
    #     return User(
    #         username=u['Name'],
    #         email=u['email'],
    #         isActive=u['isActive'],
    #         role=u['role'],
    #     )

    # # @login_manager.user_loader
    # # def load_user(user_id):
    # #     return User.get_id(user_id)
