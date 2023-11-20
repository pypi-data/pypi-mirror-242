from pathlib import Path
import sys


class InputHandler:

    name = 'input'
    text: str = ''

    def __init__(self, file=None, stdin=True):
        """Handlers take the value of the command line option"""
        if file:
            self.text = Path(file).read_text()
        elif stdin and (not sys.stdin.isatty()):
            self.text = sys.stdin.read()

    def __str__(self):
        return self.text

    @classmethod
    def fake(cls, value):
        """Return a fake InputHandler with forced values, for testing"""
        handler = cls(stdin=False)
        handler.text = value
        return handler
