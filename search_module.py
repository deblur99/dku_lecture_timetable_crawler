# 사용할 모듈 목록과 기능
# sys.import : 현재 디렉토리 참조
# selenium.webdriver : 웹 크롤링의 핵심 모듈인 selenium의 클래스와 함수 중, 클래스인 webdriver 가져오기
#                      webdriver 클래스는 Chromedriver 프로그램을 실행하여, 브라우저 창을 제어하는 데 사용함

from sys import path
from selenium import webdriver
from search.set_search_condition import *
from search.get_search_result import *

def open_window():
    '''
    webdriver 클래스의 하위 클래스인 Chrome 클래스로,\n
    객체 생성 후 크롬 창을 열어, 강의시간표 페이지를 띄우는 함수
    
    * 크롬 버전 87 이상이 설치되어 있어야 실행 가능 -> 업데이트 필수
    '''
    driver = webdriver.Chrome(path[0] + '/chromedriver.exe')
    url = 'http://webinfo.dankook.ac.kr/tiac/univ/lssn/lpci/views/lssnPopup/tmtbl.do'   # 단국대 포털 종합강의시간표 URL
    driver.implicitly_wait(5) # 5ms 동안 대기
    driver.get(url)           # webdriver 클래스의 메서드 get()으로 크롬 창 실행하고 url로 페이지 접근
    return driver             # webdriver 객체를 main.py로 반환

def select_search_condition(driver, args):
    search_by_essential_items(driver, args[0])
    search_by_additional_items(driver, args[1])
    search_by_class_name(driver, args[2])
    return None

def get_search_result(driver):
    click_search_button(driver)
    result = parse_search_result(driver)
    return result