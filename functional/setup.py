from distutils.core import setup, Extension

setup( name = 'pi', version = '0.1', 
       description = 'This is simple method for approximating Pi',
       ext_modules = Extension('pi', sources = ['pimodule.c']))
                               
