from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageTextOverlayBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        label='Image',
    )
    text = blocks.CharBlock(
        label='Text',
        max_length=200,
    )

    class Meta:
        template = 'cms/blocks/image_text_overlay.html'
        icon = 'fa-image'
