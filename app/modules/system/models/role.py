from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.id_generator import next_id
from app.db.base import Base, role_menus, user_roles

if TYPE_CHECKING:
    from .menu import Menu
    from .user import User


class Role(Base):
    __tablename__ = "sys_role"

    role_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, default=next_id, comment="角色ID"
    )
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, comment="角色名称"
    )
    code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, comment="角色编码"
    )
    desc: Mapped[str] = mapped_column(String(255), nullable=True, comment="备注")
    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    users: Mapped[list["User"]] = relationship(
        "User", secondary=user_roles, back_populates="roles"
    )
    menus: Mapped[list["Menu"]] = relationship(
        "Menu", secondary=role_menus, back_populates="roles", lazy="selectin"
    )
