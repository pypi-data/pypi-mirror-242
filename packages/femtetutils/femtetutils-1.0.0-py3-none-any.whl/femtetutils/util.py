# coding:cp932

"""Femtet ���[�e�B���e�B ���W���[��

       * Femtet�𑀍삷�邽�߂̃��W���[��

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
        # �N���X�ϐ����C���X�^���X�ʂɗ��p�������̂ŃR���X�g���N�^�Œ�`����
        self.general_process_id = 0  # �N������Femtet�ȊO�̃v���Z�XID
        self.femtet_process_id = 0   # �N������Femtet�̃v���Z�XID
        self.femtet_hwnd = 0         # Femtet�̃E�B���h�E�n���h��


def get_femtet_exe_path():
    """Femtet.exe��Path���擾

    ���W�X�g����񂩂�AFemtet.exe�̃p�X���擾����֐�

    :return: Femtet.exe�̃p�X
    ��: 'C:\\Program Files\\Femtet_Ver2023_64bit\\Program\\Femtet.exe'
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
    """Femtet.exe�̋N��

    Femtet.exe���N������

    :return: True:�v���Z�X���N����, False:�v���Z�X���N���ł��Ȃ�����
    :rtype: bool
    """

    Data.femtet_process_id = 0

    femtetpath = get_femtet_exe_path()
    if femtetpath is None:
        return False

    try:
        # windowsOS�ł�CreateProcess���Ăяo���Ă���
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
    """�v���Z�X�̋N��

    �w�肵���v���Z�X���N������

    :param command: �N���������v���Z�X�̃p�X
    ��: "notepad.exe"
    :type command: str
    :param timeout_second: �w�莞�ԂɂȂ�܂ŁA�v���Z�X�̏I����҂��܂�
    :type timeout_second: int(�b)
    :return: True:�v���Z�X���N����, False:�v���Z�X���N���ł��Ȃ�����
    :rtype: bool
    :return: [�N������] �v���Z�X����̏I���R�[�h
            [�G���[�̏ꍇ] -1:�^�C���A�E�g, -2:�v���Z�X��O�G���[����
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
    """���O�ɋN�������v���Z�X�̃v���Z�XID�擾

    execute_process()�ŋN�������v���Z�XID���擾����
    �����O�ɋN�������v���Z�X�̂ݎ擾�\

    :return: �v���Z�XID(���݂��Ȃ��ꍇ��0)
    :rtype: int
    """

    return Data.general_process_id


def get_last_executed_femtet_process_id():
    """���O�ɋN������Femtet.exe�̃v���Z�XID�擾

    execute_femtet()�ŋN�������v���Z�XID���擾����
    �����O�ɋN�������v���Z�X�̂ݎ擾�\

    :return: �v���Z�XID(���݂��Ȃ��ꍇ��0)
    :rtype: int
    """

    return Data.femtet_process_id


def auto_execute_femtet(wait_second=60):
    """Femtet.exe�̋N��(���g�p��Femtet�����݂��Ȃ��ꍇ)

    Femtet��1���N�����Ă��Ȃ��A�܂��͊�����Femtet�����ׂĎg�p���̏ꍇ��Femtet���N��

    :param wait_second: �N���܂Ŏw�莞�ԑҋ@���܂�
    :type wait_second: int(�b)
    :return: True:���g�p��Femtet���N�����܂��͐V�K��Femtet���N������, False:Femtet���N���ł��Ȃ�����
    :rtype: bool
    """

    # execute_femtet�֐����ł����������Ă��邪�A
    # �֐������s�����ɏ����𔲂���ꍇ������̂ŁA�����ł����������Ă���
    Data.femtet_process_id = 0
    Data.hWnd = 0

    wkFemtet = _dispatch_femtet()
    if wkFemtet.hWnd != 0:
        logger.info("Free Femtet is running. hWnd = %s" % wkFemtet.hWnd)
        return True

    # �V����Femtet�̋N��
    if not execute_femtet():
        # �N���Ɏ��s�����B�������͋N���Ɏ��Ԃ��������Ă���B
        logger.warning("New Femtet falied to start.")
        return False

    # ���̎��_�Ŏ����N���͂���Ă����ԁ�Femtet��MainFrame���o�Ă��Ȃ��\�����c���Ă���
    # #6849 ������HASP�̃_�C�A���O����F���Ă��܂����߁A�{����Femtet���N������܂ő҂B

    wait_time = wait_second * 2     # ���[�v������0.5�b�ҋ@���Ă���̂�2���|����
    for i in range(wait_time):
        if wkFemtet.hWnd != 0:
            # hWnd���L���Ƃ������Ƃ̓}�N���ʐM�ł���Femtet�����������Ƃ������ƁB�{�֐��̖ړI�B���B
            # hWnd�v���p�e�B�̓}�N���ʐM���ł���Femtet��MainFrame�ȊO�ɂ̓Z�b�g����Ȃ��d�l�Ȃ̂ŐM��100%
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
    """�v���Z�XID�̎擾

    �w�肳�ꂽ�E�B���h�E�n���h������v���Z�XID���擾����

    :param hwnd: CFemtet.hWnd�v���p�e�B���Z�b�g
    :type hwnd: int
    :return: �v���Z�XID(�擾�ł��Ȃ��ꍇ��0��߂�)
    :rtype: int
    """
    thread, process = _get_thread_and_process_id_from_hwnd(hwnd)
    ret = process if thread != 0 else thread    # �v���Z�XID���擾�ł��Ȃ��ꍇ��thread��0
    logger.info("Process id:{0}".format(ret))
    return ret


def is_femtet_active():
    """Femtet.exe���N������

    Femtet.exe�����݋N�����Ă��邩�𔻒肷��

    :return: True:�N����, False:�N�����Ă��Ȃ�
    :rtype: bool
    """
    wkFemtet = _dispatch_femtet()
    return (wkFemtet.hWnd != 0)


def close_femtet(hwnd, wait_second=60, isTerminate=True):
    """�w�肵���E�B���h�E�n���h����Femtet.exe�����

    Femtet.exe�̃E�B���h�E�n���h���������Ɏw�肵�A�Ώۂ�Femtet.exe�����B

    :param hwnd:Femtet�̃E�B���h�E�n���h��
        �⑫:CFemtet.hWnd�Ń}�N���Ɋ֘A�t�����ꂽ�E�B���h�E�n���h�����擾�\�B
    :type hwnd: int
    :param wait_second: ����܂őҋ@���s���ő厞��(�b)
    :type wait_second: int
    :param isTerminate: ���邱�Ƃ��o���Ȃ��ꍇ�A�����I�����邩
        True:�����I������, False:�����I�����Ȃ�
    :type isTerminate: bool

    :return: True:Femtet�����, False:Femtet�����ԓ��ɕ��邱�Ƃ��ł��Ȃ�����
    :rtype: bool
    """

    _post_wm_close_message(hwnd)    # close

    wait_time = wait_second * 2     # ���[�v������0.5�b�ҋ@���Ă���̂�2���|����
    for i in range(wait_time):
        thread, process = _get_thread_and_process_id_from_hwnd(hwnd)
        if thread == 0:
            Data.femtet_hwnd = 0
            Data.femtet_process_id = 0
            logger.info("Femtet is closed.")
            return True     # �������Ƃ��m�F
        time.sleep(0.5)

    # �w�莞�Ԍ�܂Ń��[�v�����������ꍇ�́A�ŏI�`�F�b�N
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
                    # �����I������ƁA�\�t�g�E�F�A���C�Z���X(LDK)�̔F�؃J�E���g���J������Ȃ����߁A
                    # ����Femtet�N���܂�3�����x�҂��Ȃ��Ƃ����Ȃ��B
                    logger.info("About 5 minutes waiting for license release.")
                    # �]�T���������邽��5���҂�
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
    """�w�肵���v���Z�XID�̃v���Z�X�����(�����I��)

    �v���Z�XID���w�肷��ƑΏۂ̃v���Z�X�����(�����I��)�B

    :param process_id: �v���Z�XID
    :type process_id: int
    :return: True:�v���Z�X�������I������, False:�����I���������ɃG���[����������
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
    """FemtetMacro.dll(64bit�p)��Path���擾

    ���W�X�g���̃^�C�v���C�u������񂩂�AFemtetMacro.dll�p�X���擾����֐�

    :return: FemtetMacro.dll(64bit�p)�̃p�X
    ��: "C:\\Program Files\\Femtet_Ver2023_64bit\\Program\\FemtetMacro.dll"
    :rtype: str
    """

    # �l���擾�ł��Ȃ���FileNotFoundError����������̂�
    # ���̏ꍇ��None��߂�l�Ƃ���
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
    """FemtetMacro.dll(32bit�p)��Path���擾

    ���W�X�g���̃^�C�v���C�u������񂩂�AFemtetMacro.dll�p�X���擾����֐�

    :return: FemtetMacro.dll(32bit�p)�̃p�X
    ��: "C:\\Program Files\\Femtet_Ver2023_64bit\\Program\\Macro32\\FemtetMacro.dll"
    :rtype: str
    """

    # �l���擾�ł��Ȃ���FileNotFoundError����������̂�
    # ���̏ꍇ��None��߂�l�Ƃ���
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
    # �v���W�F�N�g���ۑ��̏ꍇ�͕ۑ��_�C�A���O���o��̂ŕs�\��
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
