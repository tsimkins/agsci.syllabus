from OFS.CopySupport import CopyError
from plone.i18n.normalizer import idnormalizer
from ..content import CourseHelper, SyllabusHelper

# This event is triggered when a course is edited.  It resets the title and id
# based on the course prefix/number/name
def onCourseEdit(context, event):

    # Get the helper for the course (used to initially set the id)
    helper = CourseHelper(context)

    # Calculate a new title and id
    new_title = helper.course_title
    new_id = idnormalizer.normalize(helper.course_number)

    # Get the existing new title and id
    old_id = context.getId()
    old_title = context.title

    # This bool stores if the id/title were changed
    changed = False

    # If the new id is different than the old id, update it. If it already
    # exists, throw an error.
    if new_id != old_id:

        try:
            context.aq_parent.manage_renameObjects(ids=[old_id], new_ids=[new_id])
        except CopyError, e:
            raise ValueError(u"The id '%s' is already in use." % new_id)
            return

        changed = True

    # If the new title is different than the old title, update it.
    if new_title != old_title:

        context.title = new_title

        changed = True

    # If something was changed, reindex the object
    if changed:
        context.reindexObject()

# Update the short name when the syllabus semester or section is changed

def onSyllabusEdit(context, event):

    # Get the helper for the syllabus (used to initially set the id)
    helper = SyllabusHelper(context)

    # Get what the title and id should be
    new_title = helper.syllabus_title
    new_id = idnormalizer.normalize(new_title)

    # Get the existing new title and id
    old_id = context.getId()
    old_title = context.title

    # This bool stores if the id/title were changed
    changed = False

    # If the new id is different than the old id, update it. If it already
    # exists, throw an error.
    if new_id != old_id:

        try:
            context.aq_parent.manage_renameObjects(ids=[old_id], new_ids=[new_id])
        except CopyError, e:
            raise ValueError(u"The id '%s' is already in use." % new_id)
            return

        changed = True

    # If the new title is different than the old title, update it.
    if new_title != old_title:

        context.title = new_title

        changed = True

    # If something was changed, reindex the object
    if changed:
        context.reindexObject()