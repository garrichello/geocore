import os
from time import sleep
import django
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geocore.settings.development')
django.setup()


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        pass

    def test_can_add_a_collection_and_retrieve_it(self):
        # John is a new admin of the CLIMATE system.
        # He decides to check out the new admin-console
        # of the CLIMATE metadata database.
        self.browser.get(self.live_server_url+'/metadb/')

        # John notices the page title.
        self.assertIn('MetaDB administrative console', self.browser.title)

        # There are four tabs: Collection, Dataset, Data and Other.
        tabs = self.browser.find_elements_by_class_name('tab-pane')
        tab_ids = [tab.get_attribute('id') for tab in tabs]
        self.assertIn('tab-collection', tab_ids)
        self.assertIn('tab-dataset', tab_ids)
        self.assertIn('tab-data', tab_ids)
        self.assertIn('tab-other', tab_ids)

        # John decides to start with Collection tab.
        # There is a button Create on the tab Collection.
        create_btn = self.browser.find_element_by_class_name('js-create-collection')

        # There is a table in the tab Collection.
        _ = self.browser.find_element_by_xpath('//table[@id="collection"]')

        # Collection tab is active.
        self.assertTrue('active' in self.browser.find_element_by_id('tab-collection').get_attribute('class'))

        # The table has a header with columns names:
        # (empty string), (empty string), 'Id', 'Collection label',
        # 'Collection name', 'Collection description', 'Organization',
        # 'Organization URL' and 'Collection URL'
        got_header = [th.get_attribute('textContent') for th in self.browser.find_elements_by_xpath(
            '//table[@id="collection"]/thead/tr[1]/th')]
        correct_header = ['', '', 'Id', 'Collection label', 'Collection name', 'Collection description',
                     'Organization', 'Organization URL', 'Collection URL']
        self.assertEqual(got_header, correct_header)

        # John decides to add a new collection.
        # He presses button Create on the tab Collection.
        # A new modal window for creating a new collection opens
        # inviting him to enter corresponding info.
        create_btn.click()

        # John waits for the modal to appear (but no more than 10 sec!)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[starts-with(@id, "modal-dynamic")]'))
        )
        # John waits for the modal to be fully loaded (but no more than 10 sec!)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'id_label'))
        )

        # Then John types:
        #  'JohnCol' into a textbox Collection label,
        self.browser.find_element_by_id('id_label').send_keys('JohnCol')
        #  'http://mycollection.url' into a textbox Collection URL,
        self.browser.find_element_by_id('id_url').send_keys('http://mycollection.url')
        #  'John's collection' into a textbox name Collection name
        self.browser.find_element_by_id('id_name').send_keys("John's collection")
        #  'This is a collection created by John' into textfield Collection description
        self.browser.find_element_by_id('id_description').send_keys('This is a collection created by John')
        # and decides to add a new Organization.
        # He clicks + button next to the Organization dropdown list
        plus_btn = self.browser.find_element_by_xpath('//button[@data-url="/en/metadb/organizations/create/"]')
        plus_btn.click()
        # Another modal opens inviting to fill a simple form
        form = self.browser.find_element_by_xpath('//form[@class="js-organization-create-form"]')
        # He types 'John Brown research, USA' into a textbox Organization name
        form.find_element_by_id('id_name').send_keys('John Brown research, USA')
        # and  'http://johnbrownresearch.org/' into a textbox Organization URL
        form.find_element_by_id('id_url').send_keys('http://johnbrownresearch.org/')
        # Whe he clicks Create organization the modal fades away revealing previous form
        form.submit()
        sleep(1)
        # and in the drowpdown list Organization the new organization's name is shown
        opts = self.browser.find_elements_by_xpath('//select[@id="id_organizationi18n"]/option')
        selected_opts = [opt.get_attribute('selected') for opt in opts]
        self.assertEqual(opts[selected_opts.index('true')].text, 'John Brown research, USA')

        #Select(self.browser.find_element_by_id('id_organizationi18n')).select_by_visible_text('ECMWF, UK')

        # When he clicks Create collection modal window closes and Collection table updates.
        self.browser.find_element_by_class_name('js-collection-create-form').submit()
        sleep(2)
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_xpath('//div[starts-with(@id, "modal-dynamic")]')

        # Now table contains a new record describing his collection as follows:
        tr = self.browser.find_elements_by_xpath('//table[@id="collection"]/tbody/tr')[-1]  # last row
        col_data = [td.text for td in tr.find_elements_by_tag_name('td')]
        #  column Collection label contains 'JohnCol',
        self.assertEqual(col_data[3], 'JohnCol')
        #  column Collection name contains 'John's collection',
        self.assertEqual(col_data[4], "John's collection")
        #  column Collection description contains 'This is a collection created by John',
        self.assertEqual(col_data[5], 'This is a collection created by John')
        #  column Organization contains 'ECMWF, UK',
        self.assertEqual(col_data[6], 'John Brown research, USA')
        #  column Organization URL contains 'http://johnbrownresearch.org/',
        self.assertEqual(col_data[7], 'http://johnbrownresearch.org/')
        #  column Collection URL contains 'http://mycollection.url'.
        self.assertEqual(col_data[8], 'http://mycollection.url')
