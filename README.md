# cpims-dcs-3.0
CPIMS DCS upgrade

# cpovc_registry

## CODE BASE
Refactored all the code base for cpovc_registry to python 2.7 compatible.

# URLS
Complete tests for urls.

# MODELS
we wrote test for models.
Here you will see that we first imported TestCase and derived our test classes from it, using descriptive names so that we can easily identify any failing tests in the test output. We then call setUpTestData() to create objects that we will use but not modify in any of the test methods.

The field tests check that the values of the field labels (verbose_name) and that the size of the character fields are as expected. These methods all have descriptive names, and follow the same pattern:

        # Get an author object to test
        unit = RegOrgUnit.objects.get(id=1)
        # Get the metadata for the required field and use it to query the required field data
        field_label = unit._meta.get_field('org_unit_id_vis').verbose_name
        # Compare the value to the expected result
        self.assertEqual(field_label, 'org unit id vis')

# FORMS
Tests for forms are also written
currently tests for user login forms are done.

# HTML
Ensured all htmls unclosed tags are closed

# VIEWS
Complete tests for views

        # When retrieving pages, remember to specify the path of the URL, not the whole domain.
        response = self.client.post(self.register_details_url, org_id=2 )
        # test expected response
        self.assertEquals(response.status_code, 200)
        # Test that a given request is rendered by a given Django template.
        self.assertTemplateUsed(response, 'registry/org_units_details.html')

## GROUP MEMEBERS
1. DAVID SARUNI, 0796789225, sarunidavid11126@gmail.com, https://github.com/DavidSaruni
2. MICHOMA PETER, 0710174169, michomapeter67@gmail.com, github.com/Michomapeter
3. SHARON JEPNGETICH, 0729258337, jepngetichs65@gmail.com, https://github.com/Sharonjep 
4. ASHIOYA JOTHAM, 0792798789, victorashioya960@gmail.com, github.com/ashioyajotham
5. IMMANUEL KIMANI, 0704637682,immanuel4082@gmail.com, github.com/immanuel4082
