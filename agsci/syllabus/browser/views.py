from eea.facetednavigation.browser.app.query import FacetedQueryHandler
from eea.facetednavigation.caching import ramcache
from eea.facetednavigation.caching import cacheKeyFacetedNavigation
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
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
                return semesters.index(x.get('title', None))
            except IndexError:
                return 999

        contents = self.context.listFolderContents({'Type' : 'Syllabus', 'sort_on' : 'Title'})

        for i in contents:
            semester = getattr(i, 'semester', None)

            if semester:
                if not data.has_key(semester):

                    data[semester] = {
                                           'title' : semester,
                                           'contents' : []
                    }

                data[semester]['contents'].append(i)


        values = data.values()

        values.sort(key=lambda x: idx(x))

        return values



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