# Display a nice gui!
import maya.cmds as cmds
import logic
import operator

operations = {
    "+": operator.add,
    "-": operator.sub,
    "x": operator.mul,
    "/": operator.truediv
    }

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
        for attr in logic.get_attr():
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
        logic.apply_operation(start, end, input1, input2, output, op)


if __name__ == '__main__':
    Main()
