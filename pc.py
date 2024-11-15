from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import psycopg2

conn = psycopg2.connect(
        dbname = 'reviewing',
        user = 'reviewing',
        password = '1234',
        host = 'localhost'
    )

cur = conn.cursor()

# Chrome 옵션 설정 (헤드리스로 실행하려면)
chrome_options = Options()
chrome_options.add_argument("--headless")  # 화면을 띄우지 않고 실행
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")  # SSL 인증서 오류 무시

chrome_driver_path = 'C:\\Users\\82109\\crawling\\Crawling\\selenium\\Scripts\\chromedriver.exe'
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

slug = ''  # front, back, app, devops
url = f'https://fastcampus.co.kr/category_online_programming{slug}'
driver.get(url)

# 페이지 로드 대기
time.sleep(3)

target_count = 10 # 가져올 강의 수
collected_count = 0  # 수집된 강의 수

while collected_count < target_count:

    try:
        carousels = driver.find_elements(By.CLASS_NAME, "InfinityCourse_infinityCourse__kc8I9")
        
        for carousel in carousels:
            titles = carousel.find_elements(By.CLASS_NAME, "CourseCard_courseCardTitle__1HQgO")
            imgs = carousel.find_elements(By.CSS_SELECTOR, "img.CourseCard_courseCardImage__XcpZb")
            urls= carousel.find_elements(By.CLASS_NAME, "CourseCard_courseCardDetailContainer__PnVam")

            for title, img, url in zip(titles, imgs, urls):
                if collected_count < target_count:
                    title_text = title.text.strip()
                    url_href = url.get_attribute('href')
                    img_src = img.get_attribute('src')
                    if title_text:  # 제목이 비어 있지 않을 때만 출력
                        print('-' * 50)
                        print(f"{collected_count + 1}. 강의 제목: {title_text}")
                        print(f"   이미지 URL: {img_src}")
                        print(f"   강의 링크: {url_href}")
                    
                        course_slug = url_href.split('/')[-1]

                        cur.execute("""
                        INSERT INTO course (platform_id, category_id, title, url, thumbnail_image, slug)
                        VALUES (
                            (SELECT id FROM platform WHERE name = '패스트캠퍼스'),
                            (SELECT c.id FROM category c 
                             INNER JOIN platform p ON p.id = c.platform_id 
                             WHERE p.name = '패스트캠퍼스' AND c.slug = %s),
                            %s, %s, %s, %s
                        );
                        """, (slug, title_text, url_href, img_src, course_slug))
                        
                        conn.commit()
                        collected_count += 1
                else:
                    break  # 원하는 개수에 도달하면 루프 종료
                
    except Exception as e:
        print(f"오류 발생: {e}")
        break

    finally:
    # 데이터베이스 및 드라이버 종료
        cur.close()
        conn.close()
        driver.quit()
        print("작업 완료 및 연결 종료")