# coding: utf-8

VERSION = (0, 7, 7)
CODENAME = "keeping track"
BUILD_DT = (2021, 2, 14)

S_VERSION = ".".join(map(str, VERSION))
S_BUILD_DT = "{0:04d}-{1:02d}-{2:02d}".format(*BUILD_DT)

__version__ = S_VERSION
__build_dt__ = S_BUILD_DT

# I'm all ears
