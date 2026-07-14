"""
models package

Usage:
    from models import Base, User, Module, Material, Attempt, Badge, UserBadge, ChatSession, ChatMessage

Import order matters for relationship string-resolution: all model classes
must be imported (even indirectly) before Base.metadata.create_all() or
before any relationship() is resolved. Importing them here in __init__.py
guarantees that as soon as someone does `import models`, every mapped class
is registered on the shared Base.
"""

from .base import Base, gen_uuid
from .user import User
from .module import Module
from .material import Material
from .attempt import Attempt
from .badge import Badge
from .user_badge import UserBadge
from .chat import ChatSession, ChatMessage, ChatRole
from .auth import UserOAuth, RefreshToken 

__all__ = [
    "Base",
    "gen_uuid",
    "User",
    "Module",
    "Material",
    "Attempt",
    "Badge",
    "UserBadge",
    "ChatSession",
    "ChatMessage",
    "ChatRole",
    "UserOAuth",
    "RefreshToken"
]