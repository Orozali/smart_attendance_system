"""merge branches

Revision ID: a434d20e2fb6
Revises: ea5fe59814b0, 68a45874c90c
Create Date: 2025-04-30 15:45:51.565886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a434d20e2fb6'
down_revision: Union[str, None] = ('ea5fe59814b0', '68a45874c90c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
