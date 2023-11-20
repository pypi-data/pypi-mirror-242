# coding:cp932

"""Femtet ユーティリティ モジュール

       * Femtetを操作するためのモジュール

"""
from logging import getLogger
from pathlib import Path
from subprocess import Popen, SubprocessError, TimeoutExpired
import time
import winreg

import win32api
import win32con
from win32com.client import Dispatch
import win32process

from femtetutils.constant import FemtetClassName as femtetconst

logger = getLogger(__name__)


class Data:
    def __init__(self):
        # クラス変数をインスタンス別に利用したいのでコンストラクタで定義する
        self.general_process_id = 0  # 起動したFemtet以外のプロセスID
        self.femtet_process_id = 0   # 起動したFemtetのプロセスID
        self.femtet_hwnd = 0         # Femtetのウィンドウハンドル


def get_femtet_exe_path():
    """Femtet.exeのPathを取得

    レジストリ情報から、Femtet.exeのパスを取得する関数

    :return: Femtet.exeのパス
    例: 'C:\\Program Files\\Femtet_Ver2023_64bit\\Program\\Femtet.exe'
    :rtype: str
    """

    dllpath = _get_femtetmacro_dllpath()
    if dllpath is None:
        return None
    workpath = Path(dllpath)
    dirtpl = workpath.parts
    dirlist = list(dirtpl)

    if dirlist[-2] == r"Macro32":
        del dirlist[-2:]
    else:
        del dirlist[-1:]

    dirlist.append(r"Femtet.exe")

    dirlist[0] = dirlist[0].removesuffix('\\')
    execpath = '\\'.join(dirlist)
    logger.info(execpath)
    return execpath


def execute_femtet():
    """Femtet.exeの起動

    Femtet.exeを起動する

    :return: True:プロセスが起動中, False:プロセスが起動できなかった
    :rtype: bool
    """

    Data.femtet_process_id = 0

    femtetpath = get_femtet_exe_path()
    if femtetpath is None:
        return False

    try:
        # windowsOSではCreateProcessを呼び出している
        proc = Popen(femtetpath)
        while proc.poll() is not None:
            pass

        if proc.poll() is None:
            logger.info("Femtet process is executed. Process id = %s"
                        % proc.pid)
            Data.femtet_process_id = proc.pid
            return True
        else:
            logger.warning("Femtet process is terminated. returncode = %s"
                           % proc.returncode)
            return False
    except SubprocessError as e:
        logger.error("Catch SubprocessError.")
        logger.error(e)
        return False


def execute_process(command, timeout_second=None):
    """プロセスの起動

    指定したプロセスを起動する

    :param command: 起動したいプロセスのパス
    例: "notepad.exe"
    :type command: str
    :param timeout_second: 指定時間になるまで、プロセスの終了を待ちます
    :type timeout_second: int(秒)
    :return: True:プロセスが起動中, False:プロセスが起動できなかった
    :rtype: bool
    :return: [起動成功] プロセスからの終了コード
            [エラーの場合] -1:タイムアウト, -2:プロセス例外エラー発生
    :rtype: int
    """

    Data.general_process_id = 0
    try:
        proc = Popen(command)
        while proc.poll() is not None:
            pass

        if proc.poll() is None:
            logger.info("Process is executed. Process id = %s" % proc.pid)
            Data.general_process_id = proc.pid
        else:
            logger.warning("Process is terminated. returncode = %s"
                           % proc.returncode)
            return False

        if timeout_second is not None:
            logger.info("About %s seconds waiting for the process to finish."
                        % timeout_second)
            proc.wait(timeout_second)
            logger.info("Process is terminated. returncode = %s"
                        % proc.returncode)

        return True, proc.returncode
    except TimeoutExpired:
        logger.warning("Waiting for the process is timed out.")
        return False, -1
    except SubprocessError as e:
        logger.error("Catch SubprocessError.")
        logger.error(e)
        return False, -2


def get_last_executed_process_id():
    """直前に起動したプロセスのプロセスID取得

    execute_process()で起動したプロセスIDを取得する
    ※直前に起動したプロセスのみ取得可能

    :return: プロセスID(存在しない場合は0)
    :rtype: int
    """

    return Data.general_process_id


def get_last_executed_femtet_process_id():
    """直前に起動したFemtet.exeのプロセスID取得

    execute_femtet()で起動したプロセスIDを取得する
    ※直前に起動したプロセスのみ取得可能

    :return: プロセスID(存在しない場合は0)
    :rtype: int
    """

    return Data.femtet_process_id


def auto_execute_femtet(wait_second=60):
    """Femtet.exeの起動(未使用のFemtetが存在しない場合)

    Femtetが1つも起動していない、または既存のFemtetがすべて使用中の場合にFemtetを起動

    :param wait_second: 起動まで指定時間待機します
    :type wait_second: int(秒)
    :return: True:未使用のFemtetが起動中または新規でFemtetを起動した, False:Femtetが起動できなかった
    :rtype: bool
    """

    # execute_femtet関数内でも初期化しているが、
    # 関数を実行せずに処理を抜ける場合があるので、ここでも初期化しておく
    Data.femtet_process_id = 0
    Data.hWnd = 0

    wkFemtet = _dispatch_femtet()
    if wkFemtet.hWnd != 0:
        logger.info("Free Femtet is running. hWnd = %s" % wkFemtet.hWnd)
        return True

    # 新しいFemtetの起動
    if not execute_femtet():
        # 起動に失敗した。もしくは起動に時間がかかっている。
        logger.warning("New Femtet falied to start.")
        return False

    # この時点で自動起動はされている状態→FemtetのMainFrameが出ていない可能性が残っている
    # #6849 初期はHASPのダイアログを誤認してしまうため、本物のFemtetが起動するまで待つ。

    wait_time = wait_second * 2     # ループ処理で0.5秒待機しているので2を掛ける
    for i in range(wait_time):
        if wkFemtet.hWnd != 0:
            # hWndが有効ということはマクロ通信できるFemtetが見つかったということ。本関数の目的達成。
            # hWndプロパティはマクロ通信ができるFemtetのMainFrame以外にはセットされない仕様なので信頼100%
            Data.femtet_hwnd = wkFemtet.hWnd
            break
        time.sleep(0.5)

    if wkFemtet.hWnd != 0:
        logger.info("New Femtet is activated. hWnd = %s" % wkFemtet.hWnd)
        return True
    else:
        logger.warning("New Femtet is not activated.")
        return False


def get_process_id_from_hwnd(hwnd):
    """プロセスIDの取得

    指定されたウィンドウハンドルからプロセスIDを取得する

    :param hwnd: CFemtet.hWndプロパティをセット
    :type hwnd: int
    :return: プロセスID(取得できない場合は0を戻す)
    :rtype: int
    """
    thread, process = _get_thread_and_process_id_from_hwnd(hwnd)
    ret = process if thread != 0 else thread    # プロセスIDが取得できない場合はthreadが0
    logger.info("Process id:{0}".format(ret))
    return ret


def is_femtet_active():
    """Femtet.exeが起動中か

    Femtet.exeが現在起動しているかを判定する

    :return: True:起動中, False:起動していない
    :rtype: bool
    """
    wkFemtet = _dispatch_femtet()
    return (wkFemtet.hWnd != 0)


def close_femtet(hwnd, wait_second=60, isTerminate=True):
    """指定したウィンドウハンドルのFemtet.exeを閉じる

    Femtet.exeのウィンドウハンドルを引数に指定し、対象のFemtet.exeを閉じる。

    :param hwnd:Femtetのウィンドウハンドル
        補足:CFemtet.hWndでマクロに関連付けされたウィンドウハンドルを取得可能。
    :type hwnd: int
    :param wait_second: 閉じるまで待機を行う最大時間(秒)
    :type wait_second: int
    :param isTerminate: 閉じることが出来ない場合、強制終了するか
        True:強制終了する, False:強制終了しない
    :type isTerminate: bool

    :return: True:Femtetを閉じた, False:Femtetを時間内に閉じることができなかった
    :rtype: bool
    """

    _post_wm_close_message(hwnd)    # close

    wait_time = wait_second * 2     # ループ処理で0.5秒待機しているので2を掛ける
    for i in range(wait_time):
        thread, process = _get_thread_and_process_id_from_hwnd(hwnd)
        if thread == 0:
            Data.femtet_hwnd = 0
            Data.femtet_process_id = 0
            logger.info("Femtet is closed.")
            return True     # 閉じたことを確認
        time.sleep(0.5)

    # 指定時間後までループ処理をした場合は、最終チェック
    thread, process = _get_thread_and_process_id_from_hwnd(hwnd)
    if thread == 0:
        Data.femtet_hwnd = 0
        Data.femtet_process_id = 0
        return True
    else:
        if isTerminate:
            if _terminate_process(process):
                logger.warning("Femtet is terminated.")
                if _is_long_wait():
                    # 強制終了すると、ソフトウェアライセンス(LDK)の認証カウントが開放されないため、
                    # 次回Femtet起動まで3分程度待たないといけない。
                    logger.info("About 5 minutes waiting for license release.")
                    # 余裕を持たせるため5分待つ
                    time_left = 300
                    time_interval = 15
                    wait_count = time_left // time_interval
                    for i in range(wait_count):
                        time.sleep(time_interval)
                        time_left -= time_interval
                        logger.info("{0} seconds left.".format(time_left))
            else:
                logger.warning("Can not close Femtet.")
        else:
            logger.warning("Can not close Femtet.")
        return False


def close_process(process_id):
    """指定したプロセスIDのプロセスを閉じる(強制終了)

    プロセスIDを指定すると対象のプロセスを閉じる(強制終了)。

    :param process_id: プロセスID
    :type process_id: int
    :return: True:プロセスを強制終了した, False:強制終了処理中にエラーが発生した
    :rtype: bool
    """

    ret = _terminate_process(process_id)
    if ret:
        Data.general_process_id = 0
        logger.info(
            "Process is terminated. Process id = {0}".format(process_id))

    return ret


def _dispatch_femtet():
    return (Dispatch(femtetconst.CFemtet))


def _get_thread_and_process_id_from_hwnd(hwnd):
    return (win32process.GetWindowThreadProcessId(hwnd))


def _get_femtetmacro_dllpath():
    dllpath = _get_femtetmacro_dllpath_64()
    if dllpath is None:
        return _get_femtetmacro_dllpath_32()
    else:
        return dllpath


def _get_femtetmacro_dllpath_64():
    """FemtetMacro.dll(64bit用)のPathを取得

    レジストリのタイプライブラリ情報から、FemtetMacro.dllパスを取得する関数

    :return: FemtetMacro.dll(64bit用)のパス
    例: "C:\\Program Files\\Femtet_Ver2023_64bit\\Program\\FemtetMacro.dll"
    :rtype: str
    """

    # 値が取得できないとFileNotFoundErrorが発生するので
    # その場合はNoneを戻り値とする
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Classes\TypeLib\{7D1A10D9-22CE-4EDE-80FB-26A1E307D9FA}\1.0\0\win64",
            access=winreg.KEY_READ)
        value = winreg.QueryValue(key, "")
        return value
    except FileNotFoundError:
        return None


def _get_femtetmacro_dllpath_32():
    """FemtetMacro.dll(32bit用)のPathを取得

    レジストリのタイプライブラリ情報から、FemtetMacro.dllパスを取得する関数

    :return: FemtetMacro.dll(32bit用)のパス
    例: "C:\\Program Files\\Femtet_Ver2023_64bit\\Program\\Macro32\\FemtetMacro.dll"
    :rtype: str
    """

    # 値が取得できないとFileNotFoundErrorが発生するので
    # その場合はNoneを戻り値とする
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Classes\TypeLib\{7D1A10D9-22CE-4EDE-80FB-26A1E307D9FA}\1.0\0\win32",
            access=winreg.KEY_READ)
        value = winreg.QueryValue(key, "")
        return value
    except FileNotFoundError:
        return None


def _is_long_wait():
    dllpath = _get_femtetmacro_dllpath()
    if dllpath is None:
        return True
    return not ('_inside' in dllpath)


def _post_wm_close_message(hwnd):
    # プロジェクト未保存の場合は保存ダイアログが出るので不十分
    win32api.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


def _terminate_process(process_id):
    # https://learn.microsoft.com/ja-jp/windows/win32/debug/system-error-codes--1000-1299-
    ERROR_PROCESS_ABORTED = 0x042B
    try:
        handle = win32api.OpenProcess(1, False, process_id)
        win32api.TerminateProcess(handle, ERROR_PROCESS_ABORTED)
        # win32process.TerminateProcess(handle, ERROR_PROCESS_ABORTED)
        win32api.CloseHandle(handle)
        return True
    except Exception as e:
        logger.error("Terminate process Error.")
        logger.error(e)
        return False
