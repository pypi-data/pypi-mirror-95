import os
import sys
import ast
import tokenize
import itertools
import io
import json

try:
    from pip._vendor import pkg_resources  # type: ignore
except ImportError:
    import pkg_resources  # type: ignore


if sys.version_info < (3,):
    filter = itertools.ifilter
    map = itertools.imap


class Dependencies(list):
    index_url = None

    def params(self):
        prefix = ['--index-url', self.index_url] if self.index_url else []
        return prefix + self


class DepsReader:
    """
    Given a Python script, read the dependencies it declares.
    Does not execute the script, so expects __requires__ to be
    assigned a static list of strings.
    """

    def __init__(self, script):
        self.script = script

    @classmethod
    def try_read(cls, script_path):
        results = (subclass._try_read(script_path) for subclass in cls.__subclasses__())
        return next(filter(None, results), Dependencies())

    @classmethod
    def _try_read(cls, script_path):
        """
        Attempt to load the dependencies from the script,
        but return an empty list if unsuccessful.
        """
        try:
            reader = cls.load(script_path)
            return reader.read()
        except Exception:
            pass

    @classmethod
    def search(cls, params):
        """
        Given a (possibly-empty) series of parameters to a
        Python interpreter, return any dependencies discovered
        in a script indicated in the parameters. Only honor the
        first file found.
        """
        files = filter(os.path.isfile, params)
        return cls.try_read(next(files, None)).params()

    def read(self):
        """
        >>> DepsReader("__requires__=['foo']").read()
        ['foo']
        """
        reqs_raw = self._read('__requires__')
        strings = map(str, pkg_resources.parse_requirements(reqs_raw))
        deps = Dependencies(strings)
        try:
            deps.index_url = self._read('__index_url__')
        except Exception:
            pass
        return deps

    def _read(self, var_name):
        mod = ast.parse(self.script)
        (node,) = (
            node
            for node in mod.body
            if isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == var_name
        )
        return ast.literal_eval(node.value)


class SourceDepsReader(DepsReader):
    @classmethod
    def load(cls, script_path):
        with io.open(script_path) as stream:
            return cls(stream.read())


class NotebookDepsReader(DepsReader):
    @classmethod
    def load(cls, script_path):
        doc = json.load(open(script_path))
        lines = (
            line
            for cell in doc['cells']
            for line in cell['source'] + ['\n']
            if cell['cell_type'] == 'code' and not line.startswith('%')
        )
        return cls(''.join(lines))


def run(cmdline):
    """
    Execute the script as if it had been invoked naturally.
    """
    namespace = dict()
    filename = cmdline[0]
    namespace['__file__'] = filename
    namespace['__name__'] = '__main__'
    sys.argv[:] = cmdline

    open_ = getattr(tokenize, 'open', open)
    script = open_(filename).read()
    norm_script = script.replace('\\r\\n', '\\n')
    code = compile(norm_script, filename, 'exec')
    exec(code, namespace)
