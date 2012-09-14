import mock
import unittest

import testfacet

import facet.platform.sunos

class MockKstatResults(object):
    
    def __init__(self):
        self._stats = {}

    def set_stats(self, module, instance, name, stats):
        self._stats[(module, instance, name)] = stats 

    def get_stats(self, module, instance, name):
        return self._stats[(module, instance, name)] 

class AbstractSunOSTest(testfacet.AbstractFacetModuleTest):
    
    def get_platform_provider(self):
        return facet.platform.sunos.SunOSProvider 
    