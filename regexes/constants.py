"""
Constants that list all the regexes.
Here we use a REGEX dictionnary to be able to dynamically load the
regexes based on the name of the group currently parsed.
"""
ALT_BINARIES_TV = [
       '\"(?P<name>.*\.(rar|r\\d{1,2}))\".*\((?P<parts>\\d{1,3}\\/\\d{1,3})\)',
       '(?P<name>.*\.rar).*\((?P<parts>\\d{1,3}\\/\\d{1,3})\)',]

REGEXES = {
        'alt.binaries.tv': ALT_BINARIES_TV}
