from plone.supermodel import model
from zope import schema
from plone.app.textfield import RichText
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

    section = schema.TextLine(
        title=_(u"Section"),
        description=_(u"Optional"),
        required=False,
    )


@provider(IFormFieldProvider)
class ICourse(model.Schema):

    form.mode(title='hidden')

    title = schema.TextLine(
        title=_(u"Title"),
        required=False,
    )

    department = schema.List(
        title=_(u"Department"),
        description=_(u""),
        value_type=schema.Choice(vocabulary="agsci.syllabus.department"),
    )

    course_prefix = schema.Choice(
        title=_(u"Course Prefix"),
        required=True,
        vocabulary="agsci.syllabus.course_prefix",
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

class CourseHelper(object):

    def __init__(self, context):
        self.context = context

    @property
    def course_number(self):
        return u"%s %s" % (self.context.course_prefix, self.context.course_number)

    @property
    def course_title(self):
        return u"%s: %s" % (self.course_number, self.context.course_name)

class SyllabusHelper(object):

    def __init__(self, context):
        self.context = context

    @property
    def semester(self):
        return getattr(self.context, 'semester', '')

    @property
    def section(self):
        return getattr(self.context, 'section', '')

    @property
    def syllabus_title(self):

        if self.section:
            return u"%s, Section %s" % (self.semester, self.section)

        return self.semester

    @property
    def syllabus_title_display(self):

        course = self.context.aq_parent

        course_helper = CourseHelper(course)

        course_title = course_helper.course_title

        if self.section:
            return u"%s (%s, Section %s)" % (course_title, self.semester, self.section)

        return u"%s (%s)" % (course_title, self.semester)

class INameFromCourse(Interface):
    pass

@implementer(INameFromTitle)
@adapter(INameFromCourse)
class NameFromCourse(object):

    def __init__(self, context):
        self.context = context

    def __new__(cls, context):
        instance = super(NameFromCourse, cls).__new__(cls)
        helper = CourseHelper(context)

        instance.title = helper.course_number
        context.title = helper.course_title

        return instance

class INameFromSyllabus(Interface):
    pass

@implementer(INameFromTitle)
@adapter(INameFromSyllabus)
class NameFromSyllabus(object):

    def __init__(self, context):
        self.context = context

    def __new__(cls, context):
        instance = super(NameFromSyllabus, cls).__new__(cls)

        helper = SyllabusHelper(context)

        instance.title = helper.syllabus_title
        context.title = helper.syllabus_title

        return instance