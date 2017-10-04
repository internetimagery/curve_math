# Display a nice gui!
import maya.cmds as cmds
import operator

operations = {
    "+": operator.add,
    "-": operator.sub,
    "x": operator.mul,
    "/": operator.truediv
    }

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

class Main(object):
    def __init__(s):
        s.win = cmds.window("Curve_Math")
        cmds.columnLayout(adj=True)
        s.input1 = cmds.textFieldButtonGrp(l="1: ", bl="From CB", bc=lambda: s.select_CB(s.input1))
        s.op = cmds.optionMenu()
        for op in operations:
            cmds.menuItem(l=op)
        s.input2 = cmds.textFieldButtonGrp(l="2: ", bl="From CB", bc=lambda: s.select_CB(s.input2))
        s.equ = cmds.button(l="=", c=s.calculate)
        s.output = cmds.textFieldButtonGrp(l="2: ", bl="From CB", bc=lambda: s.select_CB(s.output))
        cmds.showWindow()

    def select_CB(s, gui):
        for attr in get_attr():
            return cmds.textFieldButtonGrp(gui, e=True, tx=attr)

    def calculate(s, *_):
        # Collect inputs
        input1 = cmds.textFieldButtonGrp(s.input1, q=True, tx=True)
        input2 = cmds.textFieldButtonGrp(s.input2, q=True, tx=True)
        output = cmds.textFieldButtonGrp(s.output, q=True, tx=True)
        if not input1 or not input2 or not output:
            raise RuntimeError("Not all fields filled!")
        if len(set((input1, input2, output))) != 3:
            raise RuntimeError("All fields must be different!")

        # What are we doing?
        op = operations[cmds.optionMenu(s.op, q=True, v=True)]
        start = cmds.playbackOptions(q=True, min=True)
        end = cmds.playbackOptions(q=True, max=True)

        # Do it!
        apply_operation(start, end, input1, input2, output, op)


if __name__ == '__main__':
    Main()
