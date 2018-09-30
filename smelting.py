import xml.etree.ElementTree as ET

craftables = ["Copper Bar", "Iron Bar"]

class SmeltingPot:
    def __init__(self):
        self.name = 0
        self.rate = 1
        self.period = 0
        self.amount = 0

    def set_name(self, name):
        self.name = name
        # also get related item data from xml

class SmeltingFloor:
    def __init__(self):
        self.smelting_xml = ET.parse('smelting.xml')
        self.smelting_root = self.smelting_xml.getroot()
        self.raw_material_xml = ET.parse('raw_material.xml')
        self.raw_material_root = self.raw_material_xml.getroot()
        self.smelting_pot = list()
        self.prod_data_set = dict()

    def set_smelting_pot(self, pot):
        self.smelting_pot.append(pot)

    def get_production_rate(self):
        for smelting_pot in self.smelting_pot:
            # get production info from each station
            # smelting pot already have it's item smelted set and item data obtained
            item_name = smelting_pot.name
            item_xml = self.smelting_root.find("./item/[name='" + item_name + "']")
            # save item produced from smelting pot
            prod_data = ProductionData()
            prod_data.name = item_xml.find("name").text
            prod_data.price = float(item_xml.find("price").text)
            prod_data.period = int(item_xml.find("production").find("time").text)
            prod_data.amount = int(item_xml.find("production").find("amount").text)
            prod_data.rate = float(prod_data.amount)/prod_data.period
            for source in item_xml.findall("./source"):
                source_data = SourceData(source.find("name").text, int(source.find("amount").text))
                prod_data.source_list.append(source_data)
            # put it into the set
            if prod_data.name not in self.prod_data_set:
                self.prod_data_set[prod_data.name] = prod_data
            else:
                self.prod_data_set[prod_data.name].rate += prod_data.rate

        return self.prod_data_set

class SourceData:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

class ProductionData:
    def __init__(self):
        self.name = 0
        self.rate = 0.0
        self.period = 0
        self.amount = 0
        self.price = 0.0
        self.source_list = list()

    def get_name(self):
        return self.name