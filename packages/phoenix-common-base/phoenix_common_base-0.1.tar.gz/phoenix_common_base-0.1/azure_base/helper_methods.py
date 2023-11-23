import re
import pandas as pd
from datetime import datetime


def isclose(a: int, b: int, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


issn_pattern = re.compile(r'^\d{8}(\d|X)$|^\d{13}$')
