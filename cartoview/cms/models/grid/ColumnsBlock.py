from django import forms
from django.apps import apps

from wagtail.core import blocks


class ColumnsBlock(blocks.StructBlock):
    def __init__(self, childblocks, ratios=(1, 1), **kwargs):
        super().__init__([
            ('column_%i' % index, childblocks)
            for index, _ in enumerate(ratios)
        ], **kwargs)
        self.ratios = ratios

    def get_column_widths(self):
        """Calculate the column widths as shares of the grid width."""
        multiplier = self.meta.grid_width // sum(self.ratios)
        return [
            multiplier * ratio
            for ratio in self.ratios
        ]

    def get_form_context(self, *args, **kwargs):
        context = super().get_form_context(*args, **kwargs)

        children = context['children']
        context.update({
            'columns': zip(children.values(), self.ratios),
        })

        return context

    def get_context(self, value, **kwargs):
        context = super().get_context(value, **kwargs)
        context.update({
            'columns': zip(value.values(), self.get_column_widths()),
        })

        return context

    class Meta:
        form_classname = 'columns-block struct-block'
        form_template = 'cms/blocks/forms/columnsblock.html'
        template = 'cms/blocks/columnsblock.html'

        grid_width = 12  # 12 columns in the grid

        if apps.is_installed('wagtailfontawesome'):
            icon = 'fa-columns'

    @property
    def media(self):
        return super().media + forms.Media(css={
            'all': ('cms/blocks/forms/columns.css',),
        })
