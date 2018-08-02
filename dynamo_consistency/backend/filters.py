


def pattern_filter(file_name, patterns):
    """
    This tells if the named file contains one of the ignored patterns.
    These are just checked to see that the file name contains one of the listed strings.
    There's no regex in here.

    :param str file_name: Name of the file to check for patterns in
    :param list patterns: List of "patterns" to check.
    :returns: True if one of the patterns is in the file_name
    :rtype: bool
    """

    # Skip over paths that include part of the list of ignored directories
    for pattern in ignore_list:
        if pattern in file_name:
            return True

    return False
