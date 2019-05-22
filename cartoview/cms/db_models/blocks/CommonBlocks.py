from wagtail.core import blocks

from .ImageTextOverlayBlock import ImageTextOverlayBlock
from .ThumbnailGalleryBlock import ThumbnailGalleryBlock


class CommonBlocks(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()
    image_text_overlay = ImageTextOverlayBlock()
    thumbnail_gallery = ThumbnailGalleryBlock()
