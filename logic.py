import collections

def get_attr():
    """ Get selected attributes, Return an iterable"""
    objs = cmds.ls(sl=True) or []
    if objs:
        attrs = cmds.channelBox("mainChannelBox", sma=True, q=True) or []
        if attrs:
            return set((a, cmds.attributeQuery(b, n=a, ln=True)) for a in objs for b in attrs if cmds.attributeQuery(b, n=a, ex=True))
    return []

def sample_at_range(in_frame, out_frame, attributes):
    """ Sample attributes at each frame """
    keys = collections.defaultdict(list)
    curr_time = cmds.currentTime(q=True)
    for frame in range(in_frame, out_frame):
        for attr in attributes:
            keys[attr].append((frame, cmds.getAttr(attr)))
    cmds.currentTime(curr_time)
    return keys
