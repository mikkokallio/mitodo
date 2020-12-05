import unittest
from mitodo import Task, TaskList, App
from unittest.mock import patch, Mock


class TestTask(unittest.TestCase):

    def test_task(self):
        """Test creating and completing a task"""
        task = Task('Create test task', 1)
        self.assertEqual(str(task), '[ ]  1: Create test task')
        task.set_done()
        self.assertEqual(str(task), '[X]  1: Create test task')


class TestTaskList(unittest.TestCase):

    def test_add_tasks(self):
        """Test tasks get added"""
        tasklist = TaskList()
        tasklist.add_task('Create test task')
        self.assertEqual(len(tasklist), 1)
        tasklist.add_task('Hey look another task')
        self.assertEqual(len(tasklist), 2)

    def test_too_short(self):
        """Test too short task raises error"""
        with self.assertRaises(ValueError) as context:
            tasklist = TaskList(min_length=4)
            tasklist.add_task('Yo!')
        self.assertTrue(
            'text must be at least 4 characters' in str(context.exception))

    def test_remove_completed(self):
        """Test that only completed are removed"""
        tasklist = TaskList()
        t1 = tasklist.add_task('Foo').get_id()
        t2 = tasklist.add_task('Bar').get_id()
        t3 = tasklist.add_task('Foo2').get_id()
        t4 = tasklist.add_task('Bar2').get_id()
        t5 = tasklist.add_task('Foo3').get_id()
        tasklist.complete_task(t1)
        tasklist.complete_task(t2)
        tasklist.remove_completed_tasks()
        self.assertEqual(len(tasklist), 3)
        self.assertEqual(tasklist.list_tasks()[0].get_text(), 'Foo2')

    def test_remove_one(self):
        """Test that any task can be removed"""
        tasklist = TaskList()
        t1 = tasklist.add_task('Foo').get_id()
        t2 = tasklist.add_task('Bar').get_id()
        t3 = tasklist.add_task('Foo2').get_id()
        t4 = tasklist.add_task('Bar2').get_id()
        t5 = tasklist.add_task('Foo3').get_id()
        removed = tasklist.remove_task(t3)
        self.assertEqual(removed.get_text(), 'Foo2')
        self.assertEqual(len(tasklist), 4)


if __name__ == "__main__":
    unittest.main()
