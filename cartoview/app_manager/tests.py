# from django.test import TestCase
# import mock
# from .models import AppTag, App
# from .config import Item


# class AppTagsTestCase(TestCase):

#     def test_AppTag_str(self):
#         mock_instance = mock.Mock(spec=AppTag)
#         mock_instance.name = "tag"
#         mock_instance.__str__ = mock.Mock(return_value=mock_instance.name)
#         self.assertEqual(AppTag.__str__(mock_instance),
#                          mock_instance.__str__())

#     def test_tag_created(self):
#         tag, created = AppTag.objects.get_or_create(name="tag")
#         self.assertEqual(created, True)
#         self.assertEqual(tag.name, "tag")


# class AppTestCase(TestCase):

#     def test_App_str(self):
#         app_mock = mock.Mock(spec=App)
#         app_mock.name = "cartoview_basic_viewer"
#         app_mock.title = "Basic Viewer"
#         app_mock.single_instance = False
#         app_mock.version = '1.2.3'
#         app_mock.settings_url = App.settings_url
#         app_mock.__str__ = mock.Mock(return_value=app_mock.title)
#         self.assertEqual(App.__str__(app_mock),
#                          app_mock.__str__())

#     def test_app_creation(self):
#         app, created = App.objects.get_or_create(
#             name="cartoview_basic_viewer", title="basic viewer",
#             single_instance=False, version='1.2.3')
#         self.assertEqual(type(app.config), Item)
#         self.assertEqual(created, True)
