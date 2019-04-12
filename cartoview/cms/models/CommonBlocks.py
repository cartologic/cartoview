from wagtail.core import blocks
from wagtail_blocks.blocks import HeaderBlock, ImageTextOverlayBlock, CroppedImagesWithTextBlock, \
    ListWithImagesBlock, ThumbnailGalleryBlock


class CommonBlocks(blocks.StreamBlock):
    header = HeaderBlock()
    paragraph = blocks.RichTextBlock()
    image_text_overlay = ImageTextOverlayBlock()
    cropped_images_with_text = CroppedImagesWithTextBlock()
    list_with_images = ListWithImagesBlock()
    thumbnail_gallery = ThumbnailGalleryBlock()
