from django.utils import timezone
from django.utils.translation import ugettext as _

from adhocracy4.comments.models import Comment
from adhocracy4.exports import mixins as a4_export_mixins
from adhocracy4.exports import views as a4_export_views
from meinberlin.apps.exports import mixins as export_mixins

from . import models


class ProposalExportView(export_mixins.ItemExportWithReferenceNumberMixin,
                         a4_export_mixins.ItemExportWithLinkMixin,
                         a4_export_mixins.ExportModelFieldsMixin,
                         a4_export_mixins.ItemExportWithRatesMixin,
                         a4_export_mixins.ItemExportWithCategoriesMixin,
                         a4_export_mixins.ItemExportWithLabelsMixin,
                         a4_export_mixins.ItemExportWithCommentCountMixin,
                         a4_export_mixins.ItemExportWithLocationMixin,
                         export_mixins.UserGeneratedContentExportMixin,
                         export_mixins.ItemExportWithModeratorFeedback,
                         export_mixins.ItemExportWithModeratorRemark,
                         a4_export_views.BaseItemExportView):
    model = models.Proposal
    fields = ['name', 'description', 'budget']
    html_fields = ['description']

    def get_queryset(self):
        return super().get_queryset() \
            .filter(module=self.module)\
            .annotate_comment_count()\
            .annotate_positive_rating_count()\
            .annotate_negative_rating_count()


class ProposalCommentExportView(a4_export_mixins.ExportModelFieldsMixin,
                                export_mixins.UserGeneratedContentExportMixin,
                                a4_export_mixins.ItemExportWithLinkMixin,
                                a4_export_mixins.ItemExportWithRatesMixin,
                                export_mixins.ItemExportWithRepliesToMixin,
                                a4_export_views.BaseItemExportView):

    model = Comment

    fields = ['id', 'comment', 'created']

    def get_queryset(self):
        comments = (Comment.objects.filter(
                    budget_proposal__module=self.module) |
                    Comment.objects.filter(
                    parent_comment__budget_proposal__module=self.module)
                    )

        return comments

    def get_base_filename(self):
        return '%s_%s' % (self.project.slug,
                          timezone.now().strftime('%Y%m%dT%H%M%S'))

    def get_virtual_fields(self, virtual):
        virtual.setdefault('id', _('ID'))
        virtual.setdefault('comment', _('Comment'))
        virtual.setdefault('created', _('Created'))
        return super().get_virtual_fields(virtual)
