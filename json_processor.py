import argparse
import json
import logging

logger = logging.getLogger(__name__)


class FlattenedBalance(object):

    def __init__(self, user_balance):
        self.__user_balance = user_balance
        self.__user_balance_value = 0

    def flatten_and_summ(self):
        self.__flatten_and_filter(self.__user_balance)

    def __flatten_and_filter(self, to_flatten):
        if isinstance(to_flatten, list):
            for value in to_flatten:
                self.__flatten_and_filter(value)
        elif isinstance(to_flatten, dict):
            for value in to_flatten.values():
                self.__flatten_and_filter(value)
        elif isinstance(to_flatten, int):
            self.__user_balance_value += to_flatten
        return

    def get_balance(self):
        return self.__user_balance_value


def create_arguments():
    parser = argparse.ArgumentParser(
        description='Script will summ all numbers in json format file')
    parser.add_argument('file_path', help='path to json file', type=str)
    return vars(parser.parse_args())


def handle_exception(exception):
    return (type(exception), exception, exception.__traceback__)

if __name__ == '__main__':
    try:
        flattened = []
        with open(create_arguments().get('file_path')) as json_file:
            json_dict = json.load(json_file)
            fb = FlattenedBalance(json_dict)
            fb.flatten_and_summ()
            print(fb.get_balance())
    except IOError as ioe:
        logger.error('Malformed file ', exc_info=handle_exception(ioe))
        print('Choose existing file. Validation not performed')
    except Exception as e:
        print('Critical error contact administrator')
        logger.error('Malformed file ', exc_info=handle_exception(e))
