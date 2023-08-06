"""
Utility routines
================

Several utility functions are used throughout sisl.

Range routines
==============

   array_arange - fast creation of sub-aranges
   strmap
   strseq
   lstranges
   erange
   list2str
   fileindex

Miscellaneous routines
======================

   str_spec
   direction - abc/012 -> 012
   angle - radian to degree
   iter_shape
   math_eval

"""
from .cmd import *
from .misc import *
from .ranges import *
from . import mathematics as math

__all__ = [s for s in dir() if not s.startswith('_')]
