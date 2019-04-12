from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail_blocks.blocks import HeaderBlock, ImageTextOverlayBlock, CroppedImagesWithTextBlock, \
    ListWithImagesBlock, ThumbnailGalleryBlock
from .grid.GridBlock import GridBlock
from .Blocks import HeroAreaBlock


class HomePage(Page):
    hero = StreamField([
        ('hero_area', HeroAreaBlock()),
        ], blank=True, null=True, help_text=mark_safe("You should add only <b>1 Hero</b>"))
    body = StreamField([
        ('grid', GridBlock()),
        ('header', HeaderBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image_text_overlay', ImageTextOverlayBlock()),
        ('cropped_images_with_text', CroppedImagesWithTextBlock()),
        ('list_with_images', ListWithImagesBlock()),
        ('thumbnail_gallery', ThumbnailGalleryBlock()),
    ], blank=True, null=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel("hero", classname="Full"),
        StreamFieldPanel("body", classname="Full"),
    ]
