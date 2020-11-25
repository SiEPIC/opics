import opics as op
import pytest 

def test_c() -> None:
    assert op.globals.c == 299792458
