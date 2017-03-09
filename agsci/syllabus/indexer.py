from Acquisition import aq_base
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from zope.component import provideAdapter

from .content import ICourse

@indexer(ICourse)
def CourseLevel(context):

    return getattr(context, 'course_level', [])

provideAdapter(CourseLevel, name='course_level')

@indexer(ICourse)
def CourseDepartment(context):

    return getattr(context, 'department', [])

provideAdapter(CourseDepartment, name='department')
