from wagtailmenus.models import MenuPage


class MenuItem(MenuPage):
    parent_page_types = ['HomePage']
    show_in_menus_default = True
