from search_module import *
# import GUI

'''
앞으로 만들어야 하는 것들
1) GUI 실행하는 함수
2) GUI에서 검색결과 받는 함수 -> 이미 완성됨
3) GUI로 값 전달하는 함수
4) GUI에서 선택한 행 가져오는 함수
'''
# 1) def execute_GUI(QWidget):

# 3) def send_lists_GUI(lists):

# 4) def retrieve_selected_row(QWidget):

# 2)
def retrieve_from_GUI():
    '''
    GUI로부터 사용자가 입력한 검색 조건 리스트를 전달받기

    * 값 가져오기 예시:
    items = ['year', 'semester', 'campus', 'category',
                 'section', 'college', 'major',
                 'grade', 'day', 'teacher', 'classname']
    '''
    
    # 전달받을 변수 search_conditions
    search_conditions = ['2020', '2학기', '죽전', '전공',
                    '', '사범대학', '', '', '', '',
                    '']

    # search_conditions의 요소를 세 부분으로 분할
    # essential_items: 필수적으로 지정해야 하는 검색 조건 리스트
    # additional_items: 선택적으로 지정하는 검색 조건 리스트
    # classname : 검색어로 입력할 교과목명
    essential_items = search_conditions[:4]
    additional_items = search_conditions[4:len(search_conditions)-1]
    classname = search_conditions[-1]

    # 각 항목을 3분할 후, 2차원 리스트 형태로 main.py로 반환
    return [essential_items, additional_items, classname]