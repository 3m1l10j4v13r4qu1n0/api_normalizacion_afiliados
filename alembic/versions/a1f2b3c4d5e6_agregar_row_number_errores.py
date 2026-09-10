"""agregar columna row_number a errores_validacion

Revision ID: a1f2b3c4d5e6
Revises: 6fecb555bfe0
Create Date: 2026-09-07 00:00:00.000000

AF-RN12 — el número de fila original que falló debe persistirse en
cada error de validación.
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1f2b3c4d5e6"
down_revision: str | Sequence[str] | None = "6fecb555bfe0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "errores_validacion",
        sa.Column("row_number", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("errores_validacion", "row_number")
