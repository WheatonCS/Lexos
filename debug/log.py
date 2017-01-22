import yaml
import inspect
import re
import os
import helpers.constants as constants


def __get_call_frame__():
    # type: () -> list
    """
    get the call frame
    :return: returns all the frame info of the call frame (call frame is kind of like call stack)
    """
    cur_frame = inspect.currentframe()
    return inspect.getouterframes(cur_frame, 2)


def __get_caller_name__():
    # type: () -> string
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
    cur_file_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_file_dir, constants.DEBUG_LOG_FILE_NAME), 'a') as log:
        log.write(' '.join(str_args) + '\n')


def __to_yaml__(obj):
    # type: (object) -> str
    """
    takes an object and convert it to an easy reading yaml
    :param obj: an python object
    :return: a string in yaml format
    """
    return '======\n' + yaml.dump(obj) + '\n======'


def __pretty_multi_array__(array):
    """
    takes an array return the array's display form in a string
    Args:
        array: an array or a 2D array

    Returns:
        if the array is a 2D array(can be a 2D array of arrays), return it like a matrix
        example:
           [1, 2]
           [3, 4]
        if the array is a 1D array, then return the string format of that array.
    """
    multi_list = False  # whether this array is more than or equal to 2 dimensional
    for item in array:
        if isinstance(item, list):
            multi_list = True
        else:
            multi_list = False
            break

    if multi_list:
        str_array = [str(subarray) for subarray in array]  # turn all the element into string
        total_str = '\n'.join(str_array)  # turn the string into a nice form
    else:
        total_str = str(array)
    return total_str


def __pretty_session__():
    # type: () -> str
    """
    this function will return the content of secure cookie session
    :return: a string that contain the json format represents the content in session
    """
    from flask import session
    session_str = str(session)
    pattern = r'<SecureCookieSession (\{.*\})>'
    session_json = re.match(pattern, session_str).group(1)
    return 'session variable \n' + session_json


def __pretty_request__():
    from flask import request
    return 'this is a request variable\n' + \
           str({'data': str(request.data),
                'form': str(request.form),
                'files': str(request.files),
                'method': request.method})


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
        from flask import session, request
        import numpy
        if obj is session:
            return __pretty_session__()
        elif obj is request:
            return __pretty_request__()
        elif isinstance(obj, list) or isinstance(obj, numpy.ndarray):
            print(__pretty_multi_array__(obj))
        else:
            return __to_yaml__(obj)
    else:
        return str(obj)


def __console_print__(*args):
    # type: (list | object) -> None
    """
    print all the arguments into a pretty format,
    together with the name of the arguments
    see the doc for `__get_caller_name__()` and `__get_call_args__()`
    :param args: a list of object to print to console
    """
    if not constants.IS_SERVER:
        caller_name = __get_caller_name__()
        caller_args_name = __get_call_args__()
        # concatenate the the value and the name together
        # to create a list of value name pair tuple, like:
        # [(value1, name1), (value2, name2)]
        arg_name_list = list(zip(args, caller_args_name))
        print('printing from function <' + caller_name + '>')
        for arg, name in arg_name_list:
            print('<' + name + '>', 'has structure: ')
            print(__pretty_object__(arg))
            print()


def __dump_print__(*args):
    # type: (list) -> None
    """
    write all the arguments with a pretty format on `debug.log` (constants.DEBUG_LOG_FILE_NAME)
    :param args: a list of object to write to logs
    """
    if not constants.IS_SERVER:
        caller_name = __get_caller_name__()
        caller_args_name = __get_call_args__()
        arg_name_list = list(zip(args, caller_args_name))
        # concatenate the the value and the name together
        # to create a list of value name pair tuple, like:
        # [(value1, name1), (value2, name2)]
        __write_log__('logging from function <' + caller_name + '>')
        for arg, name in arg_name_list:
            __write_log__('<' + name + '>', 'has structure: ')
            __write_log__(__pretty_object__(arg))
            __write_log__()


def show(*args, **kargs):
    # type: (list) -> None
    """
    print all the arguments into a pretty format and
    write all the arguments with a pretty format on `debug.log` (constants.DEBUG_LOG_FILE_NAME)
      * in order to create the dump, you need to set `constants.DUMPING = True` or `force_dump = True`
    :param args: a list of object to write to logs and print on screen
    :param kargs: a diction of optional parameters for now, the only one used is force_dump
    """
    try:
        force_dump = kargs['force_dump']
    except KeyError:
        force_dump = False
    __console_print__(*args)
    if constants.DUMPING or force_dump:
        __dump_print__(*args)
