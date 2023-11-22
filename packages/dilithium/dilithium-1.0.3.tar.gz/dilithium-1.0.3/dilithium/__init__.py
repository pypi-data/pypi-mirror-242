#!/usr/bin/env python3
# coding: utf-8
 
"""
    This module is the eshard python package for dilithium for the PQC module validation
    The source comes from https://github.com/GiacomoPope/dilithium-py with modification to have
    seed obtained from xoshiro128++ and a short seed on a 32-bit word.
"""

name = "dilithium"

from dilithium.dilithium import Dilithium
from dilithium.dilithium import DEFAULT_PARAMETERS



    