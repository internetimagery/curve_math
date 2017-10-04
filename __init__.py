# Display a nice gui!
import maya.cmds as cmds
import logic

class Main(object):
    def __init__(s):
        s.win = cmds.window("Curve_Math")
        cmds.columnLayout(adj=True)
        s.input1 = cmds.textFieldButtonGrp(l="1: ", bl="From CB", bc=lambda: s.select_CB(s.input1))

        s.input2 = cmds.textFieldButtonGrp(l="2: ", bl="From CB", bc=lambda: s.select_CB(s.input2))
        s.equ = cmds.button(l="=")
        s.output = cmds.textFieldButtonGrp(l="2: ", bl="From CB", bc=lambda: s.select_CB(s.output))
        cmds.showWindow()
    def select_CB(s, gui):
        for attr in logic.get_attr():
            return cmds.textFieldButtonGrp(gui, e=True, tx=attr)

if __name__ == '__main__':
    Main()
