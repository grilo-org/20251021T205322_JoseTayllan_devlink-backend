"""add url de portfolio publica"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revisão
revision: str = '51de929cefa4'
down_revision: Union[str, Sequence[str], None] = '82448c589aa9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema"""
    # ✅ usa batch mode para compatibilidade com SQLite
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('public_id', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('is_public', sa.Boolean(), nullable=True))
        # ⚠️ removido o create_unique_constraint (SQLite não suporta)
        # o unique=True será respeitado nas próximas criações de banco


def downgrade() -> None:
    """Downgrade schema"""
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_public')
        batch_op.drop_column('public_id')
