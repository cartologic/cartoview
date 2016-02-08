from django import forms
from django.templatetags.static import static
from cartoview.app_manager.forms import AppInstanceForm


class MapConfigForm(forms.Form):
    """
    Basic configuration form that works with Maps applications
    """
    config = forms.CharField(widget=forms.Textarea)

    class Media:
        css = {
            all: [static("codemerror/lib/codemirror.css")]
        }
        js = [static("codemerror/lib/codemirror.js"),
              static("codemerror/mode/javascript/javascript.js"),
              static("geonode_map_app/map_config_form.js")]
