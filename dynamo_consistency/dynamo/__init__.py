"""
This sub-module includes all of the interaction with dynamo
"""


from .. import opts


# This is the old version of connecting to dynamo
if opts.EXTERNAL:
    from .v1 import inventory
    from .v1 import registry
    from .v1 import siteinfo

# The new version is designed to run as a script on the dynamo server
else:
    from .v2 import inventory
    from .v2 import registry
    from .v2 import siteinfo
