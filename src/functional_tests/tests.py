import os
import unittest
from time import sleep

import django
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

import metadb

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geocore.settings.development')
django.setup()


class FullScaleTest(unittest.TestCase):

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
        qs = metadb.models.Variable.objects.filter(name='spec3m')
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
        qs = metadb.models.RootDir.objects.filter(name='/mnt/data/JohnCol/')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.File.objects.filter(name_pattern='experiment/%mm%_%year%.nc')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.AccumulationMode.objects.filter(name='mult')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.TimeStep.objects.filter(label='5h')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.Units.objects.filter(unitsi18n__name='Hz')
        if len(qs) > 0:
            qs.delete()
        qs = metadb.models.Level.objects.filter(label__in=['46', '79'])
        if len(qs) > 0:
            qs.delete()

#------------------------------------------------------------------------------------------------------

    def wait_and_type(self, form_class, element_id, text):
        loc = f'//form[@class="{form_class}"]//*[@id="{element_id}"]'
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, loc))
        )
        self.browser.find_element_by_xpath(loc).send_keys(text)
        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element_value((By.XPATH, loc), text)
        )

    def wait_and_click_add_btn(self, url):
        loc = f'//button[@data-url="{url}" and contains(@class, "js-add-button")]'
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, loc))
        )
        self.browser.find_element_by_xpath(loc).click()

    def wait_and_assert_list_after_submit(self, form_class, idd, text):
        # Modal fades away revealing previous form
        # John waits until the new entity apperars in the list
        element = f'//form[@class="{form_class}"]//div[@id="{idd}"]/a[contains(text(), "{text}")]'
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, element)))
        # and in the list the new entity is shown
        names = [it.text for it in self.browser.find_elements_by_xpath(
            f'//form[@class="{form_class}"]//div[@id="{idd}"]/a')]
        self.assertIn(text, names)

    def wait_and_assert_select_after_submit(self, form_class, idd, text):
        # Modal fades away revealing previous form
        # John waits until the new entity apperars in the dropdown list
        WebDriverWait(self.browser, 10).until(
            lambda x: self.browser.find_element_by_xpath(
                f'//select[@id="{idd}"]/option[contains(text(), "{text}")]').get_attribute(
                    'selected'))
        # and in the drowpdown list the new entity is shown
        opts = self.browser.find_elements_by_xpath(
            f'//form[@class="{form_class}"]//select[@id="{idd}"]/option')
        selected_opts = [opt.get_attribute('selected') for opt in opts]
        self.assertEqual(opts[selected_opts.index('true')].text, f'{text}')

    def add_1_element(self, form_class, element_id, value):
        # Another modal opens inviting to create a new record
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, form_class))
        )
        form = self.browser.find_element_by_class_name(form_class)
        # Then John types value into a textbox element_id,
        self.wait_and_type(form_class, element_id, value)
        # And finally clicks Create
        form.submit()

    def add_2_elements(self, form_class, element1_id, value1, element2_id, value2):
        # Another modal opens
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, form_class))
        )
        form = self.browser.find_element_by_class_name(form_class)
        # Then John types value1 into a textbox element1_id,
        self.wait_and_type(form_class, element1_id, value1)
        #  value2 into a textbox element2_id,
        self.wait_and_type(form_class, element2_id, value2)
        # And finally clicks Create
        form.submit()

    def add_3_elements(self, form_class, element1_id, value1, element2_id, value2, 
                       element3_id, value3):
        # Another modal opens
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, form_class))
        )
        form = self.browser.find_element_by_class_name(form_class)
        # Then John types value1 into a textbox element1_id,
        self.wait_and_type(form_class, element1_id, value1)
        #  value2 into a textbox element2_id,
        self.wait_and_type(form_class, element2_id, value2)
        #  value3 into a textbox element3_id,
        self.wait_and_type(form_class, element3_id, value3)
        # And finally clicks Create
        form.submit()

    def add_collection(self):
        form_class = 'js-collection-form'
        # John waits for the form to appear (but no more than 10 sec!)
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, form_class))
        )
        collection_form = self.browser.find_element_by_class_name(form_class)
        # Then John types:
        #  'JohnCol' into a textbox Collection label,
        self.wait_and_type(form_class, 'id_label', 'JohnCol')
        #  'http://mycollection.url' into a textbox Collection URL,
        self.wait_and_type(form_class, 'id_url', 'http://mycollection.url')
        #  'John's collection' into a textbox name Collection name
        self.wait_and_type(form_class, 'id_name', "John's collection")
        #  'This is a collection created by John' into textfield Collection description
        self.wait_and_type(form_class, 'id_description', 'This is a collection created by John')
        # John wants to select an organization, but finds out that the one he needs is absent.
        # So he decides to add it and clicks '+' button next to the Organization dropdown list
        self.wait_and_click_add_btn('/en/metadb/organizations/create/')

        # John adds a new organization
        self.add_2_elements('js-organization-form', 'id_name', 'John Brown research, USA',
                                                    'id_url', 'http://johnbrownresearch.org/')
        self.wait_and_assert_select_after_submit(form_class, 'id_organizationi18n', 'John Brown research, USA')

        # And finally John clicks Create collection
        collection_form.submit()

    def add_parameter(self):
        form_class = 'js-parameter-form'
        # John waits for the form to appear (but no more than 10 sec!)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH,
                f'//form[@class="{form_class}"]//*'))
        )
        parameter_form = self.browser.find_element_by_class_name(form_class)
        # Then John types:
        #  'Fogness' into a textbox Name,
        self.wait_and_type(form_class, 'id_name', 'Fogness')
        # John wants to select an accumulation mode, but finds out that the one he needs is absent.
        # So he decides to add it and clicks '+' button next to the Accumulation mode dropdown list
        self.wait_and_click_add_btn('/en/metadb/accmodes/create/')

        # John adds a new organization
        self.add_1_element('js-accmode-form', 'id_name', 'mult')
        self.wait_and_assert_select_after_submit(form_class, 'id_accumulation_mode', 'mult')

        # And finally John clicks Create parameter
        parameter_form.submit()

    def add_levels_group(self):
        form_class = 'js-levels-group-form'
        # John waits for the form to appear (but no more than 10 sec!)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, form_class))
        )
        levels_group_form = self.browser.find_element_by_class_name(form_class)
        # Then John types:
        #  'Delta levels' into a textbox Description,
        self.wait_and_type(form_class, 'id_description', 'Delta levels')
        # John wants to select an measurement unit, but finds out that the one he needs is absent.
        # So he decides to add it and clicks '+' button next to the Measurement unit dropdown list
        self.wait_and_click_add_btn('/en/metadb/units/create/')

        # John adds a unit
        self.add_1_element('js-unit-form', 'id_name', 'Hz')
        self.wait_and_assert_select_after_submit(form_class, 'id_unitsi18n', 'Hz')

        # John wants to select levels, but finds out that the ones he needs are absent.
        # So he decides to add them and clicks '+' button next to the Select levels label
        # John adds a level
        self.wait_and_click_add_btn('/en/metadb/levels/create/')
        self.add_2_elements('js-level-form', 'id_label', '46', 'id_name', '46th')
        self.wait_and_assert_list_after_submit(form_class, 'available_levels_list', '46')

        # John adds another level
        self.wait_and_click_add_btn('/en/metadb/levels/create/')
        self.add_2_elements('js-level-form', 'id_label', '79', 'id_name', '79th')
        self.wait_and_assert_list_after_submit(form_class, 'available_levels_list', '79')

        # Now John sees new levels in a list of available levels and clicks them
        # to move them to a list of selected levels
        # He adds the level 46th
        self.browser.find_element_by_xpath(
            f'//form[@class="{form_class}"]//div[@id="available_levels_list"]/a[contains(text(), "46")]').click()
        self.wait_and_assert_list_after_submit(form_class, 'selected_levels_list', '46')
        # and the level 79th
        self.browser.find_element_by_xpath(
            f'//form[@class="{form_class}"]//div[@id="available_levels_list"]/a[contains(text(), "79")]').click()
        self.wait_and_assert_list_after_submit(form_class, 'selected_levels_list', '79')

        # And finally John clicks Create
        levels_group_form.submit()

    def add_property(self, label):
        form_class = 'js-property-form'
        # John waits for the form to appear (but no more than 10 sec!)
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, form_class))
        )
        collection_form = self.browser.find_element_by_class_name(form_class)
        # Then John types label into a textbox Property label,
        self.wait_and_type(form_class, 'id_label', label)

        # John wants to select a GUI element, but finds out that the one he needs is absent.
        # So he decides to add it and clicks '+' button next to the GUI element dropdown list
        self.wait_and_click_add_btn('/en/metadb/guielements/create/')

        # John adds a new GUI element
        self.add_2_elements('js-gui-element-form', 'id_name', 'feature',
                                                   'id_caption', 'Feature')
        self.wait_and_assert_select_after_submit(form_class, 'id_gui_element', 'feature')

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
        self.assertIn('tab-specpar', tab_ids)
        self.assertIn('tab-data', tab_ids)
        self.assertIn('tab-other', tab_ids)

        # Collection tab is active.
        tab_collection = self.browser.find_element_by_id('tab-collection')
        self.assertTrue('active' in tab_collection.get_attribute('class'))

        # John decides to start with Collection tab.
        # There is a button Create on the tab Collection.
        create_btn = tab_collection.find_element_by_class_name('js-create')

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
        tab_dataset = self.browser.find_element_by_id('tab-dataset')
        self.assertTrue('active' in tab_dataset.get_attribute('class'))

        # There is a button Create on the tab Dataset.
        create_btn = tab_dataset.find_element_by_class_name('js-create')
        sleep(1)
        # John decides to add a new dataset.
        # He presses button Create on the tab Dataset.
        create_btn.click()

        # A new modal window for creating a new dataset opens inviting him to enter corresponding info.
        # John waits for the form to be fully loaded (but no more than 10 sec!)
        form_class = 'js-dataset-form'
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, form_class))
        )
        dataset_form = self.browser.find_element_by_class_name(form_class)

        # John wants to select a collection, but finds out that the one he needs is absent.
        # So he decides to add it and clicks '+' button next to the Collection dropdown list.
        self.wait_and_click_add_btn('/en/metadb/collections/create/')

        # John adds a new collection
        self.add_collection()
        self.wait_and_assert_select_after_submit(form_class, 'id_collection', 'JohnCol')

        # John wants to select a resolution, but finds out that the needed one is absent
        # So he decides to add it and clicks '+' button next to the Resolution dropdown list.
        self.wait_and_click_add_btn('/en/metadb/resolutions/create/')

        self.add_2_elements('js-resolution-form', 'id_name', '0.13x0.13', 'id_subpath1', '0.13x0.13/')
        self.wait_and_assert_select_after_submit(form_class, 'id_resolution', '0.13x0.13')

        # John wants to select a scenario, but finds out that the needed one is absent
        # So he decides to add it and clicks '+' button next to the Scenario dropdown list.
        self.wait_and_click_add_btn('/en/metadb/scenarios/create/')

        self.add_2_elements('js-scenario-form', 'id_name', 'Specific', 'id_subpath0', 'specific/')
        self.wait_and_assert_select_after_submit(form_class, 'id_scenario', 'Specific')

        # John wants to select a data kind, but finds out that the needed one is absent
        # So he decides to add it and clicks '+' button next to the Data kind dropdown list.
        self.wait_and_click_add_btn('/en/metadb/datakinds/create/')

        self.add_1_element('js-datakind-form', 'id_name', 'fractal')
        self.wait_and_assert_select_after_submit(form_class, 'id_data_kind', 'fractal')

        # John types 'JohnCol 0x13x0.13' into a textbox Description,
        self.wait_and_type(form_class, 'id_description', 'JohnCol 0x13x0.13')
        #  '20000101' into a textbox Time start,
        self.wait_and_type(form_class, 'id_time_start', '20000101')
        #  '20001231' into a textbox Time end,
        self.wait_and_type(form_class, 'id_time_end', '20001231')

        # John wants to select a file type, but finds out that the needed one is absent
        # So he decides to add it and clicks '+' button next to the File type dropdown list.
        self.wait_and_click_add_btn('/en/metadb/filetypes/create/')

        self.add_1_element('js-filetype-form', 'id_name', 'hdf5')
        self.wait_and_assert_select_after_submit(form_class, 'id_file_type', 'hdf5')

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
        tab_data = self.browser.find_element_by_id('tab-data')
        self.assertTrue('active' in tab_data.get_attribute('class'))

        # There is a button Create on the tab Dataset.
        create_btn = tab_data.find_element_by_class_name('js-create')

        # John decides to add a new dataset.
        # He presses button Create on the tab Dataset.
        create_btn.click()

        # A new modal window for creating a new data opens inviting him to enter corresponding info.
        # John waits for the form to be fully loaded (but no more than 10 sec!)
        form_class = 'js-data-form'
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, form_class))
        )
        data_form = self.browser.find_element_by_class_name(form_class)

        # John selects a collection with index=1
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, 'id_collection'))
        )
        sleep(1)
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
        self.wait_and_click_add_btn('/en/metadb/levelsvariables/create/')

        # John adds a levels variable
        self.add_1_element('js-levels-variable-form', 'id_name', 'gamma_level')
        self.wait_and_assert_select_after_submit(form_class, 'id_levels_variable', 'gamma_level')

        # John wants to select a variable, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the Variable dropdown list.
        self.wait_and_click_add_btn('/en/metadb/variables/create/')

        # John adds a variable
        self.add_1_element('js-variable-form', 'id_name', 'spec3m')
        self.wait_and_assert_select_after_submit(form_class, 'id_variable', 'spec3m')

        # John wants to select a unit of measurement, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the Unit dropdown list.
        self.wait_and_click_add_btn('/en/metadb/units/create/')

        # John adds a unit
        self.add_1_element('js-unit-form', 'id_name', 'mRd/yr')
        self.wait_and_assert_select_after_submit(form_class, 'id_unitsi18n', 'mRd/yr')

        # John decides to use Property/Property value and checks Use property checkbox
        data_form.find_element_by_id('id_use_property').click()
        # This enables Property...
        self.assertFalse(data_form.find_element_by_id('id_property').get_attribute('disabled'))
        # ... and Property value dropdown lists
        self.assertFalse(data_form.find_element_by_id('id_property_value').get_attribute('disabled'))

        # John wants to select a property, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the Proprty dropdown list.
        self.wait_and_click_add_btn('/en/metadb/properties/create/')

        # John adds a property
        self.add_property('volume')
        self.wait_and_assert_select_after_submit(form_class, 'id_property', 'volume')

        # John wants to select a property value, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the Property value dropdown list.
        self.wait_and_click_add_btn('/en/metadb/propertyvalues/create/')

        # John adds a property value
        self.add_1_element('js-property-value-form', 'id_label', 'low')
        self.wait_and_assert_select_after_submit(form_class, 'id_property_value', 'low')

        # John wants to select a root directory, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the Root directory dropdown list.
        self.wait_and_click_add_btn('/en/metadb/rootdirs/create/')

        # John adds a root directory
        self.add_1_element('js-root-dir-form', 'id_name', '/mnt/data/JohnCol/')
        self.wait_and_assert_select_after_submit(form_class, 'id_root_dir', '/mnt/data/JohnCol/')

        # John wants to select a file name pattern, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the File name pattern dropdown list.
        self.wait_and_click_add_btn('/en/metadb/filenames/create/')

        # John adds a file name pattern
        self.add_1_element('js-file-form', 'id_name_pattern', 'experiment/%mm%_%year%.nc')
        self.wait_and_assert_select_after_submit(form_class, 'id_file', 'experiment/%mm%_%year%.nc')

        # John types '3.14' into a textbox Scale...
        self.wait_and_type(form_class, 'id_scale', '3.14')
        # ... and '2.76' into a textbox Offset
        self.wait_and_type(form_class, 'id_offset', '-2.76')

        # When he clicks Create data modal window closes and Data table updates.
        data_form.submit()


#------------------------------------------------------------------------------------------------------

    def test_can_add_a_parameter_and_retrieve_it(self):
        # John decides to expoler the Parameter tab
        # He opens the main page again
        self.browser.get('http://localhost:8001/metadb/')

        # He clicks tha Parameter tab
        self.browser.find_element_by_xpath(
            '//ul[contains(@class, "nav-tabs")]//a[@href="#tab-specpar"]').click()

        # Now the Parameter tab is active.
        tab_specpar = self.browser.find_element_by_id('tab-specpar')
        self.assertTrue('active' in tab_specpar.get_attribute('class'))

        # There is a button Create on the tab Parameter.
        create_btn = tab_specpar.find_element_by_class_name('js-create')

        # John decides to add a new specific parameter.
        # He presses button Create on the tab Parameter.
        create_btn.click()

        # A new modal window for creating a new specific parameter opens inviting him to enter corresponding info.
        # John waits for the form to be fully loaded (but no more than 10 sec!)
        form_class = 'js-specpar-form'
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, form_class))
        )
        specpar_form = self.browser.find_element_by_class_name(form_class)
        sleep(1)

        # John wants to select a meteorological parameter, but finds out that the needed one is absent
        # So he decides to add it and clicks '+' button next to the Parameter dropdown list.
        self.wait_and_click_add_btn('/en/metadb/parameters/create/')

        # John adds a parameter
        self.add_parameter()
        self.wait_and_assert_select_after_submit(form_class, 'id_parameteri18n', 'Fogness')

        # John wants to select a time step, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the Time step dropdown list.
        self.wait_and_click_add_btn('/en/metadb/timesteps/create/')

        # John adds a time step
        self.add_3_elements('js-timestep-form', 'id_label', '5h', 'id_name', '5 hours',
                            'id_subpath2', '5h/')
        self.wait_and_assert_select_after_submit(form_class, 'id_time_stepi18n', '5 hours')

        # John wants to select a levels group, but finds out that the needed one is absent.
        # So he decides to add it and clicks '+' button next to the Levels group dropdown list.
        self.wait_and_click_add_btn('/en/metadb/levelsgroups/create/')

        # John adds a levels group
        self.add_levels_group()
        self.wait_and_assert_select_after_submit(form_class, 'id_lvs_group', 'Delta levels')

        # When he clicks Create specific parameter modal window closes and Parameter table updates.
        specpar_form.submit()
