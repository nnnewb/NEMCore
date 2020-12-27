import os
import sys

gui_dir = os.path.join(os.path.dirname(__file__), '..', 'gui')

if getattr(sys, 'frozen', None):
    gui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui')
