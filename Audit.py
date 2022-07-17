from typing import NamedTuple
import mysql.connector

from Config import DATABASE_USER, DATABASE_NAME
from PackageManager import DescriptionPackage
import logging


class DescriptionPackageHistory(NamedTuple):
    package: DescriptionPackage
    action: str


class Audit:
    def getPackageHistory(self, Building: str, Apartament: str) -> list:
        infoList = []
        mydb = mysql.connector.connect(user=DATABASE_USER, database=DATABASE_NAME)
        cursor = mydb.cursor()
        query = ("SELECT building,apartment,date,description,id,action FROM history "
                 " WHERE  building=%s AND apartment=%s ")
        cursor.execute(query, (Building, Apartament))
        for (building, apartment, date, description, id, action) in cursor:
            package = DescriptionPackage(building, apartment, date, description, id)
            infoList.append(DescriptionPackageHistory(package, action))

        cursor.close()
        mydb.close()
        return infoList

    def addToHistory(self, info: DescriptionPackageHistory):
        mydb = mysql.connector.connect(user=DATABASE_USER, database=DATABASE_NAME)
        cursor = mydb.cursor()
        add_package = ("INSERT INTO history"
                       " (building,apartment,date,description,id,action)"
                       " VALUES(%s,%s,%s,%s,%s,%s)")

        cursor.execute(add_package,
                       (info.package.building, info.package.apartment, info.package.date, info.package.description,
                        info.package.id, info.action))
        mydb.commit()
        logging.info(f'The package with the id {info.package.id} was added to the database history.')
        cursor.close()
        mydb.close()
