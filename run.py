# -*- coding: utf-8 -*-
__author__ = 'erikshe2003'

from app.myhtml import myhtml

if __name__ == '__main__':
    # apache
    # myhtml.run()
    # 绝对不能在生产环境中使用调试器
    myhtml.run(debug=True,port=5010)
    # myhtml.run(host='10.1.4.236',port=5000)