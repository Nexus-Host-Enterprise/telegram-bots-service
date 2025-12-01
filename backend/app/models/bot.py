import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.db.base import Base

class Bot(Base):
    __tablename__ = "bots"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = sa.Column(sa.String, nullable=False)
    template_name = sa.Column(sa.String, nullable=False)
    config = sa.Column(JSONB, nullable=True)
    tg_token_encrypted = sa.Column(sa.LargeBinary, nullable=True)
    status = sa.Column(sa.String, nullable=False, default="creating")  # creating|deploying|running|stopped|failed
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, onupdate=sa.func.now())
