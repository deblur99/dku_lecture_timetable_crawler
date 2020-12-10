import csv, psutil, os, time

def write_csv(lists):
    # timetable.csv가 있는지 찾기
    filename = 'timetable' + '.csv'

    # 파일 삭제하기
    # 해당 파일이 존재할 경우 덮어쓰기 시도
    # 프로토타입에서는 콘솔창으로 띄우지만 완성본에서는 별도의 함수를 하나 만들어서 처리
    
    if os.path.isfile(filename):
        try:
            # prototype
            '''
            print('timetable.csv 파일이 이미 존재합니다. 덮어 쓰시겠습니까?')
            print('----------------------------------------')
            print('네 (숫자 1 입력. 현재 엑셀 프로그램이 실행 중이라면, 강제 종료됩니다!!!)')
            print('아니오 (숫자 2 입력)')
            decision = input('선택: ')
            if decision == '1':
                <for 문>
            elif decision == '2':   # 함수 종료
                print('파일을 삭제하지 않았으며 저장되지 않았습니다.')
                return None
            else:   # 1, 2 이외의 값을 입력한 경우 입력 반복하기
                print('잘못된 입력입니다. 다시 시도하세요.')
            '''

            # 현재 OS상에서 실행 중인 프로세스들 중 엑셀 프로그램이 실행 중이면
            # 엑셀 프로그램을 강제 종료하고 해당 파일 삭제
            for proc in psutil.process_iter(attrs=['name']):
                if proc.info['name'] == 'EXCEL.EXE':         # 엑셀 프로그램이 현재 실행중인지 검사 
                    os.system('taskkill /f /im EXCEL.EXE')   # 실행중이라면 프로그램 강제 종료
                    time.sleep(0.005)                        # 1ms 동안 대기 -> 곧바로 파일을 삭제하면 오류 발생
                    os.system('taskkill /f /im EXCEL.EXE')
                    time.sleep(0.005)
            os.remove(filename)
               
        # 파일 삭제에 실패하면 NotImplementedError 예외 발생 -> 함수 종료
        except NotImplementedError:
            print('파일 삭제 오류: 파일이 존재하지 않습니다.')
            return None
    
    # 파일 저장하기
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)   # writer 클래스에 대한 인스턴스 생성

        column_header = ['학년', '이수구분', '교과목번호', '교과목명', '분반',
                         '1단계', '1.5단계', '2단계', '2.5/3단계', '원어',
                         '학점(설계)', '교강사', '요일/교시/강의실', '수업방법 및 비고']
                         
        writer.writerow(column_header)

        for row in lists:
            writer.writerow(row) # 각 행들을 순회하며 csv 파일에 입력