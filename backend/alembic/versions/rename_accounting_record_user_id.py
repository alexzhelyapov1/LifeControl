"""rename accounting_record user_id to owner_id

Revision ID: rename_accounting_record_user_id
Revises: rename_user_id_to_owner_id
Create Date: 2025-07-27 23:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'rename_accounting_record_user_id'
down_revision = 'rename_user_id_to_owner_id'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Переименовываем колонку user_id в owner_id в таблице accountingrecord
    op.alter_column('accountingrecord', 'user_id', new_column_name='owner_id')


def downgrade() -> None:
    # Возвращаем обратно колонку owner_id в user_id в таблице accountingrecord
    op.alter_column('accountingrecord', 'owner_id', new_column_name='user_id') 