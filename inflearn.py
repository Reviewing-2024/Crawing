from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2

conn = psycopg2.connect(
    host="localhost",       # 데이터베이스 호스트 이름
    database="reviewing",  # 데이터베이스 이름
    user="reviewing",    # 데이터베이스 사용자 이름
    password="1234" # 데이터베이스 비밀번호
)

# 커서 생성
cur = conn.cursor()

# Chrome 드라이버 생성
chrome_options = Options()
userAgent = "user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
chrome_options.add_argument(userAgent)
chrome_options.add_argument("--headless")  # Chrome을 headless 모드로 실행

driver = webdriver.Chrome(options=chrome_options)

count = 0

for page in range(1,2):
    if count >= 30:
        break
    
    # url = f"https://www.inflearn.com/courses?types=ONLINE&page_number={page}" 전체 강의 조회
    # 분야별 크롤링
    slug = '' # web-dev, front-end, back-end
    url = f"https://www.inflearn.com/courses/it-programming/{slug}?types=ONLINE&page_number={page}"
    driver.get(url)

    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.mantine-AspectRatio-root.css-2oqlco.mantine-1w8yksd'))
    )

    req = driver.page_source
    soup = BeautifulSoup(req, "html.parser")

    twoDiv = soup.find_all('ul',class_='css-2ldd65 mantine-1avyp1d')

    for i in twoDiv:
        
        print('=========')
        urls = i.find_all('a')
        thumbnails = i.find_all('div',class_='mantine-AspectRatio-root css-2oqlco mantine-1w8yksd')
        titles = i.find_all('p',class_='mantine-Text-root css-10bh5qj mantine-b3zn22')
        teachers = i.find_all('p',class_='mantine-Text-root css-1r49xhh mantine-aiouth')

        for url, thumbnail, title, teacher in zip(urls, thumbnails, titles, teachers):
            if count >= 30:
                break

            count += 1

            course_url = url.get('href')
            
            imgOrVideo = thumbnail.find('img')

            thumbnail_image = None
            thumbnail_video = None

            if imgOrVideo: # 썸네일 이미지
                thumbnail_image = thumbnail.find('img')['src']
            else: # 썸네일 비디오
                thumbnail_video = thumbnail.find('source')['src']

            title = title.text
            teacher = teacher.text

            print(title)    
            print(course_url)
            print(thumbnail_image)
            print(thumbnail_video)
            print(teacher)
            print('----------------------')

            
            cur.execute("""
            INSERT INTO course (platform_id, category_id, name, url, thumbnail_image, thumbnail_video, teacher)
            VALUES (
                (SELECT id FROM platform WHERE name = '인프런'),
                (SELECT c.id FROM category c 
                INNER JOIN platform p ON p.id = c.platform_id 
                WHERE p.name = '인프런' AND c.slug = %s),
                %s, %s, %s, %s, %s
            );
            """, (slug, title, course_url, thumbnail_image, thumbnail_video, teacher))
    
    print(count)
    conn.commit()

driver.quit()







