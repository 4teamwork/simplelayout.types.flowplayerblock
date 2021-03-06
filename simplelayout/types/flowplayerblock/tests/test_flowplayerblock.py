from Products.CMFCore.utils import getToolByName
from simplelayout.types.flowplayerblock.testing import (
    SL_FLOWERPLAYERBLOCK_INTEGRATION_TESTING)
from StringIO import StringIO
from unittest2 import TestCase
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from collective.flowplayer.interfaces import IVideo


class TestFlowplayerBlock(TestCase):

    layer = SL_FLOWERPLAYERBLOCK_INTEGRATION_TESTING

    def setUp(self):
        super(TestFlowplayerBlock, self).setUp()

        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        folder = self.portal.get(
            self.portal.invokeFactory('Folder', 'folder'))
        self.file = folder.get(
            folder.invokeFactory('File', 'file'))
        alsoProvides(self.file, IVideo)

    def test_js_registered(self):
        registry = getToolByName(self.portal, 'portal_javascripts')
        self.assertIsNotNone(
            registry.getResource(
                '++resource++simplelayout.flowplayer.js/'
                'simplelayout.flowplayer.js'))

    def test_fti_action(self):
        types = getToolByName(self.portal, 'portal_types')
        fti = types.get('File')
        action_ids = [item.id for item in fti._actions]
        self.assertIn('sl-dummy-dummy-flowplayer', action_ids)

    def test_block_view_registered(self):
        view = queryMultiAdapter((self.file, self.file.REQUEST),
                                 name="block_view-flowplayer")
        self.assertIsNotNone(view)

    def test_block_view_render(self):
        view = queryMultiAdapter((self.file, self.file.REQUEST),
                                 name="block_view-flowplayer")

        dummy = StringIO("data")
        dummy.filename = "some.flv"
        self.file.setFile(dummy)
        self.assertIn('simplelayout-block-wrapper flowplayerblock',
                      view.index())

    def test_href_returns_propper_url_if_file_id_has_extension_included(self):
        view = queryMultiAdapter((self.file, self.file.REQUEST),
                                 name="block_view-flowplayer")

        self.file.id = "some.flv"
        dummy = StringIO("data")
        dummy.filename = "some.flv"
        self.file.setFile(dummy)

        self.assertEqual(
            'http://nohost/plone/folder/some.flv/download',
            view.href())

    def test_href_returns_propper_url_if_file_id_has_no_extension_included(self):
        view = queryMultiAdapter((self.file, self.file.REQUEST),
                                 name="block_view-flowplayer")

        self.file.id = "some"
        dummy = StringIO("data")
        dummy.filename = "some.flv"
        self.file.setFile(dummy)

        self.assertEqual(
            'http://nohost/plone/folder/some/download?e=.flv',
            view.href())
