import configparser
import data_process

def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def time_overlap(class_info, other_class_info):
    if class_info['Times'][0] > other_class_info['Times'][1]:
        class_info, other_class_info = other_class_info, class_info
    if class_info['Times'][1] > other_class_info['Times'][0]:
        return class_info['Sem'] ^ other_class_info['Sem'] < 3
    return False

def valid(config, class_infos):
    if (class_infos['Units'].sum() < config.getfloat('BASIC', 'RequiredCredits')):
        return False
    for class_info in class_infos:
        for other_class_info in class_infos:
            if class_info['Course'] == other_class_info['Course']:
                continue
            if time_overlap(class_info, other_class_info):
                return False
    return True

if __name__ == '__main__':
    df = data_process.read_schedule()
    config = get_config()
    print(valid(config, df))