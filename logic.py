
def get_attr():
    """ Get selected attributes, Return an iterable"""
    objs = cmds.ls(sl=True) or []
    if objs:
        attrs = cmds.channelBox("mainChannelBox", sma=True, q=True) or []
        if attrs:
            return set("{}.{}".format(a, cmds.attributeQuery(b, n=a, ln=True)) for a in objs for b in attrs if cmds.attributeQuery(b, n=a, ex=True))
    return []

def apply_operation(in_frame, out_frame, attr1, attr2, out_attr, func):
    autokey = cmds.autoKeyframe(state=True, q=True)
    err = cmds.undoInfo(openChunk=True)
    try:
        cmds.autoKeyframe(state=False)
        for frame in range(in_frame, out_frame):
            cmds.setKeyframe(
                out_attr,
                t=frame,
                v=func(
                    cmds.getAttr(attr1, t=frame),
                    cmds.getAttr(attr2, t=frame)))
    except Exception as err:
        pass
    finally:
        cmds.autoKeyframe(state=autokey)
        cmds.undoInfo(closeChunk=True)
        if err:
            cmds.undo()
