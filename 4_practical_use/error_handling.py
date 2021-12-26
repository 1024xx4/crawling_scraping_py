import time
import requests

TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504)  # 一時的な Error を表す Status code


def main():
    """
    Main となる処理。
    :return:
    """
    response = fetch('http://httpbin.org/status/200,404,503')
    if 200 <= response.status_code < 300:
        print('Success!')
    else:
        print('Error!')


def fetch(url: str) -> requests.Response:
    """
    指定した URL に Request を送り、Response Object を返す。
    一時的な Error が起きた場合は最大３回 Retry する。３回 Retry しても成功しなかった場合は例外 Exception を発生させる。
    :param url:
    :return: Response or Exception
    """
    max_retries = 3  # 最大で３回 Retry する
    retries = 0  # 現在の Retry 回数
    while True:
        try:
            print(f'Retrieving {url}...')
            response = requests.get(url)
            print(f'Status: {response.status_code}')
            if response.status_code not in TEMPORARY_ERROR_CODES:
                return response  # 一時的な Error でなければ response を返して終了。

        except requests.exceptions.RequestException as ex:
            # Network level の Error （RequestException）の場合は Log を出力して Retry する
            print(f'Network-level exception occurred: {ex}')
            # Retry 処理
            retries += 1
            if retries >= max_retries:
                raise Exception('Too many retries.')  # Retry 回数の上限を超えた場合は例外を発生させる。

            wait = 2 ** (retries - 1)  # 指数関数的な Retry 間隔を求める
            print(f'Waiting{wait} seconds...')
            time.sleep(wait)  # wait をとる


if __name__ == '__main__':
    main()
