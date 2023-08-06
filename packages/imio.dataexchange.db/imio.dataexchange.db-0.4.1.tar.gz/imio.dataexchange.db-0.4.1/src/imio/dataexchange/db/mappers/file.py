# -*- coding: utf-8 -*-

from imio.dataexchange.db import DeclarativeBase
from imio.dataexchange.db.base import MapperBase
from imio.dataexchange.db.mappers.file_type import FileType
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import func
# from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.schema import UniqueConstraint

import json as jsonmodule

FileType  # Pyflakes


class File(DeclarativeBase, MapperBase):
    __tablename__ = u'file'
    __table_args__ = (
        UniqueConstraint(u'external_id', u'version', u'user',
                         name='user_external_id'),
    )

    id = Column(u'id', Integer, primary_key=True, unique=True, nullable=False)

    external_id = Column(u'external_id', Text, nullable=False)

    client_id = Column(u'client_id', Text, nullable=False)

    type = Column(u'type', Text, ForeignKey('file_type.id'), nullable=False)

    version = Column('version', Integer, nullable=False)

    date = Column(u'date', DateTime, nullable=False, server_default=func.now())

    update_date = Column(u'update_date', DateTime)

    user = Column(u'user', Text, nullable=False)

    _file_metadata = Column(u'metadata', Text, nullable=False)
    # file_metadata = Column(u'metadata', JSON, nullable=False)

    filepath = Column(u'filepath', Text)

    file_md5 = Column(u'file_md5', Text)

    amqp_status = Column(u'amqp_status', Boolean, nullable=False,
                         server_default="false")

    @property
    def file_metadata(self):
        return jsonmodule.loads(self._file_metadata)

    @file_metadata.setter
    def file_metadata(self, value):
        metadata = value.copy()
        if 'type' in metadata:
            del metadata['type']
        del metadata['external_id']
        del metadata['client_id']
        self._file_metadata = jsonmodule.dumps(metadata)
