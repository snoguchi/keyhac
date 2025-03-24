from keyhac import *

def configure(keymap):
    if 1:
        keymap.editor = "notepad.exe"

    def is_emacs_target(window):
        return not window.getProcessName() in ("bash.exe",
                                               "putty.exe")

    if 1:
        keymap_global = keymap.defineWindowKeymap()
        keymap_global[ "C-O" ] = "A-(25)" # toggle IME

    if 1:
        keymap_emacs = keymap.defineWindowKeymap( check_func=is_emacs_target )
        keymap_emacs[ "C-P" ] = "Up"
        keymap_emacs[ "C-N" ] = "Down"
        keymap_emacs[ "C-F" ] = "Right"
        keymap_emacs[ "C-B" ] = "Left"
        keymap_emacs[ "C-A" ] = "Home"
        keymap_emacs[ "C-E" ] = "End"
        # keymap_emacs[ "C-V" ] = "PageDown"
        keymap_emacs[ "C-S" ] = "C-F"
        keymap_emacs[ "C-W" ] = "U-Shift","C-X"
        keymap_emacs[ "C-Y" ] = "U-Shift","C-V"
        keymap_emacs[ "C-Slash"] = "C-Z"
        keymap_emacs[ "C-Space" ] = "D-Shift"
        keymap_emacs[ "C-D" ] = "U-Shift","Delete"
        keymap_emacs[ "C-H" ] = "U-Shift","Back"
        keymap_emacs[ "C-K" ] = "U-Shift","S-End","C-X"
        keymap_emacs[ "C-G" ] = "U-Shift","ESC"
