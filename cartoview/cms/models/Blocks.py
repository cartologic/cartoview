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


class FooterBlock(blocks.StructBlock):
    left_section = RawHTMLBlock(
        label='Left Section',
        required=False,
        default='<ul>' +
                '<li><a href="https://cartoview.net" target="_blank">Cartoview</a></li>' +
                '<li><a href="http://www.twitter.com" target="_blank" class="btn btn-link btn-just-icon"><i class="fa fa-twitter"></i></a></li>' +
                '<li><a href="http://www.instagram.com" target="_blank" class="btn btn-link btn-just-icon"><i class="fa fa-instagram"></i></a></li>' +
                '<li><a href="http://www.facebook.com" target="_blank" class="btn btn-link btn-just-icon"><i class="fa fa-facebook-square"></i></a></li>' +
                '</ul>',
    )
    right_section = RawHTMLBlock(
        label='Right Section',
        required=False,
        default='&copy;<script>document.write(new Date().getFullYear())</script>, made with <i class="material-icons">favorite</i> by <a href="http://cartologic.com" target="_blank">Cartologic</a> for a better web.'
    )

    class Meta:
        template = 'cms/blocks/footer.html'
        icon = "fa-window-minimize"
