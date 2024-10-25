from typing import Any, Callable, Iterable


class Callbacks:
    """
    Run an Iterable of callables and return their results as a list

    """

    def __init__(self, callbacks: list[Callable]):
        self.callbacks = (
            callbacks if isinstance(callbacks, Iterable) else set(callbacks)
        )

    def __call__(self, *args, **kwds):
        results = []
        for func in self.callbacks:
            results.append(func(*args, **kwds))
        return results


class MouseEvent:
    """
    A class that creates callbacks suitable for pynput Mouse Listener where
    the returned arguments ('x','dx',etc...) from pynput's controller are passed as keywords
    to the user's callbacks

    """

    @classmethod
    def on_move(cls, callbacks: Iterable[Callable]):
        callback = Callbacks(callbacks)

        def _on_move(x, y):
            keywords = {"x": x, "y": y}
            callback(**keywords)

        return _on_move

    @classmethod
    def on_scroll(cls, callbacks: Iterable[Callable]):
        callback = Callbacks(callbacks)

        def _on_scroll(x, y, dx, dy):
            keywords = {"x": x, "y": y, "dx": dx, "dy": dy}
            callback(**keywords)

        return _on_scroll

    @classmethod
    def on_click(cls, callbacks: Iterable[Callable]):
        callback = Callbacks(callbacks)

        def _on_click(x, y, button, pressed):
            keywords = {"x": x, "y": y, "button": button, "pressed": pressed}
            callback(**keywords)

        return _on_click


class KeyBoardEvent:
    """
    A class that creates callbacks suitable for pynput KeyBoard Listener where
    the returned arguments ('key')  from  pynput's controller are passed as keywords
    to the user's callbacks

    """

    @classmethod
    def on_press(cls, callbacks: list[Callable]):
        callback = Callbacks(callbacks)

        def _on_press(key):
            keywords = {"key": key}
            callback(**keywords)

        return _on_press

    @classmethod
    def on_release(cls, callbacks: list[Callable]):
        callback = Callbacks(callbacks)

        def _on_release(key):
            keywords = {"key": key}
            callback(**keywords)

        return _on_release
