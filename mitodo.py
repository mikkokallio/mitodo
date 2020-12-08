import json
import itertools
import os
import sys
import config


class Task:
    """An individual task item to put on a to-do list"""

    def __init__(self, text: str, id: int, done=False):
        """Create task"""
        self.__text = text
        self.__done = done
        self.__id = id

    def __str__(self):
        """Return task with id and checkbox"""
        check = 'X' if self.__done else ' '
        return f'[{check}] {self.__id:>2}: {self.__text}'

    def is_done(self) -> bool:
        """Check if task is completed"""
        return self.__done

    def set_done(self):
        """Set done to True"""
        self.__done = True

    def get_id(self) -> int:
        """Get task id"""
        return self.__id

    def get_text(self) -> str:
        """Get task text"""
        return self.__text


class TaskList:
    """A to-do list"""

    def __init__(self, min_length=2):
        """Create list of tasks with optional min length for task names"""
        self.__tasks = []
        self.__min_length = min_length
        self.id_generator = (i for i in itertools.count(1))

    def __str__(self):
        """Print task list"""
        return str([str(task) for task in (self.list_tasks())])

    def __len__(self):
        """Return total number of tasks"""
        return len(self.__tasks)

    def list_tasks(self, order_abc=False, filter_done=False) -> list:
        """List tasks ordered by id (default) or alphabetically, and optional filtering of completed tasks"""
        tasks = self.__tasks[:]
        if filter_done:
            tasks = [task for task in self.__tasks if not task.is_done()]
        if order_abc:
            tasks = sorted(self.__tasks, key=lambda task: task.get_text())
        return tasks

    def add_task(self, text: str, done=False) -> Task:
        """Add a new task to the task list, with an incremental id, and return task"""
        if len(text) >= self.__min_length:
            task = Task(text, str(next(self.id_generator)), done)
            self.__tasks.append(task)
            return task
        else:
            raise ValueError(
                f'text must be at least {self.__min_length} characters')

    def complete_task(self, id: int) -> Task:
        """Search task by id; if found, mark as completed and return the task"""
        task = next(
            (task for task in self.__tasks if task.get_id() == id), None)
        if task is not None:
            if task.is_done():
                raise ValueError('task already completed')
            else:
                task.set_done()
                return task
        else:
            raise ValueError('id not found')

    def remove_task(self, id: int) -> Task:
        """Search task by id; if found remove and return the task"""
        task = next(
            (task for task in self.__tasks if task.get_id() == id), None)
        if task is not None:
            self.__tasks = [
                task for task in self.__tasks if task.get_id() != id]
            return task
        else:
            raise ValueError('id not found')

    def remove_completed_tasks(self) -> int:
        """Remove all tasks that have been marked as completed"""
        n = len(self.__tasks)
        self.__tasks = [task for task in self.__tasks if not task.is_done()]
        return n - len(self.__tasks)


class FileHandler():
    """Component for loading and saving task list items as .yaml"""

    def __init__(self, todo_file):
        """Create file handler from filename"""
        self.__todo_file = todo_file

    def load(self):
        """Read tasks from file"""
        if os.path.exists(self.__todo_file):
            with open(self.__todo_file, 'r') as f:
                return json.loads(f.read())
        else:
            return []

    def save(self, tasks: list):
        """Write tasks to file"""
        with open(self.__todo_file, 'w') as f:
            f.write(json.dumps(
                [{'text': task.get_text(), 'done': task.is_done()} for task in tasks]))


class App:
    """Application for managing a to-do list"""

    def __init__(self):
        """Create todo app"""
        self.__tasklist = TaskList(config.MIN_LENGTH)
        self.__todo_file = FileHandler(config.FILENAME)

        for task in self.__todo_file.load():
            self.__tasklist.add_task(task['text'], task['done'])

    def list_all_tasks(self):
        """Display both active and completed tasks"""
        print('\n### All tasks\n')
        tasks = self.__tasklist.list_tasks()
        if len(tasks) > 0:
            [print(task) for task in tasks]
        else:
            print('No tasks!')

    def list_active_tasks(self):
        """Display only active tasks"""
        print('\n### Active tasks\n')
        tasks = self.__tasklist.list_tasks(filter_done=True)
        if len(tasks) > 0:
            [print(task) for task in tasks]
        else:
            print('No active tasks!')

    def add_task(self):
        """Input task name, and add that as task"""
        text = input('description: ')
        try:
            task = self.__tasklist.add_task(text)
            print(f'added task: {task.get_id()}: {task.get_text()}')
        except ValueError as ex:
            print(f'invalid task: {ex}')

    def complete_task(self):
        """Input task id and mark that task as completed"""
        id = input('id to complete: ')
        try:
            task = self.__tasklist.complete_task(id)
            print(f'completed task: {task.get_id()}: {task.get_text()}')
        except ValueError as ex:
            print(f'invalid task: {ex}')

    def remove_task(self):
        """Input task id and remove that task"""
        id = input('id to remove: ')
        try:
            task = self.__tasklist.remove_task(id)
            print(f'removed task: {task.get_id()}: {task.get_text()}')
        except ValueError as ex:
            print(f'invalid task: {ex}')

    def remove_completed_tasks(self):
        """Remove all completed tasks and display how many were removed"""
        n = self.__tasklist.remove_completed_tasks()
        print(f'removed {n} tasks')

    def show_options(self):
        """Display all commands for using the todo list"""
        print("\n### Options\n")
        [print(f'{k:>2}: {App.options[k]["text"]}') for k in App.options]

    def save_and_quit(self):
        """Save current tasks and exit app"""
        tasks = self.__tasklist.list_tasks()
        self.__todo_file.save(tasks)
        print(f'saved {len(tasks)} tasks')
        sys.exit()

    options = {
        '0': {'text': 'save and exit', 'function': save_and_quit},
        '1': {'text': 'list all tasks', 'function': list_all_tasks},
        '2': {'text': 'list active tasks', 'function': list_active_tasks},
        '3': {'text': 'add a task', 'function': add_task},
        '4': {'text': 'complete a task', 'function': complete_task},
        '5': {'text': 'remove a task', 'function': remove_task},
        '6': {'text': 'remove all completed tasks', 'function': remove_completed_tasks},
    }

    def run(self):
        """Main input loop of app"""
        self.list_all_tasks()
        self.show_options()
        while True:
            option = input("\nselect: ")
            if option in App.options:
                App.options[option]['function'](self)
            else:
                self.show_options()


if __name__ == "__main__":
    app = App()
    app.run()
