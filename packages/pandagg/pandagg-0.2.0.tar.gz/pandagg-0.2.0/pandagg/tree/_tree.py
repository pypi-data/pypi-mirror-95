#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible

from builtins import str as text

from lighttree import Tree as OriginalTree

from pandagg.utils import DSLMixin


@python_2_unicode_compatible
class Tree(DSLMixin, OriginalTree):

    KEY = None
    _type_name = None

    @classmethod
    def get_node_dsl_class(cls, name):
        return cls.node_class._get_dsl_class(name)

    def id_from_key(self, key):
        """Find node identifier based on key. If multiple nodes have the same key, takes the first found one."""
        for k, n in self.list():
            if k == key:
                return n.identifier
        raise KeyError('No node found with key "%s"' % key)

    def __str__(self):
        return "<{class_}>\n{tree}".format(
            class_=text(self.__class__.__name__), tree=self.show(limit=40)
        )

    def __repr__(self):
        return self.__str__()
