from eea.facetednavigation.browser.app.query import FacetedQueryHandler
from eea.facetednavigation.caching import ramcache
from eea.facetednavigation.caching import cacheKeyFacetedNavigation
from plone.app.textfield.value import RichTextValue
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component import getUtility
from zope.schema import getFieldsInOrder
from zope.schema.interfaces import IVocabularyFactory

from ..content import ISyllabus
from ..content.vocabulary import SemesterVocabularyFactory

class BaseView(BrowserView):

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')


class CourseView(BaseView):

    def getFolderContents(self):

        data = {}

        semesters = [x.value for x in SemesterVocabularyFactory(self.context)]
        semesters.reverse()

        def idx(x):

            try:

                s = getattr(x.getObject(), 'semester', '')

                return semesters.index(s)

            except IndexError:
                return 999

        contents = self.context.getFolderContents({'Type' : 'Syllabus', 'sort_on' : 'sortable_title'})

        contents = sorted(contents, key=lambda x: idx(x))

        return contents

class SyllabusView(BaseView):

    @property
    def course(self):
        return self.context.aq_parent

    def title(self):
        return u"%s (%s)" % (self.course.title, self.context.semester)

    def description(self):
        return getattr(self.course, 'description', '')

    def credits_offered(self):
        return getattr(self.course, 'credits_offered', '')

    def increaseHeadingLevel(self, text):

        if '<h2' in text:
            for i in reversed(range(1, 6)):
                from_header = "h%d" % i
                to_header = "h%d" % (i+1)
                text = text.replace("<%s" % from_header, "<%s" % to_header)
                text = text.replace("</%s" % from_header, "</%s" % to_header)

        return text

    def fields(self):

        class o(object):

            def __init__(self, n, d, v):
                self.name = n
                self.title = d.title
                self.value = v

            def richtext(self):
                return isinstance(self.value, RichTextValue)

        for (n,d) in getFieldsInOrder(ISyllabus):
            v = getattr(self.context, n, '')
            if n not in ['semester',]:
                yield o(n, d, v)

    def department(self):
        department = getattr(self.course, 'department', [])

        # Department vocabulary
        factory = getUtility(IVocabularyFactory, u"agsci.syllabus.department")
        vocabulary = factory(self.course)

        return [x.title for x in vocabulary if x.value in department]

class CourseContainerView(BaseView):

    def getCourseQuery(self):
        return {'Type' : 'Course', 'sort_on' : 'sortable_title'}

    def getFolderContents(self):
        return self.portal_catalog.searchResults(self.getCourseQuery())


class CourseContainerFacetedQueryHandler(CourseContainerView, FacetedQueryHandler):

    def criteria(self, sort=False, **kwargs):
        query = self.getCourseQuery()
        faceted_query = super( CourseContainerFacetedQueryHandler, self).criteria(sort, **kwargs)
        query.update(faceted_query)
        return query

    @ramcache(cacheKeyFacetedNavigation, dependencies=['eea.facetednavigation'])
    def __call__(self, *args, **kwargs):
        kwargs['batch'] = False
        self.brains = self.query(**kwargs)
        html = self.index()
        return html