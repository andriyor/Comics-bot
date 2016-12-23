#!/usr/bin/env python3
from main import *


def test_xkcd_rand():
    assert xkcd_rand() != ''
