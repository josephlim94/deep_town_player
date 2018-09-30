import xml.etree.ElementTree as ET

class MiningFloor:
    def __init__(self):
        self.location = 0
        self.capacity = 150
        self.rpm = 17

    def set_location(self, number):
        self.location = number

class ChemistryMining:
    def __init__(self):
        self.location = 0

    def set_location(self, number):
        self.location = number

class OilMining:
    def __init__(self):
        self.location = 0

    def set_location(self, number):
        self.location = number

class MiningEngine:
    def __init__(self):
        self.mining_floor_xml = ET.parse('mining_floor.xml')
        self.mining_floor_root = self.mining_floor_xml.getroot()
        self.raw_material_xml = ET.parse('raw_material.xml')
        self.raw_material_root = self.raw_material_xml.getroot()
        self.stations = list()
        self.chem_mines = list()
        self.oil_mines = list()
        self.prod_data_set = dict()

    def set_mining_station(self, station):
        self.stations.append(station)

    def set_chemistry_mining(self, chem_mining):
        self.chem_mines.append(chem_mining)

    def set_oil_mining(self, oil_mining):
        self.oil_mines.append(oil_mining)

    def get_production_rate(self):
        for station in self.stations:
            # get production info from each station
            # save them into a set
            for floor in self.mining_floor_root.findall("./area/[number='" + str(station.location) + "']"):
                #print("Floor: " + floor.find('number').text)
                for material in floor.findall("./material"):
                    print(material.find("name").text, material.find("probability").text)
                    material_name = material.find("name").text
                    material_probability = float(material.find("probability").text)/100
                    if material_name not in self.prod_data_set:
                        prod_data = ProductionData()
                        prod_data.name = material_name
                        prod_data.period = 1
                        material_data = self.raw_material_root.find("./item/[name='" + material_name + "']")
                        if material_data:
                            prod_data.price = float(material_data.find("price").text)
                        self.prod_data_set[material_name] = prod_data
                    self.prod_data_set[material_name].rate += float(station.rpm)*material_probability

        for station in self.chem_mines:
            pass

        for station in self.oil_mines:
            pass

        for material_name in self.prod_data_set:
            material = self.prod_data_set[material_name]
            material.amount = material.rate * material.period

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