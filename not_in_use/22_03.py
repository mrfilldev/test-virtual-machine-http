import enum
import json


class BoxStatus(enum.IntEnum):
    Free = 1  # – свободен
    Busy = 2  # - занят
    Unavailable = 3  # – недоступен(закрыт на ремонте)


class Boxes:
    def __init__(self, numbers, boxStatus):
        self.number = numbers
        self.status = boxStatus


def create_boxes(amount_boxes: int):
    group_of_boxes = []
    for i in range(1, amount_boxes + 1):
        group_of_boxes.append(Boxes(i, BoxStatus.Free.name))

    result = group_of_boxes
    print('result', result)
    return result


new_amount = 20

new_carwash_json = json.dumps(create_boxes(new_amount), default=lambda x: x.__dict__)
new_carwash_dict = json.loads(new_carwash_json)  # , object_hook=lambda d: SimpleNamespace(**d))

print(new_carwash_dict)
