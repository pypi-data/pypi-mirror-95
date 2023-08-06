# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from zope.interface.declarations import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class VocabularyNotFoundError(Exception):
    pass


@implementer(IVocabularyFactory)
class PropertySheetVocabulary(object):
    """
    Retrieves a vocabulary by reading a multiline property in portal_properties
    """

    def __init__(self, sheet_name, property_name, default_terms):
        self.sheet_name = sheet_name
        self.property_name = property_name
        self.default_terms = default_terms

    def iter_property_terms(self, context):
        prop_sheet = getattr(
            getToolByName(context, 'portal_properties'), self.sheet_name, None
        )
        if prop_sheet is None:
            raise VocabularyNotFoundError

        prop_lines = getattr(prop_sheet, self.property_name, None)
        if prop_lines is None:
            raise VocabularyNotFoundError

        ret = []
        for line in prop_lines:
            if '|' in line:
                value, title = line.split('|', 1)
            else:
                value = title = line
            ret.append((value.strip(), title.strip()))
        return ret

    def __call__(self, context):
        try:
            terms = self.iter_property_terms(context)
        except VocabularyNotFoundError:
            terms = self.default_terms

        return SimpleVocabulary(
            [SimpleTerm(value=t[0], token=t[0], title=t[1]) for t in terms]
        )

