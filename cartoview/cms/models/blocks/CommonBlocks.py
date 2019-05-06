from wagtail.core import blocks

from .ThumbnailGalleryBlock import ThumbnailGalleryBlock
from .ImageTextOverlayBlock import ImageTextOverlayBlock


class CommonBlocks(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()
    image_text_overlay = ImageTextOverlayBlock()
    thumbnail_gallery = ThumbnailGalleryBlock()
