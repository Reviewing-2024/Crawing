from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Chrome 옵션 설정 (헤드리스로 실행하려면)
chrome_options = Options()
chrome_options.add_argument("--headless")  # 화면을 띄우지 않고 실행
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")  # SSL 인증서 오류 무시

# ChromeDriver 경로 설정
chrome_driver_path = 'C:\\Users\\82109\\crawling\\Crawling\\selenium\\Scripts\\chromedriver.exe' # 크롬 드라이버 경로
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# FastCampus 카테고리 페이지로 이동
driver.get('https://www.codeit.kr/roadmaps?slug=web')

# 페이지 로드 대기
time.sleep(3)

target_count = 1  # 가져올 강의 수
collected_count = 0  # 수집된 강의 수

while collected_count < target_count:
    try:
        # 강의 카드 요소 찾기
        carousels = driver.find_elements(By.CLASS_NAME, "ExploreSection_contents__s8NM9")

        for carousel in carousels:
            # 요소 선택자 수정
            titles = carousel.find_elements(By.CLASS_NAME, "CommonExploreItem_title__tNRhO")
            imgs = carousel.find_elements(By.CSS_SELECTOR, "img.CommonExploreItem_icon__W_3rB")
            urls = carousel.find_elements(By.CLASS_NAME, "CommonExploreItem_outline__mn3kc.CommonExploreItem_hoverable__9MoEj")  # 링크 요소 확인

            for title, img, url in zip(titles, imgs, urls):
                if collected_count < target_count:
                    title_text = title.text.strip()
                    img_src = img.get_attribute('src')
                    url_href = url.get_attribute('href')  # href 속성 가져오기
                    if title_text:  # 제목이 비어 있지 않을 때만 출력
                        print('-' * 50)
                        print(f"{collected_count + 1}. 강의 제목: {title_text}")
                        print(f"   이미지 URL: {img_src}")
                        print(f"   강의 링크: {url_href}")
                        collected_count += 1
                else:
                    break  # 원하는 개수에 도달하면 루프 종료

    except Exception as e:
        print(f"오류 발생: {e}")
        break

# 드라이버 종료
driver.quit()
