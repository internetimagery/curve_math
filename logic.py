
def get_attr():
    """ Get selected attributes, Return an iterable"""
    objs = cmds.ls(sl=True) or []
    if objs:
        attrs = cmds.channelBox("mainChannelBox", sma=True, q=True) or []
        if attrs:
            return set("{}.{}".format(a, cmds.attributeQuery(b, n=a, ln=True)) for a in objs for b in attrs if cmds.attributeQuery(b, n=a, ex=True))
    return []

def apply_operation(in_frame, out_frame, attr1, attr2, out_attr, func):
    err = cmds.undoInfo(openChunk=True)
    try:
        for frame in range(in_frame, out_frame):
            cmds.setAttr(out_attr, func(
                cmds.getAttr(attr1),
                cmds.getAttr(attr2)))
    except Exception as err:
        pass
    finally:
        cmds.select(clear=True)
        cmds.undoInfo(closeChunk=True)
        if err:
            cmds.undo()
