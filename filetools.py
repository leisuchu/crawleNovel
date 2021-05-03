"""
    日志工具类
"""
import time
import os


def write_file_log(start_log='写入文件开始', end_log='写入文件完成', time_used=True):
    def log_print(func):
        def write_status(*args, **kw):
            start_time = 0
            end_time = 0
            print('~' * 8, end='')
            if time_used:
                start_time = time.time() * 1000

            print(start_log, end='')
            print('~' * 8, end='\n')
            func(*args, **kw)
            print('~' * 8, end='')

            if time_used:
                end_time = time.time() * 1000

            print((end_log + '耗时：' + str(end_time - start_time) + 'ms') if time_used else end_log, end='')
            print('~' * 8, end='\n')

        return write_status

    return log_print


@write_file_log(start_log='开始执行', end_log='执行完成')
def write_file(text, file_path=str(int(time.time())), next_line=True):
    current_work_path = os.getcwd()
    file_path = current_work_path + '/' + file_path + '.txt'
    had_content = None
    try:
        file = open(file_path, 'r')
        had_content = file.read()

    except IOError:
        pass

    file = open(file_path, 'a')
    if next_line and had_content:
        file.write('\n\n')

    file.write(text)
    file.close()
