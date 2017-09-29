import collections

def get_attr():
    """ Get selected attributes, Return an iterable"""
    objs = cmds.ls(sl=True) or []
    if objs:
        attrs = cmds.channelBox("mainChannelBox", sma=True, q=True) or []
        if attrs:
            return set((a, cmds.attributeQuery(b, n=a, ln=True)) for a in objs for b in attrs if cmds.attributeQuery(b, n=a, ex=True))
    return []

def run_range(in_frame, out_frame):
    curr_time = cmds.currentTime(q=True)
    for frame in range(in_frame, out_frame):
        cmds.currentTime(frame)
        yield frame
    cmds.currentTime(curr_time)

def sample_at_range(in_frame, out_frame, attributes):
    """ Sample attributes at each frame """
    keys = collections.defaultdict(list)
    for frame in run_range(in_frame. out_frame):
        for attr in attributes:
            keys[attr].append((frame, cmds.getAttr(attr)))
    return keys

def apply_at_range(in_frame, out_frame, attributes):
    """ Apply keyframes at each frame """
    for frame in run_range(in_frame, out_frame):
        for attr in attributes:
            for key in attributes[attr]:
                cmds.setAttr(attr, key[1])

def apply_operation(attr1, attr2, func):
    """ apply operation to attributes """
    new_attr = collections.defaultdict(list)
    for at1, at2 in zip(attr1, attr2):
        for k1, k2 in zip(at1, at2):
            new_attr[at2].append(k2, func(k1[1], k2[1]))
    return new_attr
