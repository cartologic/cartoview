from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.blocks import RawHTMLBlock, StreamBlock
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel


@register_setting(icon='fa-briefcase')
class SiteSettings(BaseSetting):
    logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+',
        blank=True, null=True
    )
    footer = RawHTMLBlock()
    footer = StreamField(
        StreamBlock([
            ('footer', RawHTMLBlock(
                default='<footer class="footer footer-default">' +
                        '<div class="container">' +
                        '<nav class="float-left">' +
                        '<ul>' +
                        '<li><a href="https://cartoview.net" target="_blank">Cartoview</a></li>' +
                        '<li><a href="http://www.twitter.com" target="_blank" class="btn btn-link btn-just-icon"><i class="fa fa-twitter"></i></a></li>' +
                        '<li><a href="http://www.instagram.com" target="_blank" class="btn btn-link btn-just-icon"><i class="fa fa-instagram"></i></a></li>' +
                        '<li><a href="http://www.facebook.com" target="_blank" class="btn btn-link btn-just-icon"><i class="fa fa-facebook-square"></i></a></li>' +
                        '</ul>' +
                        '</nav>' +
                        '<div class="copyright float-right">' +
                        '&copy;<script>document.write(new Date().getFullYear())</script>, made with <i class="material-icons">favorite</i> by <a href="http://cartologic.com" target="_blank">Cartologic</a> for a better web.'
                        '</div>' +
                        '</div>' +
                        '</footer>'
            )),
        ], min_num=0, max_num=1), blank=True, null=True
    )
    facebook = models.URLField(
        help_text='Your Facebook page URL',
        blank=True, null=True,
        default='https://www.facebook.com/Cartologic'
    )
    instagram = models.CharField(
        max_length=255, help_text='Your Instagram username, without the @',
        blank=True, null=True
    )
    youtube = models.URLField(
        help_text='Your YouTube channel or user account URL',
        blank=True, null=True
    )

    social_media_panel = [
        FieldPanel('facebook'),
        FieldPanel('instagram'),
        FieldPanel('youtube'),
    ]
    general_panel = [
        ImageChooserPanel('logo'),
        StreamFieldPanel("footer", classname="Full"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panel, heading='General'),
        ObjectList(social_media_panel, heading='Social Media'),
    ])

    class Meta:
        verbose_name = 'Site Settings'
