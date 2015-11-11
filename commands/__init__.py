import glob
import inspect, os

cur_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

names = [os.path.basename(name.split('.')[0]) for name in glob.glob(cur_dir + '/*')]

__all__ = list(set([command for command in names if command != '__init__']))
