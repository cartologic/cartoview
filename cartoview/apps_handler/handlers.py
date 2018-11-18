# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
from contextlib import contextmanager

from django.conf import settings
from future import standard_library
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.expression import func
from sqlalchemy.types import Boolean, DateTime

standard_library.install_aliases()


class AppsHandlerDBException(Exception):
    pass


class AppsORM(object):
    def __init__(self, db_name="apps.sqlite", engine=None, debug=False):
        self._db_name = db_name
        self.Base = declarative_base()
        self.engine = engine if engine else create_engine(
            self.get_connection_string(), echo=debug)
        self.AutoMapBase = automap_base()
        self.AutoMapBase.prepare(self.engine, reflect=True)
        self.Base.metadata.reflect(bind=self.engine)

    @contextmanager
    def session(self):
        """ Creates a context with an open SQLAlchemy session.
        """
        engine = self.engine
        connection = engine.connect()
        db_session = scoped_session(
            sessionmaker(autocommit=False, autoflush=True, bind=engine))
        yield db_session
        db_session.close()
        connection.close()

    def create_all(self):
        self.Base.metadata.create_all(self.engine, checkfirst=True)

    def get_or_create(self, model, **kwargs):
        with self.session() as session:
            instance = session.query(model).filter_by(**kwargs).first()
            if instance:
                return instance
            else:
                instance = model(**kwargs)
                session.add(instance)
                session.commit()
                return instance

    def get_connection_string(self):
        apps_dir = getattr(settings, 'APPS_DIR', None)
        if not apps_dir:
            raise AppsHandlerDBException("APPS_DIR not configured")
        connection_prefix = '''sqlite:///'''
        apps_dir = os.path.abspath(apps_dir)
        db_path = os.path.join(apps_dir, self._db_name)
        connection_str = "{}{}".format(connection_prefix, db_path)
        return connection_str


apps_orm = AppsORM()


class AppsHandlerMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __mapper_args__ = {'always_refresh': True}


class BaseModel(AppsHandlerMixin, object):

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CartoApps(BaseModel, apps_orm.Base):
    __tablename__ = 'carto_apps'
    __table_args__ = {'extend_existing': True}

    name = Column(String(100), nullable=False, unique=True)
    active = Column(Boolean, nullable=True, default=True)
    order = Column(Integer(), nullable=False, default=0)
    pending = Column(Boolean, nullable=True, default=True)

    @classmethod
    def get_next_order(cls):
        with apps_orm.session() as session:
            query = session.query(func.max(cls.order).label("max_order"))
            result = query.one()
            return result.max_order + 1

    @classmethod
    def app_exists(cls, app_name):
        with apps_orm.session() as session:
            exists = session.query(
                session.query(cls).filter(
                    cls.name == app_name).exists()).scalar()
            return exists

    @classmethod
    def delete_app(cls, app_name):
        with apps_orm.session() as session:
            obj = session.query(cls).filter(cls.name == app_name).first()
            if obj:
                session.delete(obj)
                session.commit()

    @classmethod
    def get_app_by_name(cls, app_name):
        with apps_orm.session() as session:
            obj = session.query(cls).filter(cls.name == app_name).first()
            return obj

    @classmethod
    def set_app_active(cls, app_name, active=True):
        return cls.update_app(app_name, {"active": active})

    @classmethod
    def update_app(cls, app_name, props_dict=dict()):
        obj = None
        if cls.app_exists(app_name):
            with apps_orm.session() as session:
                query = session.query(cls).filter(cls.name == app_name)
                query.update(props_dict)
                session.commit()
                obj = query.first()
        return obj

    @classmethod
    def set_app_pending(cls, app_name, pending=True):
        return cls.update_app(app_name, {"pending": pending})

    @classmethod
    def set_app_order(cls, app_name, order):
        return cls.update_app(app_name, {"order": order})
