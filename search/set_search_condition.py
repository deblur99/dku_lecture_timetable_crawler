from selenium import webdriver

def exception_handler_during_search():
    '''검색 조건을 잘못 설정했을 때 호출되는 함수'''
    print('검색 조건을 올바르게 설정하지 않았습니다. 다시 시도하세요.')
    return None

def search_by_essential_items(driver, items):
    '''
    검색에 필수적으로 요구되는 검색 조건을 지정하는 함수\n
    검색하는 항목: 연도, 학기, 캠퍼스, 과목종류
    '''
    # 검색 조건을 나타낸 부분이 가려주는 'display: none;' 속성이 있는데,
    # 이 부분을 모든 항목에서 제거하는 코드
    # 1) html 태그 중 style 태그의 속성이 display=none인 항목을 가리키는 문자열을 변수 xpath에 저장
    # 2) webdriver 클래스의 메서드 find_elements_by_xpath()는 xpath가 html 태그의 특정 부분을 가리키는 지점을 찾아
    # 3) WebElement 객체로 반환한다. container 변수에 해당 객체를 저장한다.
    xpath = "//select[@style='display: none;']"         
    container = driver.find_elements_by_xpath(xpath)    

    # driver의 메서드 execute_script로 html 태그의 속성인 display=none을 display=block으로 변경
    for i in container:
        driver.execute_script("arguments[0].style.display = 'block';", i)

    ##############################################################################################################
    # 여기부터는 각 항목 (학년, 이수구분, 교과목 번호, 교과목명, 분반, 사회적거리두기(1단계, 1.5단계, 2단계, 2.5/3단계),#
    #                    원어강의 여부, 학점(설계), 교강사명, 요일/교시/강의실, 변경내역, 수업방법 및 비고(분반))들을  #
    # 저장하는 과정이다.                                                                                          #
    # 하단 코드에 관한 주석을 서술하기에 앞서, 각 항목을 찾는 순서는 모두 동일하다.                                    #
    # 1) xpath 값 저장하기                                                                                        #
    # 2) webdriver의 메서드 find_elements_by_xpath()로 html 태그 내부에서 xpath에 해당하는 태그를 찾아,              #
    #    WebElement 속성으로 반환한 값을 변수 container에 저장                                                      #
    # 3) 각 항목에 해당하는 선택지의 목록을 딕셔너리 형태로 정리한 후                                                 #
    ##############################################################################################################
    # 연도를 나타내는 부분의 WebElement 객체로 반환하여 변수에 저장
    xpath = "//input[@id='yy']"
    container = driver.find_element_by_xpath(xpath)

    year = items[0]
    container.clear()
    container.send_keys(year)

    driver.implicitly_wait(5)

    # 학기를 나타내는 부분의 WebElement 객체로 반환하여 변수에 저장
    xpath = "//select[@id='semCd']/option"
    container = driver.find_elements_by_xpath(xpath)

    # 사용자로부터 1학기 하계계절 2학기 동계계절 중 하나를 체크박스로 입력받아서 그것에 해당하는
    # 인덱스로 변환 후 리스트에서 해당 WebElement 객체를 참조
    # 0번째부터 4번쨰 순으로, 학기 -> 1학기 -> 하계계절 -> 2학기 -> 동계계절
    semester_list = {'학기': 0, '1학기': 1, '하계계절': 2, '2학기': 3, '동계계절': 4}

    # semester 
    semester = items[1]
    container[semester_list[semester]].click()

    driver.implicitly_wait(5)

    ############################################
    # 캠퍼스 선택하는 부분의 WebElement 객체 찾아 저장
    xpath = "//select[@id='lesnPlcCd']/option"
    container = driver.find_elements_by_xpath(xpath)

    # 사용자가 캠퍼스를 선택하면 그 선택값을 검색창에 반영
    campus_list = {'캠퍼스': 0, '죽전': 1, '천안': 2}

    campus = items[2]
    container[campus_list[campus]].click()

    driver.implicitly_wait(5)

    ############################################
    # 교양과 전공 중 하나를 선택하는 부분의 WebElement 객체 찾아 저장
    # 교양 또는 전공 중 한 가지 항목 선택 -> 0은 교양, 1은 전공

    xpath = "//input[@name='qrySxn']"
    container = driver.find_elements_by_xpath(xpath)

    category_list = {'교양': 0, '전공': 1}
    category = items[3]

    try:
        container[category_list[category]].click()    
    except KeyError:
        exception_handler_during_search()

    driver.implicitly_wait(5)
    return None

def search_by_additional_items(driver, items):
    '''
    검색에 필요한 부가적인 항목을 지정하는 함수\n
    검색하는 항목: 연도, 학기, 캠퍼스, 과목종류, 교과목명을 제외한 나머지
    (과목영역, 단과대명, 전공명, 요일, 학년, 교강사명)
    '''
    def search_by_section_name(driver, item):
        '''과목 영역 선택하는 부분의 WebElement 객체 찾아 저장'''
        xpath = "//select[@id='curiCparCd']/option"
        container = driver.find_elements_by_xpath(xpath)

        # 과목 영역 목록을 0부터 대응하여 딕셔너리로 저장
        # 사용자가 과목 영역을 선택하면 그 영역에 대응하는 정수값을 가져와 검색창에 반영
        index = 1
        section_with_subject = dict()
        section_with_subject['영역'] = 0

        for section in container:
            section_with_subject[section.text] = index
            index += 1
        
        try:
            container[section_with_subject[item]].click()  # 검색창에 반영하기
        except KeyError:
            exception_handler_during_search()

        driver.implicitly_wait(5)

    def search_by_college_name(driver, item):
        '''단과대 선택하는 부분의 WebElement 객체 찾아 저장'''
        xpath = "//select[@id='colgCd']/option"
        container = driver.find_elements_by_xpath(xpath)

        # 단과대 목록을 0부터 대응하여 딕셔너리로 저장
        index = 0
        college_list = dict()
        for college in container:
            college_list[college.text] = index
            index += 1

        try:
            container[college_list[item]].click()
        except KeyError:
            exception_handler_during_search()

        driver.implicitly_wait(5)

    def search_by_major_name(driver, item):
        '''전공명 선택하는 부분의 WebElement 객체 찾아 저장'''
        xpath = "//select[@id='dpmtCd']/option"
        container = driver.find_elements_by_xpath(xpath)

        # 전공명 목록을 0부터 대응하여 딕셔너리로 저장
        index = 0
        major_list = dict()
        for major in container:
            major_list[major.text] = index
            index += 1

        try:
            container[major_list[item]].click()
        except KeyError:
            exception_handler_during_search()

        driver.implicitly_wait(5)

    def search_by_day(driver, item):
        '''요일 선택하는 부분의 WebElement 객체 찾아 저장'''
        xpath = "//select[@id='mjDowCd']/option"
        container = driver.find_elements_by_xpath(xpath)

        # 요일 목록을 0부터 대응하여 딕셔너리로 저장
        index = 1
        day_list = dict()
        day_list['요일'] = 0
        for day in container:
            day_list[day.text] = index
            index += 1

        try:
            container[day_list[item]].click()
        except KeyError:
            exception_handler_during_search()

        driver.implicitly_wait(5)

    def search_by_grade(driver, item):
        '''학년 선택하는 부분의 WebElement 객체 찾아 저장'''

        if item == '학년':
            return

        xpath = "//select[@id='grade']/option"
        container = driver.find_elements_by_xpath(xpath)

        try:
            container[int(item)].click() # container의 2번째 요소인 '2학년'에 접근하여 클릭한다
        except KeyError:
            exception_handler_during_search()

        driver.implicitly_wait(5)

    def search_by_teacher_name(driver, item):
        '''교강사명 입력 부분의 WebElement 객체 찾아 저장'''

        if item == '교강사명':
            return

        xpath = "//input[@id='pfltNm']"
        container = driver.find_element_by_xpath(xpath)

        # 사용자로부터 입력받은 교강사명을 검색창에 입력
        container.clear()
        container.send_keys(item)

        driver.implicitly_wait(5)

    # 누락된 검색조건 탐색
    new_list = []
    for item in items:
        if item == '':
            new_list.append(None)
            continue
        new_list.append(item)

    # new_list의 요소가 None이 아닌 경우에만 해당 함수 실행
    for i in range(len(new_list)):
        if new_list[i] != None:
            if i == 0:
                search_by_section_name(driver, new_list[0])
            elif i == 1:
                search_by_college_name(driver, new_list[1])
            elif i == 2:
                search_by_major_name(driver, new_list[2])
            elif i == 3:
                search_by_day(driver, new_list[3])
            elif i == 4:
                search_by_grade(driver, new_list[4])
            elif i == 5:
                search_by_teacher_name(driver, new_list[5])
    
    return None

def search_by_class_name(driver, item):
    if item == '교강사명':
        return

    xpath = "//input[@id='mjSubjKnm']"
    driver.find_element_by_xpath(xpath).send_keys(item)
    
    return