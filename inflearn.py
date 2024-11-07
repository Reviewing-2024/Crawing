from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome 드라이버 생성
chrome_options = Options()
chrome_options.add_argument("--headless")  # Chrome을 headless 모드로 실행

driver = webdriver.Chrome(options=chrome_options)

for page in range(1,4):
    
    url = f"https://www.inflearn.com/courses?types=ONLINE&page_number={page}"
    driver.get(url)

    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.mantine-AspectRatio-root.css-2oqlco.mantine-1w8yksd'))
    )

    req = driver.page_source
    soup = BeautifulSoup(req, "html.parser")

    twoDiv = soup.find_all('ul',class_='css-y21pja mantine-1avyp1d')

    for i in twoDiv:
        print('=========')
        imgDivs = i.find_all('div',class_='mantine-AspectRatio-root css-2oqlco mantine-1w8yksd')
        titles = i.find_all('p',class_='mantine-Text-root css-10bh5qj mantine-b3zn22')
        teachers = i.find_all('p',class_='mantine-Text-root css-1r49xhh mantine-aiouth')

        for imgDiv, title, teacher in zip(imgDivs, titles, teachers):
            
            imgOrVideo = imgDiv.find('img')

            if imgOrVideo: # 이미지
                thumnail = imgDiv.find('img')['src']
            else: # 비디오
                thumnail = imgDiv.find('source')['src']

            title = title.text
            teacher = teacher.text

            print(thumnail)
            print(title)
            print(teacher)
            print('----------------------')

driver.quit()







