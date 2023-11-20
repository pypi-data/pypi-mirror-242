# SPDX-License-Identifier: GPL-2.0+
# Copyright (c) 2016 Google, Inc
# Written by Simon Glass <sjg@chromium.org>
#
# Entry-type module for Intel Memory Reference Code binary blob
#

from binman.etype.blob_ext import Entry_blob_ext

class Entry_intel_refcode(Entry_blob_ext):
    """Intel Reference Code file

    Properties / Entry arguments:
        - filename: Filename of file to read into entry

    This file contains code for setting up the platform on some Intel systems.
    This is executed by U-Boot when needed early during startup. A typical
    filename is 'refcode.bin'.

    See README.x86 for information about x86 binary blobs.
    """
    def __init__(self, section, etype, node):
        super().__init__(section, etype, node)

    def GetDefaultFilename(self):
        return 'refcode.bin'
