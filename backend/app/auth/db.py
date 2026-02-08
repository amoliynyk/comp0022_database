from typing import Optional

from app.database import execute_command, execute_query_one, execute_returning


def ensure_app_users_table() -> None:
    execute_command("""
        CREATE TABLE IF NOT EXISTS app_users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(255) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)


def create_user(username: str, email: str, password_hash: str) -> Optional[dict]:
    return execute_returning(
        """
        INSERT INTO app_users (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING user_id, username, email, created_at
        """,
        (username, email, password_hash),
    )


def get_user_by_username(username: str) -> Optional[dict]:
    return execute_query_one(
        "SELECT user_id, username, email, password_hash, created_at FROM app_users WHERE username = %s",
        (username,),
    )


def get_user_by_id(user_id: int) -> Optional[dict]:
    return execute_query_one(
        "SELECT user_id, username, email, created_at FROM app_users WHERE user_id = %s",
        (user_id,),
    )
