from .mold.arg import Arg
from .base.body import *


class SaveTask(Body):
    def _saveTask(self, task_name, py_path, argdt):
        with open(py_path, mode='r', encoding='utf-8') as file:
            ml = file.read().strip()
        with self.getSql() as sqt:
            arg = Arg({'ml': ml, **argdt})
            self.setArg(sqt, task_name, arg)

    # 记录周期任务
    def saveWeekTask(self, task_name, week: int, max_error_num: int, error_week,
                     py_path: str = None,  emails=None, reload=False):
        arg = {'class': '周期',
               'week': week,
               'error_week': error_week,
               'reload': reload,
               'max_error_num': max_error_num,
               'emails': emails if emails else ['1321443305@qq.com'],
               }
        return self._saveTask(task_name, py_path, arg)

    # 记录定时(天)任务
    def saveRegularTask(self, task_name, moment: str, week_day: int, max_error_num: int,
                        error_week=3600, py_path: str = None, if_replace=False, emails=None, reload=False):
        arg = {'class': '日度',
               'moment': moment,
               'week_day': week_day,
               'error_week': error_week,
               'reload': reload,
               'max_error_num': max_error_num,
               'emails': emails if emails else ['1321443305@qq.com'],
               }
        return self._saveTask(task_name, py_path, if_replace, arg)

    # 记录定时(月)任务
    def saveMonRegularTask(self, task_name, moment: str, mon_day: int, max_error_num: int,
                           error_week=3600, py_path: str = None, if_replace=False, emails=None, reload=False):
        arg = {'class': '月度',
               'moment': moment,
               'mon_day': mon_day,
               'error_week': error_week,
               'reload': reload,
               'max_error_num': max_error_num,
               'emails': emails if emails else ['1321443305@qq.com'],
               }
        return self._saveTask(task_name, py_path, if_replace, arg)
