import argparse
import logging
from collections import Counter

logger = logging.getLogger(__name__)


class Skyphrase(object):
    def __init__(self, value):
        self.__value = value

    def is_valid(self):
        counter = Counter(self.__value.split())
        word_counts = counter.values()
        return not self.__is_single_or_empty_word(word_counts) and sum(counter.values()) == len(word_counts)

    def __is_single_or_empty_word(self, words):
        return True if len(words) <= 1 else False


class PhrasesValidator(object):

    def __init__(self):
        self.__valid_count = 0

    def validate_phrases(self, to_validate, isfile):
        if not isfile:
            if Skyphrase(to_validate).is_valid():
                self.__valid_count += 1
        else:
            with open(to_validate, 'r') as phrases_file:
                for phrase_line in phrases_file:
                    if Skyphrase(phrase_line).is_valid():
                        self.__valid_count += 1

    def print_result(self):
        print(f'Valid phrases count: {self.__valid_count}')


def create_arguments():
    parser = argparse.ArgumentParser(
        description='Validate passphrase if it is skyphrase, deals guoted strings or files')
    parser.add_argument('to_validate', help='value to valid (path to file or single phrase)', type=str)
    parser.add_argument('--isfile', help='tread argument as file path', default=False, action='store_true')
    return vars(parser.parse_args())


def handle_exception(exception):
    return (type(exception), exception, exception.__traceback__)


if __name__ == '__main__':
    validator = PhrasesValidator()
    try:
        validator.validate_phrases(**create_arguments())
        validator.print_result()
    except IOError as ioe:
        logger.error('Malformed file ', exc_info=handle_exception(ioe))
        print('Choose existing file. Validation not performed')
    except Exception as e:
        print('Critical error contact administrator')
        logger.error('Malformed file ', exc_info=handle_exception(e))
