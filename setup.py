# build with: python setup.py build

import sys
from cx_Freeze import setup, Executable
from meta_info import __description__, __version__

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
elif sys.platform == 'linux':
    base = None

executables = [
    Executable('talenttalent.py', base=base)
]

build_exe_options = {"packages": ["PySide6"], "excludes": []}

setup(
    name = "TalentTalent",
    version = __version__,
    description = __description__,
    options = {"build_exe": build_exe_options},
    executables = executables
)
