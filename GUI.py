import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTableWidget, QTableWidgetItem, QDesktopWidget, QPushButton, QHBoxLayout, QVBoxLayout, QCheckBox, QLabel, QComboBox, QLineEdit, QMenu, QGridLayout, QCheckBox, QRadioButton, QGroupBox
from PyQt5.QtCore import Qt, QCoreApplication

class searchOption(QWidget):
    def __init__(self):
        super().__init__()
        
        self.searchList = ['' for i in range(11)]
        self.clickedSemester = '1학기'
        self.clickedCampus = '죽전'
        self.clickedDomain = '영역'
        self.inputYear = '2020'
        self.clickedCollege = '단과대학'
        self.clickedMajor = '전공명'
        self.inputSubject = '교과목명'
        self.clickedDay = '요일'
        self.clickedhgrade = '학년'
        self.inputTeacher = '교강사명'

        
        self.jMajor = {'단과대학':['전공명'], '문과대학': ['전공명', '국어국문학과', '사학과', '철학과', '영미인문학과', '중어중문학과', '일어일문학과', '영어영문학과'],
         '법과대학': ['전공명', '법학과'], '사회과학대학': ['전공명', '정치외교학과', '행정학과', '도시계획부동산학부', '도시지역계획학전공', '부동산학전공', '커뮤니케이션학부', '저널리즘전공', '영상콘텐츠전공', '광고홍보전공', '응용통계학과', '상담학과',],
         '경영경제대학': ['전공명', '경제학과', '무역학과', '경영학부', '경영학전공', '회계학전공', '산업경영학과(야)', '국제학부', '국제경영학전공'], '상경대학':['전공명'], '건축대학':['전공명'],
          '공과대학': ['전공명', '전자전기공학부', '전자전기공학전공', '고분자공학전공', '파이버융합소재공학전공', '고분자공학과', '파이버시스템공학과', '소프트웨어학과', '응용컴퓨터공학과', '토목환경공학과', '기계공학과', '화학공학과', '건축학전공', '건축공학전공'],
          'SW융합대학': ['전공명', '소프트웨어학과', '컴퓨터공학과', '모바일시스템공학과', '정보통계학과', '산업보안학과', 'SW융합바이오전공', 'SW융합콘탠츠전공', 'SW융합경제경영전공', 'SW융합법학전공', '글로벌SW융합전공'],
          '사범대학': ['전공명', '한문교육과', '특수교육과', '특수교육과 초등특수교육', '특수교육과 중등특수교육', '수학교육과', '과학교육과', '과학교육과 물리전공', '과학교육과 생물전공', '체육교육과', '교직교육과'],
          '음악·예술대학':['전공명', '도예과', '커뮤니케이션디자인전공', '패션산업디자인전공', '연극전공', '영화전공', '뮤지컬전공', '무용과', '기악전공', '기악전공(피아노), 기악전공(현악)', '성악전공', '작곡전공', '국악전공'], '예술디자인대학': ['전공명'],
          '음악대학':['전공명'], '국제대학': ['모바일시스템공학과', '영상 연기 &제작 전공'], '국제학부':['전공명'], '다산링크스쿨': ['전공명'], '자연과학대학': ['전공명'], '연계전공(학부)': ['전공명']}
        
        self.cMajor = {'국제학부': ['전공명', '글로벌경영학전공'], '외국어대학': ['전공명', '중국학전공', '일본학전공', '몽골학전공', '중동학전공', '독일학전공', '프랑스학전공', '스페인중남미학전공', '러시아학전공', '포르투갈브라질학전공', '영어과'],
        '인문과학대학': ['전공명'], '공공인재대학': ['전공명', '경영학과(야)'], '행정복지대학': ['전공명', '법무행정학과'], '경상대학': ['전공명', '국제통상학부', '경제학전공', '무역학전공', '경영학부', '경영학전공', '회계학전공'],
        '과학기술대학': ['전공명', '수학과', '물리학과', '화학과', '식품영양학과', '미생물학전공', '생명과학전공', '신소재공학과', '식품공학과', '에너지공학과', '경영공학과'],
        '자연과학대학': ['전공명', '분자생물학과', '생명과학과'], '융합기술대학': ['전공명', '산업공학과', '디스플레이공학과', '원자력융합공학과'], '공학대학': ['전공명', '응용화학공학과', '컴퓨터과학과', '멀티미디어공학과', '전자공학과'],
        '생명공학대학': ['전공명', '식량생명공학전공', '동물자원학전공', '환경원예학전공', '녹지조경학전공', '의생명공학부 의생명공학전공', '제약공학과'], '예술대학': ['전공명', '미술학부 공예전공', '미술학부 동양화전공', '미술학부 서양화전공', '미술학부 조소전공', '문예창작과', '뉴뮤직과'],
        '스포츠과학대학': ['전공명', '생활체육학과', '스포츠경영학과', '운동처방재활전공', '국제스포츠전공', '태권도전공'], '의과대학': ['전공명', '의예과', '의학과'],
        '보건복지대학': ['전공명', '공공정책학과', '공공정책학과(야)', '사회복지학과', '해병대군사학과', '환경자원경제학과', '임상병리학과', '물리치료학과', '보건행정학과', '치위생학과', '심리치료학과'], '간호대학': ['간호학과'], '치과대학': ['치의예과', '치의학과'], 
        '약학대학': ['전공명', '약학과'], '연계전공(학부)': ['전공명', '메디바이오산업기술학연계전공', '토탈분석기기융합학연계전공', '식의약향장학연계전공']}
        
        self.initUI()

    def initUI(self):

        title = QLabel('종합강의시간표 검색')
        title.setAlignment(Qt.AlignHCenter)
        
        font = title.font()
        font.setFamily('10X10')
        font.setBold(True)
        font.setPointSize(40)
        title.setFont(font)

        searchbtn = QPushButton('search', self)

        layout = QGridLayout()
        layout.setSpacing(20)
        layout.addWidget(self.year(), 0, 0)
        layout.addWidget(self.semester(), 0, 1)
        layout.addWidget(self.campus(), 0, 2)
        layout.addWidget(self.liberalArts(), 1, 0)
        layout.addWidget(self.major(), 1, 1)
        layout.addWidget(self.option(), 1, 2)
        layout.addWidget(self.subject(), 3, 0, 1, 3)
        

        hbox1 = QHBoxLayout()
        hbox1.addStretch(20)
        hbox1.addWidget(searchbtn)
        hbox1.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addWidget(title)
        vbox.addStretch(2)
        vbox.addLayout(layout)
        vbox.addStretch(2)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)

        self.setLayout(vbox)

        searchbtn.clicked.connect(lambda: self.schbtn_clicked(title))
        self.dialog = QDialog()

        self.setWindowTitle('timetable')
        self.resize(1000,625)
        self.center() #center() 메서드로 창이 화면의 가운데에 위치하게 함
        self.show()

    def schbtn_clicked(self, title):
        dlg = searchResult()
        dlg.exec_()
    
    def setTableWidgetData(self):
        self.dialog.tableWidget.setItem(0, 0, QTableWidgetItem("(0,0)"))
        self.dialog.tableWidget.setItem(0, 1, QTableWidgetItem("(0,1)"))
        self.dialog.tableWidget.setItem(1, 0, QTableWidgetItem("(1,0)"))
        self.dialog.tableWidget.setItem(1, 1, QTableWidgetItem("(1,1)"))

    def semester(self):
        groupbox = QGroupBox('학기')
        #groupbox.setFlat(True)

        self.sem1 = QRadioButton('1학기')
        self.sem1.setChecked(True)
        self.sem1.clicked.connect(self.semesterClicked)
        self.sem2 = QRadioButton('여름학기')
        self.sem2.clicked.connect(self.semesterClicked)
        self.sem3 = QRadioButton('2학기')
        self.sem3.clicked.connect(self.semesterClicked)
        self.sem4 = QRadioButton('겨울학기')
        self.sem4.clicked.connect(self.semesterClicked)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.sem1)
        hbox.addWidget(self.sem2)
        hbox.addWidget(self.sem3)
        hbox.addWidget(self.sem4)
        groupbox.setLayout(hbox)

        return groupbox
    
    def semesterClicked(self):
        if self.sem1.isChecked():
            self.clickedSemester = self.sem1.text()
        elif self.sem2.isChecked():
            self.clickedSemester = self.sem2.text()
        elif self.sem3.isChecked():
            self.clickedSemester = self.sem3.text()
        else:
            self.clickedSemester = self.sem4.text()

    def campus(self):
        groupbox = QGroupBox('캠퍼스')
        #groupbox.setFlat(True)

        self.cps1 = QRadioButton('죽전')
        self.cps1.setChecked(True)
        self.cps1.clicked.connect(self.campusClicked)
        self.cps2 = QRadioButton('천안')
        self.cps2.clicked.connect(self.campusClicked)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.cps1)
        hbox.addWidget(self.cps2)
        groupbox.setLayout(hbox)   

        return groupbox

    def campusClicked(self):
        if self.cps1.isChecked():
            self.clickedCampus = self.cps1.text()
        else:
            self.clickedCampus = self.cps2.text()

    def major(self):
        self.groupbox = QGroupBox('전공')
        self.groupbox.setCheckable(True)
        self.groupbox.setChecked(False)
        self.groupbox.clicked.connect(self.dmClicked)

        if self.clickedCampus == '죽전':
            self.clg = QComboBox(self)
            self.mj = QComboBox(self)

            for x in self.jMajor.keys():
                self.clg.addItem(x)

            self.clg.activated[str].connect(lambda: self.clgClicked(self.clg))

            selected_clg = self.dmClicked

            for y in self.jMajor[selected_clg]:
                self.mj.addItem(y)


        vbox = QVBoxLayout()
        vbox.addWidget(self.clg)
        vbox.addWidget(self.mj)
        self.groupbox.setLayout(vbox)

        return self.groupbox

    def liberalArts(self):
        self.groupbox = QGroupBox('교양')
        self.groupbox.setCheckable(True)
        self.groupbox.setChecked(False)
        self.groupbox.clicked.connect(self.dmClicked)


        self.dm = QComboBox(self)
        self.dm.addItem('영역')
        self.dm.addItem('공통교양')
        self.dm.addItem('--글로벌교양')
        self.dm.addItem('--자기관리역량')
        self.dm.addItem('--사회봉사교과')
        self.dm.addItem('--종합적사고역량')
        self.dm.addItem('--자원·정보·기술활용역량')
        self.dm.addItem('--사고와표현역량')
        self.dm.addItem('--세계시민역량')
        self.dm.addItem('--자연/환경/기술')
        self.dm.addItem('--문학/역사/철학')
        self.dm.addItem('--정치/경제/사회·심리')
        self.dm.addItem('--수학/물리/화학/생물')
        self.dm.addItem('--문화/예술/체육')
        self.dm.addItem('평생교육사(필수)')
        self.dm.addItem('문화예술교육사')
        self.dm.addItem('교직')
        self.dm.addItem('군사학')
        self.dm.addItem('공통교양')
        self.dm.addItem('자유교과')
        self.dm.activated[str].connect(lambda: self.dmClicked(self.dm))
        vbox = QVBoxLayout()
        vbox.addWidget(self.dm)
        self.groupbox.setLayout(vbox)

        return self.groupbox
    
    def dmClicked(self, text):
        self.clickedDomain = text
        print(self.clickedDomain)

    def year(self):
        groupbox = QGroupBox('연도')
        self.yr = QLineEdit(self)
        self.yr.textChanged[str].connect(self.yearInput)

        hbox = QHBoxLayout()
        hbox.addWidget(self.yr)
        groupbox.setLayout(hbox)

        self.yr.setText('2020')
 
        return groupbox

    def yearInput(self, text):
        self.inputYear = text

    def subject(self):
        groupbox = QGroupBox('교과목명')
        self.sbj = QLineEdit(self)
        self.sbj.textChanged[str].connect(self.subjectInput)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.sbj)
        groupbox.setLayout(hbox)

        return groupbox

    def subjectInput(self, text):
        self.inputSubject = text

    def option(self):
        groupbox = QGroupBox('기타 옵션')

        self.day = QComboBox(self)
        self.day.addItem('요일')
        self.day.addItem('일요일')
        self.day.addItem('월요일')
        self.day.addItem('화요일')
        self.day.addItem('수요일')
        self.day.addItem('목요일')
        self.day.addItem('금요일')
        self.day.addItem('토요일')
        self.day.activated[str].connect(lambda: self.dayClicked(self.day))

        self.grade = QComboBox(self)
        self.grade.addItem('학년')
        self.grade.addItem('1')
        self.grade.addItem('2')
        self.grade.addItem('3')
        self.grade.addItem('4')
        self.grade.addItem('5')
        self.grade.addItem('6')
        self.grade.activated[str].connect(lambda: self.gradeClicked(self.grade))

        prof = QLabel('교강사명', self)
        self.tch = QLineEdit(self)
        self.tch.textChanged[str].connect(self.teacherInput) 

        vbox = QVBoxLayout()
        vbox.addWidget(self.day)
        vbox.addWidget(self.grade)
        vbox.addWidget(prof)
        vbox.addWidget(self.tch)
        groupbox.setLayout(vbox)

        return groupbox
    
    def dayClicked(self, text):
        self.clickedDay = text.currentText()

    def gradeClicked(self, text):
        self.clickedhgrade = text.currentText()

    def teacherInput(self, text):
        self.inputTeacher = text

    def center(self):
        qr = self.frameGeometry() #frameGeometry() 메서드로 창의 위치와 크기정보 가져오기
        cp = QDesktopWidget().availableGeometry().center() #사용되는 모니터 화면의 가운데 위치 파악
        qr.moveCenter(cp) #창의 직사각형 위치를 화면의 중심위치로 이동
        self.move(qr.topLeft()) #현재 창을 화면의 중심으로 이동한 직사각형 qr의 위치로 이동, 현재 창의 중심이 화면의 중심과 일치하게됨

class searchResult(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle('검색 결과')
        self.resize(1000, 625)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(1000, 625)
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(14)
        self.setTableData()
        quitbtn = QPushButton('뒤로가기', self)
        quitbtn.clicked.connect(QCoreApplication.instance().quit)
        savebtn = QPushButton('파일로 저장', self)

        hbox = QHBoxLayout()
        hbox.addStretch(20)
        hbox.addWidget(savebtn)
        hbox.addStretch(1)
        hbox.addWidget(quitbtn)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.tableWidget)
        vbox.addStretch(10)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.show()

    def setTableData(self):
        column_headers = ['수강조직', '학년', '이수구분', '교과목번호', '교과목명', '분반', '단계별 학사운영', '원어', '학점(설계)', '교강사', '요일/교시/강의실', '변경내역', '수업방법 및 비고', '추가하기']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = searchOption()
    sys.exit(app.exec_())