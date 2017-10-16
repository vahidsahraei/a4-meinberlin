from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.exports import views as export_views
from meinberlin.apps.exports import register_export

from . import models


@register_export(_('Documents with comments'))
class DocumentExportView(export_views.AbstractXlsxExportView,
                         export_views.ItemExportWithCommentsMixin):

    PARAGRAPH_TEXT_LIMIT = 100

    def get_header(self):
        return map(str, [_('Chapter'), _('Paragraph'), _('Comments')])

    def export_rows(self):
        chapters = models.Chapter.objects.filter(module=self.module)

        for chapter in chapters:
            yield [chapter.name, '', self.get_comments_data(chapter)]
            for paragraph in chapter.paragraphs.all():
                yield [chapter.name,
                       self.get_paragraph_data(paragraph),
                       self.get_comments_data(paragraph)]

    def get_paragraph_data(self, paragraph):
        if paragraph.name:
            return paragraph.name

        text = strip_tags(paragraph.text).strip()
        return text[0:self.PARAGRAPH_TEXT_LIMIT] + ' ...'
