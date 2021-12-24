import requests
from tenacity import retry, stop_after_attempt, wait_exponential

TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504)  # 一時的な Error を表す Status code


def main():
    """
    Main となる処理。
    :return: Str
    """
    response = fetch('http://httpbin.org/status/200,404,503')
    if 200 <= response.status_code < 300:
        print('Success!')
    else:
        print('Error!')


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
def fetch(url: str) -> requests.Response:
    """
    指定した URL request を送り、Response object を返す。
    一時的な Error が起きた場合は最大３回 Retry する。
    ３回 Retry しても成功しなかった場合は、例外 tenacity.RetryError を発生させる
    :param url: str
    :return: Response
    """
    print(f'Retrieving {url}...')
    response = requests.get(url)
    print(f'Status: {response.status_code}')
    if response.status_code not in TEMPORARY_ERROR_CODES:
        return response

    raise Exception(f'Temporary Error: {response.status_code}')


if __name__ == '__main__':
    main()
