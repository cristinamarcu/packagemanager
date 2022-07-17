import unittest
import mock
from PackageManager import DescriptionPackage, PackageManager


class PackageManagerTest(unittest.TestCase):

    @mock.patch("mysql.connector")
    def test_add_package(self, mock_mysql_connector):
        # GIVEN
        package = DescriptionPackage(building='Nova', apartment='9', date='2022-07-13 07:29:03.022098',
                                     description='koo', id='testAdd')
        expected_list = [package]
        packageManager = PackageManager()

        # WHEN
        packageManager.addPackage(package)
        output_list = packageManager.getPackages('Nova', '9')

        # THEN
        self.assertEqual(output_list, expected_list)

    @mock.patch("mysql.connector")
    def test_del_package(self, mock_mysql_connector):
        # GIVEN
        package = DescriptionPackage(building='Nova', apartment='9', date='2022-07-13 07:29:03.022098',
                                     description='koo', id='testDelete')
        expected_list = []
        packageManager = PackageManager()

        # WHEN
        packageManager.addPackage(package)
        packageManager.deletePackage('testDelete')
        output_list = packageManager.getPackages('Nova', '9')

        # THEN
        self.assertEqual(output_list, expected_list)
