# coding:cp932

import sys
from .constant import FemtetClassName as const
from .util import *

command = sys.argv[1]

if command=='execute_femtet':
    execute_femtet()

elif command=='close_femtet':
    if len(sys.argv)==2:
        close_femtet() # 引数が足りないのでエラーになる。エラーメッセージ表示のため実行する。
    elif len(sys.argv)==3:
        close_femtet(sys.argv[2])
    elif len(sys.argv)==4:
        close_femtet(sys.argv[2], int(sys.argv[3]))
    elif len(sys.argv)==5:
        close_femtet(sys.argv[2], int(sys.argv[3]), bool(sys.argv[4]))
    else:
        raise Exception('too many paramters for close_femtet.')


    