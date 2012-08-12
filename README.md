# python-snss -- Parse the Google Chrome "Current Session" file #

Google Chrome's "Current Session" file is used to restore window
arrangements and tabs when the browser is restarted.

The files are stored in a proprietary binary format identified by the
magic number "SNSS" and primarily documents in Chrome source
tree. `python-snss` is a python package that implements a simplistic
parser for extracting some information from them.

## Installation ##

    python setup.py install
    
## Usage ##

    import snss

    snss_path = "/Path/To/Library/Application Support/Google/Chrome/Default/Current Session"
    snss_file = snss.SNSSFile(open(snss_path))

    print snss_file[0]
