import os
import inspect
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from typing import Literal, get_args

ServerChannel = Literal[
    "connect",
    "send-message",
    "stop-generating",
]
SERVER_CHANNELS = set(get_args(ServerChannel))

ClientChannel = Literal[
    "function-display-config",
    "finish-generating",
    "update-message",
    "set-messages",
    "error",
]
CLIENT_CHANNELS = set(get_args(ClientChannel))


package_dir = os.path.dirname(__file__)
build_path = os.path.join(package_dir, '..', 'build')

app = Flask(__name__, static_folder=build_path)
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    async_mode="eventlet",
    async_handlers=True,
)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    """
    Runs when the user visits the website. Responds by sending the frontend code.
    """
    print("INDEX HIT")
    assert app.static_folder is not None
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


def socket_on(channel: ServerChannel):
    """
    A decorator for registering a handler for events emitted from frontend.

    NOTE: Assumes the frontend will always send an object, whose keys match the
    names of the parameters of your handler function.

    Serves two purposes:
        1. Enforce that the channel name is valid, in the list defined above.
        2. Automatically unpack the arguments from the socketio event.
    """
    assert channel in SERVER_CHANNELS, (
        f"Unknown channel. Please add, '{channel}', to the 'ServerChannel' type."
    )

    def decorator(func):
        param_names = set(inspect.signature(func).parameters.keys())

        @socketio.on(channel)
        def wrapper(arguments: dict | None = None):
            if arguments is None:
                return func()

            arg_names = set(arguments.keys())

            assert arg_names == param_names, (
                f"Handler for channel, '{channel}', received arguments which don't match the "
                f"handler's parameters. Expected: {list(param_names)}. Received {list(arg_names)}."
            )
            return func(**arguments)

        return wrapper

    return decorator


def socket_emit(channel: ClientChannel, *args, to: str | None = None, **kwargs):
    """
    Simple wrapper for emitting events to the frontend.

    Serves three purposes:
        1. Enforce that the channel name is valid, in the list defined above.
        2. Decide whether to use `emit` from flask-socketio, or `socketio.emit` based on whether
            the `to` parameter is provided. Flask-socketio determines the room automatically based
            on the current context. Only use `to` (and thus `socketio.emit`) when running in a separate
            green thread, such as when using `socketio.start_background_task`, since the context is lost.
        3. Call `socketio.sleep(0)` after emitting, to ensure the event is sent immediately, rather
            than when the current function finishes.
    """
    assert channel in CLIENT_CHANNELS, (
        f"Unknown channel. Please add, '{channel}', to the 'ClientChannel' type."
    )
    if to is None:
        emit(channel, *args, **kwargs)
    else:
        socketio.emit(channel, *args, to=to, **kwargs)

    socketio.sleep(0)


def run_app(**kwargs):
    socketio.run(app, **kwargs)
