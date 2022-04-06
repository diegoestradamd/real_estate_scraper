from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--incognito")

driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
