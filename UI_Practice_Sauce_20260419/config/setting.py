import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG = os.path.join(BASE_DIR, 'config', 'base.ini')
TEST_YAML = os.path.join(BASE_DIR, 'testyaml')
TEST_DATA = os.path.join(BASE_DIR, 'testdata')
REPORT = os.path.join(BASE_DIR, 'report')
LOG = os.path.join(BASE_DIR, 'log')