import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from task_manager import Task, TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)

        self.filename = Path(temporary_directory.name) / "tasks.json"
        filename_patch = patch.object(TaskManager, "FILENAME", str(self.filename))
        filename_patch.start()
        self.addCleanup(filename_patch.stop)

        self.manager = TaskManager()

    def test_saves_all_task_fields_as_json(self):
        self.manager._tasks = [
            Task(1, "Write tests"),
            Task(2, "Review changes", completed=True),
        ]

        self.manager.save_tasks()

        with self.filename.open("r", encoding="utf-8") as file:
            saved_tasks = json.load(file)

        self.assertEqual(
            saved_tasks,
            [
                {"id": 1, "description": "Write tests", "completed": False},
                {"id": 2, "description": "Review changes", "completed": True},
            ],
        )

    def test_saving_empty_task_list_writes_empty_json_array(self):
        self.filename.write_text("stale content", encoding="utf-8")
        self.manager._tasks = []

        self.manager.save_tasks()

        with self.filename.open("r", encoding="utf-8") as file:
            saved_tasks = json.load(file)

        self.assertEqual(saved_tasks, [])

    def test_saving_tasks_overwrites_existing_file(self):
        self.filename.write_text('[{"old": "data"}]', encoding="utf-8")
        self.manager._tasks = [Task(3, "Current task", completed=True)]

        self.manager.save_tasks()

        with self.filename.open("r", encoding="utf-8") as file:
            saved_tasks = json.load(file)

        self.assertEqual(
            saved_tasks,
            [{"id": 3, "description": "Current task", "completed": True}],
        )

    def test_add_task_assigns_id_and_persists_task(self):
        output = io.StringIO()

        with redirect_stdout(output):
            self.manager.add_task("Prepare presentation")

        self.assertEqual(len(self.manager._tasks), 1)
        self.assertEqual(self.manager._tasks[0].id, 1)
        self.assertEqual(self.manager._tasks[0].description, "Prepare presentation")
        self.assertFalse(self.manager._tasks[0].completed)
        self.assertIn("Task added:", output.getvalue())

        reloaded_manager = TaskManager()
        self.assertEqual(reloaded_manager._tasks[0].description, "Prepare presentation")
        self.assertEqual(reloaded_manager._next_id, 2)

    def test_list_tasks_prints_all_tasks(self):
        self.manager._tasks = [
            Task(1, "Prepare presentation"),
            Task(2, "Send invitation", completed=True),
        ]
        output = io.StringIO()

        with redirect_stdout(output):
            self.manager.list_tasks()

        self.assertEqual(
            output.getvalue(),
            "[ ] #1: Prepare presentation\n[Completed] #2: Send invitation\n",
        )

    def test_list_tasks_prints_message_when_empty(self):
        output = io.StringIO()

        with redirect_stdout(output):
            self.manager.list_tasks()

        self.assertEqual(output.getvalue(), "No tasks available.\n")

    def test_complete_task_marks_task_and_persists_change(self):
        self.manager._tasks = [Task(1, "Prepare presentation")]
        output = io.StringIO()

        with redirect_stdout(output):
            self.manager.complete_task(1)

        self.assertTrue(self.manager._tasks[0].completed)
        self.assertIn("Task completed:", output.getvalue())

        with self.filename.open("r", encoding="utf-8") as file:
            saved_tasks = json.load(file)
        self.assertTrue(saved_tasks[0]["completed"])

    def test_complete_task_reports_unknown_id(self):
        self.manager._tasks = [Task(1, "Prepare presentation")]
        output = io.StringIO()

        with redirect_stdout(output):
            self.manager.complete_task(99)

        self.assertFalse(self.manager._tasks[0].completed)
        self.assertEqual(output.getvalue(), "Task not found 99.\n")
        self.assertFalse(self.filename.exists())

    def test_delete_task_removes_task_and_persists_change(self):
        self.manager._tasks = [Task(1, "Prepare presentation"), Task(2, "Send invitation")]
        output = io.StringIO()

        with redirect_stdout(output):
            self.manager.delete_task(1)

        self.assertEqual([task.id for task in self.manager._tasks], [2])
        self.assertIn("Task removed:", output.getvalue())

        with self.filename.open("r", encoding="utf-8") as file:
            saved_tasks = json.load(file)
        self.assertEqual(saved_tasks, [{"id": 2, "description": "Send invitation", "completed": False}])

    def test_delete_task_reports_unknown_id(self):
        self.manager._tasks = [Task(1, "Prepare presentation")]
        output = io.StringIO()

        with redirect_stdout(output):
            self.manager.delete_task(99)

        self.assertEqual([task.id for task in self.manager._tasks], [1])
        self.assertEqual(output.getvalue(), "Task not found 99.\n")
        self.assertFalse(self.filename.exists())

    def test_load_task_restores_tasks_and_next_id(self):
        self.filename.write_text(
            '[{"id": 4, "description": "Prepare presentation", "completed": true}]',
            encoding="utf-8",
        )

        self.manager.load_task()

        self.assertEqual(len(self.manager._tasks), 1)
        self.assertEqual(self.manager._tasks[0].id, 4)
        self.assertEqual(self.manager._tasks[0].description, "Prepare presentation")
        self.assertTrue(self.manager._tasks[0].completed)
        self.assertEqual(self.manager._next_id, 5)


if __name__ == "__main__":
    unittest.main()