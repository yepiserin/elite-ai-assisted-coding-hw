import sqlite3
from typing import List, Dict, Any, Optional

DATABASE_PATH = "story_builder.db"

def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = get_db()
    cursor = conn.cursor()

    # Create mice_cards table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mice_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER DEFAULT 1,
            code TEXT NOT NULL,
            opening TEXT NOT NULL,
            closing TEXT NOT NULL,
            nesting_level INTEGER NOT NULL
        )
    """)

    # Create try_cards table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS try_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER DEFAULT 1,
            type TEXT NOT NULL,
            attempt TEXT NOT NULL,
            failure TEXT NOT NULL,
            consequence TEXT NOT NULL,
            order_num INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def get_mice_cards(story_id: int = 1) -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mice_cards WHERE story_id = ? ORDER BY nesting_level", (story_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_try_cards(story_id: int = 1) -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM try_cards WHERE story_id = ? ORDER BY order_num", (story_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_mice_card(code: str, opening: str, closing: str, nesting_level: int, story_id: int = 1) -> int:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mice_cards (story_id, code, opening, closing, nesting_level)
        VALUES (?, ?, ?, ?, ?)
    """, (story_id, code, opening, closing, nesting_level))
    conn.commit()
    card_id = cursor.lastrowid
    conn.close()
    return card_id

def add_try_card(type: str, attempt: str, failure: str, consequence: str, order_num: int, story_id: int = 1) -> int:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO try_cards (story_id, type, attempt, failure, consequence, order_num)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (story_id, type, attempt, failure, consequence, order_num))
    conn.commit()
    card_id = cursor.lastrowid
    conn.close()
    return card_id

def update_mice_card(card_id: int, code: str, opening: str, closing: str, nesting_level: int) -> None:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE mice_cards
        SET code = ?, opening = ?, closing = ?, nesting_level = ?
        WHERE id = ?
    """, (code, opening, closing, nesting_level, card_id))
    conn.commit()
    conn.close()

def update_try_card(card_id: int, type: str, attempt: str, failure: str, consequence: str, order_num: int) -> None:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE try_cards
        SET type = ?, attempt = ?, failure = ?, consequence = ?, order_num = ?
        WHERE id = ?
    """, (type, attempt, failure, consequence, order_num, card_id))
    conn.commit()
    conn.close()

def delete_mice_card(card_id: int) -> None:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mice_cards WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()

def delete_try_card(card_id: int) -> None:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM try_cards WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()

def clear_all_data(story_id: int = 1) -> None:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mice_cards WHERE story_id = ?", (story_id,))
    cursor.execute("DELETE FROM try_cards WHERE story_id = ?", (story_id,))
    conn.commit()
    conn.close()
