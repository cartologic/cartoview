from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class PartnerLogo(blocks.StructBlock):
    image = ImageChooserBlock(
        label='Image',
    )
    link = blocks.CharBlock(
        label='link',
        max_length=200,
        required=False
    )


class PartnersLogosBlock(blocks.StructBlock):
    image_items = blocks.ListBlock(
        PartnerLogo(),
        label="Image",
    )

    class Meta:
        template = 'cms/blocks/partners_logos.html'
        icon = 'fa-object-ungroup'
