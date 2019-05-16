import os
from configparser import ConfigParser

# 项目路径
#rootDir = os.path.split(os.path.realpath(__file__))[0]
# config.ini文件路径
#configFilePath = os.path.join(rootDir, 'config.ini')
configFilePath = 'config.ini'

def get_config_values(section, option):
    """
    根据传入的section获取对应的value
    :param section: ini配置文件中用[]标识的内容
    :return:
    """
    config = ConfigParser()
    config.read(configFilePath, encoding="utf-8-sig")
    # return config.items(section=section)
    return config.get(section=section, option=option)

def set_config_values(section,option,val):
    config = ConfigParser()
    config.read(configFilePath, encoding="utf-8-sig")
    config.set(section=section,option=option,value=val)
    config.write(open(configFilePath, "w"))
