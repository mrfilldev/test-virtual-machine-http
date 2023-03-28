class Order:

    def __init__(self, _id, CarWashId, BoxNumber, ContractId, Sum, Status, DateCreate, SumCompleted, SumPaidStationCompleted):

        self.Id = _id
        self.CarWashId = int(CarWashId)
        self.BoxNumber = BoxNumber
        self.ContractId = ContractId
        self.Sum = Sum
        self.Status = Status
        self.DateCreate = DateCreate
        self.SumPaidStationCompleted = SumCompleted
        self.SumCompleted = SumPaidStationCompleted
