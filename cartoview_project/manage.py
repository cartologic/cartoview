#!/usr/bin/env python
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTOVIEW_DIR = os.path.join(BASE_DIR, 'Cartoview')
sys.path.append(CARTOVIEW_DIR)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cartoview_project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
