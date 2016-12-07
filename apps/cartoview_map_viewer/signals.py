from django.dispatch import Signal

widgets = Signal(providing_args=['request'])
