from typing import NamedTuple
import mysql.connector
from Config import DATABASE_USER, DATABASE_NAME


class DescriptionPackage(NamedTuple):
    building: str
    apartment: str
    date: str
    description: str
    id: str


class PackageManager:
    infoList = []

    def __init__(self):
        mydb = mysql.connector.connect(user=DATABASE_USER, database=DATABASE_NAME)
        cursor = mydb.cursor()
        query = "SELECT building,apartment,date,description,id FROM packages"
        cursor.execute(query)
        for (building, apartment, date, description, id) in cursor:
            self.infoList.append(DescriptionPackage(building, apartment, date, description, id))
        cursor.close()
        mydb.close()

    def addPackage(self, package: DescriptionPackage):
        self.infoList.append(package)
        print(self.infoList)
        mydb = mysql.connector.connect(user=DATABASE_USER, database=DATABASE_NAME)
        cursor = mydb.cursor()
        add_package = ("INSERT INTO packages"
                       " (building,apartment,date,description,id)"
                       " VALUES(%s,%s,%s,%s,%s)")

        cursor.execute(add_package,
                       (package.building, package.apartment, package.date, package.description, package.id))
        mydb.commit()
        cursor.close()
        mydb.close()

    def getPackages(self, Building: str, Apartment: str) -> list:
        listpackage = []
        for package in self.infoList:
            if package.building == Building and package.apartment == Apartment:
                listpackage.append(package)
        return listpackage

    def getPackage(self, packageid: str) -> DescriptionPackage:
        package = None
        for elem in self.infoList:
            if elem.id == packageid:
                package = elem
                break
        return package

    def deletePackage(self, packageid: str):
        mydb = mysql.connector.connect(user=DATABASE_USER, database=DATABASE_NAME)
        cursor = mydb.cursor()
        for package in self.infoList:
            print(package.id + " " + packageid)
            if package.id == packageid:
                self.infoList.remove(package)
                del_package = "DELETE FROM packages WHERE id=%s"
                cursor.execute(del_package, [packageid])
        mydb.commit()
        cursor.close()
        mydb.close()
