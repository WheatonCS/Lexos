import yaml
import inspect
import re
import helpers.constants as constants
from flask import session


def __get_call_frame__():
    # type: () -> list
    """
    get the call frame
    :return: returns all the frame info of the call frame (call frame is kind of like call stack)
    """
    cur_frame = inspect.currentframe()
    return inspect.getouterframes(cur_frame, 2)


def __get_caller_name__():
    # type: () -> caller_name
    """
    get the caller name of `show` function
    showing which function is calling the show function
    Example: if there is `def test(): debug.log.show(this)`
            then this function will return 'test' to the show function
    :return: the name of the caller of `show` function
    """
    call_frame = __get_call_frame__()
    caller_name = call_frame[4][3]
    return caller_name


def __get_call_args__():
    # type: () -> str | list[str]
    """
    get the call argument of `show function`
    * the regex will break if you call stuff like `debug.show(show())`
    Example: if there is `def test(): debug.log.show(this, haha)`
            then this function will return ['this', 'haha'] to the show function
    :return:
    :return: a list of string or a string that is the name of the argument
    """
    call_frame = __get_call_frame__()
    call_args_str = call_frame[4][4][1]
    # match
    pattern = r'.*show\((.*)\)'
    call_args_str = re.match(pattern, call_args_str).group(1)
    call_args_name = call_args_str.split(',')
    # if there is more than 1 arguments
    if isinstance(call_args_name, list):
        call_args_name = [name.strip() for name in call_args_name]
    # if there is only 1 argument
    elif isinstance(call_args_name, str):
        call_args_name = call_args_name.strip()
    else:
        raise TypeError('the type of your call args cannot be identified, Please contact the developer')
    return call_args_name


def __write_log__(*args):
    # type: (list[object]) -> object
    """
    this function simulates the behavior of `print` in python3
    this can take any number of parameters and write to the `debug.log`(constants.DEBUG_LOG_FILE_NAME)
        with space in between each value of the argument
    :param args: any number of parameter you want to write to write to `debug.log`
    """
    str_args = [str(arg) for arg in args]
    with open(constants.DEBUG_LOG_FILE_NAME, 'a') as log:
        log.write(' '.join(str_args) + '\n')


def __to_yaml__(obj):
    # type: (object) -> str
    """
    takes an object and convert it to an easy reading yaml
    :param obj: an python object
    :return: a string in yaml format
    """
    return '======\n'+yaml.dump(obj)+'\n======'


def __pretty_session__():
    # type: () -> str
    """
    this function will return the content of secure cookie session
    :return: a string that contain the json format represents the content in session
    """
    session_str = str(session)
    pattern = r'<SecureCookieSession (\{.*\})>'
    session_json = re.match(pattern, session_str).group(1)
    return 'session variable \n' + session_json


def __pretty_object__(obj):
    # type: (object) -> str
    """
    take any object (can be session or a regular object)
    and convert it into a readable form
    :param obj: an object, can be regular object or session
                (for now, `request` will break the function)
    :return: if the object is a system type (system can handle the display of the object)
                just cast the object into string
             if the object is a session
                 the result of `__pretty_session__()`, a json represent the content of session
             else (for example a file_manager, session_manager, file_info)
                  return the content of the object in yaml format
    """
    if str(type(obj)) not in constants.SYS_TYPE:
        if obj is session:
            return __pretty_session__()
        else:
            return __to_yaml__(obj)
    else:
        return str(obj)


def __console_print__(*args):
    # type: (list) -> None
    """
    print all the arguments into a pretty format
    :param args: a list of object to print to console
    """
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
    # type: (list) -> None
    """
    write all the arguments with a pretty format on `debug.log` (constants.DEBUG_LOG_FILE_NAME)
    :param args: a list of object to write to logs
    """
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
    # type: (list) -> None
    """
    print all the arguments into a pretty format and
    write all the arguments with a pretty format on `debug.log` (constants.DEBUG_LOG_FILE_NAME)
      * in order to create the dump, you need to set `constants.DUMPING = True` or use force_dump argument
    :param args: a list of object to write to logs and print on screen
    """
    force_dump = False
    __console_print__(*args)
    if constants.DUMPING or force_dump:
        __dump_print__(*args)
