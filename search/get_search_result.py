from GUI import searchResult
from selenium import webdriver
import pandas as pd

def click_search_button(driver):
    '''입력한 검색 조건을 가지고 검색 버튼을 클릭하는 함수'''
    ############################################
    # 모든 항목이 입력되었을 때, 검색 버튼을 누름
    xpath = "//button[@id='btn_search']"
    driver.find_element_by_xpath(xpath).click()

def parse_search_result(driver, category):
    '''검색 결과를 2차원 리스트로 변환하는 함수'''
    ############################################
    # 검색 결과를 WebElement로 가져와 String으로 형변환 후 필요한 항목만 남기고 결과 리스트에 추가하여 반환
    return_result = []

    # 검색 결과 전체에 해당하는 항목을 xpath에 저장
    xpath = "//table[@id='mjLctTmtblDscTbl']/tbody/tr"
    container = driver.find_elements_by_xpath(xpath)

    # 검색 결과가 있는지 확인 -> 결과가 없어 비어있는 리스트의 경우 함수 종료
    if container[0].text == '조회된 데이터가 없습니다.':
        print('검색된 항목이 없습니다. 다시 시도하세요.')
        return None

    for search_result_raw in container:
        # 열 목록 저장
        list_result = ['' for x in range(14)]
        '''
        list_result = ['학년', '이수구분', '교과목번호', '교과목명', '분반',
                        '1단계', '2단계', '3단계', '4단계', '원어',
                        '학점(설계학점)', '교강사', '요일/교시/강의실', '수업방식 및 비고']
        '''

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
        
        # 2) 이수구분
        for word in search_result.split():
            if word.isdigit() == True:
                index = search_result.split().index(word)
                word = search_result.split()[index + 1]
                if word == 'POSE(Open':
                    search_result = search_result.replace('POSE(Open source', 'POSE(Opensource')
                    word = search_result.split()[index + 1]
                list_result[1] = word
                break

        # 3) 교과목번호, 교과목명, 분반
        full_classname = ''
        for word in search_result.split():
            index = search_result.split().index(word)
            if word == list_result[1]: # 처음 숫자인 부분은 학년 항목이므로 이를 확인하여 건너뜀        
                list_result[2] = search_result.split()[index + 1]
                if search_result.split()[index + 3].isdigit() == False:
                    full_classname = search_result.split()[index + 2] + ' ' + search_result.split()[index + 3]
                    list_result[3] = full_classname.replace(' ', '')
                    
                    search_result = search_result.replace(full_classname, full_classname.replace(' ', ''))

                    list_result[4] = search_result.split()[index + 3]
                    break
            
                list_result[3] = search_result.split()[index + 2]
                list_result[4] = search_result.split()[index + 3]
                break

        # 4) 학점 및 교강사
        # 학점 부분을 찾으면 되는데 이때는 ( 문자가 포함되어 있는 요소를 찾으면 됨
        slicing_index = search_result.split().index(list_result[4])
        if '(' in list_result[1]:
            slicing_index = search_result.split().index(list_result[3])

        score_isAppended = False
        for word in search_result.split()[slicing_index + 1:]:
            if '(' in word:
                list_result[10] = word # 학점
                score_isAppended = True
                continue
            if score_isAppended == True:
                list_result[11] = word # 교강사
                if word == search_result.split()[-1]:
                    break
                # 교강사명이 2어절인 경우 뒷부분까지 붙여넣기
                elif '~' not in search_result.split()[search_result.split().index(list_result[11]) + 1]:
                    list_result[11] += search_result.split()[search_result.split().index(list_result[11]) + 1]
                    break
                else:
                    break

        # 5) 거리두기 단계 및 원어강의 여부
        index = search_result.split().index(list_result[2])
        distance_list = ['원격수업', '원격강의', '대면수업']
        english_list = ['영어A', '영어B']

        #debug
        print(search_result)

        if full_classname != '':
            if full_classname.split()[0] == search_result.split()[index + 1]:
                index += 1

        if search_result.split()[index + 3] in distance_list:
            distance_list = search_result.split()[9:]
            start_index = 5

            for dist_item in distance_list:
                list_result[start_index] = dist_item
                print(dist_item, end=" ")
                start_index += 1

        index = search_result.split().index(list_result[10])
        if search_result.split()[index - 1] in english_list:
            list_result[9] = search_result.split()[index - 1]

        # 6) 요일/교시/강의실
        # ~문자가 있는 요소면 강의시간이므로 이걸 활용해 요일 자리를 탐색
        time_isFound = False
        for item in search_result.split():
            if ('~' in item) and ('[' not in item) and (']' not in item):
                index = search_result.split().index(item)
                time_isFound = True
                break

        # 7) 비고사항
        if time_isFound == True:
            list_result[12] = search_result.split()[index]
            
            if len(search_result.split()[index:]) > 1:
                for item in search_result.split()[index+1:]:
                    if '~' in item and ('[' not in item) and (']' not in item):
                        list_result[12] += '\n' + item
                        continue
                    list_result[13] += item

        #debug
        print(list_result)

        return_result.append(list_result)

    driver.close()

    return return_result