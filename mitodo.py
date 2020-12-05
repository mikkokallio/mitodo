import itertools


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


if __name__ == "__main__":
    tasklist = TaskList()
    tasklist.add_task('Add tasklist to todo app')
    tasklist.add_task('Add second task')
    n = tasklist.add_task('Yoyoyo')
    print(tasklist)
    print(n.get_id())
