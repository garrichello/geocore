import os
from time import sleep
import django
#from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import NoSuchElementException
import metadb

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geocore.settings.development')
django.setup()


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        qs = metadb.models.Organization.objects.filter(url='http://johnbrownresearch.org/')
        if len(qs) > 0:
            qs.get().delete()
        qs = metadb.models.Resolution.objects.filter(name='0.13x0.13')
        if len(qs) > 0:
            qs.get().delete()
        qs = metadb.models.Scenario.objects.filter(name='Specific')
        if len(qs) > 0:
            qs.get().delete()
        qs = metadb.models.DataKind.objects.filter(name='fractal')
        if len(qs) > 0:
            qs.get().delete()
        qs = metadb.models.FileType.objects.filter(name='hdf5')
        if len(qs) > 0:
            qs.get().delete()
        pass

#------------------------------------------------------------------------------------------------------

    def wait_and_assert_select_after_submit(self, form, idd, text):
        # Modal fades away revealing previous form 'Create a new dataset'
        # John waits until the new collection label apperars in the dropdown list
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, 
            f'//select[@id="{idd}"]/option[contains(text(), "{text}")]'))
        )
        # and in the drowpdown list Collection the new collections's label is shown
        opts = form.find_elements_by_xpath(f'//select[@id="{idd}"]/option')
        selected_opts = [opt.get_attribute('selected') for opt in opts]
        self.assertEqual(opts[selected_opts.index('true')].text, f'{text}')


    def add_organization(self):
        # Another modal opens inviting to fill a simple form
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-organization-create-form'))
        )
        organization_form = self.browser.find_element_by_xpath('//form[@class="js-organization-create-form"]')
        # He types 'John Brown research, USA' into a textbox Organization name
        organization_form.find_element_by_id('id_name').send_keys('John Brown research, USA')
        # and  'http://johnbrownresearch.org/' into a textbox Organization URL
        organization_form.find_element_by_id('id_url').send_keys('http://johnbrownresearch.org/')
        # When he clicks Create organization the modal fades away revealing previous form
        organization_form.submit()

    def add_collection(self):
        # John waits for the form to appear (but no more than 10 sec!)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-collection-create-form'))
        )
        collection_form = self.browser.find_element_by_class_name('js-collection-create-form')
        # Then John types:
        #  'JohnCol' into a textbox Collection label,
        collection_form.find_element_by_id('id_label').send_keys('JohnCol')
        #  'http://mycollection.url' into a textbox Collection URL,
        collection_form.find_element_by_id('id_url').send_keys('http://mycollection.url')
        #  'John's collection' into a textbox name Collection name
        collection_form.find_element_by_id('id_name').send_keys("John's collection")
        #  'This is a collection created by John' into textfield Collection description
        collection_form.find_element_by_id('id_description').send_keys('This is a collection created by John')
        # John wants to select an organization, butrealizes that the one he needs is absent.
        # So he decides to add it and clicks '+' button next to the Organization dropdown list
        plus_btn = collection_form.find_element_by_xpath('//button[@data-url="/en/metadb/organizations/create/"]')
        plus_btn.click()

        # John adds a new organization
        self.add_organization()
        self.wait_and_assert_select_after_submit(collection_form, 'id_organizationi18n', 'John Brown research, USA')

        # And finally John clicks Create collection
        collection_form.submit()

    def add_resolution(self):
        # Another modal opens inviting to create a new resolution
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-resolution-create-form'))
        )
        resolution_form = self.browser.find_element_by_class_name('js-resolution-create-form')
        # Then John types:
        #  '0.13x0.13' into a textbox Resolution name,
        resolution_form.find_element_by_id('id_name').send_keys('0.13x0.13')
        #  '0.13x0.13/' into a textbox Resolution subpath,
        resolution_form.find_element_by_id('id_subpath1').send_keys('0.13x0.13/')
        # And finally clicks Create resolution
        resolution_form.submit()

    def add_scenario(self):
        # Another modal opens inviting to create a new scenario
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-scenario-create-form'))
        )
        scenario_form = self.browser.find_element_by_class_name('js-scenario-create-form')
        # Then John types:
        #  'Specific' into a textbox Scenario name,
        scenario_form.find_element_by_id('id_name').send_keys('Specific')
        #  'specific/' into a textbox Resolution subpath,
        scenario_form.find_element_by_id('id_subpath0').send_keys('specific/')
        # And finally clicks Create scenario
        scenario_form.submit()

    def add_datakind(self):
        # Another modal opens inviting to create a new data kind
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-datakind-create-form'))
        )
        datakind_form = self.browser.find_element_by_class_name('js-datakind-create-form')
        # Then John types:
        #  'fractal' into a textbox Data kind name,
        datakind_form.find_element_by_id('id_name').send_keys('fractal')
        # And finally clicks Create scenario
        datakind_form.submit()

    def add_filetype(self):
        # Another modal opens inviting to create a new file type
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-filetype-create-form'))
        )
        filetype_form = self.browser.find_element_by_class_name('js-filetype-create-form')
        # Then John types:
        #  'hdf5' into a textbox Data kind name,
        filetype_form.find_element_by_id('id_name').send_keys('hdf5')
        # And finally clicks Create scenario
        filetype_form.submit()

    def add_variable(self):
        # Another modal opens inviting to create a new variable
        # (in fact, levels variable is just another variable)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-variable-create-form'))
        )
        variable_form = self.browser.find_element_by_class_name('js-variable-create-form')
        # Then John types:
        #  'gamma_level' into a textbox Data kind name,
        variable_form.find_element_by_id('id_name').send_keys('gamma_level')
        # And finally clicks Create variable
        variable_form.submit()

#------------------------------------------------------------------------------------------------------

    def test_can_add_a_collection_and_retrieve_it(self):
        # John is a new admin of the CLIMATE system.
        # He decides to check out the new admin-console
        # of the CLIMATE metadata database.
        self.browser.get('http://localhost:8001/metadb/')

        # John notices the page title.
        self.assertIn('MetaDB administrative console', self.browser.title)

        # There are four tabs: Collection, Dataset, Data and Other.
        tabs = self.browser.find_elements_by_class_name('tab-pane')
        tab_ids = [tab.get_attribute('id') for tab in tabs]
        self.assertIn('tab-collection', tab_ids)
        self.assertIn('tab-dataset', tab_ids)
        self.assertIn('tab-data', tab_ids)
        self.assertIn('tab-other', tab_ids)

        # Collection tab is active.
        self.assertTrue('active' in self.browser.find_element_by_id('tab-collection').get_attribute('class'))

        # John decides to start with Collection tab.
        # There is a button Create on the tab Collection.
        create_btn = self.browser.find_element_by_class_name('js-create-collection')

        # John wants to add a new collection.
        # He presses button Create on the tab Collection.
        create_btn.click()

        # John adds a new collection
        self.add_collection()

        # John waits until the all enterd data apperars in the data table
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH,
            '//table[@id="collection"]/tbody/tr/td[contains(text(), "JohnCol")]'))
        )
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

#------------------------------------------------------------------------------------------------------

    def test_can_add_a_dataset_and_retrieve_it(self):
        # John decides to expoler the Dataset tab
        # He opens the main page again
        self.browser.get('http://localhost:8001/metadb/')

        # He clicks tha Datset tab
        self.browser.find_element_by_xpath(
            '//ul[contains(@class, "nav-tabs")]//a[@href="#tab-dataset"]').click()

        # Now the Dataset tab is active.
        self.assertTrue('active' in self.browser.find_element_by_id('tab-dataset').get_attribute('class'))

        # There is a button Create on the tab Dataset.
        create_btn = self.browser.find_element_by_class_name('js-create-dataset')

        # John decides to add a new dataset.
        # He presses button Create on the tab Dataset.
        create_btn.click()

        # A new modal window for creating a new dataset opens inviting him to enter corresponding info.
        # John waits for the form to be fully loaded (but no more than 10 sec!)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-dataset-create-form'))
        )
        dataset_form = self.browser.find_element_by_class_name('js-dataset-create-form')

        # John wants to select a collection, but realizes that the one he needs is absent.
        # So he decides to add it and clicks '+' button next to the Collection dropdown list.
        plus_btn = self.browser.find_element_by_xpath(
            '//form[@class="js-dataset-create-form"]//button[@data-url="/en/metadb/collections/create/"]')
        plus_btn.click()

        # John adds a new collection
        self.add_collection()
        self.wait_and_assert_select_after_submit(dataset_form, 'id_collection', 'JohnCol')

        # John wants to select a resolution, but realizes that the needed one is absent
        # So he decides to add it and clicks '+' button next to the Resolution dropdown list.
        plus_btn = self.browser.find_element_by_xpath(
            '//form[@class="js-dataset-create-form"]//button[@data-url="/en/metadb/resolutions/create/"]')
        plus_btn.click()

        self.add_resolution()
        self.wait_and_assert_select_after_submit(dataset_form, 'id_resolution', '0.13x0.13')

        # John wants to select a scenario, but realizes that the needed one is absent
        # So he decides to add it and clicks '+' button next to the Scenario dropdown list.
        plus_btn = self.browser.find_element_by_xpath(
            '//form[@class="js-dataset-create-form"]//button[@data-url="/en/metadb/scenarios/create/"]')
        plus_btn.click()

        self.add_scenario()
        self.wait_and_assert_select_after_submit(dataset_form, 'id_scenario', 'Specific')

        # John wants to select a data kind, but realizes that the needed one is absent
        # So he decides to add it and clicks '+' button next to the Data kind dropdown list.
        plus_btn = self.browser.find_element_by_xpath(
            '//form[@class="js-dataset-create-form"]//button[@data-url="/en/metadb/datakinds/create/"]')
        plus_btn.click()

        self.add_datakind()
        self.wait_and_assert_select_after_submit(dataset_form, 'id_data_kind', 'fractal')

        # John types 'JohnCol 0x13x0.13' into a textbox Description,
        dataset_form.find_element_by_id('id_description').send_keys('JohnCol 0x13x0.13')
        #  '20000101' into a textbox Time start,
        dataset_form.find_element_by_id('id_time_start').send_keys('20000101')
        #  '20001231' into a textbox Time end,
        dataset_form.find_element_by_id('id_time_end').send_keys('20001231')

        # John wants to select a file type, but realizes that the needed one is absent
        # So he decides to add it and clicks '+' button next to the File type dropdown list.
        plus_btn = self.browser.find_element_by_xpath(
            '//form[@class="js-dataset-create-form"]//button[@data-url="/en/metadb/filetypes/create/"]')
        plus_btn.click()

        self.add_filetype()
        self.wait_and_assert_select_after_submit(dataset_form, 'id_file_type', 'hdf5')

        # When he clicks Create dataset modal window closes and Dataset table updates.
        dataset_form.submit()

        # John waits until the all enterd data apperars in the data table
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, 
            '//table[@id="dataset"]/tbody/tr/td[contains(text(), "JohnCol")]'))
        )
        # Now table contains a new record describing his dataset as follows:
        tr = self.browser.find_elements_by_xpath('//table[@id="dataset"]/tbody/tr')[-1]  # last row
        col_data = [td.text for td in tr.find_elements_by_tag_name('td')]
        #  column Collection label contains 'JohnCol',
        self.assertEqual(col_data[4], 'JohnCol')
        #  column Resolution contains '0x13x0.13',
        self.assertEqual(col_data[5], "0.13x0.13")
        #  column Scenario contains 'Specific',
        self.assertEqual(col_data[6], 'Specific')
        #  column Data kind contains 'db',
        self.assertEqual(col_data[7], 'fractal')
        #  column File type contains 'hdf5',
        self.assertEqual(col_data[8], 'hdf5')
        #  column Time start contains '20000101',
        self.assertEqual(col_data[9], '20000101')
        #  column Time end contains '20001231',
        self.assertEqual(col_data[10], '20001231')
        #  column Dataset description contains 'JohnCol 0x13x0.13',
        self.assertEqual(col_data[11], 'JohnCol 0x13x0.13')

#------------------------------------------------------------------------------------------------------

    def test_can_add_a_data_and_retrieve_it(self):
        # John decides to expoler the Data tab
        # He opens the main page again
        self.browser.get('http://localhost:8001/metadb/')

        # He clicks tha Datset tab
        self.browser.find_element_by_xpath(
            '//ul[contains(@class, "nav-tabs")]//a[@href="#tab-data"]').click()

        # Now the Dataset tab is active.
        self.assertTrue('active' in self.browser.find_element_by_id('tab-data').get_attribute('class'))

        # There is a button Create on the tab Dataset.
        create_btn = self.browser.find_element_by_class_name('js-create-data')

        # John decides to add a new dataset.
        # He presses button Create on the tab Dataset.
        create_btn.click()

        # A new modal window for creating a new data opens inviting him to enter corresponding info.
        # John waits for the form to be fully loaded (but no more than 10 sec!)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-data-create-form'))
        )
        data_form = self.browser.find_element_by_class_name('js-data-create-form')

        # John selects a collection with index=1
        Select(data_form.find_element_by_id('id_collection')).select_by_index(1)
        WebDriverWait(self.browser, 10).until(lambda x:
            len(data_form.find_elements_by_xpath('//select[@id="id_resolution"]/option')) > 1
        )

        # Then selects a resolution with index=1
        Select(data_form.find_element_by_id('id_resolution')).select_by_index(1)
        WebDriverWait(self.browser, 10).until(lambda x:
            len(data_form.find_elements_by_xpath('//select[@id="id_scenario"]/option')) > 1
        )

        # And selects a scenario with index=1
        Select(data_form.find_element_by_id('id_scenario')).select_by_index(1)
        
        # Next, John selects parameter with index=1
        Select(data_form.find_element_by_id('id_parameteri18n')).select_by_index(1)
        WebDriverWait(self.browser, 10).until(lambda x:
            len(data_form.find_elements_by_xpath('//select[@id="id_time_stepi18n"]/option')) > 1
        )
        # Then selects time step with index=1
        Select(data_form.find_element_by_id('id_time_stepi18n')).select_by_index(1)
        WebDriverWait(self.browser, 10).until(lambda x:
            len(data_form.find_elements_by_xpath('//select[@id="id_levels_group"]/option')) > 1
        )
        # And selects a levels group with index=1
        Select(data_form.find_element_by_id('id_levels_group')).select_by_index(1)
        WebDriverWait(self.browser, 10).until(lambda x:
            len(data_form.find_element_by_id('id_levels_namesi18n').get_attribute('value')) > 0
        )

        # John checks out Levels names field.
        # It contains a list of levels in the selected levels group (not empty).
        self.assertTrue(
            len(data_form.find_element_by_id('id_levels_namesi18n').get_attribute('value')) > 0)

        # John decides to use Levels variable and checks Use levels variable checkbox
        data_form.find_element_by_id('id_use_lvsvar').click()
        # This enables Levels variable dropdown list
        self.assertFalse(data_form.find_element_by_id('id_levels_variable').get_attribute('disabled'))
        # John wants to select a levels variable, but realizes that the needed one is absent
        # So he decides to add it and clicks '+' button next to the Levels variable dropdown list.
        plus_btn = data_form.find_element_by_xpath(
            '//button[@data-url="/en/metadb/variable/create/"]')
        plus_btn.click()

        # John adds a levels variable
        self.add_variable()
        self.wait_and_assert_select_after_submit(data_form, 'id_levels_variable', 'gamma_level')

