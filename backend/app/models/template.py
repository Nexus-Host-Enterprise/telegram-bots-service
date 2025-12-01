import sqlalchemy as sa
from app.db.base import Base

class Template(Base):
    __tablename__ = "templates"
    name = sa.Column(sa.String, primary_key=True)
    version = sa.Column(sa.String, nullable=False, default="1.0")
    description = sa.Column(sa.String, nullable=True)
    config_schema = sa.Column(sa.JSON, nullable=True)
    code_bundle = sa.Column(sa.String, nullable=True)  # path or identifier
