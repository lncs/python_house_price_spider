import logging
import logging.handlers
import sys
import os
import datetime
import configparser

"""
使用方法:
    1、导入模块 from logpublic import *
    2、记录日志
        app_logger.debug("app_logger debug")
        app_logger.info("app_logger info")
        app_logger.warning("app_logger warning")
        app_logger.info("app_logger info")
        app_logger.warning("hello {} warning".format("test"))
        app_logger.error("app_logger error")
        app_logger.critical("app_logger critical")
"""


def log_building(log_name='runlog'):
    try:
        # create logger
        logger = logging.getLogger(__name__)

        # set format
        # format_str=logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
        # formatter = logging.Formatter('[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s','%Y%m%d%H%M%S') # set datafmt
        formatter = logging.Formatter('[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s')  # [%(thread)d]

        # create stander output handler
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # create file handler
        file_handler = logging.FileHandler("./logs/%s.log" % log_name, encoding='utf-8')
        file_handler.setFormatter(formatter)
        # logger.addHandler(file_handler)

        # add TimedRotatingFileHandler
        trfilehandler = logging.handlers.TimedRotatingFileHandler("./logs/%s.log" % log_name, when='D', interval=1, backupCount=2)
        # trfilehandler = logging.handlers.TimedRotatingFileHandler("./logs/%s.log" % log_name, when='M', interval=1, backupCount=2)
        # 设置后缀名称，跟strftime的格式一样，按日期计
        # trfilehandler.suffix = "%Y-%m-%d-runlog.log"
        # 设置后缀名称，跟strftime的格式一样，按照分钟计
        trfilehandler.suffix = "%Y%m%d-%H%M.log"
        trfilehandler.setFormatter(formatter)
        # logger.addHandler(trfilehandler)

        # add RotatingFileHandler
        rfilehandler = logging.handlers.RotatingFileHandler("./logs/%s.log" % log_name, maxBytes=1024000000, backupCount=5)
        rfilehandler.setFormatter(formatter)
        logger.addHandler(rfilehandler)

        # must be set
        logger.setLevel(logging.WARNING)

        return logger
    except Exception as e:
        logging.shutdown()
        raise e


def get_config_info(fpath):
    """
    :param fpath: ini文件
    :return: ini文件中的key-value字典
    """
    try:
        # 记事本打开ini文件之后，会存在 \ufeff 的问题,文件最好使用gbk保存
        conf_dict = {}
        cfg = configparser.ConfigParser()
        cfg.read(fpath)
        # 遍历sections内容
        for section in cfg.sections():
            # 将ini中的item组合到字典中,key=section+_option
            # 获取指定section中的options
            # print(cfg.items(section))
            for item in cfg.items(section):
                # print(item)
                key = section + '_' + item[0]
                value = item[1]
                if conf_dict.get(key, None) == None:
                    conf_dict[key] = value
        print(conf_dict)
        return conf_dict
    except Exception as e:
        raise e


def get_log_level(level):
    """
    :param level: 日志级别
    :return: logging模块中对应的日志级别
    """
    DEBUG_LEVEL = {'CRITICAL': logging.CRITICAL,
                   'ERROR': logging.ERROR,
                   'WARNING': logging.WARNING,
                   'INFO': logging.INFO,
                   'DEBUG': logging.DEBUG,
                   'NOTSET': logging.NOTSET,
                   '5': logging.CRITICAL,
                   '4': logging.ERROR,
                   '3': logging.WARNING,
                   '2': logging.INFO,
                   '1': logging.DEBUG,
                   '0': logging.NOTSET
                   }
    try:
        return DEBUG_LEVEL.get(level.upper())
    except Exception as e:
        raise e


def create_logs_floder():
    # create logs file folders
    logs_dir = os.path.join(os.path.curdir, "logs")
    if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        pass
    else:
        os.mkdir(logs_dir)


def set_logname():
    # get current time & set log name
    i = datetime.datetime.now()
    date_str = str(i.year) + "-" + str(i.month) + "-" + str(i.day)
    log_name = date_str + "-runlog"
    return log_name


def get_config_level():
    # get config info
    conf_info = get_config_info('conf.ini')
    # get log level
    log_level = conf_info.get('log_def_level')
    print('配置文件中设置的日志级别为:{}'.format(log_level))
    return log_level


# 程序启动即执行的内容
create_logs_floder()
log_level = get_config_level()
app_logger = log_building(set_logname())

if (log_level and get_log_level(log_level)):
    app_logger.setLevel(get_log_level(log_level))
else:
    app_logger.warning("当前配置的日志级别为{},按照默认级别3(WARNING)处理".format(log_level))


if __name__ == '__main__':
    # dict_info = get_config_info("conf.ini")
    # print (dict_info)

    # print (get_log_level("5"))

    user_name = 'linan '
    app_logger.info("app_logger info")
    app_logger.info("helle {}".format(user_name))
