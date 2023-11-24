import datetime
import time

from .strop import restrop, restrop_list

def gettime(func):
    def get():
        start = datetime.datetime.now()
        print(restrop("==="))
        func()
        end = datetime.datetime.now()
        TotalTimeSpent = (end - start).seconds
        print(restrop_list(["===",
                            "开始时间 ", start.strftime('%Y-%m-%d  %H:%M:%S'),
                            "     结束时间 ", end.strftime('%Y-%m-%d  %H:%M:%S'),
                            "     总耗时 ", TotalTimeSpent, "s"
                            ],
                           [(0, 1, 0),
                            (), (0, 3, 0),
                            (), (0, 4, 0),
                            (), (0, 5, 0), ()
                            ])
              )
    return get
