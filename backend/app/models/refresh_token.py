import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = sa.Column(sa.String, nullable=False, unique=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    revoked = sa.Column(sa.Boolean, default=False)
