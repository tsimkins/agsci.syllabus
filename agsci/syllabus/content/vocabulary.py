from Products.CMFCore.utils import getToolByName
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import directlyProvides, implements
from datetime import datetime, timedelta

class StaticVocabulary(object):

    implements(IVocabularyFactory)

    preserve_order = False

    items = ['N/A',]

    def __call__(self, context):

        items = self.items

        if not self.preserve_order:
            items = list(set(self.items))
            items.sort()

        terms = [SimpleTerm(x,title=x) for x in items]

        return SimpleVocabulary(terms)

class KeyValueVocabulary(object):

    implements(IVocabularyFactory)

    items = [
        ('N/A', 'N/A'),
    ]

    def __call__(self, context):

        return SimpleVocabulary(
            [
                SimpleTerm(x, title=y) for (x, y) in self.items
            ]
        )

class SemesterVocabulary(StaticVocabulary):

    preserve_order = True

    @property
    def items(self):

        # Semester dates
        data = [
                    ('2017-01-09', 'Spring 2017'),
                    ('2017-05-08', 'Summer 2017'),
                    ('2017-08-21', 'Fall 2017'),
                    ('2018-01-08', 'Spring 2018'),
                    ('2018-05-14', 'Summer 2018'),
                    ('2018-08-20', 'Fall 2018'),
                    ('2019-01-07', 'Spring 2019'),
                    ('2019-05-13', 'Summer 2019'),
                    ('2019-08-26', 'Fall 2019'),
                    ('2020-01-13', 'Spring 2020'),
                    ('2020-05-18', 'Summer 2020'),
                    ('2020-08-24', 'Fall 2020'),
                    ('2021-01-11', 'Spring 2021'),
                    ('2021-05-17', 'Summer 2021'),
                    ('2021-08-23', 'Fall 2021'),
                    ('2022-01-10', 'Spring 2022'),
                    ('2022-05-16', 'Summer 2022'),
                    ('2022-08-22', 'Fall 2022')
        ]

        # Year ahead
        max_date = datetime.now() + timedelta(days=365)

        # Filter dates
        return [
            x[1] for x in data if datetime.strptime(x[0], '%Y-%m-%d') <= max_date
        ]

class DepartmentVocabulary(KeyValueVocabulary):

    items = [
        ('ABE', 'Agricultural and Biological Engineering'),
        ('AESE', 'Agricultural Economics, Sociology, and Education'),
        ('ANSC', 'Animal Science'),
        ('ESM', 'Ecosystem Science and Management'),
        ('ENT', 'Entomology'),
        ('FDSC', 'Food Science'),
        ('PPEM', 'Plant Pathology and Environmental Microbiology'),
        ('PLANT', 'Plant Science'),
        ('VBSC', 'Veterinary and Biomedical Sciences'),

        ('AG', 'Ag Adm (Deans Off)'),
        ('BRS', 'Biorenewable Systems'),
        ('ERM', 'Environmental Resource Management'),
        ('INTL', 'International'),
        ('PPATH', 'PPATH'),
        ('OTHER', 'Other'),
    ]

class CoursePrefixVocabulary(KeyValueVocabulary):

    @property
    def items(self):

        values = [
            'ABE',
            'AEE',
            'AEREC',
            'AG',
            'AGBM',
            'AGCOM',
            'AGECO',
            'AGRO',
            'ANSC',
            'ASM',
            'AYFCE',
            'BE',
            'BRS',
            'CED',
            'CEDEV',
            'ENT',
            'ERM',
            'FDSC',
            'FOR',
            'HORT',
            'INTAD',
            'INTAG',
            'PLANT',
            'PPATH',
            'PPEM',
            'RSOC',
            'SOILS',
            'SPAN',
            'TURF',
            'VBSC',
            'WFS',
            'WP',
            'YFE'
        ]

        values = [(x,x) for x in values]

        values.insert(0, (u'', u'Select a Course Prefix...'))

        return values

SemesterVocabularyFactory = SemesterVocabulary()
DepartmentVocabularyFactory = DepartmentVocabulary()
CoursePrefixVocabularyFactory = CoursePrefixVocabulary()