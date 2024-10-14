import pytest
import sys
import os
# sys.path.insert(0, 'C/Users/ivan/Desktop/skypro_python/kurs_3_github/kurs_3/src')
# from project import *
from ..src.project import open_file

def test_open_file():
    assert open_file("operations.json")

test_open_file()    