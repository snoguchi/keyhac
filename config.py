# -*- mode: python; coding: utf-8-dos -*-

##
## Windows の操作を emacs のキーバインドで行うための設定（keyhac版）
##

# このスクリプトは、keyhac で動作します。
#   https://sites.google.com/site/craftware/keyhac
# スクリプトですので、使いやすいようにカスタマイズしてご利用ください。
#
# この内容は、utf-8-dos の coding-system で config.py の名前でセーブして
# 利用してください。また、このスクリプトの最後の方にキーボードマクロの
# キーバインドの設定があります。英語キーボードと日本語キーボードで設定の
# 内容を変える必要があるので、利用しているキーボードに応じて if文 の設定を
# 変更してください。（現在の設定は、日本語キーボードとなっています。）
#
# emacs の挙動と明らかに違う動きの部分は以下のとおりです。
# ・左の Ctrlキー と Altキー のみが、emacs用のキーとして認識される。
# ・ESC の二回押下で、ESC を入力できる。
# ・C-o と C-\ で IME の切り替えが行われる。
# ・C-c、C-z は、Windows の「コピー」、「取り消し」が機能するようにしている。
# ・C-x C-y で、クリップボード履歴を表示する。（C-n で選択を移動し、Enter で確定する）
# ・C-x o は、一つ前にフォーカスがあったウインドウに移動する。
#   NTEmacs から Windowsアプリケーションソフトを起動した際に戻るのに便利。
# ・C-k を連続して実行しても、クリップボードへの削除文字列の蓄積は行われない。
#   C-u による行数指定をすると、削除行を一括してクリップボードに入れることができる。
# ・C-l は、アプリケーションソフト個別対応とする。recenter 関数で個別に指定すること。
#   この設定では、Sakura Editor のみ対応している。
# ・キーボードマクロは emacs の挙動と異なり、IME の変換キーも含めた入力したキー
#   そのものを記録します。このため、キーボードマクロ記録時や再生時、IMEの状態に
#   留意した利用が必要となります。
# ・Excel の場合、^Enter に F2（セル編集モード移行）を割り当てている。（オプション）
# ・Emacs の場合、IME 切り替え用のキーを C-\ に置き換える方法を提供している。（オプション）

from time   import sleep
from keyhac import *

def configure(keymap):

    # emacs のキーバインドに"したくない"アプリケーションソフトを指定する（False を返す）
    # keyhac のメニューから「内部ログ」を ON にすると processname や classname を確認することができます
    def is_emacs_target(window):
        if window.getProcessName() in ("cmd.exe",            # cmd
                                       "mintty.exe",         # mintty
                                       "emacs.exe",          # Emacs
                                       "emacs-w32.exe",      # Emacs
                                       "runemacs.exe",       # Emacs
                                       "gvim.exe",           # GVim
                                       # "eclipse.exe",        # Eclipse
                                       "xyzzy.exe",          # xyzzy
                                       "VirtualBox.exe",     # VirtualBox
                                       "XWin.exe",           # Cygwin/X
                                       "Xming.exe",          # Xming
                                       "putty.exe",          # PuTTY
                                       "ttermpro.exe",       # TeraTerm
                                       "MobaXterm.exe",      # MobaXterm
                                       "TurboVNC.exe",       # TurboVNC
                                       "vncviewer.exe"):     # UltraVNC
            return False
        return True

    # input method の切り替え"のみをしたい"アプリケーションソフトを指定する（True を返す）
    # 指定できるアプリケーションソフトは、is_emacs_target で除外指定したものからのみとする
    def is_im_target(window):
        if window.getProcessName() in ("cmd.exe",            # cmd
                                       "mintty.exe",         # mintty
                                       "gvim.exe",           # GVim
                                       # "eclipse.exe",        # Eclipse
                                       "xyzzy.exe",          # xyzzy
                                       "putty.exe",          # PuTTY
                                       "ttermpro.exe",       # TeraTerm
                                       "MobaXterm.exe"):     # MobaXterm
            return True
        return False

    keymap_emacs = keymap.defineWindowKeymap(check_func=is_emacs_target)
    keymap_im    = keymap.defineWindowKeymap(check_func=is_im_target)

    # mark がセットされると True になる
    keymap_emacs.is_marked = False

    # 検索が開始されると True になる
    keymap_emacs.is_searching = False

    # キーボードマクロの play 中 は True になる
    keymap_emacs.is_playing_kmacro = False

    # universal-argument コマンドが実行されると True になる
    keymap_emacs.is_universal_argument = False

    # digit-argument コマンドが実行されると True になる
    keymap_emacs.is_digit_argument = False

    # コマンドのリピート回数を設定する
    keymap_emacs.repeat_counter = 1

    ########################################################################
    # IMEの切替え
    ########################################################################

    def toggle_input_method():
        keymap.command_InputKey("A-(25)")()
        if 1:
            if keymap_emacs.is_playing_kmacro == False:
                sleep(0.05) # delay

                # IME の状態を取得する
                if keymap.wnd.getImeStatus():
                    message = "[あ]"
                else:
                    message = "[_A]"

                # IMEの状態をバルーンヘルプで表示する
                keymap.popBalloon("ime_status", message, 500)

    ########################################################################
    # ファイル操作
    ########################################################################

    def find_file():
        keymap.command_InputKey("C-o")()

    def save_buffer():
        keymap.command_InputKey("C-s")()

    def write_file():
        keymap.command_InputKey("A-f", "A-a")()

    ########################################################################
    # カーソル移動
    ########################################################################

    def backward_char():
        keymap.command_InputKey("Left")()

    def forward_char():
        keymap.command_InputKey("Right")()

    def backward_word():
        keymap.command_InputKey("C-Left")()

    def forward_word():
        keymap.command_InputKey("C-Right")()

    def previous_line():
        keymap.command_InputKey("Up")()

    def next_line():
        keymap.command_InputKey("Down")()

    def move_beginning_of_line():
        keymap.command_InputKey("Home")()

    def move_end_of_line():
        keymap.command_InputKey("End")()
        if keymap.getWindow().getClassName() == "_WwG": # Microsoft Word
            if keymap_emacs.is_marked:
                keymap.command_InputKey("Left")()

    def beginning_of_buffer():
        keymap.command_InputKey("C-Home")()

    def end_of_buffer():
        keymap.command_InputKey("C-End")()

    def scroll_up():
        keymap.command_InputKey("PageUp")()

    def scroll_down():
        keymap.command_InputKey("PageDown")()

    def recenter():
        if keymap.getWindow().getClassName() == "EditorClient": # Sakura Editor
            keymap.command_InputKey("C-h")()

    ########################################################################
    # カット / コピー / 削除 / アンドゥ
    ########################################################################

    def delete_backward_char():
        keymap.command_InputKey("Back")()

    def delete_char():
        keymap.command_InputKey("Delete")()

    def backward_kill_word():
        keymap.command_InputKey("C-S-Left", "C-x")()

    def kill_word():
        keymap.command_InputKey("C-S-Right", "C-x")()

    def kill_line():
        keymap_emacs.is_marked = True
        mark(move_end_of_line)()
        keymap.command_InputKey("C-c", "Delete")()

    def kill_line2():
        if keymap_emacs.repeat_counter == 1:
            kill_line()
        else:
            keymap_emacs.is_marked = True
            if keymap.getWindow().getClassName() == "_WwG": # Microsoft Word
                for i in range(keymap_emacs.repeat_counter):
                    mark(next_line)()
                mark(move_beginning_of_line)()
            else:
                for i in range(keymap_emacs.repeat_counter - 1):
                    mark(next_line)()
                mark(move_end_of_line)()
                mark(forward_char)()
            kill_region()

    def kill_region():
        keymap.command_InputKey("C-x")()

    def kill_ring_save():
        keymap.command_InputKey("C-c")()
        if not keymap.getWindow().getClassName().startswith("EXCEL"): # Microsoft Excel 以外
            # 選択されているリージョンのハイライトを解除するために Esc を発行しているが、
            # アプリケーションソフトによっては効果なし
            keymap.command_InputKey("Esc")()

    def windows_copy():
        keymap.command_InputKey("C-c")()

    def yank():
        keymap.command_InputKey("C-v")()

    def undo():
        keymap.command_InputKey("C-z")()

    def set_mark_command():
        if keymap_emacs.is_marked:
            keymap_emacs.is_marked = False
        else:
            keymap_emacs.is_marked = True

    def mark_whole_buffer():
        keymap.command_InputKey("C-End", "C-S-Home")()

    def mark_page():
        keymap.command_InputKey("C-End", "C-S-Home")()

    def open_line():
        keymap.command_InputKey("Enter", "Up", "End")()

    ########################################################################
    # バッファ / ウインドウ操作
    ########################################################################

    def kill_buffer():
        keymap.command_InputKey("C-F4")()

    def other_window():
        keymap.command_InputKey("D-Alt")()
        keymap.command_InputKey("Tab")()
        sleep(0.01) # delay
        keymap.command_InputKey("U-Alt")()

    ########################################################################
    # 文字列検索 / 置換
    ########################################################################

    def isearch_backward():
        if keymap_emacs.is_searching:
            keymap.command_InputKey("S-F3")()
        else:
            keymap.command_InputKey("C-f")()
            keymap_emacs.is_searching = True

    def isearch_forward():
        if keymap_emacs.is_searching:
            keymap.command_InputKey("F3")()
        else:
            keymap.command_InputKey("C-f")()
            keymap_emacs.is_searching = True

    ########################################################################
    # キーボードマクロ
    ########################################################################

    def kmacro_start_macro():
        keymap.command_RecordStart()

    def kmacro_end_macro():
        keymap.command_RecordStop()
        # キーボードマクロの終了キー C-x ) の C-x がマクロに記録されてしまうのを削除する
        # キーボードマクロの終了キーの前提を C-x ) としていることについては、とりえず了承ください
        if len(keymap.record_seq) >= 4:
            if (((keymap.record_seq[len(keymap.record_seq) - 1] == (162, True) and   # U-LCtrl
                  keymap.record_seq[len(keymap.record_seq) - 2] == ( 88, True)) or   # U-X
                 (keymap.record_seq[len(keymap.record_seq) - 1] == ( 88, True) and   # U-X
                  keymap.record_seq[len(keymap.record_seq) - 2] == (162, True))) and # U-LCtrl
                keymap.record_seq[len(keymap.record_seq) - 3] == (88, False)):       # D-X
                   keymap.record_seq.pop()
                   keymap.record_seq.pop()
                   keymap.record_seq.pop()
                   if keymap.record_seq[len(keymap.record_seq) - 1] == (162, False): # D-LCtrl
                       for i in range(len(keymap.record_seq) - 1, -1, -1):
                           if keymap.record_seq[i] == (162, False): # D-LCtrl
                               keymap.record_seq.pop()
                           else:
                               break
                   else:
                       # コントロール系の入力が連続して行われる場合があるための対処
                       keymap.record_seq.append((162, True)) # U-LCtrl

    def kmacro_end_and_call_macro():
        keymap_emacs.is_playing_kmacro = True
        keymap.command_RecordPlay()
        keymap_emacs.is_playing_kmacro = False

    ########################################################################
    # その他
    ########################################################################

    def newline():
        keymap.command_InputKey("Enter")()

    def newline_and_indent():
        keymap.command_InputKey("Enter", "Tab")()

    def indent_for_tab_command():
        keymap.command_InputKey("Tab")()

    def keybord_quit():
        if not keymap.getWindow().getClassName().startswith("EXCEL"): # Microsoft Excel 以外
            # 選択されているリージョンのハイライトを解除するために Esc を発行しているが、
            # アプリケーションソフトによっては効果なし
            keymap.command_InputKey("Esc")()
        keymap.command_RecordStop()

    def kill_emacs():
        keymap.command_InputKey("A-F4")()

    def universal_argument():
        if keymap_emacs.is_universal_argument == True:
            if keymap_emacs.is_digit_argument == True:
                keymap_emacs.is_universal_argument = False
            else:
                keymap_emacs.repeat_counter = keymap_emacs.repeat_counter * 4
        else:
            keymap_emacs.is_universal_argument = True
            keymap_emacs.repeat_counter = keymap_emacs.repeat_counter * 4

    def digit_argument(number):
        if keymap_emacs.is_digit_argument == True:
            keymap_emacs.repeat_counter = keymap_emacs.repeat_counter * 10 + number
        else:
            keymap_emacs.repeat_counter = number
            keymap_emacs.is_digit_argument = True

    def clipboard_list():
        keymap_emacs.is_marked = False
        keymap.command_ClipboardList()

    ########################################################################
    # 共通関数
    ########################################################################

    def self_insert_command(key):
        return keymap.command_InputKey(key)

    def digit(number):
        def _digit():
            if keymap_emacs.is_universal_argument == True:
                digit_argument(number)
            else:
                reset_counter(reset_mark(repeat(keymap.command_InputKey(str(number)))))()
        return _digit

    def digit2(number):
        def _digit2():
            keymap_emacs.is_universal_argument = True
            digit_argument(number)
        return _digit2

    def mark(func):
        def _mark():
            if keymap_emacs.is_marked:
                # D-Shift だと、M-< や M-> 押下時に、D-Shift が解除されてしまう。その対策。
                keymap.command_InputKey("D-LShift")()
                keymap.command_InputKey("D-RShift")()
            func()
            if keymap_emacs.is_marked:
                keymap.command_InputKey("U-LShift")()
                keymap.command_InputKey("U-RShift")()
        return _mark

    def reset_mark(func):
        def _reset_mark():
            func()
            keymap_emacs.is_marked = False
        return _reset_mark

    def reset_counter(func):
        def _reset_counter():
            func()
            keymap_emacs.is_universal_argument = False
            keymap_emacs.is_digit_argument = False
            keymap_emacs.repeat_counter = 1
        return _reset_counter

    def reset_search(func):
        def _reset_search():
            func()
            keymap_emacs.is_searching = False
        return _reset_search

    def repeat(func):
        def _repeat():
            repeat_counter = keymap_emacs.repeat_counter
            keymap_emacs.repeat_counter = 1
            for i in range(repeat_counter):
                func()
        return _repeat

    def repeat2(func):
        def _repeat2():
            if keymap_emacs.is_marked == True:
                keymap_emacs.repeat_counter = 1
            repeat(func)()
        return _repeat2

    ########################################################################
    # キーバインド
    ########################################################################

    # http://homepage3.nifty.com/ic/help/rmfunc/vkey.htm
    # http://www.azaelia.net/factory/vk.html

    # マルチストロークキーの設定
    keymap_emacs["Esc"]            = keymap.defineMultiStrokeKeymap("Esc")
    keymap_emacs["LC-OpenBracket"] = keymap.defineMultiStrokeKeymap("C-OpenBracket")
    # keymap_emacs["LC-x"]           = keymap.defineMultiStrokeKeymap("C-x")
    keymap_emacs["LC-q"]           = keymap.defineMultiStrokeKeymap("C-q")

    # 0-9キーの設定
    for key in range(10):
        keymap_emacs[        str(key)]           = digit(key)
        keymap_emacs["LC-" + str(key)]           = digit2(key)
        keymap_emacs["LA-" + str(key)]           = digit2(key)
        keymap_emacs["Esc"][ str(key)]           = digit2(key)
        keymap_emacs["LC-OpenBracket"][str(key)] = digit2(key)
        keymap_emacs["S-" + str(key)] = reset_counter(reset_mark(repeat(self_insert_command("S-" + str(key)))))

    # SPACE, A-Zキーの設定
    for vkey in [32] + list(range(65, 90 + 1)):
        keymap_emacs[  "(" + str(vkey) + ")"] = reset_counter(reset_mark(repeat(self_insert_command(  "(" + str(vkey) + ")"))))
        keymap_emacs["S-(" + str(vkey) + ")"] = reset_counter(reset_mark(repeat(self_insert_command("S-(" + str(vkey) + ")"))))

    # 10key の特殊文字キーの設定
    for vkey in [106, 107, 109, 110, 111]:
        keymap_emacs[  "(" + str(vkey) + ")"] = reset_counter(reset_mark(repeat(self_insert_command(  "(" + str(vkey) + ")"))))

    # 特殊文字キーの設定
    for vkey in list(range(186, 192 + 1)) + list(range(219, 222 + 1)) + [226]:
        keymap_emacs[  "(" + str(vkey) + ")"] = reset_counter(reset_mark(repeat(self_insert_command(  "(" + str(vkey) + ")"))))
        keymap_emacs["S-(" + str(vkey) + ")"] = reset_counter(reset_mark(repeat(self_insert_command("S-(" + str(vkey) + ")"))))

    # quoted-insertキーの設定
    for vkey in range(1, 255):
        keymap_emacs["LC-q"][  "("   + str(vkey) + ")"] = reset_search(reset_counter(reset_mark(repeat(self_insert_command(  "("   + str(vkey) + ")")))))
        keymap_emacs["LC-q"]["S-("   + str(vkey) + ")"] = reset_search(reset_counter(reset_mark(repeat(self_insert_command("S-("   + str(vkey) + ")")))))
        keymap_emacs["LC-q"]["C-("   + str(vkey) + ")"] = reset_search(reset_counter(reset_mark(repeat(self_insert_command("C-("   + str(vkey) + ")")))))
        keymap_emacs["LC-q"]["C-S-(" + str(vkey) + ")"] = reset_search(reset_counter(reset_mark(repeat(self_insert_command("C-S-(" + str(vkey) + ")")))))
        keymap_emacs["LC-q"]["A-("   + str(vkey) + ")"] = reset_search(reset_counter(reset_mark(repeat(self_insert_command("A-("   + str(vkey) + ")")))))
        keymap_emacs["LC-q"]["A-S-(" + str(vkey) + ")"] = reset_search(reset_counter(reset_mark(repeat(self_insert_command("A-S-(" + str(vkey) + ")")))))

    # Esc の二回押しを Esc とする設定
    keymap_emacs["Esc"]["Esc"]                      = reset_counter(self_insert_command("Esc"))
    keymap_emacs["LC-OpenBracket"]["C-OpenBracket"] = reset_counter(self_insert_command("Esc"))

    # universal-argumentキーの設定
    keymap_emacs["LC-u"] = universal_argument

    # 「IMEの切替え」のキー設定
    keymap_emacs["(243)"]   = toggle_input_method
    keymap_emacs["(244)"]   = toggle_input_method
    keymap_emacs["LA-(25)"] = toggle_input_method
    keymap_emacs["LC-Yen"]  = toggle_input_method
    keymap_emacs["LC-o"]    = toggle_input_method # or open_line

    keymap_im["(243)"]   = toggle_input_method
    keymap_im["LA-(25)"] = toggle_input_method
    keymap_im["LC-Yen"]  = toggle_input_method
    keymap_im["LC-o"]    = toggle_input_method

    # 「ファイル操作」のキー設定
    # keymap_emacs["LC-x"]["C-f"] = reset_search(reset_counter(reset_mark(find_file)))
    # keymap_emacs["LC-x"]["C-s"] = reset_search(reset_counter(reset_mark(save_buffer)))
    # keymap_emacs["LC-x"]["C-w"] = reset_search(reset_counter(reset_mark(write_file)))

    # 「カーソル移動」のキー設定
    keymap_emacs["LC-b"] = reset_search(reset_counter(repeat(mark(backward_char))))
    keymap_emacs["LC-f"] = reset_search(reset_counter(repeat(mark(forward_char))))

    keymap_emacs["LA-b"]                = reset_search(reset_counter(repeat(mark(backward_word))))
    keymap_emacs["Esc"]["b"]            = reset_search(reset_counter(repeat(mark(backward_word))))
    keymap_emacs["LC-OpenBracket"]["b"] = reset_search(reset_counter(repeat(mark(backward_word))))

    keymap_emacs["LA-f"]                = reset_search(reset_counter(repeat(mark(forward_word))))
    keymap_emacs["Esc"]["f"]            = reset_search(reset_counter(repeat(mark(forward_word))))
    keymap_emacs["LC-OpenBracket"]["f"] = reset_search(reset_counter(repeat(mark(forward_word))))

    keymap_emacs["LC-p"] = reset_search(reset_counter(repeat(mark(previous_line))))
    keymap_emacs["LC-n"] = reset_search(reset_counter(repeat(mark(next_line))))
    keymap_emacs["LC-a"] = reset_search(reset_counter(mark(move_beginning_of_line)))
    keymap_emacs["LC-e"] = reset_search(reset_counter(mark(move_end_of_line)))

    keymap_emacs["LA-S-Comma"]                 = reset_search(reset_counter(mark(beginning_of_buffer)))
    keymap_emacs["Esc"]["S-Comma"]             = reset_search(reset_counter(mark(beginning_of_buffer)))
    keymap_emacs["LC-OpenBracket"]["S-Comma"]  = reset_search(reset_counter(mark(beginning_of_buffer)))

    keymap_emacs["LA-S-Period"]                = reset_search(reset_counter(mark(end_of_buffer)))
    keymap_emacs["Esc"]["S-Period"]            = reset_search(reset_counter(mark(end_of_buffer)))
    keymap_emacs["LC-OpenBracket"]["S-Period"] = reset_search(reset_counter(mark(end_of_buffer)))

    keymap_emacs["LA-v"]                = reset_search(reset_counter(mark(scroll_up)))
    keymap_emacs["Esc"]["v"]            = reset_search(reset_counter(mark(scroll_up)))
    keymap_emacs["LC-OpenBracket"]["v"] = reset_search(reset_counter(mark(scroll_up)))

    # keymap_emacs["LC-v"] = reset_search(reset_counter(mark(scroll_down)))
    keymap_emacs["LC-l"] = reset_search(reset_counter(recenter))

    # 「カット / コピー / 削除 / アンドゥ」のキー設定
    keymap_emacs["LC-h"]    = reset_search(reset_counter(reset_mark(repeat2(delete_backward_char))))
    keymap_emacs["LC-d"]    = reset_search(reset_counter(reset_mark(repeat2(delete_char))))
    keymap_emacs["LC-Back"] = reset_search(reset_counter(reset_mark(repeat(backward_kill_word))))

    keymap_emacs["LA-Delete"]                = reset_search(reset_counter(reset_mark(repeat(backward_kill_word))))
    keymap_emacs["Esc"]["Delete"]            = reset_search(reset_counter(reset_mark(repeat(backward_kill_word))))
    keymap_emacs["LC-OpenBracket"]["Delete"] = reset_search(reset_counter(reset_mark(repeat(backward_kill_word))))

    keymap_emacs["LC-Delete"] = reset_search(reset_counter(reset_mark(repeat(kill_word))))

    keymap_emacs["LA-d"]                = reset_search(reset_counter(reset_mark(repeat(kill_word))))
    keymap_emacs["Esc"]["d"]            = reset_search(reset_counter(reset_mark(repeat(kill_word))))
    keymap_emacs["LC-OpenBracket"]["d"] = reset_search(reset_counter(reset_mark(repeat(kill_word))))

    keymap_emacs["LC-k"] = reset_search(reset_counter(reset_mark(kill_line2)))
    keymap_emacs["LC-w"] = reset_search(reset_counter(reset_mark(kill_region)))

    keymap_emacs["LA-w"]                = reset_search(reset_counter(reset_mark(kill_ring_save)))
    keymap_emacs["Esc"]["w"]            = reset_search(reset_counter(reset_mark(kill_ring_save)))
    keymap_emacs["LC-OpenBracket"]["w"] = reset_search(reset_counter(reset_mark(kill_ring_save)))

    keymap_emacs["LC-c"]          = reset_search(reset_counter(reset_mark(windows_copy)))
    keymap_emacs["LC-y"]          = reset_search(reset_counter(reset_mark(yank)))
    keymap_emacs["LC-z"]          = reset_search(reset_counter(reset_mark(undo)))
    keymap_emacs["LC-Slash"]      = reset_search(reset_counter(reset_mark(undo)))
    keymap_emacs["LC-Underscore"] = reset_search(reset_counter(reset_mark(undo)))
    # keymap_emacs["LC-x"]["u"]     = reset_search(reset_counter(reset_mark(undo)))
    keymap_emacs["LC-Space"]      = reset_search(reset_counter(set_mark_command))

    # 英語キーボードを利用する場合、LC-2 の設定（数引数の指定で利用）が LC-Atmark の設定で上書きされるのでコメント化
    # keymap_emacs["LC-Atmark"]     = reset_search(reset_counter(set_mark_command))

    # keymap_emacs["LC-x"]["h"]     = reset_search(reset_counter(reset_mark(mark_whole_buffer)))
    # keymap_emacs["LC-x"]["C-p"]   = reset_search(reset_counter(reset_mark(mark_page)))

    # 「バッファ / ウインドウ操作」のキー設定
    # keymap_emacs["LC-x"]["k"] = reset_search(reset_counter(reset_mark(kill_buffer)))
    # keymap_emacs["LC-x"]["o"] = reset_search(reset_counter(reset_mark(other_window)))

    # 「文字列検索 / 置換」のキー設定
    keymap_emacs["LC-r"] = reset_counter(reset_mark(isearch_backward))
    keymap_emacs["LC-s"] = reset_counter(reset_mark(isearch_forward))

    # 「キーボードマクロ」のキー設定
    # if 1:
        # 日本語キーボードの場合
        # keymap_emacs["LC-x"]["S-8"] = kmacro_start_macro
        # keymap_emacs["LC-x"]["S-9"] = kmacro_end_macro
    # else:
        # 英語キーボードの場合
        # keymap_emacs["LC-x"]["S-9"] = kmacro_start_macro
        # keymap_emacs["LC-x"]["S-0"] = kmacro_end_macro

    # keymap_emacs["LC-x"]["e"] = reset_search(reset_counter(repeat(kmacro_end_and_call_macro)))

    # 「その他」のキー設定
    keymap_emacs["LC-m"]        = reset_counter(reset_mark(repeat(newline)))
    keymap_emacs["Enter"]       = reset_counter(reset_mark(repeat(newline)))
    keymap_emacs["LC-j"]        = reset_counter(reset_mark(newline_and_indent))
    keymap_emacs["LC-i"]        = reset_counter(reset_mark(repeat(indent_for_tab_command)))
    keymap_emacs["Tab"]         = reset_counter(reset_mark(repeat(indent_for_tab_command)))
    keymap_emacs["LC-g"]        = reset_search(reset_counter(reset_mark(keybord_quit)))
    # keymap_emacs["LC-x"]["C-c"] = reset_search(reset_counter(reset_mark(kill_emacs)))
    # keymap_emacs["LC-x"]["C-y"] = reset_search(reset_counter(reset_mark(clipboard_list)))

    # Excel のキー設定（オプション）
    if 1:
        keymap_excel = keymap.defineWindowKeymap(class_name='EXCEL*')
        # C-Enter 押下で、「セル編集モード」に移行する
        keymap_excel["LC-Enter"] = reset_search(reset_counter(reset_mark(self_insert_command("F2"))))

    # Emacs のキー設定（オプション）
    if 0:
        keymap_real_emacs = keymap.defineWindowKeymap(class_name='Emacs')
        # IME 切り替え用のキーを C-\ に置き換える
        keymap_real_emacs["(28)"]    = self_insert_command("C-Yen") # 「変換」キー
        keymap_real_emacs["(29)"]    = self_insert_command("C-Yen") # 「無変換」キー
        keymap_real_emacs["(242)"]   = self_insert_command("C-Yen") # 「カタカナ・ひらがな」キー
        keymap_real_emacs["(243)"]   = self_insert_command("C-Yen") # 「半角／全角」キー
        keymap_real_emacs["(244)"]   = self_insert_command("C-Yen") # 「半角／全角」キー
        keymap_real_emacs["LA-(25)"] = self_insert_command("C-Yen") # 「Alt-`」 キー
