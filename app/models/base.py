"""
Re-exports the app's existing declarative Base so every model in this
package attaches to the same metadata / registry as the rest of the app.
"""

import uuid

from app.db.base import Base  # existing `Base = declarative_base()`


def gen_uuid() -> str:
    """Default factory for varchar-based primary keys."""
    return str(uuid.uuid4())