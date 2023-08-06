.. image:: https://raw.githubusercontent.com/senaite/senaite.api/master/static/api-logo.png
   :alt: senaite.api
   :height: 64 px
   :align: center

- **SENAITE.API**: *The Swiss-Army-Knife for SENAITE Core and Add-on developers*

.. image:: https://img.shields.io/pypi/v/senaite.api.svg?style=flat-square
   :target: https://pypi.python.org/pypi/senaite.api

.. image:: https://img.shields.io/github/issues-pr/senaite/senaite.api.svg?style=flat-square
   :target: https://github.com/senaite/senaite.api/pulls

.. image:: https://img.shields.io/github/issues/senaite/senaite.api.svg?style=flat-square
   :target: https://github.com/senaite/senaite.api/issues

.. image:: https://img.shields.io/badge/README-GitHub-blue.svg?style=flat-square
   :target: https://github.com/senaite/senaite.api#readme

About
=====

SENAITE API is the Swiss-Army-Knife for SENAITE Core and Add-on developers. It
provides a sane interface for common tasks in SENAITE, like e.g. object
creation, lookup by ID/UID, search etc.

Please see the doctests for further details and usage:

-  `Core API Documentation`_
-  `Analysis API Documentation`_


Installation
============

Please follow the installations instructions for `Plone 4`_ and
`senaite.lims`_.

To install SENAITE API, you have to add `senaite.api` into the
`eggs` list inside the `[buildout]` section of your
`buildout.cfg`::

   [buildout]
   parts =
       instance
   extends =
       http://dist.plone.org/release/4.3.17/versions.cfg
   find-links =
       http://dist.plone.org/release/4.3.17
       http://dist.plone.org/thirdparty
   eggs =
       Plone
       Pillow
       senaite.lims
       senaite.api
   zcml =
   eggs-directory = ${buildout:directory}/eggs

   [instance]
   recipe = plone.recipe.zope2instance
   user = admin:admin
   http-address = 0.0.0.0:8080
   eggs =
       ${buildout:eggs}
   zcml =
       ${buildout:zcml}

   [versions]
   setuptools =
   zc.buildout =


**Note**

The above example works for the buildout created by the unified
installer. If you however have a custom buildout you might need to add
the egg to the `eggs` list in the `[instance]` section rather than
adding it in the `[buildout]` section.

Also see this section of the Plone documentation for further details:
https://docs.plone.org/4/en/manage/installing/installing_addons.html

**Important**

For the changes to take effect you need to re-run buildout from your
console::

   bin/buildout


.. _Plone 4: https://docs.plone.org/4/en/manage/installing/index.html
.. _senaite.lims: https://github.com/senaite/senaite.lims#installation
.. _Core API Documentation: https://github.com/senaite/senaite.api/blob/master/src/senaite/api/docs/API.rst
.. _Analysis API Documentation: https://github.com/senaite/senaite.api/blob/master/src/senaite/api/docs/API_analysis.rst


SENAITE API DOCTEST
===================

The SENAITE LIMS API provides single functions for single purposes.
This Test builds completely on the API without any further imports needed.

Running this test from the buildout directory::

    bin/test test_doctests -t API

Introduction
------------

The purpose of this API is to help coders to follow the DRY principle (Don't
Repeat Yourself). It also ensures that the most effective and efficient method is
used to achieve a task.

Import it first::

    >>> from senaite import api


Getting the Portal
------------------

The Portal is the SENAITE LIMS root object::

    >>> portal = api.get_portal()
    >>> portal
    <PloneSite at /plone>


Getting the Setup object
------------------------

The Setup object gives access to all of the Bika configuration settings::

    >>> bika_setup = api.get_setup()
    >>> bika_setup
    <BikaSetup at /plone/bika_setup>


Creating new Content
--------------------

Creating new contents in Bika LIMS requires some special knowledge.
This function helps to do it right and creates a content for you.

Here we create a new `Client` in the `plone/clients` folder::

    >>> client = api.create(portal.clients, "Client", title="Test Client")
    >>> client
    <Client at /plone/clients/client-1>

     >>> client.Title()
     'Test Client'


Getting a Tool
--------------

There are many ways to get a tool in Bika LIMS / Plone. This function
centralizes this functionality and makes it painless::

    >>> api.get_tool("bika_setup_catalog")
    <BikaSetupCatalog at /plone/bika_setup_catalog>

Trying to fetch an non-existing tool raises a custom `SenaiteAPIError`::

    >>> api.get_tool("NotExistingTool")
    Traceback (most recent call last):
    [...]
    SenaiteAPIError: No tool named 'NotExistingTool' found.

This error can also be used for custom methods with the `fail` function::

    >>> api.fail("This failed badly")
    Traceback (most recent call last):
    [...]
    SenaiteAPIError: This failed badly


Getting an Object
-----------------

Getting a tool from a catalog brain is a common task in Bika LIMS. This function
provides an unified interface to portal objects **and** brains.
Furthermore it is idempotent, so it can be called multiple times in a row.

We will demonstrate the usage on the client object we created above::

    >>> api.get_object(client)
    <Client at /plone/clients/client-1>

    >>> api.get_object(api.get_object(client))
    <Client at /plone/clients/client-1>

Now we show it with catalog results::

    >>> portal_catalog = api.get_tool("portal_catalog")
    >>> brains = portal_catalog(portal_type="Client")
    >>> brains
    [<Products.ZCatalog.Catalog.mybrains object at 0x...>]

    >>> brain = brains[0]

    >>> api.get_object(brain)
    <Client at /plone/clients/client-1>

    >>> api.get_object(api.get_object(brain))
    <Client at /plone/clients/client-1>

No supported objects raise an error::

    >>> api.get_object(object())
    Traceback (most recent call last):
    [...]
    SenaiteAPIError: <object object at 0x...> is not supported.

To check if an object is supported, e.g. is an ATCT, Dexterity, ZCatalog or
Portal object, we can use the `is_object` function::

    >>> api.is_object(client)
    True

    >>> api.is_object(brain)
    True

    >>> api.is_object(api.get_portal())
    True

    >>> api.is_object(None)
    False

  >>> api.is_object(object())
    False


Checking if an Object is the Portal
-----------------------------------

Sometimes it can be handy to check if the current object is the portal::

    >>> api.is_portal(portal)
    True

    >>> api.is_portal(client)
    False

    >>> api.is_portal(object())
    False


Checking if an Object is a Catalog Brain
----------------------------------------

Knowing if we have an object or a brain can be handy. This function checks this for you::

    >>> api.is_brain(brain)
    True

    >>> api.is_brain(api.get_object(brain))
    False

    >>> api.is_brain(object())
    False


Checking if an Object is a Dexterity Content
--------------------------------------------

This function checks if an object is a `Dexterity` content type::

    >>> api.is_dexterity_content(client)
    False

    >>> api.is_dexterity_content(portal)
    False

We currently have no `Dexterity` contents, so testing this comes later...


Checking if an Object is an AT Content
--------------------------------------

This function checks if an object is an `Archetypes` content type::

    >>> api.is_at_content(client)
    True

    >>> api.is_at_content(portal)
    False

    >>> api.is_at_content(object())
    False


Getting the Schema of a Content
-------------------------------

The schema contains the fields of a content object. Getting the schema is a
common task, but differs between `ATContentType` based objects and `Dexterity`
based objects. This function brings it under one umbrella::

    >>> schema = api.get_schema(client)
    >>> schema
    <Products.Archetypes.Schema.Schema object at 0x...>

Catalog brains are also supported::

    >>> api.get_schema(brain)
    <Products.Archetypes.Schema.Schema object at 0x...>


Getting the Fields of a Content
-------------------------------

The fields contain all the values that an object holds and are therefore
responsible for getting and setting the information.

This function returns the fields as a dictionary mapping of `{"key": value}`::

    >>> fields = api.get_fields(client)
    >>> fields.get("ClientID")
    <Field ClientID(string:rw)>

Catalog brains are also supported::

    >>> api.get_fields(brain).get("ClientID")
    <Field ClientID(string:rw)>


Getting the ID of a Content
---------------------------

Getting the ID is a common task in Bika LIMS.
This function takes care that catalog brains are not waked up for this task::

    >>> api.get_id(portal)
    'plone'

    >>> api.get_id(client)
    'client-1'

    >>> api.get_id(brain)
    'client-1'


Getting the Title of a Content
------------------------------

Getting the Title is a common task in Bika LIMS.
This function takes care that catalog brains are not waked up for this task::

    >>> api.get_title(portal)
    u'Plone site'

    >>> api.get_title(client)
    'Test Client'

    >>> api.get_title(brain)
    'Test Client'


Getting the Description of a Content
------------------------------------

Getting the Description is a common task in Bika LIMS.
This function takes care that catalog brains are not waked up for this task::

    >>> api.get_description(portal)
    ''

    >>> api.get_description(client)
    ''

    >>> api.get_description(brain)
    ''


Getting the UID of a Content
----------------------------

Getting the UID is a common task in Bika LIMS.
This function takes care that catalog brains are not waked up for this task.

The portal object actually has no UID. This funciton defines it therfore to be `0`::

    >>> api.get_uid(portal)
    '0'

    >>> uid_client = api.get_uid(client)
    >>> uid_client_brain = api.get_uid(brain)
    >>> uid_client is uid_client_brain
    True


Getting the URL of a Content
----------------------------

Getting the URL is a common task in Bika LIMS.
This function takes care that catalog brains are not waked up for this task::

    >>> api.get_url(portal)
    'http://nohost/plone'

    >>> api.get_url(client)
    'http://nohost/plone/clients/client-1'

    >>> api.get_url(brain)
    'http://nohost/plone/clients/client-1'


Getting the Icon of a Content
-----------------------------

::

    >>> api.get_icon(client)
    '<img width="16" height="16" src="http://nohost/plone/++resource++bika.lims.images/client.png" title="Test Client" />'

    >>> api.get_icon(brain)
    '<img width="16" height="16" src="http://nohost/plone/++resource++bika.lims.images/client.png" title="Test Client" />'

    >>> api.get_icon(client, html_tag=False)
    'http://nohost/plone/++resource++bika.lims.images/client.png'

    >>> api.get_icon(client, html_tag=False)
    'http://nohost/plone/++resource++bika.lims.images/client.png'


Getting an object by UID
------------------------

This function finds an object by its uinique ID (UID).
The portal object with the defined UId of '0' is also supported::

    >>> api.get_object_by_uid('0')
    <PloneSite at /plone>

    >>> api.get_object_by_uid(uid_client)
    <Client at /plone/clients/client-1>

    >>> api.get_object_by_uid(uid_client_brain)
    <Client at /plone/clients/client-1>

If a default value is provided, the function will never fail.  Any exception
or error will result in the default value being returned::

    >>> api.get_object_by_uid('invalid uid', 'default')
    'default'

    >>> api.get_object_by_uid(None, 'default')
    'default'


Getting an object by Path
-------------------------

This function finds an object by its physical path::

    >>> api.get_object_by_path('/plone')
    <PloneSite at /plone>

    >>> api.get_object_by_path('/plone/clients/client-1')
    <Client at /plone/clients/client-1>

Paths outside the portal raise an error::

    >>> api.get_object_by_path('/root')
    Traceback (most recent call last):
    [...]
    SenaiteAPIError: Not a physical path inside the portal.

Any exception returns default value::

    >>> api.get_object_by_path('/invaid/path', 'default')
    'default'

    >>> api.get_object_by_path(None, 'default')
    'default'


Getting the Physical Path of an Object
--------------------------------------

The physical path describes exactly where an object is located inside the portal.
This function unifies the different approaches to get the physical path and does
so in the most efficient way::

    >>> api.get_path(portal)
    '/plone'

    >>> api.get_path(client)
    '/plone/clients/client-1'

    >>> api.get_path(brain)
    '/plone/clients/client-1'

    >>> api.get_path(object())
    Traceback (most recent call last):
    [...]
    SenaiteAPIError: <object object at 0x...> is not supported.


Getting the Physical Parent Path of an Object
---------------------------------------------

This function returns the physical path of the parent object::

    >>> api.get_parent_path(client)
    '/plone/clients'

    >>> api.get_parent_path(brain)
    '/plone/clients'

However, this function goes only up to the portal object::

    >>> api.get_parent_path(portal)
    '/plone'

Like with the other functions, only portal objects are supported::

    >>> api.get_parent_path(object())
    Traceback (most recent call last):
    [...]
    SenaiteAPIError: <object object at 0x...> is not supported.


Getting the Parent Object
-------------------------

This function returns the parent object::

    >>> api.get_parent(client)
    <ClientFolder at /plone/clients>

Brains are also supported::

    >>> api.get_parent(brain)
    <ClientFolder at /plone/clients>

The function can also use a catalog query on the `portal_catalog` and return a
brain, if the passed parameter `catalog_search` was set to true. ::

    >>> api.get_parent(client, catalog_search=True)
    <Products.ZCatalog.Catalog.mybrains object at 0x...>

    >>> api.get_parent(brain, catalog_search=True)
    <Products.ZCatalog.Catalog.mybrains object at 0x...>

However, this function goes only up to the portal object::

    >>> api.get_parent(portal)
    <PloneSite at /plone>

Like with the other functions, only portal objects are supported::

    >>> api.get_parent(object())
    Traceback (most recent call last):
    [...]
    SenaiteAPIError: <object object at 0x...> is not supported.


Searching Objects
-----------------

Searching in Bika LIMS requires knowledge in which catalog the object is indexed.
This function unifies all Bika LIMS catalog to a single search interface::

    >>> results = api.search({'portal_type': 'Client'})
    >>> results
    [<Products.ZCatalog.Catalog.mybrains object at 0x...>]

Multiple content types are also supported::

    >>> results = api.search({'portal_type': ['Client', 'ClientFolder'], 'sort_on': 'getId'})
    >>> map(api.get_id, results)
    ['client-1', 'clients']

Now we create some objects which are located in the `bika_setup_catalog`::

    >>> instruments = bika_setup.bika_instruments
    >>> instrument1 = api.create(instruments, "Instrument", title="Instrument-1")
    >>> instrument2 = api.create(instruments, "Instrument", title="Instrument-2")
    >>> instrument3 = api.create(instruments, "Instrument", title="Instrument-3")

    >>> results = api.search({'portal_type': 'Instrument', 'sort_on': 'getId'})
    >>> len(results)
    3

    >>> map(api.get_id, results)
    ['instrument-1', 'instrument-2', 'instrument-3']

Queries which result in multiple catalogs will be refused, as it would require
manual merging and sorting of the results afterwards. Thus, we fail here::

    >>> results = api.search({'portal_type': ['Client', 'ClientFolder', 'Instrument'], 'sort_on': 'getId'})
    Traceback (most recent call last):
    [...]
    SenaiteAPIError: Multi Catalog Queries are not supported, please specify a catalog.

Catalog queries w/o any `portal_type`, default to the `portal_catalog`, which
will not find the following items::

    >>> analysiscategories = bika_setup.bika_analysiscategories
    >>> analysiscategory1 = api.create(analysiscategories, "AnalysisCategory", title="AC-1")
    >>> analysiscategory2 = api.create(analysiscategories, "AnalysisCategory", title="AC-2")
    >>> analysiscategory3 = api.create(analysiscategories, "AnalysisCategory", title="AC-3")

    >>> results = api.search({"id": "analysiscategory-1"})
    >>> len(results)
    0

Would we add the `portal_type`, the search function would ask the
`archetype_tool` for the right catalog, and it would return a result::

    >>> results = api.search({"portal_type": "AnalysisCategory", "id": "analysiscategory-1"})
    >>> len(results)
    1

We could also explicitly define a catalog to achieve the same::

    >>> results = api.search({"id": "analysiscategory-1"}, catalog="bika_setup_catalog")
    >>> len(results)
    1

To see inactive or dormant items, we must explicitly query them of filter them
afterwars manually::

    >>> results = api.search({"portal_type": "AnalysisCategory", "id": "analysiscategory-1"})
    >>> len(results)
    1

Now we deactivate the item::

    >>> analysiscategory1 = api.do_transition_for(analysiscategory1, 'deactivate')
    >>> api.is_active(analysiscategory1)
    False

The search will still find the item::

    >>> results = api.search({"portal_type": "AnalysisCategory", "id": "analysiscategory-1"})
    >>> len(results)
    1

Unless we filter it out manually::

    >>> len(filter(api.is_active, results))
    0

Or provide a correct query::

    >>> results = api.search({"portal_type": "AnalysisCategory", "id": "analysiscategory-1", "inactive_status": "active"})
    >>> len(results)
    1


Getting the registered Catalogs
-------------------------------

Bika LIMS uses multiple catalogs registered via the Archetype Tool. This
function returns a list of registered catalogs for a brain or object::

    >>> api.get_catalogs_for(client)
    [<CatalogTool at /plone/portal_catalog>]

    >>> api.get_catalogs_for(instrument1)
    [<BikaSetupCatalog at /plone/bika_setup_catalog>, <CatalogTool at /plone/portal_catalog>]

    >>> api.get_catalogs_for(analysiscategory1)
    [<BikaSetupCatalog at /plone/bika_setup_catalog>]


Getting an Attribute of an Object
---------------------------------

This function handles attributes and methods the same and returns their value.
It also handles security and is able to return a default value instead of
raising an `Unauthorized` error::

    >>> uid_brain = api.safe_getattr(brain, "UID")
    >>> uid_obj = api.safe_getattr(client, "UID")

    >>> uid_brain == uid_obj
    True

    >>> api.safe_getattr(brain, "review_state")
    'active'

    >>> api.safe_getattr(brain, "NONEXISTING")
    Traceback (most recent call last):
    [...]
    SenaiteAPIError: Attribute 'NONEXISTING' not found.

    >>> api.safe_getattr(brain, "NONEXISTING", "")
    ''

Getting the Portal Catalog
--------------------------

This tool is needed so often, that this function just returns it::

    >>> api.get_portal_catalog()
    <CatalogTool at /plone/portal_catalog>


Getting the Review History of an Object
---------------------------------------

The review history gives information about the objects' workflow changes::

    >>> review_history = api.get_review_history(client)
    >>> sorted(review_history[0].items())
    [('action', None), ('actor', 'test_user_1_'), ('comments', ''), ('review_state', 'active'), ('time', DateTime('...'))]


Getting the Revision History of an Object
-----------------------------------------

The review history gives information about the objects' workflow changes::

    >>> revision_history = api.get_revision_history(client)
    >>> sorted(revision_history[0])
    ['action', 'actor', 'actor_home', 'actorid', 'comments', 'review_state', 'state_title', 'time', 'transition_title', 'type']
    >>> revision_history[0]["transition_title"]
    u'Create'


Getting the assigned Workflows of an Object
-------------------------------------------

This function returns all assigned workflows for a given object::

    >>> api.get_workflows_for(bika_setup)
    ('bika_one_state_workflow',)

    >>> api.get_workflows_for(client)
    ('bika_client_workflow', 'bika_inactive_workflow')

This function also supports the portal_type as parameter::

    >>> api.get_workflows_for(api.get_portal_type(client))
    ('bika_client_workflow', 'bika_inactive_workflow')


Getting the Workflow Status of an Object
----------------------------------------

This function returns the state of a given object::

    >>> api.get_workflow_status_of(client)
    'active'

It is also capable to get the state of another state variable::

    >>> api.get_workflow_status_of(client, "inactive_state")
    'active'

Deactivate the client::

    >>> api.do_transition_for(client, "deactivate")
    <Client at /plone/clients/client-1>

    >>> api.get_workflow_status_of(client, "inactive_state")
    'inactive'

    >>> api.get_workflow_status_of(client)
    'active'

Reactivate the client::

    >>> api.do_transition_for(client, "activate")
    <Client at /plone/clients/client-1>

    >>> api.get_workflow_status_of(client, "inactive_state")
    'active'


Getting the available transitions for an object
-----------------------------------------------

This function returns all possible transitions from all workflows in the
object's workflow chain.

Let's create a Batch. It should allow us to invoke transitions from two
workflows; 'close' from the bika_batch_workflow, and 'cancel' from the
bika_cancellation_workflow::

    >>> batch1 = api.create(portal.batches, "Batch", title="Test Batch")
    >>> transitions = api.get_transitions_for(batch1)
    >>> len(transitions)
    2

The transitions are returned as a list of dictionaries. Since we cannot rely on
the order of dictionary keys, we will have to satisfy ourselves here with
checking that the two expected transitions are present in the return value::

    >>> 'Close' in [t['title'] for t in transitions]
    True
    >>> 'Cancel' in [t['title'] for t in transitions]
    True


Getting the creation date of an object
--------------------------------------

This function returns the creation date of a given object::

    >>> created = api.get_creation_date(client)
    >>> created
    DateTime('...')


Getting the modification date of an object
------------------------------------------

This function returns the modification date of a given object::

    >>> modified = api.get_modification_date(client)
    >>> modified
    DateTime('...')


Getting the review state of an object
-------------------------------------

This function returns the review state of a given object::

    >>> review_state = api.get_review_status(client)
    >>> review_state
    'active'

It should also work for catalog brains::

    >>> portal_catalog = api.get_tool("portal_catalog")
    >>> results = portal_catalog({"portal_type": "Client", "UID": api.get_uid(client)})
    >>> len(results)
    1
    >>> api.get_review_status(results[0]) == review_state
    True


Getting the registered Catalogs of an Object
--------------------------------------------

This function returns a list of all registered catalogs within the
`archetype_tool` for a given portal_type or object::

    >>> api.get_catalogs_for(client)
    [<CatalogTool at /plone/portal_catalog>]

It also supports the `portal_type` as a parameter::

    >>> api.get_catalogs_for("Analysis")
    [<BikaAnalysisCatalog at /plone/bika_analysis_catalog>]


Transitioning an Object
-----------------------

This function performs a workflow transition and returns the object::

    >>> client = api.do_transition_for(client, "deactivate")
    >>> api.is_active(client)
    False

    >>> client = api.do_transition_for(client, "activate")
    >>> api.is_active(client)
    True


Getting inactive/cancellation state of different workflows
----------------------------------------------------------

There are two workflows allowing an object to be set inactive.  We provide
the is_active function to return False if an item is set inactive with either
of these workflows.

In the search() test above, the is_active function's handling of brain states
is tested.  Here, I just want to test if object states are handled correctly.

For setup types, we use bika_inctive_workflow::

    >>> method1 = api.create(portal.methods, "Method", title="Test Method")
    >>> api.is_active(method1)
    True
    >>> method1 = api.do_transition_for(method1, 'deactivate')
    >>> api.is_active(method1)
    False

For transactional types, bika_cancellation_workflow is used::

    >>> batch1 = api.create(portal.batches, "Batch", title="Test Batch")
    >>> api.is_active(batch1)
    True
    >>> batch1 = api.do_transition_for(batch1, 'cancel')
    >>> api.is_active(batch1)
    False


Getting the granted Roles for a certain Permission on an Object
---------------------------------------------------------------

This function returns a list of Roles, which are granted the given Permission
for the passed in object::

    >>> api.get_roles_for_permission("Modify portal content", bika_setup)
    ['LabManager', 'Manager']



Checking if an Object is Versionable
------------------------------------

Some contents in Bika LIMS support versioning. This function checks this for you.

Instruments are not versionable::

    >>> api.is_versionable(instrument1)
    False

Analysisservices are versionable::

    >>> analysisservices = bika_setup.bika_analysisservices
    >>> analysisservice1 = api.create(analysisservices, "AnalysisService", title="AnalysisService-1")
    >>> analysisservice2 = api.create(analysisservices, "AnalysisService", title="AnalysisService-2")
    >>> analysisservice3 = api.create(analysisservices, "AnalysisService", title="AnalysisService-3")

    >>> api.is_versionable(analysisservice1)
    True


Getting the Version of an Object
--------------------------------

This function returns the version as an integer::

    >>> api.get_version(analysisservice1)
    0

Calling `processForm` bumps the version::

    >>> analysisservice1.processForm()
    >>> api.get_version(analysisservice1)
    1


Getting a Browser View
----------------------

Getting a browser view is a common task in Bika LIMS::

    >>> api.get_view("plone")
    <Products.Five.metaclass.Plone object at 0x...>

    >>> api.get_view("workflow_action")
    <Products.Five.metaclass.WorkflowAction object at 0x...>


Getting the Request
-------------------

This function will return the global request object::

    >>> api.get_request()
    <HTTPRequest, URL=http://nohost>


Getting a Group
---------------

Users in Bika LIMS are managed in groups. A common group is the `Clients` group,
where all users of client contacts are grouped.
This function gives easy access and is also idempotent::

    >>> clients_group = api.get_group("Clients")
    >>> clients_group
    <GroupData at /plone/portal_groupdata/Clients used for /plone/acl_users/source_groups>

    >>> api.get_group(clients_group)
    <GroupData at /plone/portal_groupdata/Clients used for /plone/acl_users/source_groups>

Non-existing groups are not found::

    >>> api.get_group("NonExistingGroup")


Getting a User
--------------

Users can be fetched by their user id. The function is idempotent and handles
user objects as well::

    >>> from plone.app.testing import TEST_USER_ID
    >>> user = api.get_user(TEST_USER_ID)
    >>> user
    <MemberData at /plone/portal_memberdata/test_user_1_ used for /plone/acl_users>

    >>> api.get_user(api.get_user(TEST_USER_ID))
    <MemberData at /plone/portal_memberdata/test_user_1_ used for /plone/acl_users>

Non-existing users are not found::

    >>> api.get_user("NonExistingUser")


Getting User Properties
-----------------------

User properties, like the email or full name, are stored as user properties.
This means that they are not on the user object. This function retrieves these
properties for you::

    >>> properties = api.get_user_properties(TEST_USER_ID)
    >>> sorted(properties.items())
    [('description', ''), ('email', ''), ('error_log_update', 0.0), ('ext_editor', False), ...]

    >>> sorted(api.get_user_properties(user).items())
    [('description', ''), ('email', ''), ('error_log_update', 0.0), ('ext_editor', False), ...]

An empty property dict is returned if no user could be found::

    >>> api.get_user_properties("NonExistingUser")
    {}

    >>> api.get_user_properties(None)
    {}


Getting Users by their Roles
----------------------------

::

    >>> from operator import methodcaller

Roles in Bika LIMS are basically a name for one or more permissions. For
example, a `LabManager` describes a role which is granted the most permissions.

To see which users are granted a certain role, you can use this function::

    >>> labmanagers = api.get_users_by_roles(["LabManager"])
    >>> sorted(labmanagers, key=methodcaller('getId'))
    [<PloneUser 'test_labmanager'>, <PloneUser 'test_labmanager1'>, <PloneUser 'test-user'>]

A single value can also be passed into this function::

    >>> sorted(api.get_users_by_roles("LabManager"), key=methodcaller('getId'))
    [<PloneUser 'test_labmanager'>, <PloneUser 'test_labmanager1'>, <PloneUser 'test-user'>]


Getting the Current User
------------------------

Getting the current logged in user::

    >>> api.get_current_user()
    <MemberData at /plone/portal_memberdata/test_user_1_ used for /plone/acl_users>


Getting the Contact associated to a Plone user
----------------------------------------------

Getting a Plone user previously registered with no contact assigned::

    >>> user = api.get_user('test_labmanager1')
    >>> contact = api.get_user_contact(user)
    >>> contact is None
    True

Assign a new contact to this user::

    >>> labcontacts = bika_setup.bika_labcontacts
    >>> labcontact = api.create(labcontacts, "LabContact", Firstname="Lab", Lastname="Manager")
    >>> labcontact.setUser(user)
    True

And get the contact associated to the user::

    >>> api.get_user_contact(user)
    <LabContact at /plone/bika_setup/bika_labcontacts/labcontact-1>

As well as if we specify only `LabContact` type::

    >>> api.get_user_contact(user, ['LabContact'])
    <LabContact at /plone/bika_setup/bika_labcontacts/labcontact-1>

But fails if we specify only `Contact` type::

    >>> nuser = api.get_user_contact(user, ['Contact'])
    >>> nuser is None
    True


Creating a Cache Key
--------------------

This function creates a good cache key for a generic object or brain::

    >>> key1 = api.get_cache_key(client)
    >>> key1
    'Client-client-1-...'

This can be also done for a catalog result brain::

    >>> portal_catalog = api.get_tool("portal_catalog")
    >>> brains = portal_catalog({"portal_type": "Client", "UID": api.get_uid(client)})
    >>> key2 = api.get_cache_key(brains[0])
    >>> key2
    'Client-client-1-...'

The two keys should be equal::

    >>> key1 == key2
    True

The key should change when the object get modified::

    >>> from zope.lifecycleevent import modified
    >>> client.setClientID("TESTCLIENT")
    >>> modified(client)
    >>> portal.aq_parent._p_jar.sync()
    >>> key3 = api.get_cache_key(client)
    >>> key3 != key1
    True

.. important:: Workflow changes do not change the modification date!
               A custom event subscriber will update it therefore.

A workflow transition should also change the cache key::

    >>> _ = api.do_transition_for(client, transition="deactivate")
    >>> api.get_inactive_status(client)
    'inactive'
    >>> key4 = api.get_cache_key(client)
    >>> key4 != key3
    True


Cache Key decorator
-------------------

This decorator can be used for `plone.memoize` cache decorators in classes.
The decorator expects that the first argument is the class instance (`self`) and
the second argument a brain or object::

    >>> from plone.memoize.volatile import cache

    >>> class BikaClass(object):
    ...     @cache(api.bika_cache_key_decorator)
    ...     def get_very_expensive_calculation(self, obj):
    ...         print "very expensive calculation"
    ...         return "calculation result"

Calling the (expensive) method of the class does the calculation just once::

    >>> instance = BikaClass()
    >>> instance.get_very_expensive_calculation(client)
    very expensive calculation
    'calculation result'
    >>> instance.get_very_expensive_calculation(client)
    'calculation result'

The decorator can also handle brains::

    >>> instance = BikaClass()
    >>> portal_catalog = api.get_tool("portal_catalog")
    >>> brain = portal_catalog(portal_type="Client")[0]
    >>> instance.get_very_expensive_calculation(brain)
    very expensive calculation
    'calculation result'
    >>> instance.get_very_expensive_calculation(brain)
    'calculation result'


ID Normalizer
-------------

Normalizes a string to be usable as a system ID::

    >>> api.normalize_id("My new ID")
    'my-new-id'

    >>> api.normalize_id("Really/Weird:Name;")
    'really-weird-name'

    >>> api.normalize_id(None)
    Traceback (most recent call last):
    [...]
    SenaiteAPIError: Type of argument must be string, found '<type 'NoneType'>'


File Normalizer
---------------

Normalizes a string to be usable as a file name::

    >>> api.normalize_filename("My new ID")
    'My new ID'

    >>> api.normalize_filename("Really/Weird:Name;")
    'Really-Weird-Name'

    >>> api.normalize_filename(None)
    Traceback (most recent call last):
    [...]
    SenaiteAPIError: Type of argument must be string, found '<type 'NoneType'>'


Check if an UID is valid
------------------------

Checks if an UID is a valid 23 alphanumeric uid::

    >>> api.is_uid("ajw2uw9")
    False

    >>> api.is_uid(None)
    False

    >>> api.is_uid("")
    False

    >>> api.is_uid("0")
    False

    >>> api.is_uid('0e1dfc3d10d747bf999948a071bc161e')
    True

Checks if an UID is a valid 23 alphanumeric uid and with a brain::

    >>> api.is_uid("ajw2uw9", validate=True)
    False

    >>> api.is_uid(None, validate=True)
    False

    >>> api.is_uid("", validate=True)
    False

    >>> api.is_uid("0", validate=True)
    False

    >>> api.is_uid('0e1dfc3d10d747bf999948a071bc161e', validate=True)
    False

    >>> asfolder = self.portal.bika_setup.bika_analysisservices
    >>> serv = api.create(asfolder, "AnalysisService", title="AS test")
    >>> serv.setKeyword("as_test")
    >>> uid = serv.UID()
    >>> api.is_uid(uid, validate=True)
    True


Check if a Date is valid
------------------------

Do some imports first::

    >>> from datetime import datetime
    >>> from DateTime import DateTime

Checks if a DateTime is valid::

    >>> now = DateTime()
    >>> api.is_date(now)
    True

    >>> now = datetime.now()
    >>> api.is_date(now)
    True

    >>> now = DateTime(now)
    >>> api.is_date(now)
    True

    >>> api.is_date(None)
    False

    >>> api.is_date('2018-04-23')
    False


Try conversions to Date
-----------------------

Try to convert to DateTime::

    >>> now = DateTime()
    >>> zpdt = api.to_date(now)
    >>> zpdt.ISO8601() == now.ISO8601()
    True

    >>> now = datetime.now()
    >>> zpdt = api.to_date(now)
    >>> pydt = zpdt.asdatetime()

Note that here, for the comparison between dates, we convert DateTime to python
datetime, cause DateTime.strftime() is broken for timezones (always looks at
system time zone, ignores the timezone and offset of the DateTime instance
itself)::

    >>> pydt.strftime('%Y-%m-%dT%H:%M:%S') == now.strftime('%Y-%m-%dT%H:%M:%S')
    True

Try the same, but with utcnow() instead::

    >>> now = datetime.utcnow()
    >>> zpdt = api.to_date(now)
    >>> pydt = zpdt.asdatetime()
    >>> pydt.strftime('%Y-%m-%dT%H:%M:%S') == now.strftime('%Y-%m-%dT%H:%M:%S')
    True

Now we convert just a string formatted date::

    >>> strd = "2018-12-01 17:50:34"
    >>> zpdt = api.to_date(strd)
    >>> zpdt.ISO8601()
    '2018-12-01T17:50:34'

Now we convert just a string formatted date, but with timezone::

    >>> strd = "2018-12-01 17:50:34 GMT+1"
    >>> zpdt = api.to_date(strd)
    >>> zpdt.ISO8601()
    '2018-12-01T17:50:34+01:00'

We also check a bad date here (note the month is 13)::

    >>> strd = "2018-13-01 17:50:34"
    >>> zpdt = api.to_date(strd)
    >>> api.is_date(zpdt)
    False

And with European format::

    >>> strd = "01.12.2018 17:50:34"
    >>> zpdt = api.to_date(strd)
    >>> zpdt.ISO8601()
    '2018-12-01T17:50:34'

    >>> zpdt = api.to_date(None)
    >>> zpdt is None
    True

Use a string formatted date as fallback::

    >>> strd = "2018-13-01 17:50:34"
    >>> default_date = "2018-01-01 19:30:30"
    >>> zpdt = api.to_date(strd, default_date)
    >>> zpdt.ISO8601()
    '2018-01-01T19:30:30'

Use a DateTime object as fallback::

    >>> strd = "2018-13-01 17:50:34"
    >>> default_date = "2018-01-01 19:30:30"
    >>> default_date = api.to_date(default_date)
    >>> zpdt = api.to_date(strd, default_date)
    >>> zpdt.ISO8601() == default_date.ISO8601()
    True

Use a datetime object as fallback::

    >>> strd = "2018-13-01 17:50:34"
    >>> default_date = datetime.now()
    >>> zpdt = api.to_date(strd, default_date)
    >>> dzpdt = api.to_date(default_date)
    >>> zpdt.ISO8601() == dzpdt.ISO8601()
    True

Use a non-conversionable value as fallback::

    >>> strd = "2018-13-01 17:50:34"
    >>> default_date = "something wrong here"
    >>> zpdt = api.to_date(strd, default_date)
    >>> zpdt is None
    True


Check if floatable
------------------

::

    >>> api.is_floatable(None)
    False

    >>> api.is_floatable("")
    False

    >>> api.is_floatable("31")
    True

    >>> api.is_floatable("31.23")
    True

    >>> api.is_floatable("-13")
    True

    >>> api.is_floatable("12,35")
    False


Convert to a float number
-------------------------

::

    >>> api.to_float("2")
    2.0

    >>> api.to_float("2.234")
    2.234

With default fallback::

    >>> api.to_float(None, 2)
    2.0

    >>> api.to_float(None, "2")
    2.0

    >>> api.to_float("", 2)
    2.0

    >>> api.to_float("", "2")
    2.0

    >>> api.to_float(2.1, 2)
    2.1

    >>> api.to_float("2.1", 2)
    2.1

    >>> api.to_float("2.1", "2")
    2.1


API Analysis
============

The api_analysis provides single functions for single purposes especifically
related with analyses.

Running this test from the buildout directory::

    bin/test test_textual_doctests -t API_analysis


Test Setup
----------

Needed Imports::

    >>> import re
    >>> from AccessControl.PermissionRole import rolesForPermissionOn
    >>> from bika.lims import api
    >>> from bika.lims.api.analysis import is_out_of_range
    >>> from bika.lims.content.analysisrequest import AnalysisRequest
    >>> from bika.lims.content.sample import Sample
    >>> from bika.lims.content.samplepartition import SamplePartition
    >>> from bika.lims.utils.analysisrequest import create_analysisrequest
    >>> from bika.lims.utils.sample import create_sample
    >>> from bika.lims.utils import tmpID
    >>> from bika.lims.workflow import doActionFor
    >>> from bika.lims.workflow import getCurrentState
    >>> from bika.lims.workflow import getAllowedTransitions
    >>> from DateTime import DateTime
    >>> from plone.app.testing import TEST_USER_ID
    >>> from plone.app.testing import TEST_USER_PASSWORD
    >>> from plone.app.testing import setRoles

Functional Helpers::

    >>> def start_server():
    ...     from Testing.ZopeTestCase.utils import startZServer
    ...     ip, port = startZServer()
    ...     return "http://{}:{}/{}".format(ip, port, portal.id)

Variables::

    >>> portal = self.portal
    >>> request = self.request
    >>> bikasetup = portal.bika_setup

We need to create some basic objects for the test::

    >>> setRoles(portal, TEST_USER_ID, ['LabManager',])
    >>> date_now = DateTime().strftime("%Y-%m-%d")
    >>> date_future = (DateTime() + 5).strftime("%Y-%m-%d")
    >>> client = api.create(portal.clients, "Client", Name="Happy Hills", ClientID="HH", MemberDiscountApplies=True)
    >>> contact = api.create(client, "Contact", Firstname="Rita", Lastname="Mohale")
    >>> sampletype = api.create(bikasetup.bika_sampletypes, "SampleType", title="Water", Prefix="W")
    >>> labcontact = api.create(bikasetup.bika_labcontacts, "LabContact", Firstname="Lab", Lastname="Manager")
    >>> department = api.create(bikasetup.bika_departments, "Department", title="Chemistry", Manager=labcontact)
    >>> category = api.create(bikasetup.bika_analysiscategories, "AnalysisCategory", title="Metals", Department=department)
    >>> supplier = api.create(bikasetup.bika_suppliers, "Supplier", Name="Naralabs")
    >>> Cu = api.create(bikasetup.bika_analysisservices, "AnalysisService", title="Copper", Keyword="Cu", Price="15", Category=category.UID(), DuplicateVariation="0.5")
    >>> Fe = api.create(bikasetup.bika_analysisservices, "AnalysisService", title="Iron", Keyword="Fe", Price="10", Category=category.UID(), DuplicateVariation="0.5")
    >>> Au = api.create(bikasetup.bika_analysisservices, "AnalysisService", title="Gold", Keyword="Au", Price="20", Category=category.UID(), DuplicateVariation="0.5")
    >>> Mg = api.create(bikasetup.bika_analysisservices, "AnalysisService", title="Magnesium", Keyword="Mg", Price="20", Category=category.UID(), DuplicateVariation="0.5")
    >>> service_uids = [api.get_uid(an) for an in [Cu, Fe, Au, Mg]]

Create an Analysis Specification for `Water`::

    >>> sampletype_uid = api.get_uid(sampletype)
    >>> rr1 = {"keyword": "Au", "min": "-5", "max":  "5", "warn_min": "-5.5", "warn_max": "5.5"}
    >>> rr2 = {"keyword": "Cu", "min": "10", "max": "20", "warn_min":  "9.5", "warn_max": "20.5"}
    >>> rr3 = {"keyword": "Fe", "min":  "0", "max": "10", "warn_min": "-0.5", "warn_max": "10.5"}
    >>> rr4 = {"keyword": "Mg", "min": "10", "max": "10"}
    >>> rr = [rr1, rr2, rr3, rr4]
    >>> specification = api.create(bikasetup.bika_analysisspecs, "AnalysisSpec", title="Lab Water Spec", SampleType=sampletype_uid, ResultsRange=rr)
    >>> spec_uid = api.get_uid(specification)

Create a Reference Definition for blank::

    >>> blankdef = api.create(bikasetup.bika_referencedefinitions, "ReferenceDefinition", title="Blank definition", Blank=True)
    >>> blank_refs = [{'uid': Au.UID(), 'result': '0', 'min': '0', 'max': '0'},]
    >>> blankdef.setReferenceResults(blank_refs)

And for control::

    >>> controldef = api.create(bikasetup.bika_referencedefinitions, "ReferenceDefinition", title="Control definition")
    >>> control_refs = [{'uid': Au.UID(), 'result': '10', 'min': '9.99', 'max': '10.01'},
    ...                 {'uid': Cu.UID(), 'result': '-0.9','min': '-1.08', 'max': '-0.72'},]
    >>> controldef.setReferenceResults(control_refs)

    >>> blank = api.create(supplier, "ReferenceSample", title="Blank",
    ...                    ReferenceDefinition=blankdef,
    ...                    Blank=True, ExpiryDate=date_future,
    ...                    ReferenceResults=blank_refs)
    >>> control = api.create(supplier, "ReferenceSample", title="Control",
    ...                      ReferenceDefinition=controldef,
    ...                      Blank=False, ExpiryDate=date_future,
    ...                      ReferenceResults=control_refs)

Create an Analysis Request::

    >>> values = {
    ...     'Client': api.get_uid(client),
    ...     'Contact': api.get_uid(contact),
    ...     'DateSampled': date_now,
    ...     'SampleType': sampletype_uid,
    ...     'Specification': spec_uid,
    ...     'Priority': '1',
    ... }

    >>> ar = create_analysisrequest(client, request, values, service_uids)
    >>> success = doActionFor(ar, 'receive')

Create a new Worksheet and add the analyses::

    >>> worksheet = api.create(portal.worksheets, "Worksheet")
    >>> analyses = map(api.get_object, ar.getAnalyses())
    >>> for analysis in analyses:
    ...     worksheet.addAnalysis(analysis)

Add a duplicate for `Cu`::

    >>> position = worksheet.get_slot_position(ar, 'a')
    >>> duplicates = worksheet.addDuplicateAnalyses(position)
    >>> duplicates.sort(key=lambda analysis: analysis.getKeyword(), reverse=False)

Add a blank and a control::

    >>> blanks = worksheet.addReferenceAnalyses(blank, service_uids)
    >>> blanks.sort(key=lambda analysis: analysis.getKeyword(), reverse=False)
    >>> controls = worksheet.addReferenceAnalyses(control, service_uids)
    >>> controls.sort(key=lambda analysis: analysis.getKeyword(), reverse=False)


Check if results are out of range
---------------------------------

First, get the analyses from slot 1 and sort them asc::

    >>> analyses = worksheet.get_analyses_at(1)
    >>> analyses.sort(key=lambda analysis: analysis.getKeyword(), reverse=False)

Set results for analysis `Au` (min: -5, max: 5, warn_min: -5.5, warn_max: 5.5)::

    >>> au_analysis = analyses[0]
    >>> au_analysis.setResult(2)
    >>> is_out_of_range(au_analysis)
    (False, False)

    >>> au_analysis.setResult(-2)
    >>> is_out_of_range(au_analysis)
    (False, False)

    >>> au_analysis.setResult(-5)
    >>> is_out_of_range(au_analysis)
    (False, False)

    >>> au_analysis.setResult(5)
    >>> is_out_of_range(au_analysis)
    (False, False)

    >>> au_analysis.setResult(10)
    >>> is_out_of_range(au_analysis)
    (True, True)

    >>> au_analysis.setResult(-10)
    >>> is_out_of_range(au_analysis)
    (True, True)

Results in shoulders?::

    >>> au_analysis.setResult(-5.2)
    >>> is_out_of_range(au_analysis)
    (True, False)

    >>> au_analysis.setResult(-5.5)
    >>> is_out_of_range(au_analysis)
    (True, False)

    >>> au_analysis.setResult(-5.6)
    >>> is_out_of_range(au_analysis)
    (True, True)

    >>> au_analysis.setResult(5.2)
    >>> is_out_of_range(au_analysis)
    (True, False)

    >>> au_analysis.setResult(5.5)
    >>> is_out_of_range(au_analysis)
    (True, False)

    >>> au_analysis.setResult(5.6)
    >>> is_out_of_range(au_analysis)
    (True, True)


Check if results for duplicates are out of range
------------------------------------------------

Get the first duplicate analysis that comes from `Au`::

    >>> duplicate = duplicates[0]

A Duplicate will be considered out of range if its result does not match with
the result set to the analysis that was duplicated from, with the Duplicate
Variation in % as the margin error. The Duplicate Variation assigned in the
Analysis Service `Au` is 0.5%::

    >>> dup_variation = au_analysis.getDuplicateVariation()
    >>> dup_variation = api.to_float(dup_variation)
    >>> dup_variation
    0.5

Set an in-range result (between -5 and 5) for routine analysis and check all
variants on it's duplicate. Given that the duplicate variation is 0.5, the
valid range for the duplicate must be `Au +-0.5%`::

    >>> result = 2.0
    >>> au_analysis.setResult(result)
    >>> is_out_of_range(au_analysis)
    (False, False)

    >>> duplicate.setResult(result)
    >>> is_out_of_range(duplicate)
    (False, False)

    >>> dup_min_range = result - (result*(dup_variation/100))
    >>> duplicate.setResult(dup_min_range)
    >>> is_out_of_range(duplicate)
    (False, False)

    >>> duplicate.setResult(dup_min_range - 0.5)
    >>> is_out_of_range(duplicate)
    (True, True)

    >>> dup_max_range = result + (result*(dup_variation/100))
    >>> duplicate.setResult(dup_max_range)
    >>> is_out_of_range(duplicate)
    (False, False)

    >>> duplicate.setResult(dup_max_range + 0.5)
    >>> is_out_of_range(duplicate)
    (True, True)

Set an out-of-range result, but within shoulders, for routine analysis and check
all variants on it's duplicate. Given that the duplicate variation is 0.5, the
valid range for the duplicate must be `Au +-0.5%`::

    >>> result = 5.5
    >>> au_analysis.setResult(result)
    >>> is_out_of_range(au_analysis)
    (True, False)

    >>> duplicate.setResult(result)
    >>> is_out_of_range(duplicate)
    (False, False)

    >>> dup_min_range = result - (result*(dup_variation/100))
    >>> duplicate.setResult(dup_min_range)
    >>> is_out_of_range(duplicate)
    (False, False)

    >>> duplicate.setResult(dup_min_range - 0.5)
    >>> is_out_of_range(duplicate)
    (True, True)

    >>> dup_max_range = result + (result*(dup_variation/100))
    >>> duplicate.setResult(dup_max_range)
    >>> is_out_of_range(duplicate)
    (False, False)

    >>> duplicate.setResult(dup_max_range + 0.5)
    >>> is_out_of_range(duplicate)
    (True, True)

Set an out-of-range and out-of-shoulders result, for routine analysis and check
all variants on it's duplicate. Given that the duplicate variation is 0.5, the
valid range for the duplicate must be `Au +-0.5%`::

    >>> result = -7.0
    >>> au_analysis.setResult(result)
    >>> is_out_of_range(au_analysis)
    (True, True)

    >>> duplicate.setResult(result)
    >>> is_out_of_range(duplicate)
    (False, False)

    >>> dup_min_range = result - (abs(result)*(dup_variation/100))
    >>> duplicate.setResult(dup_min_range)
    >>> is_out_of_range(duplicate)
    (False, False)

    >>> duplicate.setResult(dup_min_range - 0.5)
    >>> is_out_of_range(duplicate)
    (True, True)

    >>> dup_max_range = result + (abs(result)*(dup_variation/100))
    >>> duplicate.setResult(dup_max_range)
    >>> is_out_of_range(duplicate)
    (False, False)

    >>> duplicate.setResult(dup_max_range + 0.5)
    >>> is_out_of_range(duplicate)
    (True, True)


Check if results for Reference Analyses (blanks + controls) are out of range
----------------------------------------------------------------------------

Reference Analyses (controls and blanks) do not use the result ranges defined in
the specifications, rather they use the result range defined in the Reference
Sample they have been generated from. In turn, the result ranges defined in
Reference Samples can be set manually or acquired from the Reference Definition
they might be associated with. Another difference from routine analyses is that
reference analyses don't expect a valid range, rather a discrete value, so
shoulders are built based on % error.

Blank Analyses
..............

The first blank analysis corresponds to `Au`::

    >>> au_blank = blanks[0]

For `Au` blank, as per the reference definition used above, the expected result
is 0 +/- 0.1%. Since the expected result is 0, no shoulders will be considered
regardless of the % of error. Thus, result will always be "out-of-shoulders"
when out of range::

    >>> au_blank.setResult(0.0)
    >>> is_out_of_range(au_blank)
    (False, False)

    >>> au_blank.setResult("0")
    >>> is_out_of_range(au_blank)
    (False, False)

    >>> au_blank.setResult(0.0001)
    >>> is_out_of_range(au_blank)
    (True, True)

    >>> au_blank.setResult("0.0001")
    >>> is_out_of_range(au_blank)
    (True, True)

    >>> au_blank.setResult(-0.0001)
    >>> is_out_of_range(au_blank)
    (True, True)

    >>> au_blank.setResult("-0.0001")
    >>> is_out_of_range(au_blank)
    (True, True)

Control Analyses
................

The first control analysis corresponds to `Au`::

    >>> au_control = controls[0]

For `Au` control, as per the reference definition used above, the expected
result is 10 +/- 0.1% = 10 +/- 0.01

First, check for in-range values::

    >>> au_control.setResult(10)
    >>> is_out_of_range(au_control)
    (False, False)

    >>> au_control.setResult(10.0)
    >>> is_out_of_range(au_control)
    (False, False)

    >>> au_control.setResult("10")
    >>> is_out_of_range(au_control)
    (False, False)

    >>> au_control.setResult("10.0")
    >>> is_out_of_range(au_control)
    (False, False)

    >>> au_control.setResult(9.995)
    >>> is_out_of_range(au_control)
    (False, False)

    >>> au_control.setResult("9.995")
    >>> is_out_of_range(au_control)
    (False, False)

    >>> au_control.setResult(10.005)
    >>> is_out_of_range(au_control)
    (False, False)

    >>> au_control.setResult("10.005")
    >>> is_out_of_range(au_control)
    (False, False)

    >>> au_control.setResult(9.99)
    >>> is_out_of_range(au_control)
    (False, False)

    >>> au_control.setResult("9.99")
    >>> is_out_of_range(au_control)
    (False, False)

    >>> au_control.setResult(10.01)
    >>> is_out_of_range(au_control)
    (False, False)

    >>> au_control.setResult("10.01")
    >>> is_out_of_range(au_control)
    (False, False)

Now, check for out-of-range results::

    >>> au_control.setResult(9.98)
    >>> is_out_of_range(au_control)
    (True, True)

    >>> au_control.setResult("9.98")
    >>> is_out_of_range(au_control)
    (True, True)

    >>> au_control.setResult(10.011)
    >>> is_out_of_range(au_control)
    (True, True)

    >>> au_control.setResult("10.011")
    >>> is_out_of_range(au_control)
    (True, True)

And do the same with the control for `Cu` that expects -0.9 +/- 20%::

    >>> cu_control = controls[1]

First, check for in-range values::

    >>> cu_control.setResult(-0.9)
    >>> is_out_of_range(cu_control)
    (False, False)

    >>> cu_control.setResult("-0.9")
    >>> is_out_of_range(cu_control)
    (False, False)

    >>> cu_control.setResult(-1.08)
    >>> is_out_of_range(cu_control)
    (False, False)

    >>> cu_control.setResult("-1.08")
    >>> is_out_of_range(cu_control)
    (False, False)

    >>> cu_control.setResult(-1.07)
    >>> is_out_of_range(cu_control)
    (False, False)

    >>> cu_control.setResult("-1.07")
    >>> is_out_of_range(cu_control)
    (False, False)

    >>> cu_control.setResult(-0.72)
    >>> is_out_of_range(cu_control)
    (False, False)

    >>> cu_control.setResult("-0.72")
    >>> is_out_of_range(cu_control)
    (False, False)

    >>> cu_control.setResult(-0.73)
    >>> is_out_of_range(cu_control)
    (False, False)

    >>> cu_control.setResult("-0.73")
    >>> is_out_of_range(cu_control)
    (False, False)

Now, check for out-of-range results::

    >>> cu_control.setResult(0)
    >>> is_out_of_range(cu_control)
    (True, True)

    >>> cu_control.setResult("0")
    >>> is_out_of_range(cu_control)
    (True, True)

    >>> cu_control.setResult(-0.71)
    >>> is_out_of_range(cu_control)
    (True, True)

    >>> cu_control.setResult("-0.71")
    >>> is_out_of_range(cu_control)
    (True, True)

    >>> cu_control.setResult(-1.09)
    >>> is_out_of_range(cu_control)
    (True, True)

    >>> cu_control.setResult("-1.09")
    >>> is_out_of_range(cu_control)
    (True, True)


Changelog
=========
1.2.3 (2018-06-23)
------------------

- More PyPI fixtures


1.2.2 (2018-06-23)
------------------

- PyPI Documentation Page fixtures


1.2.1 (2018-06-23)
------------------

- Better Documentation Page for PyPI
- Fixed formatting of Doctests


1.2.0 (2018-06-23)
------------------

**Added**

- Added `is_uid` function

**Removed**

**Changed**

- Added SENAITE CORE API functions

**Fixed**

- Fixed Tests

**Security**


1.1.0 (2018-01-03)
------------------

**Added**

**Removed**

**Changed**

- License changed to GPLv2
- Integration to SENAITE CORE

**Fixed**

- Fixed Tests

**Security**


1.0.2 (2017-11-24)
------------------

- #397(bika.lims) Fix Issue-396: AttributeError: uid_catalog on AR publication


1.0.1 (2017-09-30)
------------------

- Fixed broken release (missing MANIFEST.in)


1.0.0 (2017-09-30)
------------------

- First release


