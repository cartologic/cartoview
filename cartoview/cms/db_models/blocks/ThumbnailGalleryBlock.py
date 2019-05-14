from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class StyleChoiceBlock(blocks.ChoiceBlock):
    choices = (
        ('rounded', 'Square'),
        ('rounded-circle', 'Rounded'),
    )


class ThumbnailImage(blocks.StructBlock):
    image = ImageChooserBlock(
        label='Image',
    )


class ThumbnailGalleryBlock(blocks.StructBlock):
    style = StyleChoiceBlock(
        label='Style',
        default='rounded'
    )
    image_items = blocks.ListBlock(
        ThumbnailImage(),
        label="Image",
    )

    class Meta:
        template = 'cms/blocks/thumbnail_gallery.html'
        icon = 'fa-object-ungroup'
