""" Module used to perform Consistency Checks using XRootD.

:author: Daniel Abercrombie <dabercro@mit.edu>
"""

from .backend import logsetup

# This is the intended interface for users
__all__ = ['checkphedex', 'config', 'datatypes', 'getsitecontents', 'getinventorycontents']

__version__ = '1.2.3'
