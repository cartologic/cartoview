from django import template
from django.http import HttpRequest
from django.template import Context, Template
from django.test.testcases import TestCase

from geonode.people.models import Profile


class CartoviewTemplateTagsTest(TestCase):
    fixtures = ['sample_admin.json', ]

    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def test_template_tags(self):
        rendered = self.render_template(
            """{% load cartoview_tags %}x={{test_dict|dump_json}}""", {
                "test_dict": {"foo": "bar"}}
        )
        self.assertEqual(rendered, u'x={"foo": "bar"}')
        self.assertRaises(
            template.TemplateSyntaxError,
            self.render_template,
            """{% load cartoview_tags %%}}x={{test_dict|dump_json}}""", {
                "test_dict": {"foo": "bar"}}
        )
        req = HttpRequest()
        req.user = Profile.objects.filter(username="admin").first()
        rendered = self.render_template(
            """{% load cartoview_tags %}{% facets as facets %}{{facets}}""", {
                "request": req}
        )
        # self.assertEqual(
        #     rendered, u'{u&#39;raster&#39;: 0, u&#39;vector&#39;: 0, u&#39;' +  # noqa
        #     'remote&#39;: 0, u&#39;document&#39;: 0, u&#39;map&#39;: 0}')
        self.assertRaises(
            template.TemplateSyntaxError,
            self.render_template,
            """{% load cartoview_tags %%}}x={{test_dict|dump_json}}""", {
                "test_dict": {"foo": "bar"}}
        )
