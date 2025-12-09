from __future__ import annotations

import time

import schedule

from todo_app.commands.autoclose_overdue import autoclose_overdue_tasks


def run_autoclose_job() -> None:
    """
    Job wrapper: calls the autoclose command once and logs the result.
    """
    count = autoclose_overdue_tasks()
    print(f"[scheduler] Auto-closed {count} overdue tasks.")


def main() -> None:
    """
    Run the scheduler loop.

    For development we use a short interval.
    """
    # every 15 seconds for demo/presentation
    schedule.every(15).seconds.do(run_autoclose_job)
    print("[scheduler] Started. Running autoclose job every 15 seconds. Press Ctrl+C to stop.")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()