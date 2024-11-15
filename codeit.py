from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import psycopg2

conn = psycopg2.connect(
    dbname='reviewing',
    user='reviewing',
    password='1234',
    host='localhost'
)

cur = conn.cursor()

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")

chrome_driver_path = 'C:\\Users\\82109\\crawling\\Crawling\\selenium\\Scripts\\chromedriver.exe'
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

slug = ''  # FRONTEND, BACKEND, FULLSTACK
url = f"https://www.codeit.kr/explore?page=1&category={slug}&difficulty=&types="
driver.get(url)

# 페이지 로드 대기
time.sleep(3)

target_count = 10
collected_count = 0  

try:
    while collected_count < target_count:
        carousels = driver.find_elements(By.CLASS_NAME, "TopicList_grid__7bZ8U")

        for carousel in carousels:
            titles = carousel.find_elements(By.CLASS_NAME, "TopicCommonCard_title__0KrCI")
            urls = carousel.find_elements(By.CLASS_NAME, "TopicCommonCard_body__3_gHR")

            for title, url in zip(titles, urls):
                if collected_count < target_count:
                    title_text = title.text.strip()
                    url_href = url.get_attribute('href')
                    if title_text:
                        print('-' * 50)
                        print(f"{collected_count + 1}. 강의 제목: {title_text}")
                        print(f"   강의 링크: {url_href}")

                        course_slug = url_href.split('/')[-1]

                        cur.execute("""
                        INSERT INTO course (platform_id, category_id, title, url, slug)
                        VALUES (
                            (SELECT id FROM platform WHERE name = '코드잇'),
                            (SELECT c.id FROM category c 
                             INNER JOIN platform p ON p.id = c.platform_id 
                             WHERE p.name = '코드잇' AND c.slug = %s),
                            %s, %s, %s
                        );
                        """, (slug, title_text, url_href, course_slug))
                        conn.commit()
                        collected_count += 1
                else:
                    break

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    # 데이터베이스 및 드라이버 종료
    cur.close()
    conn.close()
    driver.quit()
    print("작업 완료 및 연결 종료")