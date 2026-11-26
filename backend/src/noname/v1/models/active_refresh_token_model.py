from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, func

from noname.v1 import database


class ActiveRefreshTokenModel(database.Base):
    __tablename__ = "active_refresh_tokens"

    jti = Column(type_=String, primary_key=True)
    expires_at = Column(type_=TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(
        type_=TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
