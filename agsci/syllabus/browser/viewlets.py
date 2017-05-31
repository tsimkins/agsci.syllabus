from Products.agCommon.browser.viewlets import TitleViewlet as _TitleViewlet
from .views import SyllabusView

class TitleViewlet(_TitleViewlet):

    def index(self):
        v = SyllabusView(self.context, self.request)

        title = v.title()

        return u"<title>%s &mdash; Syllabi &mdash; %s</title>" % (title, self.org_title)