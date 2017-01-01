# -*- coding: utf-8 -*-
'''file magic functions'''

DEFAULT_MAGIC = {"DOC Header": ["d0cf11e0a1b11ae1"],
                 "DOC Footer": ["576f72642e446f63756d656e742e"],
                 "XLS Header": ["d0cf11e0a1b11ae1"],
                 "XLS Footer": ["feffffff000000000000000057006f0072006b0062006f006f006b00"],
                 "PPT Header": ["d0cf11e0a1b11ae1"],
                 "PPT Footer": ["a0461df0"],
                 "ZIP Header": ["504b030414"],
                 "ZIP Footer": ["504b050600"],
                 "ZIPLock Footer": ["504b030414000100630000000000"],
                 "JPG Header": ["ffd8ffe000104a464946000101"],
                 "GIF Header": ["474946383961"],
                 "GIF Footer": ["2100003b00"],
                 "PDF Header": ["25504446"],
                 "PDF-Header": ["2623323035"],
                 "PDF Footer": ["2525454f46"],
                 "Torrent Header": ["616e6e6f756e6365"],
                 "GZ Header": ["1f8b0808"],
                 "TAR Header": ["1f8b0800"],
                 "TAR.GZ Header": ["1f9d9070"],
                 "EPUB Header": ["504b03040a000200"],
                 "PNG Header": ["89504e470d0a1a0a"],
                 "8192 Header": ["6d51514e42"],
                 "4096 Header": ["6d51494e4246672f"],
                 "2048 Header": ["952e3e2e584b7a"],
                 "Secret Header": ["526172211a0700"],
                 "RAR Header": ["6d51454e424667"],
                 "UTF8 header": ["efedface"],
                 "OGG Header": ["4f676753"],
                 "WAV Header": ["42494646", "57415645"],
                 "AVI Header": ["42494646", "41564920"],
                 "MIDI Header": ["4d546864"],
                 "7z Header": ["377abcaf271c"],
                 "7z Footer": ["0000001706"],
                 "DMG Header": ["7801730d626260"],
                 "Wikileaks": ["57696b696c65616b73"],
                 "Julian Assange": ["4a756c69616e20417373616e6765"],
                 "Mendax": ["4d656e646178"]}


def check_magic(hexcode, magic=DEFAULT_MAGIC):
    '''Returns a string listing magic bytes found in the given hexcode and compared against the magic dictionary of keys to lists of values.

    This is the hex header search function.  It searches the line of hex for any of these known header hex values.
    '''
    return ' '.join('{} Found'.format(key)
                   for key, values in magic.iteritems()
                   if all(v.lower() in hexcode for v in values))
