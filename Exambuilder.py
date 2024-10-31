from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel
import PIL
from kivymd.uix.textfield import MDTextField
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.properties import ObjectProperty,StringProperty
import webbrowser
from kivymd.uix.segmentedbutton import MDSegmentedButton,MDSegmentedButtonItem,MDSegmentButtonLabel
from kivymd.uix.navigationrail import MDNavigationRail,MDNavigationRailItem,MDNavigationRailItemLabel
from Base import *
from Questions import *
from Practice import *
from widgets import *
from Admin import *
from kivy.config import Config
from kivymd.icon_definitions import *
from kivy.core import spelling
import os, sys
from kivy.resources import resource_add_path, resource_find

Config.set('graphics', 'width', '1250')
Config.set('graphics', 'height', '700')

class PdfSubjectsScreen(MDScreen):
    sem=1
    def on_pre_enter(self):
        wid=self.ids['subjects_pdf']
        wid.clear_widgets()
        db= handler()
        dic=db.get_sem_pdfs(self.sem)
        for i in dic.keys():
            wid.size_hint_y=(0.2*(len(wid.children)/2 if len(wid.children)%2==0 else (len(wid.children)+1)/2))
            wid.add_widget(PdfCard(subject=i,file=dic[i]['filename']))
        

class HomeScreen(MDScreen):
    def add_exam_row(self,x):
        self.ids['Exam_table'].add_widget(TableData(text= str(x[0]),color= 'white',size_hint_x= 0.1))
        self.ids['Exam_table'].add_widget(TableData(text= x[1],color= 'white',size_hint_x= 0.3))
        self.ids['Exam_table'].add_widget(TableData(text= x[2],color= 'white',size_hint_x= 0.4))
        self.ids['Exam_table'].add_widget(TableData(text= x[3],color= 'white',size_hint_x= 0.18))
    def add_practice_row(self,x):
        self.ids['Practice_table'].add_widget(TableData(text= str(x[0]),color= 'white',size_hint_x= 0.1))
        self.ids['Practice_table'].add_widget(TableData(text= x[1],color= 'white',size_hint_x= 0.3))
        self.ids['Practice_table'].add_widget(TableData(text= x[2],color= 'white',size_hint_x= 0.4))
        self.ids['Practice_table'].add_widget(TableData(text= x[3],color= 'white',size_hint_x= 0.1))

class manage(MDScreenManager):
    def startexam(self,subject):
        self.current = 'exam'
        self.current_screen.start(os.path.abspath(os.path.join('_internal/QuestionPapers',subject)),subject)
    def startpractice(self,subject,instance):
        self.current = 'practice'
        self.current_screen.start(os.path.abspath(os.path.join('_internal/QuestionPapers',subject)),subject)

class ResultScreen(MDScreen):      
    def on_enter(self):
        maxmarks,marks=len(self.manager.main.questions),self.manager.main.score
        percentage=int(float(marks)/float(maxmarks)*100)
        g=['A+','A','B+','B','C+','C','D']
        if percentage>35:
            self.ids['marks'].text='Marks Obtained :  {}\nMax Marks          :  {}\nPercentage         :  {}\nGrade                    :  {} '.format(marks,maxmarks,str(percentage)+'%',g[10-int(float(percentage)/10)])
            self.ids['pfimage'].source='imagess//pass.png' 
        else:
            self.ids['marks'].text='Marks Obtained :  {}\nMax Marks          :  {}\nPercentage         :  {}\nGrade                    :  {} '.format(marks,maxmarks,percentage,'-')
            self.ids['pfimage'].source='imagess//fail.png' 
    def backtomain(self):
        self.manager.get_screen('base').ids['nd'].current='home'
        self.manager.current='base'


class Exambuilder(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"  # "Purple", "Red"
        sm=manage()
        #Builder.load_file("builder.kv")
        sm.add_widget(base(name='base'))
        sm.add_widget(QuestionScreen(name='exam'))
        sm.add_widget(ResultScreen(name='result'))
        sm.add_widget(PracticeQuestionsScreen(name='practice'))
        sm.current='base'
        return sm
    def on_start(self):
        exam_db=handler()
        subject= list(exam_db.get_subject().keys())
        self.root.get_screen('base').ids['exam'].ids['subjects'].size_hint[1]*=len(subject)//4+1 if len(subject)%4!=0 else len(subject)//4
        for i in range(len(subject)):
            self.root.get_screen('base').ids['exam'].ids['subjects'].add_widget(
                ExamCard(subject=subject[i],file="imagess\\Android.png"))
            
        self.root.get_screen('base').ids['practice'].ids['subjects'].size_hint[1]*=len(subject)//4+1 if len(subject)%4!=0 else len(subject)//4
        for i in range(len(subject)):
            self.root.get_screen('base').ids['practice'].ids['subjects'].add_widget(
                MDCard(MDLabel(text= subject[i],halign='center'),
                    on_release=partial(self.root.startpractice,subject[i]),
                )
            )
        for i in range(7):
            self.root.get_screen('base').ids['st_m'].ids['sem'].add_widget(SemCard(text = 'Semester '+str(i+1),on_release=partial(self.root.get_screen('base').get_pdfs,i+1)))
        self.root.get_screen('base').ids['st_m'].ids['sem'].add_widget(SemCard(text = 'Electives',on_release=partial(self.root.get_screen('base').get_pdfs,0)))
    
if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    Exambuilder().run()

    # path of the log directory
    Config.set('kivy', 'log_dir', 'your_chosen_log_dir_path')
    
    # filename of the log file
    Config.set('kivy', 'log_name', "anything_you_want_%y-%m-%d_%_.log")
    
    # Keep log_maxfiles recent logfiles while purging the log directory. Set ‘log_maxfiles’ to -1 to disable logfile purging (eg keep all logfiles).
    Config.set('kivy', 'log_maxfiles', 1000)

    # minimum log level which is what you need to not see kivy's default info logs
    Config.set('kivy', 'log_level', 'error')
    
    # apply all these changes
    Config.write()