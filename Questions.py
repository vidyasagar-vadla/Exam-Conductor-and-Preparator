from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.clock import Clock
from widgets import *
from kivymd.uix.button import MDButton,MDButtonText
from functools import partial
from datetime import datetime



class QuestionScreen(MDScreen):
    file=''
    def start(self,folder,subject):
        self.checkboxes=[i for i in self.children[1].children if isinstance(i,MDCheckbox)]
        self.checkboxes={chr(100-i):self.checkboxes[i] for i in range(4)}
        self.subject=subject
        self.time_arr=[0,1,0]
        self.event = Clock.schedule_interval(self.updatetime,1)
        self.main=Exam(folder)
        for i in range(len(self.main.questions)):
            self.ids['questions'].add_widget(MDButton(
                MDButtonText(text='Q{}'.format(str(i+1).zfill(2))
                             ),on_release=partial(self.gotoqtn,i)
                        )
                    )
        self.file=os.path.join(self.main.home,self.main.questions[self.main.current]) if len(self.main.questions)>0 else ''
        self.ids['img'].source=self.file
        self.ids['img'].reload()
    def gotoqtn(self,n,instance):
        self.main.current=n
        self.file=os.path.join(self.main.home,self.main.questions[self.main.current])
        self.ids['img'].source=self.file
        self.ids['img'].reload()
        if self.main.selected_option !='NA':
            self.checkboxes[self.main.selected_option].active=False
        if self.main.current+1 in self.main.answers.keys():
            if self.main.answers[self.main.current+1]!='NA':
                self.checkboxes[self.main.answers[self.main.current+1]].active=True
    def selection(self,value):
        self.main.selected_option=value
    def save_next(self,instance):
        self.main.answers[int(self.file.split('Slide')[1][0])+1]=self.main.selected_option
        if self.main.current<len(self.main.questions)-1:
            self.gotoqtn(self.main.current+1,None)
    def time_str(self,x):
        return '{:0>2d}:{:0>2d}:{:0>2d}'.format(self.time_arr[0],self.time_arr[1],self.time_arr[2])
    def updatetime(self,x=0):
        self.time_arr[2] -= 1
        if self.time_arr[2]==-1:
            self.time_arr[1]-=1
            self.time_arr[2]=59
        if self.time_arr[1]== -1:
            self.time_arr[0]-=1
            self.time_arr[1]=59
        if max(self.time_arr)==0:
            self.submit(None)
        self.ids['Time'].text = self.time_str(self.time_arr)
    def submit(self,instance):
        self.event.cancel()
        self.main.score=0
        for i,j in self.main.answers.items():
            if self.main.keys[i]==j:
                self.main.score+=1
        self.manager.current='result'
        self.manager.main=self.main
        db=handler()
        db.score_in_db(self.manager.get_screen('base').user,self.subject,self.main.score,len(self.main.questions))
        self.manager.get_screen('base').ids['nd'].get_screen('home').add_exam_row([db.last_out('userscores',self.manager.get_screen('base').user),self.subject,datetime.now().strftime(r'%Y-%m-%d, %I:%M %p'),str(self.main.score)+'/'+str(len(self.main.questions))])
