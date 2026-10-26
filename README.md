# TaskBridge ERD to PostgreSQL Schema

This submission translates the supplied TaskBridge ERD into an executable PostgreSQL schema and corrects the design inconsistencies in the starter files.

## Problems in the original ERD and starter schema

- `users.id` was not declared as a primary key, so user rows had no enforced identity.
- `tasks.user_id` and `tasks.project_id` were plain integers without foreign keys, allowing orphaned tasks.
- `users.name`, `users.email`, `projects.name`, and `tasks.title` were nullable even though the system needs them to identify records.
- `users.email` had no uniqueness constraint, allowing duplicate accounts.
- `task_owner_name` duplicated user data inside `tasks`. It could disagree with the referenced user and violated normalization. The corrected design removes it and uses `user_id` as the single source of ownership.
- The starter schema had no indexes for the two relationship columns used by task lists.

## Corrected design

The corrected ERD contains three entities. One user can be assigned many tasks, and one project can contain many tasks. Each task belongs to exactly one user and one project, represented by non-null foreign keys. A task therefore has one owner relationship and one project relationship without duplicating names.

The corrected design adds a primary key to every table, requires essential fields with `NOT NULL`, enforces unique email addresses, and indexes task lookups by user, project, and the combined project/user access path. Delete behavior is explicit: users cannot be removed while they own tasks, while deleting a project cascades to its tasks.

## Database schema explanation

`users.id` is referenced by `tasks.user_id`. `projects.project_id` is referenced by `tasks.project_id`. The two foreign keys implement the ERD's one-to-many relationships. `schema.sql` uses `SERIAL` identifiers for PostgreSQL compatibility and includes named constraints so `psql` output is easy to inspect.

## Verification

The included Python verification harness executes the schema in SQLite with foreign keys enabled, inserts valid users, projects, and tasks, and confirms that invalid user and project references are rejected. It also checks the expected primary keys, unique email constraint, and indexes.

```bash
python3 scripts/verify_schema.py
```

For PostgreSQL:

```bash
createdb taskbridge
psql -d taskbridge -f schema.sql
\dt
\d users
\d projects
\d tasks
```
