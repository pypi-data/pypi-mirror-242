# coding:cp932

import sys
from .constant import FemtetClassName as const
from logging import basicConfig, getLogger, StreamHandler, Formatter, DEBUG

# この設定を行うとルートロガーを直接使用してしまうので使わないこと
# basicConfig(level=DEBUG, format='%(levelname)s: %(message)s')

# ログ設定(標準出力にログを追加するため、新たにロガーを追加する)
logger = getLogger(__name__)
logger.setLevel(DEBUG)

stdouthandle = StreamHandler(stream=sys.stdout)
format = Formatter('%(levelname)s: %(message)s')
stdouthandle.setFormatter(format)

logger.addHandler(stdouthandle)

# パッケージ内関数が出力するログを出力しない場合は、呼び出し元で下記の設定を行うこと
# from logging import disable
# disable() # Femtetユーティリティパッケージ関数が出すログを出力しない場合
