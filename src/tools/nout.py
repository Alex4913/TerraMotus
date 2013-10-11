import contextlib
import sys

# A dummy stream for data where written data goes nowhere
class DummyFile(object):
    def write(self, x): pass

# A function to be used with a 'with' statement to block
# printing anything, even errors
@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = DummyFile()
    yield
    sys.stdout = save_stdout
