import os, sys
import re
import runpy
from contextlib import contextmanager

@contextmanager
def pushd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)

@contextmanager
def change_argv(argv):
    old_argv = sys.argv
    sys.argv = argv
    try:
        yield
    finally:
        sys.argv = old_argv

@contextmanager
def on_syspath(dirpath):
    old_path = sys.path
    sys.path = [dirpath] + sys.path
    try:
        yield
    finally:
        sys.path = old_path


def file_cmp(file1, file2):
    with open(file1, 'r') as f1:
        with open(file2, 'r') as f2:
            a1 = f1.readlines()
            a2 = f2.readlines()
            assert len(a1) == len(a2)
            first = True
            for left, right in zip(a1, a2):
                if first:
                    left  = re.sub('[0-9]{4}\\\\-[0-9]{2}\\\\-[0-9]{2}', '!!DATE!!', left)
                    right = re.sub('[0-9]{4}\\\\-[0-9]{2}\\\\-[0-9]{2}', '!!DATE!!', right)
                    first = False
                assert left == right


class TestAllExapmles(object):
    def test_old_example(self):
        with on_syspath(os.getcwd()):
            with pushd('examples/old_format'):
                with change_argv(['setup.py', 'build_manpage']):
                    try:
                        os.remove('example.1')
                    except OSError:
                        pass
                    runpy.run_path('setup.py')
                    file_cmp('example.1', 'expected-output.1')


    def test_copr(self):
        with on_syspath(os.getcwd()):
            with pushd('examples/copr'):
                name = 'copr-cli.1'
                prefix = '/usr'
                idir = os.path.join(os.getcwd(), 'i')
                with change_argv(['setup.py', 'install', '--root', idir, '--prefix', prefix]):
                    try:
                        os.remove(name)
                    except OSError:
                        pass
                    runpy.run_path('setup.py')
                    import subprocess
                    subprocess.call('find i', shell=True)
                    file_cmp('i/usr/share/man/man1/' + name, 'expected-output.1')
                    file_cmp(name, 'expected-output.1')

    def test_distgen(self):
        with on_syspath(os.getcwd()):
            with pushd('examples/raw-description'):
                name = 'man/dg.1'
                prefix = '/usr'
                idir = os.path.join(os.getcwd(), 'i')
                with change_argv(['setup.py', 'install', '--root', idir, '--prefix', prefix]):
                    try:
                        os.remove(name)
                    except OSError:
                        pass
                    runpy.run_path('setup.py')
                    import subprocess
                    subprocess.call('find i', shell=True)
                    file_cmp('i/usr/share/man/man1/' + os.path.basename(name), 'expected-output.1')
                    file_cmp(name, 'expected-output.1')
