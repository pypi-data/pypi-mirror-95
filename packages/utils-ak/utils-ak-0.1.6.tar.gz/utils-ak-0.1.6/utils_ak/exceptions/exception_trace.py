""" Python exceptions traceback functionality. """
import sys
import traceback


# https://stackoverflow.com/questions/13210436/get-full-traceback

class FauxTb(object):
    def __init__(self, tb_frame, tb_lineno, tb_next):
        self.tb_frame = tb_frame
        self.tb_lineno = tb_lineno
        self.tb_next = tb_next


def current_stack(skip=0):
    try:
        1 / 0
    except ZeroDivisionError:
        f = sys.exc_info()[2].tb_frame
    for i in range(skip + 2):
        f = f.f_back
    lst = []
    while f is not None:
        lst.append((f, f.f_lineno))
        f = f.f_back
    return lst


def extend_traceback(tb, stack):
    """Extend traceback with stack info."""
    head = tb
    for tb_frame, tb_lineno in stack:
        head = FauxTb(tb_frame, tb_lineno, head)
    return head


def full_exc_info():
    """Like sys.exc_info, but includes the full traceback."""
    t, v, tb = sys.exc_info()
    full_tb = extend_traceback(tb, current_stack(1))
    return t, v, full_tb


if __name__ == '__main__':
    import logging


    def func():
        try:
            raise Exception('Dummy')
        except Exception as e:
            t, v, full_tb = full_exc_info()
            print(t)
            print(v)
            print(full_tb)

            print(traceback.format_exc())
            # _logging.error("Something awful happened!", exc_info=full_exc_info())
            # _logging.error("Something awful happened!", exc_info=e)
            # print(traceback.format_exc())


    def func2():
        func()


    func2()
