import yaml
import inspect
import re
import helpers.constants as constants
from flask import session


def __get_call_frame__():
    """

    :return:
    """
    cur_frame = inspect.currentframe()
    return inspect.getouterframes(cur_frame, 2)


def __get_caller_name__():
    call_frame = __get_call_frame__()
    caller_name = call_frame[4][3]
    return caller_name


def __get_call_args__():
    call_frame = __get_call_frame__()
    call_args_str = call_frame[4][4][1]
    pattern = r'.*show\((.*)\)'
    call_args_str = re.match(pattern, call_args_str).group(1)
    call_args_name = call_args_str.split(',')
    if isinstance(call_args_name, list):
        call_args_name = [name.strip() for name in call_args_name]
    elif isinstance(call_args_name, str):
        call_args_name = call_args_name.strip()
    else:
        raise TypeError('the type of your call args cannot be identified, Please contact the developer')
    return call_args_name


def __write_log__(*args):
    with open(constants.DEBUG_LOG_FILE_NAME, 'a') as log:
        log.write(' '.join(args) + '\n')


def __to_yaml__(obj):
    return '======\n'+yaml.dump(obj)+'\n======'


def __pretty_session__():
    session_str = str(session)
    pattern = r'<SecureCookieSession (\{.*\})>'
    session_json = re.match(pattern, session_str).group(1)
    return 'session variable \n' + session_json


def __pretty_object__(obj):
    if str(type(obj)) not in constants.SYS_TYPE:
        if obj is session:
            return __pretty_session__()
        else:
            return __to_yaml__(obj)
    else:
        return str(obj)


def __console_print__(*args):
    if not constants.IS_SERVER:
        caller_name = __get_caller_name__()
        caller_args_name = __get_call_args__()
        arg_name_list = zip(args, caller_args_name)
        print 'printing from function <' + caller_name + '>'
        for arg, name in arg_name_list:
            print '<' + name + '>', 'has structure: '
            print __pretty_object__(arg)
            print


def __dump_print__(*args):
    if not constants.IS_SERVER:
        caller_name = __get_caller_name__()
        caller_args_name = __get_call_args__()
        arg_name_list = zip(args, caller_args_name)
        __write_log__('logging from function <' + caller_name + '>')
        for arg, name in arg_name_list:
            __write_log__('<' + name + '>', 'has structure: ')
            __write_log__(__pretty_object__(arg))
            __write_log__()


def show(*args):
    force_dump = False
    __console_print__(*args)
    if constants.DUMPING or force_dump:
        __dump_print__(*args)
