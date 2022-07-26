from selenium import webdriver
driver = webdriver.Chrome()
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
driver = webdriver.Chrome()

def test_cards_of_pets():
    driver = webdriver.Chrome(r'C:\Users\елена\PycharmProjects\pythonProject1\Selenium\chromedriver.exe')
    driver.implicitly_wait(5)
    # авторизуемся, заходим на страницу "мои питомцы"
    driver.get('https://petfriends.skillfactory.ru/login')
    # driver.find_element_by_id('email').send_keys("epansenko21@mail.ru ")
    # driver.find_element_by_id('pass').send_keys("193788")
    # driver.find_element_by_css_selector('button[type="submit"]').click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "email"))).send_keys("epansenko21@mail.ru ")
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "pass"))).send_keys("193788")
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    driver.find_element_by_link_text('Мои питомцы').click()
    #получаем массив всех моих питомцев
    # info_of_my_pets = driver.find_elements_by_css_selector('div td')
    info_of_my_pets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div td')))
    # формируем списки имен, типов и возрастов животных
    names = info_of_my_pets[0::4]
    types = info_of_my_pets[1::4]
    ages = info_of_my_pets[2::4]
    #получаем кусок текста с логином, количеством питомцев, друзей и сообщений
    # quantity_of_pets_full=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]').text
    quantity_of_pets_full = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left'))).text
    # получаем индекс символа буквы П слова "Питомцев"
    index_pets=quantity_of_pets_full.find('Питомцев')
    # получаем индекс символа буквы Д слова "Друзей"
    index_friends=quantity_of_pets_full.find('Друзей')
    # получаем срез строки от пробела после слова "Питомцев" до начала слова "Друзей"
    # (на всякий случай удаляем лишние пробелы, должно остаться только число)
    quantity_of_pets=quantity_of_pets_full[index_pets+10:index_friends].replace(' ','')
    # проверяем, соответствует ли количество питомцев по профилю реальному количеству имен питомцев
    assert int(quantity_of_pets)==len(names),"В таблице присутствуют не все питомцы"
    # получаем фото питомцев
    # images = driver.find_elements_by_css_selector('.table table-hover tbody tr th img')
    images = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr th img')))
    count = 0
    # проходим циклом по массиву фотографий, считаем количество фото с текстом base64 в атрибуте src
    for i in range(len(images)):
        if 'base64' in images[i].get_attribute('src'):
            count += 1
    if (len(images) % 2) == 0:
        assert count >= (len(images)/2), 'Фото присутствует менее чем у половины питомцев'
    else:
        assert count >= (len(images)/2+1), 'Фото присутствует менее чем у половины питомцев'
    # проверяем, что у всех питомцев есть имя
    assert '' not in names,'Не у всех питомцев есть имя'
    # проверяем, что у всех питомцев есть порода
    assert '' not in types,'Не у всех питомцев есть порода'
    # проверяем, что у всех питомцев есть возраст
    count_noage=0
    assert '' not in ages,'Не у всех питомцев есть возраст'
    # проверяем, что у всех питомцев разные имена
    assert len(names)==len(list(set(names))),'В списке есть питомцы с разным именем'
    # проверяем, что в списке нет повторяющихся питомцев, для этого сначала убедимся, что предыдущий тест не пройден и есть повтор имен
    if len(names)!=len(list(set(names))):
        # удаляем из списка элементы-крестики (удалить питомца)
        del info_of_my_pets[::4]
        # группируем каждые три элемента списка питомцев в кортеж (имя,порода,возраст)
        info_of_my_pets_tuple = [tuple(info_of_my_pets[i:i+3]) for i in range(0, len(info_of_my_pets), 3)]
        # проверяем, есть ли в списке кортежей одинаковые элементы
        assert len(info_of_my_pets_tuple) == len(list(set(info_of_my_pets_tuple)))

