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
    host = 'localhost',
    port = '5432'
)

cur = conn.cursor()

# Chrome 옵션 설정 (헤드리스로 실행하려면)
chrome_options = Options()
chrome_options.add_argument("--headless")  # 화면을 띄우지 않고 실행
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")  # SSL 인증서 오류 무시

# ChromeDriver 경로 설정 (chromedriver가 PATH에 있으면 경로 생략 가능)
chrome_driver_path = 'C:\\Users\\82109\\crawling\\Crawling\\selenium\\Scripts\\chromedriver.exe' # 크롬 드라이버 경로

service = Service(executable_path=chrome_driver_path)
# 웹드라이버 실행
driver = webdriver.Chrome(service=service, options=chrome_options)

# FastCampus 카테고리 페이지로 이동
driver.get('https://fastcampus.co.kr/category_online_programmingfront')

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
                    if title_text:  # 제목이 비어 있지 않을 때만 출력
                        print('-' * 50)
                        print(f"{collected_count + 1}. 강의 제목: {title_text}")
                        print(f"   이미지 URL: {img.get_attribute('src')}")
                        print(f"   강의 링크: {url_href}")
                        collected_count += 1

                        cur.execute("""
                            INSERT INTO course (name, url, thumbnail_image, teacher)
                            VALUES (%s, %s, %s);
                        """, (title_text, url_href, img))
                        
                        conn.commit()
                else:
                    break  # 원하는 개수에 도달하면 루프 종료
                
    except Exception as e:
        print(f"오류 발생: {e}")
        break