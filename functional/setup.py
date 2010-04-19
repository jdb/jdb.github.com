from distutils.core import setup, Extension
mod = Extension('pi', sources = ['pimodule.c'])
setup (name = 'pi', version = '0.1', ext_modules = [mod],
       description = 'This is simple method for approximating Pi')
