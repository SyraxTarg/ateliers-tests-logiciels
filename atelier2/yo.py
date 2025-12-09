class Laboratory():

    def __init__(self, substances: list[str]):

        self.stock = []

        for s in substances:
            self.stock.append(
                {
                    "name":s,
                    "quantity": 0
                }
            )

    def getQuantity(self, substance: str)-> float:
        found_substance = ""
        index = -1
        for s in self.stock:
            index += 1
            if s["name"] == substance:
                found_substance = s
                break
        if found_substance == "":
            raise Exception("No such substance in stock")

        quantity = self.stock[index]["quantity"]
        print(quantity)
        return quantity


substances = [
            "ethanol",
            "copper",
            "bleach",
            "azote",
            "salt",
            "antimatter"
        ]
l = Laboratory(substances)
l.getQuantity("azote")