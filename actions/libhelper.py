"""
This module is used to solve the relative import problem
"""
import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
from models import user
