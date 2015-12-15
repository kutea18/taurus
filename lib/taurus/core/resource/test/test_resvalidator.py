#!/usr/bin/env python

#############################################################################
##
## This file is part of Taurus
##
## http://taurus-scada.org
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
## Taurus is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Taurus is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""Test for taurus.core.resource.test.test_resvalidator..."""

import os.path as osp

import taurus
from taurus.external import unittest
from taurus.core.test import (valid, invalid, names,
                              AbstractNameValidatorTestCase)
from taurus.core.resource.resvalidator import (ResourceAuthorityNameValidator,
                                               ResourceDeviceNameValidator,
                                               ResourceAttributeNameValidator)


@valid(name='res:attr_2')
@valid(name='res:foo02')
@valid(name='res:localhosy')
@invalid(name='res:foo:10000') # Invalid key
@invalid(name='res:10000') # Invalid key
@invalid(name='res:127.0.0.1') # Invalid key
@invalid(name='res:tango_1')  # Invalid tango URI
class ResourceAuthorityValidatorTestCase(AbstractNameValidatorTestCase,
                                         unittest.TestCase):
    """
        Test for ResourceAuthorityNameValidator loading the resources
        from a dictionary.
    """
    validator = ResourceAuthorityNameValidator

    def setUp(self):
        unittest.TestCase.setUp(self)
        f = taurus.Factory('res')
        d = {'tango_1': 'foo:10000',
             'foo02': 'tango://foo:10000',
             'localhost': 'eval://localhost'
             }
        f.reloadResource(d)

@valid(name='res:MyDev')
@valid(name='res:tangoDev1')
@valid(name='res:tangoDev_bck')
@invalid(name='res:123') # Invalid key
@invalid(name='res:wrong_dev') # Invalid eval URI
class ResourceDeviceValidatorTestCase(AbstractNameValidatorTestCase,
                                      unittest.TestCase):
    """
        Test for ResourceDeviceNameValidator loading the resources
        from a dictionary.
    """
    validator = ResourceDeviceNameValidator

    def setUp(self):
        unittest.TestCase.setUp(self)
        f = taurus.Factory('res')
        d = {'MyDev': 'eval:@foo',
             'tangoDev1': 'tango://foo:10000/a/b/c',
             'tangoDev_bck': 'tango://a/b/c',
             'wrong_dev': 'eval://mydev',
             }
        f.reloadResource(d)

@names(name='MyAttr', out=('eval://localhost/@DefaultEvaluator/1', '1', '1'))
@names(name='foo', out=('eval://localhost/@Foo/True', '@Foo/True', 'True'))
@valid(name='res:MyAttr')
@valid(name='res:My_Attr')
@valid(name='res:attr_1')
@valid(name='res:attr_2')
@valid(name='res:attr_tango_bck_1')
@valid(name='res:attr_tango_bck_2')
@valid(name='res:attr-state')
@valid(name='res:attr1')
@valid(name='res:foo')
@valid(name='res:Foo')
@invalid(name='res:res_attr')
@invalid(name='res:1')
@invalid(name='res:1foo')
@invalid(name='res: foo')
@invalid(name='res:dev1') # Is a device!
@invalid(name='res:dev2') # Is a device!
@invalid(name='res:NotExist') # Not existing reference!
class ResourceAttributeValidatorTestCase(AbstractNameValidatorTestCase,
                                         unittest.TestCase):
    """
        Test for ResourceAttributeNameValidator loading the resources
        from a dictionary.
    """
    validator = ResourceAttributeNameValidator

    def setUp(self):
        unittest.TestCase.setUp(self)
        f = taurus.Factory('res')
        d = {'MyAttr': 'eval:1',
             'My_Attr': 'eval:foo=1;bar=2;foo+bar',
             'attr_1': 'tango:a/b/c/d',
             'attr_2': 'a/b/c/d',
             'attr_tango_bck_1': 'tango://a/b/c/d',
             'attr_tango_bck_2': 'tango://foo:10000/a/b/c/d',
             'attr-state': 'a/b/c/state',
             'attr1': 'eval:"Hello_World!!"',
             'foo': 'eval:/@Foo/True',
             '1foo': 'eval:2',
             'Foo': 'eval:False',
             'res_attr' 'res:attr1'
             'dev1': 'tango:a/b/c', # invalid
             'dev2': 'eval:@foo',   # invalid
             }
        f.reloadResource(d)

@names(name='MyAttr', out=('eval://localhost/@DefaultEvaluator/1', '1', '1'))
@names(name='foo', out=('eval://localhost/@Foo/True', '@Foo/True', 'True'))
@valid(name='res:MyAttr')
@valid(name='res:My_Attr')
@valid(name='res:attr_1')
@valid(name='res:attr_2')
@valid(name='res:attr1')
@valid(name='res:foo')
@valid(name='res:Foo')
@invalid(name='res:res_attr')
@invalid(name='res:1')
@invalid(name='res:1foo')
@invalid(name='res: foo')
@invalid(name='res:dev1') # Is a device!
@invalid(name='res:dev2') # Is a device!
@invalid(name='res:NotExist') # Not existing reference!
class ResourceAttributeValidatorTestCase2(AbstractNameValidatorTestCase,
                                          unittest.TestCase):
    """
        Test for ResourceAttributeNameValidator loading the resources
        from a File.
    """
    validator = ResourceAttributeNameValidator

    def setUp(self):
        unittest.TestCase.setUp(self)
        f = taurus.Factory('res')
        file_name = osp.join(osp.dirname(osp.abspath(__file__)),
                             'res/attr_resources_file.py')
        f.reloadResource(file_name)