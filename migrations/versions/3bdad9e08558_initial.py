# migrations/versions/3bdad9e08558_initial.py
"""initial

Revision ID: 3bdad9e08558
Revises: 
Create Date: 2025-04-11 23:05:47.708032
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '3bdad9e08558'
down_revision = None
branch_labels = None
depends_on = None

def table_exists(connection, table_name):
    """Check if a table exists in the database."""
    inspector = inspect(connection)
    return table_name in inspector.get_table_names()

def upgrade() -> None:
    # Get the connection
    connection = op.get_bind()
    
    # Safely create tables
    if not table_exists(connection, 'user_activity'):
        op.create_table('user_activity',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('activity_type', sa.String(length=50), nullable=False),
        sa.Column('activity_data', sa.String(length=255), nullable=True),
        sa.Column('xp_earned', sa.Integer(), nullable=True),
        sa.Column('coins_earned', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_user_activity_id'), 'user_activity', ['id'], unique=False)
    
    if not table_exists(connection, 'lessons'):
        op.create_table('lessons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('type', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('task', sa.Text(), nullable=True),
        sa.Column('expected_output', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('xp_reward', sa.Integer(), nullable=True),
        sa.Column('coins_reward', sa.Integer(), nullable=True),
        sa.Column('estimated_time_minutes', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_lessons_id'), 'lessons', ['id'], unique=False)
    
    if not table_exists(connection, 'coding_challenges'):
        op.create_table('coding_challenges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('difficulty', sa.String(length=20), nullable=True),
        sa.Column('starter_code', sa.Text(), nullable=True),
        sa.Column('solution_code', sa.Text(), nullable=True),
        sa.Column('expected_output', sa.Text(), nullable=True),
        sa.Column('hints', sa.Text(), nullable=True),
        sa.Column('points', sa.Integer(), nullable=True),
        sa.Column('lesson_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_coding_challenges_id'), 'coding_challenges', ['id'], unique=False)
    
    if not table_exists(connection, 'quiz_questions'):
        op.create_table('quiz_questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lesson_id', sa.Integer(), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_quiz_questions_id'), 'quiz_questions', ['id'], unique=False)
    
    if not table_exists(connection, 'user_progress'):
        op.create_table('user_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('lesson_id', sa.Integer(), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('attempts', sa.Integer(), nullable=True),
        sa.Column('last_attempt_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'lesson_id', name='uc_user_lesson')
        )
        op.create_index(op.f('ix_user_progress_id'), 'user_progress', ['id'], unique=False)
    
    if not table_exists(connection, 'quiz_options'):
        op.create_table('quiz_options',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('option_text', sa.Text(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['question_id'], ['quiz_questions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_quiz_options_id'), 'quiz_options', ['id'], unique=False)
    
    if not table_exists(connection, 'user_challenges'):
        op.create_table('user_challenges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('challenge_id', sa.Integer(), nullable=False),
        sa.Column('completed', sa.Boolean(), nullable=True),
        sa.Column('code_submitted', sa.Text(), nullable=True),
        sa.Column('attempts', sa.Integer(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['challenge_id'], ['coding_challenges.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_user_challenges_id'), 'user_challenges', ['id'], unique=False)

def downgrade() -> None:
    # Get the connection
    connection = op.get_bind()
    
    # Drop tables only if they exist
    tables_to_drop = [
        ('user_challenges', 'ix_user_challenges_id'),
        ('quiz_options', 'ix_quiz_options_id'),
        ('user_progress', 'ix_user_progress_id'),
        ('quiz_questions', 'ix_quiz_questions_id'),
        ('coding_challenges', 'ix_coding_challenges_id'),
        ('lessons', 'ix_lessons_id'),
        ('user_activity', 'ix_user_activity_id')
    ]
    
    for table_name, index_name in tables_to_drop:
        if table_exists(connection, table_name):
            op.drop_index(op.f(index_name), table_name=table_name)
            op.drop_table(table_name)