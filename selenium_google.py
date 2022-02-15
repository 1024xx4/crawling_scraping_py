from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

options = ChromeOptions()
# Headless mode を有効にするには、次の行の Comment out を解除する
# options.headless = True
driver = Chrome(options=options)  # Chrome の WebDriver object を作成する

# Google の TOP 画面を開く
driver.get('https://www.google.co.jp')

# Title に「Google」が含まれていることを確認する。
assert 'Google' in driver.title

# 検索語を入力して送信する。
input_element = driver.find_element('name', 'q')
input_element.send_keys('Python')
input_element.send_keys(Keys.RETURN)

# Title に「Python」が含まれていることを確認する。
assert 'Python' in driver.title

# Screenshot を撮る。
driver.save_screenshot('search_results.png')

# 検索結果を表示する
for h3 in driver.find_elements(By.CSS_SELECTOR, 'a > h3'):
    a = h3.find_element_by_xpath('..')
    print(h3.text)
    print(a.get_attribute('href'))

driver.quit()  # Browser を終了する
