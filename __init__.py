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


if __name__ == '__main__':
    Main()
