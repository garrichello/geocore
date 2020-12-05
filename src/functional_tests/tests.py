import os
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
from time import sleep
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geocore.settings.development')
django.setup()


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        qs = metadb.models.Organization.objects.filter(url='http://johnbrownresearch.org/')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.Resolution.objects.filter(name='0.13x0.13')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.Scenario.objects.filter(name='Specific')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.DataKind.objects.filter(name='fractal')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.FileType.objects.filter(name='hdf5')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.Variable.objects.filter(name='gamma_level')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.FileType.objects.filter(name='soec3m')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.GuiElement.objects.filter(name='feature')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.Property.objects.filter(label='value')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.PropertyValue.objects.filter(label='low')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.Units.objects.filter(unitsi18n__name='mRd/yr')
        if len(qs) > 0:
            qs.delete()

#------------------------------------------------------------------------------------------------------

    def wait_and_assert_select_after_submit(self, form, idd, text):
        # Modal fades away revealing previous form 'Create a new dataset'
        # John waits until the new collection label apperars in the dropdown list
        WebDriverWait(self.browser, 10).until(
            lambda x: self.browser.find_element_by_xpath(
                f'//select[@id="{idd}"]/option[contains(text(), "{text}")]').get_attribute(
                    'selected'))
        # and in the drowpdown list Collection the new collections's label is shown
        opts = form.find_elements_by_xpath(f'//select[@id="{idd}"]/option')
        selected_opts = [opt.get_attribute('selected') for opt in opts]
        self.assertEqual(opts[selected_opts.index('true')].text, f'{text}')

    def add_1_element(self, form_class, element_id, value):
        # Another modal opens inviting to create a new record
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, form_class))
        )
        form = self.browser.find_element_by_class_name(form_class)
        # Then John types value into a textbox element_id,
        form.find_element_by_id(element_id).send_keys(value)
        # And finally clicks Create
        form.submit()

    def add_2_elements(self, form_class, element1_id, value1, element2_id, value2):
        # Another modal opens
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, form_class))
        )
        form = self.browser.find_element_by_class_name(form_class)
        # Then John types value1 into a textbox element2_id,
        form.find_element_by_id(element1_id).send_keys(value1)
        #  value2 into a textbox element2_id,
        form.find_element_by_id(element2_id).send_keys(value2)
        # And finally clicks Create scenario
        form.submit()

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
        # John wants to select an organization, but finds out that the one he needs is absent.
        # So he decides to add it and clicks '+' button next to the Organization dropdown list
        plus_btn = collection_form.find_element_by_xpath('//button[@data-url="/en/metadb/organizations/create/"]')
        plus_btn.click()

        # John adds a new organization
        self.add_2_elements('js-organization-create-form', 'id_name', 'John Brown research, USA',
                                                           'id_url', 'http://johnbrownresearch.org/')
        self.wait_and_assert_select_after_submit(collection_form, 'id_organizationi18n', 'John Brown research, USA')

        # And finally John clicks Create collection
        collection_form.submit()


    def add_property(self, label):
        # John waits for the form to appear (but no more than 10 sec!)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-property-create-form'))
        )
        collection_form = self.browser.find_element_by_class_name('js-property-create-form')
        # Then John types label into a textbox Property label,
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'id_label'))
        )
        collection_form.find_element_by_id('id_label').send_keys(label)

        # John wants to select a GUI element, but finds out that the one he needs is absent.
        # So he decides to add it and clicks '+' button next to the GUI element dropdown list
        plus_btn = collection_form.find_element_by_xpath('//button[@data-url="/en/metadb/guielements/create/"]')
        plus_btn.click()

        # John adds a new GUI element
        self.add_2_elements('js-gui-element-create-form', 'id_name', 'feature',
                                                         'id_caption', 'Feature')
        self.wait_and_assert_select_after_submit(collection_form, 'id_gui_element', 'feature')

        # And finally John clicks Create collection
        collection_form.submit()


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

        # John wants to select a collection, but finds out that the one he needs is absent.
        # So he decides to add it and clicks '+' button next to the Collection dropdown list.
        sleep(1)
        plus_btn = self.browser.find_element_by_xpath(
            '//form[@class="js-dataset-create-form"]//button[@data-url="/en/metadb/collections/create/"]')
        plus_btn.click()

        # John adds a new collection
        self.add_collection()
        self.wait_and_assert_select_after_submit(dataset_form, 'id_collection', 'JohnCol')

        # John wants to select a resolution, but finds out that the needed one is absent
        # So he decides to add it and clicks '+' button next to the Resolution dropdown list.
        plus_btn = self.browser.find_element_by_xpath(
            '//form[@class="js-dataset-create-form"]//button[@data-url="/en/metadb/resolutions/create/"]')
        plus_btn.click()

        self.add_2_elements('js-resolution-create-form', 'id_name', '0.13x0.13', 'id_subpath1', '0.13x0.13/')
        self.wait_and_assert_select_after_submit(dataset_form, 'id_resolution', '0.13x0.13')

        # John wants to select a scenario, but finds out that the needed one is absent
        # So he decides to add it and clicks '+' button next to the Scenario dropdown list.
        plus_btn = self.browser.find_element_by_xpath(
            '//form[@class="js-dataset-create-form"]//button[@data-url="/en/metadb/scenarios/create/"]')
        plus_btn.click()

        self.add_2_elements('js-scenario-create-form', 'id_name', 'Specific', 'id_subpath0', 'specific/')
        self.wait_and_assert_select_after_submit(dataset_form, 'id_scenario', 'Specific')

        # John wants to select a data kind, but finds out that the needed one is absent
        # So he decides to add it and clicks '+' button next to the Data kind dropdown list.
        plus_btn = self.browser.find_element_by_xpath(
            '//form[@class="js-dataset-create-form"]//button[@data-url="/en/metadb/datakinds/create/"]')
        plus_btn.click()

        self.add_1_element('js-datakind-create-form', 'id_name', 'fractal')
        self.wait_and_assert_select_after_submit(dataset_form, 'id_data_kind', 'fractal')

        # John types 'JohnCol 0x13x0.13' into a textbox Description,
        dataset_form.find_element_by_id('id_description').send_keys('JohnCol 0x13x0.13')
        #  '20000101' into a textbox Time start,
        dataset_form.find_element_by_id('id_time_start').send_keys('20000101')
        #  '20001231' into a textbox Time end,
        dataset_form.find_element_by_id('id_time_end').send_keys('20001231')

        # John wants to select a file type, but finds out that the needed one is absent
        # So he decides to add it and clicks '+' button next to the File type dropdown list.
        plus_btn = self.browser.find_element_by_xpath(
            '//form[@class="js-dataset-create-form"]//button[@data-url="/en/metadb/filetypes/create/"]')
        plus_btn.click()

        self.add_1_element('js-filetype-create-form', 'id_name', 'hdf5')
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

        # John wants to select a levels variable, but finds out that the needed one is absent
        # So he decides to add it and clicks '+' button next to the Levels variable dropdown list.
        plus_btn = data_form.find_element_by_xpath(
            '//button[@data-url="/en/metadb/levelsvariables/create/"]')
        plus_btn.click()

        # John adds a levels variable
        self.add_1_element('js-levels-variable-create-form', 'id_name', 'gamma_level')
        self.wait_and_assert_select_after_submit(data_form, 'id_levels_variable', 'gamma_level')

        # John wants to select a variable, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the Variable dropdown list.
        plus_btn = data_form.find_element_by_xpath(
            '//button[@data-url="/en/metadb/variables/create/"]')
        plus_btn.click()

        # John adds a variable
        self.add_1_element('js-variable-create-form', 'id_name', 'spec3m')
        self.wait_and_assert_select_after_submit(data_form, 'id_variable', 'spec3m')

        # John wants to select a unit of measurement, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the Unit dropdown list.
        plus_btn = data_form.find_element_by_xpath(
            '//button[@data-url="/en/metadb/units/create/"]')
        plus_btn.click()

        # John adds a unit
        self.add_1_element('js-unit-create-form', 'id_name', 'mRd/yr')
        self.wait_and_assert_select_after_submit(data_form, 'id_unitsi18n', 'mRd/yr')

        # John decides to use Property/Property value and checks Use property checkbox
        data_form.find_element_by_id('id_use_property').click()
        # This enables Property...
        self.assertFalse(data_form.find_element_by_id('id_property').get_attribute('disabled'))
        # ... and Property value dropdown lists
        self.assertFalse(data_form.find_element_by_id('id_property_value').get_attribute('disabled'))

        # John wants to select a property, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the Proprty dropdown list.
        plus_btn = data_form.find_element_by_xpath(
            '//button[@data-url="/en/metadb/properties/create/"]')
        plus_btn.click()

        # John adds a property
        self.add_property('volume')
        self.wait_and_assert_select_after_submit(data_form, 'id_property', 'volume')

        # John wants to select a property value, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the Property value dropdown list.
        plus_btn = data_form.find_element_by_xpath(
            '//button[@data-url="/en/metadb/propertyvalues/create/"]')
        plus_btn.click()

        # John adds a property value
        self.add_1_element('js-property-value-create-form', 'id_label', 'low')
        self.wait_and_assert_select_after_submit(data_form, 'id_property_value', 'low')

        # John wants to select a root directory, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the Root directory dropdown list.
        plus_btn = data_form.find_element_by_xpath(
            '//button[@data-url="/en/metadb/rootdirs/create/"]')
        plus_btn.click()

        # John adds a root directory
        self.add_1_element('js-root-dir-create-form', 'id_name', '/mnt/data/JohnCol/')
        self.wait_and_assert_select_after_submit(data_form, 'id_root_dir', '/mnt/data/JohnCol/')

        # John wants to select a file name pattern, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the File name pattern dropdown list.
        plus_btn = data_form.find_element_by_xpath(
            '//button[@data-url="/en/metadb/filenames/create/"]')
        plus_btn.click()

        # John adds a file name pattern
        self.add_1_element('js-file-create-form', 'id_name_pattern', 'experiment/%mm%_%year%.nc')
        self.wait_and_assert_select_after_submit(data_form, 'id_file', 'experiment/%mm%_%year%.nc')

        # John types '3.14' into a textbox Scale...
        data_form.find_element_by_id('id_scale').send_keys('3.14')
        # ... and '2.76' into a textbox Offset
        data_form.find_element_by_id('id_offset').send_keys('-2.76')

        # When he clicks Create data modal window closes and Data table updates.
        data_form.submit()
