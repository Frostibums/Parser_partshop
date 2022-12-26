from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def init_driver():
    driver1 = webdriver.Chrome()
    driver1.wait = WebDriverWait(driver1, 5)
    return driver1


def get_marks(link: str) -> list[str]:
    marks_links = []
    driver.get(link)
    mark_blocks = driver.find_elements(By.CLASS_NAME, "mark-item__description")
    for block in mark_blocks:
        marks_links.append(block.find_element(By.CLASS_NAME, "mark-item__title").get_attribute("href"))
    return marks_links


def get_parts(mark_link: str) -> list[str]:
    parts_links = []
    page_number = 1
    while 1:
        driver.get(f"{mark_link}/?page={page_number}")
        product_items = driver.find_elements(By.CLASS_NAME, "product-item")
        if not product_items:
            return parts_links
        for product in product_items:
            parts_links.append(product.find_element(By.CLASS_NAME, "product-item__title").get_attribute("href"))
        page_number += 1


def get_part_data(part_link: str) -> list[str]:
    driver.get(part_link)
    name = driver.find_element(By.CLASS_NAME, "product-main-h1").find_element(By.TAG_NAME, "h1").text
    price = driver.find_element(By.CLASS_NAME, "product__price-value").text.removesuffix(" i")
    description = driver.find_element(By.CLASS_NAME, "product-description").find_element(By.TAG_NAME, "p").text
    detail_characteristics = driver.find_elements(By.CLASS_NAME, "har_line")
    detail_numbers = filter(lambda characteristic: 'номер детали' in characteristic.text, detail_characteristics)
    detail_numbers = list(detail_numbers)[0].text.split("\n")[1]
    data = [part_link, name, price, description, detail_numbers]
    return data


if __name__ == "__main__":
    driver = init_driver()
    catalog_link = "https://pnevmo-pro.ru/katalog/"
    for mark in get_marks(catalog_link):
        for part in get_parts(mark):
            print(*get_part_data(part))
    driver.quit()
