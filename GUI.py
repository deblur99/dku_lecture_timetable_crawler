import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTableWidget, QTableWidgetItem, QDesktopWidget, QPushButton, QHBoxLayout, QVBoxLayout, QCheckBox, QLabel, QComboBox, QLineEdit, QGridLayout, QCheckBox, QRadioButton, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel, qPixelFormatCmyk
import json
import search_module
import export_csv

search_result = []
save_into_file = []

# 크롤러 메인 함수 정의하는 부분
def search(got_conditions):
    driver = search_module.open_window()

    essential_items = got_conditions[:4]
    additional_items = got_conditions[4:len(got_conditions)-1]
    classname = got_conditions[-1]
    
    # 각 항목을 3분할 후, 2차원 리스트 형태로 main.py로 반환
    got_conditions = [essential_items, additional_items, classname]

    search_module.select_search_condition(driver, got_conditions)
    result = search_module.get_search_result(driver, got_conditions[0][-1])
    return result

#메인 검색창 클래스
class searchOption(QWidget):
    def __init__(self):
        super().__init__()
        
        #사용자로부터 받은 검색 조건을 저장할 리스트
        self.searchList = ['' for i in range(11)]

        #변수 선언 및 기본 값 설정
        self.clickedSemester = '2학기'
        self.clickedCampus = '죽전'
        self.clickedDomain = '교양'
        self.clickedType = '영역'
        self.clickedCollege = '단과대명'
        self.clickedMajor = '전공명'
        self.inputYear = '2021'
        self.inputSubject = '교과목명'
        self.clickedDay = '요일'
        self.clickedGrade = '학년'
        self.inputTeacher = '교강사명'

        #각 캠퍼스의 단과대학과 전공명을 {단과대: [전공1, 전공2 ,...]}형식의 딕셔너리 형태로 선언 
        self.majorDic = {'단과대학':['전공명'], '----죽전----': ['전공명'], '문과대학': ['전공명', '국어국문학과', '사학과', '철학과', '영미인문학과', '중어중문학과', '일어일문학과', '영어영문학과'], 
        '법과대학': ['전공명', '법학과'], '사회과학대학': ['전공명', '정치외교학과', '행정학과', '도시계획부동산학부', '도시지역계획학전공', '부동산학전공', '커뮤니케이션학부', '저널리즘전공', '영상콘텐츠전공', '광고홍보전공', '응용통계학과', '상담학과',], 
        '경영경제대학': ['전공명', '경제학과', '무역학과', '경영학부', '경영학전공', '회계학전공', '산업경영학과(야)', '국제학부', '국제경영학전공'], 
        '상경대학':['전공명'], '건축대학':['전공명'], '공과대학': ['전공명', '전자전기공학부', '전자전기공학전공', '고분자공학전공', '파이버융합소재공학전공', '고분자공학과', '파이버시스템공학과', '소프트웨어학과', '응용컴퓨터공학과', '토목환경공학과', '기계공학과', '화학공학과', '건축학전공', '건축공학전공'], 
        'SW융합대학': ['전공명', '소프트웨어학과', '컴퓨터공학과', '모바일시스템공학과', '정보통계학과', '산업보안학과', 'SW융합바이오전공', 'SW융합콘텐츠전공', 'SW융합경제경영전공', 'SW융합법학전공', '글로벌SW융합전공'],
        '사범대학': ['전공명', '한문교육과', '특수교육과', '특수교육과 초등특수교육', '특수교육과 중등특수교육', '수학교육과', '과학교육과', '과학교육과 물리전공', '과학교육과 생물전공', '체육교육과', '교직교육과'],
        '음악·예술대학':['전공명', '도예과', '커뮤니케이션디자인전공', '패션산업디자인전공', '연극전공', '영화전공', '뮤지컬전공', '무용과', '기악전공', '기악전공(피아노), 기악전공(현악)', '성악전공', '작곡전공', '국악전공'], '예술디자인대학': ['전공명'],
        '음악대학':['전공명'], '국제대학': ['모바일시스템공학과', '영상 연기 &제작 전공'], '국제학부':['전공명'], '다산링크스쿨': ['전공명'], '자연과학대학': ['전공명'], '연계전공(학부)': ['전공명'],
        '----천안----': ['전공명'], '국제학부': ['전공명', '글로벌경영학전공'], '외국어대학': ['전공명', '중국학전공', '일본학전공', '몽골학전공', '중동학전공', '독일학전공', '프랑스학전공', '스페인중남미학전공', '러시아학전공', '포르투갈브라질학전공', '영어과'],
        '인문과학대학': ['전공명'], '공공인재대학': ['전공명', '경영학과(야)'], '행정복지대학': ['전공명', '법무행정학과'], '경상대학': ['전공명', '국제통상학부', '경제학전공', '무역학전공', '경영학부', '경영학전공', '회계학전공'],
        '과학기술대학': ['전공명', '수학과', '물리학과', '화학과', '식품영양학과', '미생물학전공', '생명과학전공', '신소재공학과', '식품공학과', '에너지공학과', '경영공학과'],
        '자연과학대학': ['전공명', '분자생물학과', '생명과학과'], '융합기술대학': ['전공명', '산업공학과', '디스플레이공학과', '원자력융합공학과'], '공학대학': ['전공명', '응용화학공학과', '컴퓨터과학과', '멀티미디어공학과', '전자공학과'], 
        '생명공학대학': ['전공명', '식량생명공학전공', '동물자원학전공', '환경원예학전공', '녹지조경학전공', '의생명공학부 의생명공학전공', '제약공학과'], '예술대학': ['전공명', '미술학부 공예전공', '미술학부 동양화전공', '미술학부 서양화전공', '미술학부 조소전공', '문예창작과', '뉴뮤직과'], 
        '스포츠과학대학': ['전공명', '생활체육학과', '스포츠경영학과', '운동처방재활전공', '국제스포츠전공', '태권도전공'], '의과대학': ['전공명', '의예과', '의학과'], 
        '보건복지대학': ['전공명', '공공정책학과', '공공정책학과(야)', '사회복지학과', '해병대군사학과', '환경자원경제학과', '임상병리학과', '물리치료학과', '보건행정학과', '치위생학과', '심리치료학과'], '간호대학': ['전공명', '간호학과'], '치과대학': ['전공명', '치의예과', '치의학과'], 
        '약학대학': ['전공명', '약학과'], '연계전공(학부)': ['전공명', '메디바이오산업기술학연계전공', '토탈분석기기융합학연계전공', '식의약향장학연계전공']}
        
        #검색 결과에서 선택한 항목을 저장할 빈 리스트 선언
        self.savedList = []

        self.initUI()

    #검색창 화면 설정
    def initUI(self):

        #화면 상단 타이틀
        title = QLabel('종합강의시간표 검색')
        title.setAlignment(Qt.AlignHCenter)
        font = title.font()
        font.setFamily('10X10')
        font.setBold(True)
        font.setPointSize(40)
        title.setFont(font)

        #화면 오른쪽 하단 검색버튼 생성
        searchbtn = QPushButton('search', self)

        #그리드 레이아웃에 각각 위젯 추가
        layout = QGridLayout()
        layout.setSpacing(20)
        layout.addWidget(self.year(), 0, 0)
        layout.addWidget(self.semester(), 0, 1)
        layout.addWidget(self.campus(), 0, 2)
        layout.addWidget(self.liberalArts(), 1, 0)
        layout.addWidget(self.major(), 1, 1)
        layout.addWidget(self.option(), 1, 2)
        layout.addWidget(self.subject(), 3, 0, 1, 3)
        
        #QHBoxLayOut을 사용하여 검색버튼 여백 설정
        hbox = QHBoxLayout()
        hbox.addStretch(20)
        hbox.addWidget(searchbtn)
        hbox.addStretch(1)

        #QVBoxLayout을 사용하여 화면 상단 타이틀과 위젯레이아웃, 검색버튼 수직배열(레이아웃 중첩) 
        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addWidget(title)
        vbox.addStretch(2)
        vbox.addLayout(layout)
        vbox.addStretch(2)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        #화면의 레이아웃을 vbox 객체로 설정
        self.setLayout(vbox)

        #검색 버튼이 눌렸을때 함수실행
        searchbtn.clicked.connect(lambda: self.schbtn_clicked(title))
        self.dialog = QDialog()

        #창 설정
        self.setWindowTitle('timetable')
        self.resize(1000,625)
        self.center() #center() 메서드로 창이 화면의 가운데에 위치하게 함
        self.show()

    #검색버튼 연결 함수
    def schbtn_clicked(self, title):
        #searchList에 각각의 조건들을 추가
        self.searchList = [self.inputYear, self.clickedSemester, self.clickedCampus, self.clickedDomain, self.clickedType, 
        self.clickedCollege, self.clickedMajor, self.clickedDay, self.clickedGrade, self.inputTeacher, self.inputSubject]

        try:
            if self.clickedDomain == '교양':
                pass
            elif self.clickedCollege == '단과대명' or self.clickedMajor == '전공명':
                raise ValueError
            
            global search_result # 검색 결과 리스트를 저장할 변수는 전역 변수로 참조함

            search_result = search(self.searchList)

        except ValueError or KeyError:
            print('올바르지 않은 검색 조건입니다.')
                                        
        #검색결과 창 실행 (새로운 클래스)
        dlg = searchResult()
        dlg.exec_()
    

    #연도 위젯
    def year(self):
        #Groupbox로 연도 표현
        groupbox = QGroupBox('연도')
        #텍스트 창 생성
        self.yr = QLineEdit(self)
        #텍스트창에 내용 입력시 함수 연결
        self.yr.textChanged[str].connect(self.yearInput)

        #hbox객체를 생성하여 groupbox내에서 위젯 배치
        hbox = QHBoxLayout()
        hbox.addWidget(self.yr)
        #groupbox의 레이아웃을 hbox로 설정
        groupbox.setLayout(hbox)

        return groupbox
    
    #연도 입력시 연결되는 함수
    def yearInput(self, text):
        #입력된 텍스트(연도)를 inputYear에 저장
        self.inputYear = text

    #학기 선택 위젯
    def semester(self):
        #Groupbox로 학기 표현
        groupbox = QGroupBox('학기')

        #학기의 각 항목들을 RadioButton으로 생성
        #각 버튼이 선택되었을 때 함수 연결
        self.sem1 = QRadioButton('1학기')
        self.sem1.clicked.connect(self.semesterClicked)
        self.sem2 = QRadioButton('여름학기')
        self.sem2.clicked.connect(self.semesterClicked)
        self.sem3 = QRadioButton('2학기')
        self.sem3.clicked.connect(self.semesterClicked)
        self.sem4 = QRadioButton('겨울학기')
        self.sem4.clicked.connect(self.semesterClicked)

        #기본으로 1학기 버튼이 선택되어있게 설정
        self.sem3.setChecked(True)

        #hbox객체를 생성하여 groupbox내에서 각 버튼 배치
        hbox = QHBoxLayout()
        hbox.addWidget(self.sem1)
        hbox.addWidget(self.sem2)
        hbox.addWidget(self.sem3)
        hbox.addWidget(self.sem4)
        #groupbox의 레이아웃을 hbox로 설정
        groupbox.setLayout(hbox)

        return groupbox

    #학기 버튼 선택시 연결되는 함수
    def semesterClicked(self):
        if self.sem1.isChecked():
            #clickedSemester에 선택된 학기의 텍스트를 반환하여 저장
            self.clickedSemester = self.sem1.text() 
        elif self.sem2.isChecked():
            self.clickedSemester = self.sem2.text()
        elif self.sem3.isChecked():
            self.clickedSemester = self.sem3.text()
        else:
            self.clickedSemester = self.sem4.text()

    #캠퍼스 위젯
    def campus(self):
        #Groupbox로 캠퍼스 표현
        groupbox = QGroupBox('캠퍼스')

        #캠퍼스의 각 항목들을 RadioButton으로 생성
        self.cps1 = QRadioButton('죽전')
        #기본으로 죽전 버튼이 선택되어있게 설정
        self.cps1.setChecked(True)
        #각 버튼이 선택되었을 때 함수 연결
        self.cps1.clicked.connect(self.campusClicked)
        self.cps2 = QRadioButton('천안')
        self.cps2.clicked.connect(self.campusClicked)

        #hbox객체를 생성하여 groupbox내에서 각 버튼 배치
        hbox = QHBoxLayout()
        hbox.addWidget(self.cps1)
        hbox.addWidget(self.cps2)
        #groupbox의 레이아웃을 hbox로 설정
        groupbox.setLayout(hbox)   

        return groupbox
    
    #캠퍼스 버튼 선택시 연결되는 함수
    def campusClicked(self):
        if self.cps1.isChecked():
            #clickedCampus에 선택된 학기의 텍스트를 반환하여 저장
            self.clickedCampus = self.cps1.text()
        else:
            self.clickedCampus = self.cps2.text()

    #교양 위젯
    def liberalArts(self):
        #Groupbox로 교양조건 표현
        self.groupbox = QGroupBox('교양')
        #groupbox 자체에 체크박스를 설정하여 체크했을때만 하위 항목 선택 가능하게함
        self.groupbox.setCheckable(True)
        self.groupbox.setChecked(False)

        #교양영역에 대한 combobox생성, 각각 항목 추가
        self.dm = QComboBox(self)
        self.dm.addItem('영역')
        self.dm.addItem('공통교양')
        self.dm.addItem('--자기관리역량')
        self.dm.addItem('--사회봉사교과')
        self.dm.addItem('--종합적사고역량')
        self.dm.addItem('--자원·정보·기술활용역량')
        self.dm.addItem('--사고와표현역량')
        self.dm.addItem('--세계시민역량')
        self.dm.addItem('--자연/환경/기술')
        self.dm.addItem('--문학/역사/철학')
        self.dm.addItem('--정치/경제/사회･심리')
        self.dm.addItem('--수학/물리/화학/생물')
        self.dm.addItem('--문화/예술/체육')
        self.dm.addItem('평생교육사(필수)')
        self.dm.addItem('문화예술교육사')
        self.dm.addItem('교직')
        self.dm.addItem('군사학')
        self.dm.addItem('공통교양')
        self.dm.addItem('자유교과')
        #항목이 선택되었을 때 함수연결
        self.dm.activated[str].connect(lambda: self.LAClicked(self.dm))
       
        #vbox객체를 생성하여 groupbox내에서 위젯 배치
        vbox = QVBoxLayout()
        vbox.addWidget(self.dm)
        #groupbox의 레이아웃을 vbox로 설정
        self.groupbox.setLayout(vbox)

        return self.groupbox
    
    #교양영역 선택시 연결되는 함수
    def LAClicked(self, text):
        #clickedType에 선택된 교양영역의 텍스트를 반환하여 저장
        self.clickedType = text.currentText()
        self.clickedDomain = '교양'
    
    #전공 위젯
    def major(self):
        #groupbox로 전공조건 표현
        self.groupbox = QGroupBox('전공')
        #groupbox 자체에 체크박스를 설정하여 체크했을때만 하위 항목 선택 가능하게함
        self.groupbox.setCheckable(True)
        self.groupbox.setChecked(False)
        
        self.model = QStandardItemModel()

        #단과대명 combobox생성
        self.clg = QComboBox(self)
        self.clg.setModel(self.model)
        #전공명 combobox생성
        self.mj = QComboBox(self)
        self.mj.setModel(self.model)
        
        #생성자에서 정의한 전공목록의 딕셔너리에서 값을 가져와서 combobox에 추가
        for k, v in self.majorDic.items():
            college = QStandardItem(k)
            self.model.appendRow(college)
            for value in v:
                major = QStandardItem(value)
                college.appendRow(major)

        #선택된 단과대명에 따른 전공명만 보이게 함
        self.clg.currentIndexChanged.connect(self.updateCollege)
        self.updateCollege(0)

        #각 combobox에서 항목 선택시 함수 실행
        self.clg.activated[str].connect(lambda: self.clgClicked(self.clg))
        self.mj.activated[str].connect(lambda: self.MJClicked(self.mj))

        #단과대 combobox와 전공 combobox를 vbox객체로 수직 배치
        vbox = QVBoxLayout()
        vbox.addWidget(self.clg)
        vbox.addWidget(self.mj)
        #groupbox의 레이아웃을 vbox로 설정
        self.groupbox.setLayout(vbox)

        return self.groupbox

    #선택된 단과대명에 따른 전공명만 보이게 하는 함수
    def updateCollege(self, index):
        indx = self.model.index(index, 0, self.clg.rootModelIndex())
        self.mj.setRootModelIndex(indx)
        self.mj.setCurrentIndex(0)

    #단과대명 combobox와 연결된 함수
    def clgClicked(self, text):
        #clickedCollege에 선택된 학기의 텍스트를 반환하여 저장
        self.clickedCollege = text.currentText()
        #clickedDomain에 '전공' 저장
        self.clickedDomain = '전공'

    #전공명 combobox와 연결된 함수
    def MJClicked(self, text):
        #clickedCollege에 선택된 학기의 텍스트를 반환하여 저장
        self.clickedMajor = text.currentText()
        #clickedDomain에 '전공' 저장
        self.clickedDomain = '전공'

    #교과목명 위젯
    def subject(self):
        #Groupbox로 교과목명 표현
        groupbox = QGroupBox('교과목명')
        #텍스트 창 생성
        self.sbj = QLineEdit(self)
        #텍스트창에 내용 입력시 함수 연결
        self.sbj.textChanged[str].connect(self.subjectInput)
        
        #hbox객체를 생성하여 groupbox내에서 위젯 배치
        hbox = QHBoxLayout()
        hbox.addWidget(self.sbj)
        #groupbox의 레이아웃을 hbox로 설정
        groupbox.setLayout(hbox)

        return groupbox
    
    #교과목명 입력시 연결되는 함수
    def subjectInput(self, text):
        #입력된 교과목명을 inputSubject에 저장
        self.inputSubject = text

    #이외의 나머지 검색옵션 위젯
    def option(self):
        #Groupbox로 검색옵션 표현
        groupbox = QGroupBox('기타 옵션')

        #요일에 대한 combobox 생성
        self.day = QComboBox(self)
        #각 항목 추가
        self.day.addItem('요일')
        self.day.addItem('일요일')
        self.day.addItem('월요일')
        self.day.addItem('화요일')
        self.day.addItem('수요일')
        self.day.addItem('목요일')
        self.day.addItem('금요일')
        self.day.addItem('토요일')
        #combobox에서 항목 선택시 함수 실행
        self.day.activated[str].connect(lambda: self.dayClicked(self.day))

        #학년에 대한 combobox 생성
        self.grade = QComboBox(self)
        #각 항목 추가
        self.grade.addItem('학년')
        self.grade.addItem('1')
        self.grade.addItem('2')
        self.grade.addItem('3')
        self.grade.addItem('4')
        self.grade.addItem('5')
        self.grade.addItem('6')
        #combobox에서 항목 선택시 함수 실행
        self.grade.activated[str].connect(lambda: self.gradeClicked(self.grade))

        #설명 라벨
        prof = QLabel('교강사명', self)
        #텍스트 창 생성
        self.tch = QLineEdit(self)
        #텍스트창에 내용 입력시 함수 실행
        self.tch.textChanged[str].connect(self.teacherInput) 

        #vbox객체를 생성하여 groupbox내에서 각 위젯 배치
        vbox = QVBoxLayout()
        vbox.addWidget(self.day)
        vbox.addWidget(self.grade)
        vbox.addWidget(prof)
        vbox.addWidget(self.tch)
        #groupbox의 레이아웃을 vbox로 설정
        groupbox.setLayout(vbox)

        return groupbox
    
    #요일 항목 선택시 연결되는 함수
    def dayClicked(self, text):
        #clickedDay에 선택된 요일의 텍스트를 반환하여 저장
        self.clickedDay = text.currentText()

    #학년 항목 선택시 연결되는 함수
    def gradeClicked(self, text):
        #clickedGrade에 선택된 요일의 텍스트를 반환하여 저장
        self.clickedGrade = text.currentText()

    #교강사명 입력시 연결되는 함수
    def teacherInput(self, text):
        #입력된 교강사명을 inputSubject에 저장
        self.inputTeacher = text

    #창을 실행 모니터화면의 가운데로 정렬하는 함수
    def center(self):
        qr = self.frameGeometry() #frameGeometry() 메서드로 창의 위치와 크기정보 가져오기
        cp = QDesktopWidget().availableGeometry().center() #사용되는 모니터 화면의 가운데 위치 파악
        qr.moveCenter(cp) #창의 직사각형 위치를 화면의 중심위치로 이동
        self.move(qr.topLeft()) #현재 창을 화면의 중심으로 이동한 직사각형 qr의 위치로 이동, 현재 창의 중심이 화면의 중심과 일치하게됨

#검색결과를 띄워주는 두 번째 창, QDialog를 사용하여 생성
class searchResult(QDialog):
    def __init__(self):
        super().__init__()
        #__에서 가져온 검색결과리스트
        self.resultList = search_result
        '''
        검색 결과 리스트 예시
        [['2', '융합선택', '450170', '실험영화연구', '2', '병행강의', '병행강의', '온라인강의2', '온라인강의2', '', '3(0)', '나호원', '목5~10(체육B205)', ''], 
        ['3', '전공선택', '521220', '고급모바일실험2', '1', '병행강의', '병행강의', '병행강의', '온라인강의2', '영어A', '1(0)', '유시환', '목1~4(국제210)', ''], 
        ['2', '전공필수', '521200', '기초모바일실험2', '1', '전체대면', '전체대면', '전체대면', '온라인강의2', '영어A', '1(0)', '이현우', '금3~6(국제210)', ''], 
        ['3', '전공선택', '521220', '고급모바일 실험2', '1', '병행강의', '병행강의', '병행강의', '온라인강의2', '영어A', '1(0)', '유시환', '목1~4(국제210)', ''], 
        ['3', '전공필수', '472590', '고급FPGA실험', '1', '병행강의', '병행강의', '병행강의', '온라인강의2', '', '1(0)', '김규철', '화13~16(2공522)', ''], 
        ['3', '전공필수', '472590', '고급FPGA실험', '2', '병행강의', '병행강의', '병행강의', '온라인강의2', '', '1(0)', '김규철', '수15~18(2공522)', ''], 
        ['3', '전공필수', '472590', '고급FPGA실험', '3', '병행강의', '병행강의', '병행강의', '온라인강의2', '', '1(0)', '김규철', '목6~9(2공522)', ''], 
        ['3', '전공필수', '472590', '고급FPGA실험', '4', '병행강의', '병행강의', '병행강의', '온라인강의2', '', '1(0)', '김규철', '금9~12(2공522)', ''], 
        ['4', '전공선택', '472610', '고급임베디드시스템실험', '1', '병행강의', '병행강의', '병행강의', '온라인강의2', '', '1(0)', '최용근', '화15~18(2공521)', ''], 
        ['4', '전공선택', '472610', '고급임베디드시스템실험', '2', '병행강의', '병행강의', '병행강의', '온라인강의2', '', '1(0)', '최용근', '수15~18(2공521)', ''], 
        ['4', '전공선택', '472610', '고급임베디드시스템실험', '3', '병행강의', '병행강의', '병행강의', '온라인강의2', '', '1(0)', '최용근', '목13~16(2공521)', ''], 
        ['4', '전공선택', '472610', '고급임베디드시스템실험', '4', '병행강의', '병행강의', '병행강의', '온라인강의2', '', '1(0)', '최용근', '금1~4(2공521)', ''], 
        ['2', '전공필수', '472570', '디지털논리회로실험', '1', '전체대면', '전체대면', '전체대면', '온라인강의2', '영어B', '1(0)', '최천원', '월15~18(2공421)', '']]
        '''
        #결과 리스트를 사전화함
        self.resultDic = dict()
        for i in range(len(self.resultList)):
            self.resultDic[i] = self.resultList[i]

        self.savedList = []

        self.initUI()
    
    #검색결과 화면 설정
    def initUI(self):
        #기본 설정
        self.setWindowTitle('검색 결과')
        self.resize(1000, 625)
        #검색결과 개수에따른 행 개수 
        self.numRow = len(self.resultList)
        #표 생성
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(self.numRow)
        self.tableWidget.setColumnCount(15)
        self.tableWidget.setColumnWidth(0,15)
        self.tableWidget.setFixedSize(1000,500)
        #표에 데이터 입력
        self.setTableData()
        self.insertCheckbox() 

        #창 하단에 설명 추가
        explanation = QLabel('체크박스를 클릭하여 내 리스트에 추가한 후 파일로 저장하여 확인할 수 있습니다.')
        explanation.setAlignment(Qt.AlignHCenter)
        #뒤로가기 버튼생성
        quitbtn = QPushButton('뒤로가기', self)
        quitbtn.clicked.connect(self.close)
        #저장버튼 생성
        savebtn = QPushButton('파일로 저장', self)
        savebtn.clicked.connect(lambda: export_csv.write_csv(save_into_file))

        #hbox객체를 생성하여 설명, 뒤로가기버튼, 저장버튼 배치
        hbox = QHBoxLayout()
        hbox.addStretch(10)
        hbox.addWidget(explanation)
        hbox.addStretch(10)
        hbox.addWidget(savebtn)
        hbox.addStretch(1)
        hbox.addWidget(quitbtn)
        hbox.addStretch(1)

        #vbox객체를 생성하여 tablewidget과 hbox를 수직으로 배치
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.tableWidget)
        vbox.addStretch(10)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        #창의 레이아웃을 vbox객체로 설정
        self.setLayout(vbox)

        self.show()

    #1열(0번째)에 체크박스 생성, 체크여부를 반환하기 위해 item을 생성하여 같은 cell에 배치
    def insertCheckbox(self):
        self.checkBoxList = []
        for i in range(self.numRow):
            item = checkboxItem()
            self.tableWidget.setItem(i, 0, item)  
            ckbox = MyCheckBox(item)
            ckbox.clicked.connect(self.ckboxChanged)
            self.tableWidget.setCellWidget(i, 0, ckbox)

    
    #체크박스 클릭시 체크된 cell의 행을 받아 이에 해당하는 리스트를 결과리스트에 추가
    def ckboxChanged(self):
        self.ckbox = self.sender()
        global save_into_file
        save_into_file.append(self.resultList[self.ckbox.get_row()])

    #tablewidget에 data추가
    def setTableData(self):
        #행의 제목을 지정하고 배치
        columnHeaders = ['', '학년', '이수구분', '교과목번호', '교과목명', '분반', '1단계', '2단계', '3단계', '4단계', '원어', '학점(설계)', '교강사', '요일/교시/강의실', '수업방법 및 비고']
        self.tableWidget.setHorizontalHeaderLabels(columnHeaders)

        #결과사전에서 값을 가져와 각 cell에 배치
        for k, v in self.resultDic.items():
            row = k
            for col, val in enumerate(v):
                item = QTableWidgetItem(val)
                self.tableWidget.setItem(row, col + 1, item)

        self.tableWidget.resizeColumnsToContents()

#체크박스 생성을 위한 class
class MyCheckBox(QCheckBox):
    def __init__(self, item):
        super().__init__()
        self.item = item
        self.mycheckvalue = 0
        self.stateChanged.connect(self.item.my_setdata)
    
    def get_row(self):
        return self.item.row()

#item을 생성하기 위한 class
class checkboxItem(QTableWidgetItem):
    def __init__(self):
        super().__init__()
        self.setData(Qt.UserRole, 0)

    def __lt__(self, other):
        return self.data(Qt.UserRole) < other.data(Qt.UserRole)

    def my_setdata(self, value):
        self.setData(Qt.UserRole, value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #QApplication 객체에서 exec_메서드를 호출해 이벤트 루프 생성
    ex = searchOption()
    sys.exit(app.exec_())