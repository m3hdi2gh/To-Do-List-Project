from __future__ import annotations

from datetime import date, datetime, UTC

from sqlalchemy import select

from todo_app.db.session import SessionLocal
from todo_app.db.models import TaskORM, TaskStatusEnum


def autoclose_overdue_tasks() -> int:
    """
    Find all tasks with deadline < today and status != done,
    mark them as done and set closed_at to now.

    Returns the number of tasks that were updated.
    """
    today = date.today()
    now = datetime.now(UTC)

    with SessionLocal() as session:
        # Query all overdue tasks
        stmt = select(TaskORM).where(
            TaskORM.deadline.is_not(None),
            TaskORM.deadline < today,
            TaskORM.status != TaskStatusEnum.DONE,
        )
        tasks = session.scalars(stmt).all()

        for t in tasks:
            t.status = TaskStatusEnum.DONE
            t.closed_at = now

        session.commit()
        return len(tasks)


def main() -> None:
    """
    Entry point for this command.
    """
    count = autoclose_overdue_tasks()
    print(f"Auto-closed {count} overdue tasks.")


if __name__ == "__main__":
    main()