"""rename user_id to owner_id

Revision ID: rename_user_id_to_owner_id
Revises: 8bc7d015e690
Create Date: 2025-07-27 23:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'rename_user_id_to_owner_id'
down_revision = '8bc7d015e690'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Переименовываем колонку user_id в owner_id в таблице location
    op.alter_column('location', 'user_id', new_column_name='owner_id')
    
    # Переименовываем колонку user_id в owner_id в таблице sphere
    op.alter_column('sphere', 'user_id', new_column_name='owner_id')


def downgrade() -> None:
    # Возвращаем обратно колонку owner_id в user_id в таблице location
    op.alter_column('location', 'owner_id', new_column_name='user_id')
    
    # Возвращаем обратно колонку owner_id в user_id в таблице sphere
    op.alter_column('sphere', 'owner_id', new_column_name='user_id') 