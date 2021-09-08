# mitodo
A simple text-based todo app.

To run the app from a Docker container, use: `docker run -it -v ${PWD}/todo.json:/app/todo.json mitodo`

This binds a local `todo.json` file to the container so you can persist any changes. Make sure you have that file in the folder when running from a container!

Run app locally: `python3 mitodo.py`

Run tests: `python3 test.py`
