import search_module
import receive_and_send
import export_csv

# execute_GUI(QWidget) -> GUI 실행하기

# 밑에 있는 코드들은 GUI가 작동중일 때만 동작할 것 (맨 마지막 csv 저장부분 앞까지 while문으로 감쌈)

# 최종적으로 선택된 과목들의 리스트를 my_timetable 변수에 저장
my_timetable = []

# GUI에서 검색 조건을 가져와서 get_conditions 변수에 저장
got_conditions = receive_and_send.retrieve_from_GUI()

# receive_and_send 모듈의 함수 select_search_condition를 호출하여
# 크롬 창을 연 후 webdriver를 반환하여 driver 변수에 저장
driver = search_module.open_window()

# 검색 조건 설정하기
search_module.select_search_condition(driver, got_conditions)

# 검색 후 검색 결과 가져와 result 변수에 저장
result = search_module.get_search_result(driver, got_conditions[0][-1])

# GUI에 검색 결과 보내기
# send_lists_GUI(lists)

# GUI로 전달한 2차원 리스트 중에서 사용자가 선택한 행 한 개를 받아 my_timetable 변수에 추가
# row = retrieve_selected_row(QWidget)
# my_timetable.append(row)

# 완성된 강의시간표를 csv 파일로 저장 -> 저장하고 프로그램 종료하기
# export_csv.write_csv(my_timetable)
export_csv.write_csv(result)