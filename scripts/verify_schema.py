from pathlib import Path
import sqlite3

root = Path(__file__).resolve().parents[1]
conn = sqlite3.connect(':memory:')
conn.execute('PRAGMA foreign_keys = ON')
schema = (root / 'schema.sql').read_text().replace('SERIAL', 'INTEGER')
conn.executescript(schema)

conn.execute("INSERT INTO users (name, email) VALUES ('Ari Chen', 'ari@example.com')")
conn.execute("INSERT INTO projects (name, description) VALUES ('Launch plan', 'TaskBridge launch work')")
conn.execute("INSERT INTO tasks (title, user_id, project_id) VALUES ('Write brief', 1, 1)")

for sql in [
    "INSERT INTO users (name, email) VALUES ('Duplicate', 'ari@example.com')",
    "INSERT INTO tasks (title, user_id, project_id) VALUES ('Orphan user', 999, 1)",
    "INSERT INTO tasks (title, user_id, project_id) VALUES ('Orphan project', 1, 999)",
]:
    try:
        conn.execute(sql)
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError(f'constraint did not reject: {sql}')

assert conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0] == 3
assert conn.execute("SELECT COUNT(*) FROM pragma_index_list('tasks')").fetchone()[0] >= 3
assert conn.execute("SELECT name FROM users").fetchone()[0] == 'Ari Chen'
print('schema verification passed: 3 tables, valid relationships, unique email, and indexes')
