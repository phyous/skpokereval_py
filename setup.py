#!/usr/bin/env python3
# encoding: utf-8

from distutils.core import setup, Extension

module1 = Extension('handEvaluatorCPP', sources=['src/Main.cpp'])

setup(name='SKPokerEvalPywrap',
      version='1.0',
      description='Python wrapper for SKPokerEval',
      ext_modules=[module1])