from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail_blocks.blocks import HeaderBlock, ImageTextOverlayBlock, CroppedImagesWithTextBlock, \
    ListWithImagesBlock, ThumbnailGalleryBlock
from .GridBlock import GridBlock
from .Blocks import NavigationBarBlock, HeroAreaBlock, FooterBlock


class HomePage(Page):
    body = StreamField([
        ('navigation_bar', NavigationBarBlock()),
        ('hero_area', HeroAreaBlock()),
        ('grid', GridBlock()),
        ('footer', FooterBlock()),
        ('header', HeaderBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image_text_overlay', ImageTextOverlayBlock()),
        ('cropped_images_with_text', CroppedImagesWithTextBlock()),
        ('list_with_images', ListWithImagesBlock()),
        ('thumbnail_gallery', ThumbnailGalleryBlock()),
    ], blank=True, null=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel("body", classname="Full"),
    ]
