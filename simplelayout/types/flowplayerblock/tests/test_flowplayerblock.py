from unittest2 import TestCase
from Products.CMFCore.utils import getToolByName
from simplelayout.types.flowplayerblock.testing import (
    SL_FLOWERPLAYERBLOCK_INTEGRATION_TESTING)


class TestFlowplayerBlock(TestCase):

    layer = SL_FLOWERPLAYERBLOCK_INTEGRATION_TESTING

    def setUp(self):
        super(TestFlowplayerBlock, self).setUp()

        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

    def test_js_registered(self):
        registry = getToolByName(self.portal, 'portal_javascripts')
        self.assertIsNotNone(
            registry.getResource(
                '++resource++simplelayout.flowplayer.js/'
                'simplelayout.flowplayer.js'))

