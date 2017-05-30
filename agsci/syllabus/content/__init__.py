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

    instructor = RichText(
        title=u"Instructor",
        required=False
    )

    learning_objectives = RichText(
        title=u"Learning Objectives",
        required=False
    )

    grading_details = RichText(
        title=u"Grading Details",
        required=False
    )

    required_course_materials = RichText(
        title=u"Required Course Materials",
        required=False
    )

    course_schedule = RichText(
        title=u"Course Schedule",
        required=False
    )

    additional_information = RichText(
        title=u"Additional Information",
        required=False
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

    credits_offered = schema.Decimal(
        title=_(u"Credits Offered"),
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
        return u"%s-%s" % (self.context.course_prefix, self.context.course_number)

    @property
    def course_title(self):
        return u"%s: %s" % (self.course_number, self.context.course_name)

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