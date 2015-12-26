import json
import urllib.request


__author__ = 'Anton Vakhrushev'
__email__ = 'anwinged@ya.ru'


MDASH_URL = 'http://mdash.ru/api.v1.php'


class TypographError(RuntimeError):
    pass


class Typograph(object):

    def __init__(self, rules = None):
        self.rules = self.__prepare_rules(rules)

    def process(self, text):
        data = self.__prepare_data(text)
        answer = self.__request(data)
        answer = json.loads(answer)
        self.__ensure_answer_is_correct(answer)
        return answer['result']

    def __prepare_data(self, text):
        data = {}
        data.update(self.rules)
        data.update({'text': text})
        return data

    def __request(self, data):
        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')
        request = urllib.request.Request(MDASH_URL, data)
        responce = urllib.request.urlopen(request)
        return responce.read().decode('utf-8')

    def __ensure_answer_is_correct(self, answer):
        if answer.get('status') == 'error':
            raise TypographError()

    def __prepare_rules(self, params):

        def convert(v):
            return 'on' if v == 'on' or v == True else 'off'

        result = {}
        params = params or {}

        for k in params:
            result[k] = convert(params[k])

        return result


if __name__ == '__main__':
    params = {
        'Text.paragraphs': False,
        'Text.breakline': 'off',
    }
    t = Typograph(params)
    print(t.process('"Вы все еще кое-как верстаете в "Ворде"? - Тогда мы идем к вам!"'))
