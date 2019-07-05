# from keats import Keats
# from os.path import abspath, dirname, join
# import re
# from glob import glob
# from termcolor import cprint
#
#
# here = abspath(dirname(__file__))
# keats = Keats(join(here, '..'))
#
#
# def files_to_lines(files):
#     for path in files:
#         with open(path, 'r') as f:
#             lines = f.readlines()
#         for linenum, line in enumerate(lines):
#             yield path, linenum, line
#
#
# def str_find_entry(entry):
#     return "{p}:{n}:{pos} - found '{pattern}'".format(
#         p=entry['file'],
#         n=entry['line'],
#         pos=entry['start'],
#         pattern=entry['pattern']
#     )
#
#
# def find(files, patterns, verbose=False):
#     if isinstance(patterns, str):
#         patterns = [patterns]
#     found = []
#
#     for path in files:
#         with open(path, 'r') as f:
#             lines = f.readlines()
#         for linenum, line in enumerate(lines):
#             for patternstr in patterns:
#                 pattern = re.compile(patternstr)
#                 for m in pattern.finditer(line):
#                     entry = {
#                         'file': path,
#                         'pattern': str(patternstr),
#                         'line': linenum,
#                         'match': m,
#                         'start': m.start(),
#                         'end': m.end()
#                     }
#                     found.append(entry)
#
#     if verbose:
#         for e in found:
#             cprint(str_find_entry(e), 'blue')
#     return found
#
#
# def find_and_replace(files, replacements):
#     info = []
#     for path in files:
#         with open(path, 'rU') as f:
#             text = f.read()
#         with open(path, 'w') as f:
#             for p, r in replacements.items():
#                 text, num = re.subn(p, r, text)
#                 if num:
#                     info.append("{} | replaced {} with {} {} times".format(path, p, r, num))
#     print(info)
#             # f.write(text)
#
#
# all_python_files = list(glob(join(keats.pkg.directory, "**", "*.py"), recursive=True))
#
#
# def test_find():
#
#     print(find(all_python_files, ["import"], verbose=True))
