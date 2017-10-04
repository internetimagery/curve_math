import maya.cmds as cmds

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
        # Collect data:
        attr1_data = []
        attr2_data = []
        for frame in range(int(in_frame), int(out_frame) + 1):
            attr1_data.append(cmds.getAttr(attr1, t=frame))
            attr2_data.append(cmds.getAttr(attr2, t=frame))
        for i, (at1, at2) in enumerate(zip(attr1_data, attr2_data)):
            frame = i + in_frame
            ans = func(at1, at2)
            cmds.setKeyframe(out_attr, t=frame, v=ans)
    except Exception as err:
        raise
    finally:
        cmds.autoKeyframe(state=autokey)
        cmds.undoInfo(closeChunk=True)
        if err:
            cmds.undo()
