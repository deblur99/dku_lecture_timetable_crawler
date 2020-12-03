from selenium import webdriver

def click_search_button(driver):
    '''입력한 검색 조건을 가지고 검색 버튼을 클릭하는 함수'''
    ############################################
    # 모든 항목이 입력되었을 때, 검색 버튼을 누름
    xpath = "//button[@id='btn_search']"
    driver.find_element_by_xpath(xpath).click()

def parse_search_result(driver):
    '''검색 결과를 2차원 리스트로 변환하는 함수'''
    # 검색 결과를 WebElement로 가져와 String으로 형변환 후 필요한 항목만 남기고 결과 리스트에 추가하여 반환

    # 열 목록 저장
    list_columns = ['학년', '이수구분', '교과목번호', '교과목명', '분반',
                    '1단계', '1.5단계', '2단계', '2.5/3단계', '원어',
                    '학점(설계학점)', '교강사', '요일/교시/강의실', '수업방식 및 비고']

    ############################################
    # 검색 결과 전체에 해당하는 항목을 xpath에 저장
    xpath = "//table[@id='mjLctTmtblDscTbl']/tbody/tr"
    container = driver.find_elements_by_xpath(xpath)

    # 검색 결과가 있는지 확인 -> 결과가 없어 비어있는 리스트의 경우 함수 종료
    if container[0].text == '조회된 데이터가 없습니다.':
        print('검색된 항목이 없습니다. 다시 시도하세요.')
        return None

    search_results = [] # 검색 결과를 저장할 빈 리스트 생성
    for search_result in container: 
        # WebElement 객체 container에 저장된 2차원 리스트의 요소는 모두 WebElement 객체
        # 따라서, WebElement 객체가 저장한 값을 참조하려면 .text로 문자열 변환하여야 한다.
        # 문자열 변환 후 .split()으로 리스트로 변환한다.
        # 변환된 리스트인 search_result는 search_results에 추가하여 2차원 리스트를 만든다.
        search_result = search_result.text.split()
        search_results.append(search_result)

    # 검색 결과를 반환할 리스트 초기화
    return_result = []

    for search_result in search_results: # 2차원 리스트 형태의 검색 결과의 요소인 1차원 리스트를 반복
        # 반복문에 쓰이는 변수 초기화
        # index : find_result 리스트의 요소에 접근하기 위한 변수
        # find_result : 공백 문자열을 요소로 가지는 검색 결과 항목을 나타내는 리스트
        # grade_isFound : 학년 항목 탐색을 위한 플래그 변수 (수강조직 항목을 제외하기 위함)
        
        index = 0
        find_result = [' ' for x in range(len(list_columns))] #
        grade_isFound = False
        
        for col in search_result: # 1차원 리스트 search_result의 요소 (=각 항목) 반복
            if (index >= len(find_result)): # 모든 항목을 찾았는지 여부 검사하여, 모두 찾으면 반복문 탈출
                break

            # 수강조직 다음 부분 탐색 (수강조직은 목록에 추가하지 않음)
            if grade_isFound == False:
                if col.isdigit() == False: # 학년 이전 항목은 수강조직 항목이므로 문자열 -> 현재 항목 생략
                    continue
                else:
                    grade_isFound = True # 학년 항목을 발견하면 grade_isFound 플래그를 False로 변경해 조건문 탈출

            if col == '국문' or col == 'ENG': # 강의계획서 버튼 text부분 제거
                continue

            if index == 9: # 9번째 index에서
                if col == '영어A' or col == '영어B': # 원어강의 여부 검사 -> 원어강의가 아니면 해당 항목을 비어있는 상태로 남겨두기                
                    find_result[index] = col # 원어강의 항목을 리스트에 저장 후 index 1 증가하고 다음 col으로 넘어감
                    index += 1
                    continue
                else: # 원어강의 항목이 없을 경우 그대로 index 1 증가
                    index += 1
            
            # 변수 col의 값을 find_result의 index 요소에 저장하고, index 1 증가
            find_result[index] = col
            index += 1
        
        # 1차원 리스트 find_result에 모든 항목을 저장하면, find_result들의 2차원 리스트인 return_result에 추가
        return_result.append(find_result)


    # return_result의 0번째 요소에 list_columns 삽입
    return_result.insert(0, list_columns)

    # 창 닫기
    driver.close()

    # 2차원 리스트로 변환된 검색 결과를 반환
    return return_result