import unittest
from BuildingManager import ApartmentInfo, BuildingManager

#TODO: respecta formatul cu #GIVE/WHEN/THEN. Pune commenturi
#TODO: nu iti pune numarul de telefon real in test
#TODO: adauga test pentru Package Manager. Nu e ok sa testezi adaugarea in baza de date asa ca
#      mysql trebuie sa fie facut mock. Testezi doar ca se adauga/sterge corect in lista interna.

class BuildingManagerTest(unittest.TestCase):
    def test_no_building(self):
        # GIVEN
        expected_list = []
        buildingManager = BuildingManager("{}")

        # WHEN
        output_list = buildingManager.getBuildings()

        # THEN
        self.assertEqual(output_list, expected_list)

    def test_one_building(self):
        # GIVEN
        expected_list = ['Apollo']
        buildingManager = BuildingManager('{"Apollo": []}')

        # WHEN
        output_list = buildingManager.getBuildings()

        # THEN
        self.assertEqual(output_list, expected_list)

    def test_two_buildings(self):
        # GIVEN
        expected_list = ['Apollo', 'Nova']
        buildingManager = BuildingManager('{"Apollo": [],"Nova": []}')

        # WHEN
        output_list = buildingManager.getBuildings()

        # THEN
        self.assertEqual(output_list, expected_list)

    def test_no_apart(self):
        # GIVEN
        expected_list = []
        buildingManager = BuildingManager('{"Apollo":[]}')

        # WHEN
        output_list = buildingManager.getApartments('Apollo')

        # THEN
        self.assertEqual(output_list, expected_list)

    def test_one_apart(self):

        # GIVEN
        expected_list = ["1"]
        buildingManager = BuildingManager('{"Apollo":[{"number":"1"}]}')

        # WHEN
        output_list = buildingManager.getApartments('Apollo')

        # THEN
        self.assertEqual(output_list, expected_list)

    def test_two_apart(self):

        # GIVEN
        expected_list = ["1", "2"]
        buildingManager = BuildingManager('{"Apollo":[{"number":"1"},{"number":"2"}]}')

        # WHEN
        output_list = buildingManager.getApartments('Apollo')

        # THEN
        self.assertEqual(output_list, expected_list)

    def test_getapart_info(self):

        # GIVEN
        expected_list = ApartmentInfo("cristina", "0744089913", "ercvbv")
        buildingManager = BuildingManager('{"Apollo":[{"number":"1","contact_name":"cosmin",'
                                          '"contact_nr":"0742062984","email":"ooooooo"},{"number":"2",'
                                          '"contact_name":"cristina","contact_nr":"0744089913","email":"ercvbv"}]}')

        # WHEN
        output_list = buildingManager.getApartmentInfo('Apollo', '2')

        # THEN
        self.assertEqual(output_list, expected_list)

    def test_getapart_no_info(self):

        # GIVEN

        expected_list = None
        buildingManager = BuildingManager('{"Apollo":[{"number":"1"}]}')

        # WHEN
        output_list = buildingManager.getApartmentInfo('Apollo', '2')

        # THEN
        self.assertEqual(output_list, expected_list)
