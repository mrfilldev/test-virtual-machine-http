class Order:

    def __init__(self, _id, CarWashId, BoxNumber, ContractId, Sum, Status, DateCreate, SumCompleted, SumPaidStationCompleted):

        self.id = _id
        self.CarWashId = CarWashId
        self.BoxNumber = BoxNumber
        self.ContractId = ContractId
        self.Sum = Sum
        self.Status = Status
        self.DateCreate = DateCreate
        self.SumPaidStationCompleted = SumCompleted
        self.SumCompleted = SumPaidStationCompleted
