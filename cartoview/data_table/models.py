from django.db import models
from django.db.models import Model
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList, StreamFieldPanel, MultiFieldPanel
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.contrib.table_block.blocks import TableBlock


class TableBlock(StreamBlock):
    table = TableBlock()

    class Meta:
        icon = 'cogs'


class DataTable(Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    values = StreamField(TableBlock(max_num=1, min_num=0, block_counts={'table': {'max_num': 1, 'min_num': 0}}))

    general_panel = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                FieldPanel('description'),
                FieldPanel('additional_info'),
            ],
            heading="Info",
        ),
        StreamFieldPanel('values'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panel, heading='General'),
    ])

    def __str__(self):
        return "Table (" + self.name + ")"

    class Meta:
        verbose_name = 'Data Table'
        verbose_name_plural = 'Data Tables'
