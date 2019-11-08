import configparser
import data_process

def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def valid(config, class_infos):
    if (class_infos['Units'].sum() < config.getfloat('BASIC', 'RequiredCredits')):
        return False
    return True

if __name__ == '__main__':
    df = data_process.read_schedule()
    config = get_config()
    print(valid(config, df))