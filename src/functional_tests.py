from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8001/metadb/')

assert 'MetaDB administration' in browser.title
