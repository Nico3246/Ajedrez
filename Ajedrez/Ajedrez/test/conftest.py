# test/conftest.py
import sys
import os

# Calcula la ruta absoluta de ../src con respecto a este archivo
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "src"))
sys.path.insert(0, src_path)
