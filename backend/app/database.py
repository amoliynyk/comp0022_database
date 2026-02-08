import logging
from contextlib import contextmanager
from typing import Any, Optional

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

from app.config import settings

logger = logging.getLogger(__name__)

_pool: Optional[pool.ThreadedConnectionPool] = None


def init_pool() -> None:
    global _pool
    try:
        _pool = pool.ThreadedConnectionPool(
            minconn=2,
            maxconn=10,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
        )
        logger.info("Database connection pool created")
    except psycopg2.OperationalError as e:
        logger.warning("Could not connect to database: %s", e)
        _pool = None


def close_pool() -> None:
    global _pool
    if _pool:
        _pool.closeall()
        _pool = None
        logger.info("Database connection pool closed")


@contextmanager
def get_connection():
    if _pool is None:
        raise ConnectionError("Database pool is not initialised")
    conn = _pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)


def execute_query(sql: str, params: tuple = ()) -> list[dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return [dict(row) for row in cur.fetchall()]


def execute_query_one(sql: str, params: tuple = ()) -> Optional[dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
            return dict(row) if row else None


def execute_command(sql: str, params: tuple = ()) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)


def execute_returning(sql: str, params: tuple = ()) -> Optional[dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
            return dict(row) if row else None


def is_healthy() -> bool:
    try:
        execute_query_one("SELECT 1")
        return True
    except Exception:
        return False
