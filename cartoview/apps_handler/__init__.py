# -*- coding: utf-8 -*-
from .handlers import apps_orm
from .utils import create_apps_dir
create_apps_dir()
apps_orm.create_all()
