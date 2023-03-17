import omni.kit.commands # New
import omni.usd # New
from typing import List # New
import omni.ui as ui



class MyExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[dli.example.command_library] MyExtension startup")

        self._window = ui.Window("My Window", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                ui.Label("Prim Scaler")

                def on_click():
                    prim_paths = get_selection()
                    print(prim_paths)
                    omni.kit.commands.execute('ScaleIncrement', prim_paths=prim_paths)

                ui.Button("Scale up!", clicked_fn=lambda: on_click())

    def on_shutdown(self):
        print("[dli.example.command_library] MyExtension shutdown")
        self._window.destroy()
        self._window = None

class ScaleIncrement(omni.kit.commands.Command):
    def __init__(self, prim_paths:  List[str]):
        self.prim_paths = prim_paths
        self.stage = omni.usd.get_context().get_stage()

    def do(self):
        self.set_scale()
    def undo(self):
        self.set_scale(True)

    def set_scale(self, undo: bool=False):
        for path in self.prim_paths:
            prim = self.stage.GetPrimAtPath(path)
            old_scale = prim.GetAttribute('xformOp:scale').Get()
            new_scale = tuple(x + 1 for x in old_scale)
            print(new_scale)
            if undo:
                new_scale = tuple(x - 1 for x in old_scale)
            prim.GetAttribute('xformOp:scale').Set(new_scale)


def get_selection() -> List[str]:
    """Get the list of currently selected prims"""
    return omni.usd.get_context().get_selection().get_selected_prim_paths()

