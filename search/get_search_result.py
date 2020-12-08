from selenium import webdriver

def click_search_button(driver):
    '''입력한 검색 조건을 가지고 검색 버튼을 클릭하는 함수'''
    ############################################
    # 모든 항목이 입력되었을 때, 검색 버튼을 누름
    xpath = "//button[@id='btn_search']"
    driver.find_element_by_xpath(xpath).click()

def parse_search_result(driver, category):
    '''검색 결과를 2차원 리스트로 변환하는 함수'''
    # 검색 결과를 WebElement로 가져와 String으로 형변환 후 필요한 항목만 남기고 결과 리스트에 추가하여 반환
    return_result = []

    # 열 목록 저장
    list_result = ['' for x in range(14)]
    '''
    list_result = ['학년', '이수구분', '교과목번호', '교과목명', '분반',
                    '1단계', '1.5단계', '2단계', '2.5/3단계', '원어',
                    '학점(설계학점)', '교강사', '요일/교시/강의실', '수업방식 및 비고']
    '''

    ############################################
    # 검색 결과 전체에 해당하는 항목을 xpath에 저장
    xpath = "//table[@id='mjLctTmtblDscTbl']/tbody/tr"
    container = driver.find_elements_by_xpath(xpath)

    # 검색 결과가 있는지 확인 -> 결과가 없어 비어있는 리스트의 경우 함수 종료
    if container[0].text == '조회된 데이터가 없습니다.':
        print('검색된 항목이 없습니다. 다시 시도하세요.')
        return None

    for search_result_raw in container: 
        # WebElement 객체 container에 저장된 2차원 리스트의 요소는 모두 WebElement 객체
        # 따라서, WebElement 객체가 저장한 값을 참조하려면 .text로 문자열 변환하여야 한다.
        # 문자열 변환 후 .split()으로 리스트로 변환한다.
        # 변환된 리스트인 search_result는 search_results에 추가하여 2차원 리스트를 만든다.
        search_result = search_result_raw.text.replace('\n', ' ').replace('국문 ', '').replace('ENG ', '')
        
        # 1) 학년 항목부터 문자열을 리스트로 변환
        for word in search_result.split():
            if word.isdigit() == True:
                list_result[0] = word
                break
        
        for word in search_result.split():
            if word.isdigit() == True:
                index = list_result.index(word)
                word = list_result[index + 1]
                if word == 'POSE(Open':
                    word += list_result[index + 2]
                list_result[1] = word
                break

        print(list_result)

        # 공백 문자를 모두 제거하여 열의 모든 요소를 띄어쓰기 없는 문자열로 만듦
        search_result = search_result.replace(' ', '')
        '''
        # 1) 학년의 앞 항목들을 제거하는 과정
        # 문자 단위로 비교하기
        # 숫자(=학년)이 나올 경우 반복문 탈출 후 숫자 앞부분을 문자열에서 제거
        before_grade = ''
        for chr in search_result:
            if chr.isdigit() == True:
                break
            else: before_grade += chr
        search_result = search_result.replace(before_grade, '')
        '''
        # 2) POSE 과목종류 중 띄어쓰기로 구분되어 있는 부분을 하나로 합쳐 저장하기
        list_columns[1] = word[1]
        pose = ''
        for word in list_result:
            if word == 'POSE(Open':
                pose = word
                index = list_result.index(word)
            elif word == 'source)':
                pose += word
                list_columns[1] = pose

        # 3) 강의시간 찾는 과정
        # 강의시간은 요일 앞에 있다.
        # 먼저 ) 부분의 뒷부분을 찾고, 월~토나 공백이 나올 때까지 chr을 name 문자열에 추가한다.
        days = ''
        for day in list_result:
            if list_result.index(day) > 3 and '~' in day:
                days += day + '\n'
        list_columns[12] = days
        
        passed_time = False
        for chr in search_result:
            if chr == '~':  # '~'를 찾으면 그 지점이 시간을 나타냄
                index = search_result.index(chr)
                passed_time = True
            if '~' in search_result[index] and passed_time == True:
                index = search_result.index(chr)
                try:
                    if search_result[index + 1] in ['월', '화', '수', '목', '금', '토', '일']:
                        continue
                    else:
                        break
                except IndexError:  # ) 부분이 문자열의 마지막 부분이라 예외가 발생했다면
                    break
        
        # 4) 원어강의 여부 검사
        if '영어A' not in list_result and '영어B' not in list_result:
            list_result.insert(9, '')
        # 5) 교강사명 추가
        name = ''
        if len(list_result) >= 12: # new
            for word in list_result:
                if word == list_result[11]:
                    name += word
                    if '~' not in list_result[12]:
                        name += list_result[12]
                        list_result.insert(11, name)
                        list_result.pop(12)
                    else:
                        break
        
        # 강의시간 추가
        time = ''
        if len(list_result) >= 13: # new
            for word in list_result:
                if (('~' in word) or ('(' in word)) and (list_result.index(word) >= 12 and list_result.index(word) <= 13):
                    time += '\n' + word
                    if list_result.index(word) == 13:
                        list_result.pop(list_result.index(word))
                
                list_result[12] = time.strip()
        
        # 수업방법 및 비고 추가
        misc = ''
        for word in list_result:
            if len(list_result) > 13:
                if not(('월' in word) or ('화' in word) or ('수' in word) or ('목' in word) or ('금' in word) or ('토' in word)):
                    misc += list_result[13]
                    list_result.pop(13)
                
        list_result.append(misc)
                    
        # 검색 결과를 반환할 리스트에 행 추가
        return_result.append(list_result)
    
    # 창 닫기
    driver.close()

    # debug
    return_result.append(list_columns)

    # 2차원 리스트로 변환된 검색 결과를 반환
    return return_result
'''    elif category == '교양':
       search_results = []
        for search_result_raw in container:
            search_results.append(search_result_raw.text.split())
        for search_result in search_results: # 2차원 리스트 형태의 검색 결과의 요소인 1차원 리스트를 반복
            # 반복문에 쓰이는 변수 초기화
            # index : find_result 리스트의 요소에 접근하기 위한 변수
            # find_result : 공백 문자열을 요소로 가지는 검색 결과 항목을 나타내는 리스트
            # grade_isFound : 학년 항목 탐색을 위한 플래그 변수 (수강조직 항목을 제외하기 위함)
            # time : 강의 시간을 저장하는 리스트로, 만약 주 2일 이상 수업일 경우 전체 결과 출력 시,
            #        두 번째 강의 시간이 그 다음 열로 밀리게 된다. 이를 방지하기 위하여, 
            #        강의 시간을 리스트에 저장하고, 모두 찾으면 공백 문자를 기준으로 join하여 문자열로 변환한다.
            # time_isFound : 강의 시간 탐색 전후를 나누는 분기점을 의미한다.

            index = 0
            find_result = [' ' for x in range(len(list_columns))]
            
            grade_isFound = False

            time = []

            for col in search_result: # 1차원 리스트 search_result의 요소 (=각 항목) 반복
                if (index == len(list_columns)): # 모든 항목을 찾았는지 여부 검사하여, 모두 찾으면 반복문 탈출
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

                if index == 12:
                    if '~' in col:
                        find_time = search_result.index(col)
                        time.append(col)
                        try:
                            if '~' in search_result[find_time + 1]:
                                continue
                        except IndexError:
                            pass

                    col = '\n'.join(time)
                
                if index < 13:
                    # 변수 col의 값을 find_result의 index 요소에 저장하고, index 1 증가
                    find_result[index] = col
                    index += 1

                elif index == 13:  # 마지막 항목인 수업방법 및 비고 부분 추가하기 (중간에 변경사항 부분 건너뛰기)
                    if '강사' not in search_result[-1]:
                        find_result[index] = search_result[-1]
                        break
                    print(search_result[-1])
                    

            # 1차원 리스트 find_result에 모든 항목을 저장하면, find_result들의 2차원 리스트인 return_result에 추가
            return_result.append(find_result)

        # 창 닫기
        driver.close()

        # 2차원 리스트로 변환된 검색 결과를 반환
        return return_result
'''