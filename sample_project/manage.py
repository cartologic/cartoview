#!/usr/bin/env python

import os
import sys
current_folder = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_folder, os.path.pardir)))

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cartoview_project.settings")
    execute_from_command_line(sys.argv)

