import unittest
from mitodo import *


class TestTask(unittest.TestCase):

    def test_add_task(self):
        """Test create and complete task"""
        task = Task('Create test task', 1)
        self.assertEqual(str(task), '[ ]  1: Create test task')
        task.set_done()
        self.assertEqual(str(task), '[X]  1: Create test task')


if __name__ == "__main__":
    unittest.main()
