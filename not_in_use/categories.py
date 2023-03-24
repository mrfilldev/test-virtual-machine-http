import enum


class CategoryAuto(enum.IntEnum):
    Compact = 10
    MiddleSize = 20
    Crossover = 30
    OffRoad = 40
    MicroBus = 50


for i in list(CategoryAuto):
    print(i.name)
