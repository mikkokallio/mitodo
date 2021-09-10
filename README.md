# mitodo
A simple text-based todo app.

To run the app from a Docker container, do the following: 
1. Create a local file `todo.json` with content the `[]`.
2. Run `docker run -it -v ${PWD}/todo.json:/app/todo.json mitodo`

This binds the local `todo.json` file to the container so you can persist any todo items you add.

Run app locally: `python3 mitodo.py`

Run tests: `python3 test.py`
