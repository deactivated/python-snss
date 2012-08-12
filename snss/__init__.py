from cStringIO import StringIO
from construct import *

__all__ = ["SNSSFile"]


class Padded(Construct):
    def __init__(self, name, subcon, length):
        Construct.__init__(self, name)
        self.subcon = subcon
        self.length = length

    def _parse(self, stream, context):
        p = stream.read(self.length(context))
        return self.subcon._parse(StringIO(p), context)


def ChromeString(name, encoding=None, wide=False):
    """
    An encoded, aligned, Pascal-style string.
    """
    align = lambda l: l + ((4 - (l & 3)) & 3)

    if wide:
        width, encoding = 2, 'utf_16_le'
    else:
        width, encoding = 1, encoding

    def decode(c):
        s = c[name][:width * c['str-len']]
        if encoding:
            s = s.decode(encoding)
        return s

    return Embed(Struct(
        'str',
        ULInt32('str-len'),
        Reconfig(name, Field('val', lambda c: align(width * c['str-len']))),
        Reconfig(name, Value('val', decode))
    ))


"""
UpdateTabNavigationCommand payload

Defined in `base_session_service.cc`.
"""
snss_tab = Padded('tab', Struct(
    "tab",
    ULInt32("len"),
    SLInt32('id'),
    SLInt32('index'),

    ChromeString('url'),
    ChromeString('title', wide=True),
    ChromeString('content_state'),
    SLInt32('transition_type'),
    SLInt32('type_mask'),
    ChromeString('referrer'),
    SLInt32('referrer_policy'),
), lambda c: c.len - 1)


snss_bounds = Struct(
    "bounds3",
    SLInt32("window_id"),
    SLInt32("x"),
    SLInt32("y"),
    SLInt32("w"),
    SLInt32("h"),
    SLInt32("show_state")
)


snss_pair = Struct(
    "pair",
    SLInt32("id"),
    SLInt32("index")
)


snss_default = Padded('skip', Padding(0), lambda c: c.len - 1)


snss_command = Struct(
    "command",
    ULInt16("len"),
    ULInt8("cmd_id"),
    Switch(
        "content", lambda c: c.cmd_id, {
            0: snss_pair,       # SetTabWindow
            2: snss_pair,       # SetTabIndexInWindow
            5: snss_pair,       # TabNavigationPathPrunedFromBack
            6: snss_tab,        # UpdateTabNavigation
            7: snss_pair,       # SetSelectedNavigationIndex
            8: snss_pair,       # SetSelectedTabInIndex
            9: snss_pair,       # SetWindowType
            11: snss_pair,      # TabNavigationPathPrunedFromFront
            12: snss_default,   # SetPinnedState
            13: snss_default,   # SetExtensionAppID,
            14: snss_bounds,    # SetWindowBounds3
            15: snss_default,   # SetWindowAppName
            16: snss_default,   # TabClosed
            17: snss_default,   # WindowClosed
            18: snss_default,   # SetTabUserAgentOverride
            19: snss_default,   # CommandSessionStorageAssociated
        }, snss_default))


snss_root = Struct(
    "snss",
    String("SNSS", 4),
    SLInt32("version"),
    GreedyRange(snss_command),
)


class SNSSCommand(object):

    def __init__(self, container):
        self.container = container
        self.command_id = container.cmd_id

    def __getitem__(self, k):
        return self.container.content[k]

    def __repr__(self):
        return str(dict(self.container.content))

    __getattr__ = __getitem__


class SNSSFile(object):

    def __init__(self, input_stream):
        p = snss_root.parse_stream(input_stream)
        self.commands = [SNSSCommand(c) for c in p.command]

    def __iter__(self):
        return iter(self.commands)

    def __getitem__(self, k):
        return self.commands[k]
