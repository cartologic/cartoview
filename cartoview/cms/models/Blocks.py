from wagtail.core import blocks
from wagtail.core.blocks import RawHTMLBlock
from wagtail.images.blocks import ImageChooserBlock

from .IconChoiceBlock import IconChoiceBlock


class ThemeChoiceBlock(blocks.ChoiceBlock):
    choices = (
        ('primary', 'Primary'),
        ('info', 'Info'),
        ('success', 'Success'),
        ('danger', 'Danger'),
        ('warning', 'Warning'),
        ('default', 'Default'),
    )


class SingleMainHeaderLink(blocks.StructBlock):
    theme = ThemeChoiceBlock(
        label='Theme',
        default='info'
    )
    icon = IconChoiceBlock(
        label='Icon',
        required=False,
    )
    text = blocks.CharBlock(
        label='Text',
        max_length=120,
    )
    link = blocks.URLBlock(required=False, default='Link')

    class Meta:
        template = 'cms/blocks/single_main_header_link.html'


class HeroAreaBlock(blocks.StructBlock):
    main_text = blocks.CharBlock(
        label='Main Text',
        required=False,
        max_length=120,
    )
    body_text = blocks.RichTextBlock(
        label='Body Text',
        required=False,
    )
    background_image = ImageChooserBlock(
        label='Background Image',
    )
    links = blocks.ListBlock(
        SingleMainHeaderLink(),
        label='Link',
    )

    class Meta:
        template = 'cms/blocks/hero_area.html'
        icon = "fa-wpexplorer"


class MapCatalogBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        label='Title',
        max_length=240,
    )

    class Meta:
        template = 'cms/blocks/map_catalog.html'
        icon = "fa-map"
