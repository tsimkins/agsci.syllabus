from plone.supermodel import model
from zope import schema
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile.field import NamedBlobFile
from zope.interface import Interface, provider, invariant, Invalid, implementer, implements
from plone.app.content.interfaces import INameFromTitle
from agsci.syllabus import syllabusMessageFactory as _
from zope.component import adapter

@provider(IFormFieldProvider)
class ICourseContainer(model.Schema):

    pass

@provider(IFormFieldProvider)
class ISyllabus(model.Schema):

    semester = schema.Choice(
        title=_(u"Semester"),
        description=_(u""),
        vocabulary="agsci.syllabus.semester",
        required=True,
    )

    file = NamedBlobFile(
        title=_(u"Syllabus PDF File"),
        description=_(u""),
        required=True,
    )

@provider(IFormFieldProvider)
class ICourse(model.Schema):

    form.mode(title='hidden')

    title = schema.TextLine(
        title=_(u"Title"),
        required=False,
    )

    course_number = schema.TextLine(
        title=_(u"Course Number"),
        required=True,
    )

    course_name = schema.TextLine(
        title=_(u"Course Name"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Course Description"),
        required=False,
    )

    department = schema.List(
        title=_(u"Department"),
        description=_(u""),
        value_type=schema.Choice(vocabulary="agsci.syllabus.department"),
    )

    course_level = schema.List(
        title=_(u"Course Level"),
        description=_(u""),
        value_type=schema.Choice(vocabulary="agsci.syllabus.course_level"),
    )

class INameFromCourse(Interface):
    pass

@implementer(INameFromTitle)
@adapter(INameFromCourse)
class NameFromCourse(object):

    def __init__(self, context):
        self.context = context

    def __new__(cls, context):
        instance = super(NameFromCourse, cls).__new__(cls)
        title = "%s: %s" % (context.course_number, context.course_name)
        instance.title = context.course_number
        context.title = title
        return instance

class INameFromSemester(Interface):
    pass

@implementer(INameFromTitle)
@adapter(INameFromSemester)
class NameFromSemester(object):

    def __init__(self, context):
        self.context = context

    def __new__(cls, context):
        instance = super(NameFromSemester, cls).__new__(cls)
        instance.title = context.semester
        context.title = context.semester
        return instance