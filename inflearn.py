from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome 드라이버 생성
chrome_options = Options()
userAgent = "user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
chrome_options.add_argument(userAgent)
chrome_options.add_argument("--headless")  # Chrome을 headless 모드로 실행

driver = webdriver.Chrome(options=chrome_options)

for page in range(1,2):
    
    url = f"https://www.inflearn.com/courses?types=ONLINE&page_number={page}"
    driver.get(url)

    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.mantine-AspectRatio-root.css-2oqlco.mantine-1w8yksd'))
    )

    req = driver.page_source
    soup = BeautifulSoup(req, "html.parser")

    twoDiv = soup.find_all('ul',class_='css-2ldd65 mantine-1avyp1d')

    count = 0

    for i in twoDiv:
        print('=========')
        urls = i.find_all('a')
        thumbnails = i.find_all('div',class_='mantine-AspectRatio-root css-2oqlco mantine-1w8yksd')
        titles = i.find_all('p',class_='mantine-Text-root css-10bh5qj mantine-b3zn22')
        teachers = i.find_all('p',class_='mantine-Text-root css-1r49xhh mantine-aiouth')

        for url, thumbnail, title, teacher in zip(urls, thumbnails, titles, teachers):
            count += 1

            course_url = url.get('href')
            
            imgOrVideo = thumbnail.find('img')

            if imgOrVideo: # 썸네일 이미지
                course_thumbnail = thumbnail.find('img')['src']
            else: # 썸네일 비디오
                course_thumbnail = thumbnail.find('source')['src']

            title = title.text
            teacher = teacher.text

            print(course_url)
            print(course_thumbnail)
            print(title)
            print(teacher)
            print('----------------------')
    
    print(count)

driver.quit()







