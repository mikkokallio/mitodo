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

if __name__ == "__main__":
    task = Task('Create todo app', 1)
    print(task)