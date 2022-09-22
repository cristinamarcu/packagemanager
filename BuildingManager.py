import json
from typing import NamedTuple
from Config import BUILDINGS_FILE_PATH


class ApartmentInfo(NamedTuple):
    name: str
    telephone: str
    email: str


class BuildingManager:
    buildingDict = {}

    def __init__(self, jsonData=None):
        if not jsonData:
            buildingjson = open(BUILDINGS_FILE_PATH)
            jsonData = buildingjson.read()
        self.buildingDict = json.loads(jsonData)

    def getBuildings(self) -> list:
        return list(self.buildingDict.keys())

    def getApartments(self, building) -> list:
        if building in self.buildingDict:
            mylist = []
            for i in range(0, len(self.buildingDict[building])):
                mylist.append(self.buildingDict[building][i]["number"])
            return mylist
        else:
            return []

    def getApartmentInfo(self, building, apartment) -> ApartmentInfo:
        if building in self.buildingDict.keys():
            for elem in self.buildingDict[building]:
                if elem["number"] == apartment:
                    return ApartmentInfo(elem["contact_name"], elem["contact_nr"], elem["email"])
