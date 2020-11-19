'''
methods not used models
'''
import os
import sys
import traceback


def get_func_name(level=-3):
    _, _, func_name, _ = traceback.extract_stack()[level]
    return func_name

def get_detail_exception_info(exception_object: Exception):
    """
    Returns the short occurred exception description.
    :param exception_object:
    :return:
    """
    _, _, traceback = sys.exc_info()
    if traceback:
        # import traceback as tb
        # tb.print_tb(traceback, file=sys.stdout)

        return '{message} ({code} in {file}: {line})'.format(
            message=str(exception_object),
            code=exception_object.__class__.__name__,
            file=os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1],
            line=sys.exc_info()[2].tb_lineno,
        )
    else:
        return f'{str(exception_object)} ({exception_object.__class__.__name__})'
