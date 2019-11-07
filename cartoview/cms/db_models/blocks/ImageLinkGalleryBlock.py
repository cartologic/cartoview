from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageLink(blocks.StructBlock):
    image = ImageChooserBlock(
        label='Image',
    )
    link = blocks.CharBlock(
        label='Link',
        max_length=200,
    )


class ImageLinkGalleryBlock(blocks.StructBlock):
    image_items = blocks.ListBlock(
        ImageLink(),
        label="Image",
    )
    single_image_width = blocks.IntegerBlock(
        help_text="in pixels"
    )

    class Meta:
        template = 'cms/blocks/image_link_gallery.html'
        icon = 'fa-cubes'
