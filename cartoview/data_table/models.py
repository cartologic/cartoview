import csv

from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList, \
    StreamFieldPanel, MultiFieldPanel
from wagtail.core.blocks import StreamBlock, CharBlock, StructBlock, ChoiceBlock
from wagtail.core.fields import StreamField
from django.db import models
from .factory import DynamicModel

field_mapping = {
    'text': models.TextField(null=True, blank=True),
    'number': models.FloatField(null=True, blank=True)
}


class FieldTypeChoiceBlock(ChoiceBlock):
    choices = (
        ('text', 'Text'),
        ('number', 'Number'),
    )


class FieldsListBlock(StructBlock):
    name = CharBlock()
    type = FieldTypeChoiceBlock()


class DataTable(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    fields = StreamField(
        StreamBlock([
            ('field', FieldsListBlock()),
        ]), blank=True, null=True)
    upload_file = models.FileField(blank=True, null=True)

    general_panel = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                FieldPanel('description'),
                FieldPanel('additional_info'),
            ],
            heading="Info",
        ),
        StreamFieldPanel('fields'),
    ]
    data_upload_panel = [
        FieldPanel('upload_file', help_text="Upload a CSV file!"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panel, heading='General'),
        ObjectList(data_upload_panel, heading='Data Upload'),
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


@receiver(post_save, sender=DataTable)
def create_model_table(sender, instance, **kwargs):
    created = kwargs.get('created')
    if created:
        pre_fields = [d[1] for d in instance.fields.stream_data]
        module_name = 'fake_project.{}.{}'.format(instance.name.lower(), instance.name.lower())
        temp_fields = {f['name']: field_mapping[f['type']] for f in pre_fields}
        model = DynamicModel.create_model(instance.name.capitalize(), instance.name,
                                          app_label='fake_app',
                                          module=module_name,
                                          fields=temp_fields)
        DynamicModel.create_model_table(model)


@receiver(post_delete, sender=DataTable)
def delete_model_table(sender, instance, *args, **kwargs):
    pre_fields = [d['value'] for d in instance.fields.stream_data]
    module_name = 'fake_project.{}.{}'.format(instance.name.lower(), instance.name.lower())
    temp_fields = {f['name']: field_mapping[f['type']] for f in pre_fields}
    model = DynamicModel.create_model(instance.name.capitalize(), instance.name,
                                      app_label=instance.name.lower(),
                                      module=module_name,
                                      fields=temp_fields)
    try:
        DynamicModel.delete_model_table(model)
    except BaseException:
        pass
