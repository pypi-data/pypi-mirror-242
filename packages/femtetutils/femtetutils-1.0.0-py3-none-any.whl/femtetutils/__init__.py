# coding:cp932

import sys
from .constant import FemtetClassName as const
from logging import basicConfig, getLogger, StreamHandler, Formatter, DEBUG

# ���̐ݒ���s���ƃ��[�g���K�[�𒼐ڎg�p���Ă��܂��̂Ŏg��Ȃ�����
# basicConfig(level=DEBUG, format='%(levelname)s: %(message)s')

# ���O�ݒ�(�W���o�͂Ƀ��O��ǉ����邽�߁A�V���Ƀ��K�[��ǉ�����)
logger = getLogger(__name__)
logger.setLevel(DEBUG)

stdouthandle = StreamHandler(stream=sys.stdout)
format = Formatter('%(levelname)s: %(message)s')
stdouthandle.setFormatter(format)

logger.addHandler(stdouthandle)

# �p�b�P�[�W���֐����o�͂��郍�O���o�͂��Ȃ��ꍇ�́A�Ăяo�����ŉ��L�̐ݒ���s������
# from logging import disable
# disable() # Femtet���[�e�B���e�B�p�b�P�[�W�֐����o�����O���o�͂��Ȃ��ꍇ
