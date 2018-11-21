# -*- coding: utf-8 -*-
from .utils import create_apps_dir
create_apps_dir()
from .handlers import apps_orm  # noqa
apps_orm.create_all()
