# from django.urls import reverse
# from django.utils.safestring import mark_safe
# from wagtail.admin.menu import MenuItem
# from wagtail.core import hooks
# from django.conf.urls import url
# from django.http import HttpResponse


# class WelcomePanel:
#     order = 1

#     def render(self):
#         return mark_safe("""
#         <section class="panel summary nice-padding">
#           <h3>No, but seriously -- welcome to the admin homepage.</h3>
#         </section>
#         """)


# def admin_view(request):
#     return HttpResponse(
#         "I have approximate knowledge of many things!",
#         content_type="text/plain")


# @hooks.register('register_admin_urls')
# def urlconf_time():
#     return [
#         url(r'^how_did_you_almost_know_my_name/$', admin_view, name='frank'),
#     ]


# @hooks.register('construct_homepage_panels')
# def add_another_welcome_panel(request, panels):
#     return panels.append(WelcomePanel())


# @hooks.register('register_admin_menu_item')
# def register_frank_menu_item():
#     return MenuItem('Frank', reverse('frank'), classnames='icon icon-folder-inverse', order=10000)
