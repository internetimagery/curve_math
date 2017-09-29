# Display a nice gui!
import maya.cmds as cmds

class Main(object):
    def __init__(s):

        s.gui_attr = {
            "input1": [],
            "input2": [],
            "output": [],
        }

        s.win = cmds.window("Curve_Math")
        cmds.columnLayout(adj=True)
        for attr in s.gui_attr:
            cmds.textFieldButtonGrp(
                label=attr,
                buttonLabel="Get selected"
            )
        cmds.text(l= "TODO: change this operation field!")
        cmds.intFieldGrp(nf=2)
        cmds.button(l="Calculate!")
        cmds.showWindow()

    def get_attr(s):
        """ Get selected attributes"""
        objs = cmds.ls(sl=True) or []
        if objs:
            attrs = cmds.channelBox("mainChannelBox", sma=True, q=True) or []
            if attrs:
                return set((a, cmds.attributeQuery(b, n=a, ln=True)) for a in objs for b in attrs if cmds.attributeQuery(b, n=a, ex=True))
        return []

if __name__ == '__main__':
    Main()
