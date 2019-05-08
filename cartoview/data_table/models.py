import csv

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList, \
    StreamFieldPanel, MultiFieldPanel
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.contrib.table_block.blocks import TableBlock


class TableBlock(StreamBlock):
    table = TableBlock()

    class Meta:
        icon = 'cogs'


class DataTable(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    upload_file = models.FileField(blank=True, null=True)
    values = StreamField(TableBlock(max_num=1, min_num=0,
                                    block_counts={'table': {'max_num': 1, 'min_num': 0}}
                                    ))

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
        FieldPanel('upload_file', help_text="Upload a CSV file instead!"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panel, heading='General'),
    ])

    def __str__(self):
        return "Table (" + self.name + ")"

    def clean(self):
        if self.upload_file:
            decoded_file = self.upload_file.file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)
            if not self.values.stream_data[0][1]:
                initial_data = {
                    'data': [],
                    'first_row_is_table_header': False,
                    'first_col_is_table_header': False
                }
                temp_stream_data = [['table', initial_data, self.values.stream_data[0][2]]]
                self.values.stream_data = temp_stream_data
            else:
                self.values.stream_data[0][1]['data'] = []
            for row in csv_reader:
                self.values.stream_data[0][1]['data'].append(row)
                self.upload_file = None

    class Meta:
        verbose_name = 'Data Table'
        verbose_name_plural = 'Data Tables'
