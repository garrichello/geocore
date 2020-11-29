from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_add_a_collection_and_retrieve_it(self):
        # John is a new admin of the CLIMATE system.
        # He decides to check out the new admin-console
        # of the CLIMATE metadata database.
        self.browser.get('http://localhost:8001/metadb/')

        # John notices the page title.
        self.assertIn('MetaDB administration', self.browser.title)
        self.fail('Finish the test!')

        # There are four tabs: Collection, Dataset, Data and Other.

        # John decides to start with Collection tab.
        # There is a button Create on the tab Collection.

        # There is a table the tab Collection.

        # Collection tab is active.

        # The table has a header with columns names:
        # (empty string), (empty string), 'Id', 'Collection label', 
        # 'Collection name', 'Collection description', 'Organization',
        # 'Organization URL' and 'Collection URL'

        # John decides to add a new collection.
        # He presses button Create on the tab Collection.
        # A new modal window for creating a new collection opens 
        # inviting him to enter corresponding info.

        # John types: 
        #  'JohnCol' into a textbox Collection label,
        #  'http://mycollection.url' into a textbox Collection URL,
        #  'John's collection' into a textbox name Collection name
        #  'This is a collection created by John' into textfield Collection description
        # and selects 'ECMWF, UK' in a dropdown list Organization.

        # When he clicks Create collection modal window closes
        # and Collection table updates.
        # Now table contains a new record describing his collection as follows:
        #  column Collection label contains 'JohnCol',
        #  column Collection name contains 'John's collection',
        #  column Collection description contains 'This is a collection created by John',
        #  column Organization contains 'ECMWF, UK',
        #  column Collection URL contains 'http://mycollection.url'.
