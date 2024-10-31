from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.clock import Clock
from widgets import *
from datetime import datetime,timedelta



class PracticeQuestionsScreen(MDScreen):
    file=''
    selected_option=''
    def start(self,folder,subject):
        self.checkboxes=[i for i in self.children[1].children if isinstance(i,MDCheckbox)]
        self.checkboxes={chr(100-i):self.checkboxes[i] for i in range(4)}
        self.subject=subject
        self.time_arr=[0,0,0]
        self.event = Clock.schedule_interval(self.updatetime,1)
        self.main=Exam(folder)
        self.file=os.path.join(self.main.home,self.main.questions[self.main.current]) if len(self.main.questions)>0 else ''
        self.ids['img'].source=self.file
        self.ids['img'].reload()
    def gotoqtn(self,n,instance):
        self.main.selected_option='NA'
        self.main.current=n
        for i in [ i for i in self.children[1].children if isinstance(i,MDCheckbox)]:
            i.active=False
        self.file=os.path.join(self.main.home,self.main.questions[self.main.current])
        self.ids['img'].source=self.file
        self.ids['img'].reload()
        if self.main.selected_option !='NA':
            self.checkboxes[self.main.selected_option].active=False
        if self.main.current+1 in self.main.answers.keys():
            if self.main.answers[self.main.current+1]!='NA':
                self.checkboxes[self.main.answers[self.main.current+1]].active=True
    
    def nav(self,n):
        if len(self.main.questions)>self.main.current+n>=0:
            self.gotoqtn(self.main.current+n,None)
    def selection(self,value):
        self.main.selected_option=value
    def save(self,instance):
        self.main.answers[int(self.file.split('Slide')[1][0])+1]=self.main.selected_option
        self.ids['explanation'].text='Chosen Option : {}\nAnswer: {}\nExplanation : {}'.format(self.main.selected_option,self.main.keys[self.main.current+1],'None')
    def time_str(self,x):
        return '{:0>1d}:{:0>2d}:{:0>2d}'.format(self.time_arr[0],self.time_arr[1],self.time_arr[2])
    def updatetime(self,x=0):
        self.time_arr[2] += 1
        if self.time_arr[2]==60:
            self.time_arr[1]+=1
            self.time_arr[2]=00
        if self.time_arr[1]== 60:
            self.time_arr[0]+=1
            self.time_arr[1]=00
        self.ids['Time'].text = self.time_str(self.time_arr)
    def backtomain(self,instance):
        self.event.cancel()
        self.manager.get_screen('base').ids['nd'].current='home'
        self.manager.current='base'
        db= handler()
        db.Practice_in_db(self.manager.current_screen.user,self.subject,(datetime.now()-timedelta(hours=self.time_arr[0],minutes=self.time_arr[1],seconds=self.time_arr[2])).strftime(r'%Y-%m-%d, %H:%M:%S'),self.time_str(self.time_arr))
        self.manager.get_screen('base').ids['nd'].current_screen.add_practice_row([db.last_out('practice',self.manager.get_screen('base').user),self.subject,(datetime.now()-timedelta(hours=self.time_arr[0],minutes=self.time_arr[1],seconds=self.time_arr[2])).strftime(r'%Y-%m-%d %I:%M %p'),self.time_str(self.time_arr)])
