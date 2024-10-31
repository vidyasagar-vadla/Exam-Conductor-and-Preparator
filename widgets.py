from kivymd.uix.card import MDCard
import os
from kivy.uix.button import Button
from kivymd.app import MDApp
from databasehandling import handler
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout



############### Pdf Subjects Card #################       
class PdfCard(MDCard):
    def __init__(self, subject,file,*args, **kwargs):
        self.subject = str(subject)
        self.file=str(file)
        super().__init__(*args, **kwargs)
############### StudyMaterials Category Card #################       
class SemCard(Button):
    text =''
############### Exam Widget Card with Start Exam Button #################
class ExamCard(MDCard):
    def __init__(self, subject,file,*args, **kwargs):
        self.subject = str(subject)
        self.file=str(file)
        super().__init__(*args, **kwargs)
    def start(self):
        MDApp.get_running_app().root.startexam(self.subject)

############### User Object for Each Exam #################
class Exam():
    def __init__(self,subject) -> None:
        db=handler()
        self.home=subject
        self.keys=db.get_answers(subject.split('\\')[-1])
        self.answers={}
        self.current=0
        print(subject)
        q=os.listdir(subject)
        self.questions = [i for i in q if i[-3::]=='jpg']
        self.selected_option='NA'

############### homepage table data #################
class TableData(Label):
    pass

class Upload_admin(Button):
    def __init__(self,widget, **kwargs):
        self.widget=widget
        self.dialog=None
        super().__init__(**kwargs)
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = Popup(title='Choose',content=FloatLayout(size_hint= [1, 1],
                pos_hint= {'center_x': 0.5,'center_y': 0.5},
                ),
                size_hint= [0.6, 0.8],
                pos_hint= {'center_x': 0.5,'center_y': 0.5},
                )
            self.fc=FileChooserIconView(dirselect=True,
                    path="../" , # Set initial directory (optional)
                    filters = ['*.png','*.jpg','*.jpeg','*.csv','*.pdf'],
                    size_hint= [1, 1],
                    pos_hint= {'center_x': 0.5,'center_y': 0.5},
                    )
            self.dialog.content.add_widget(self.fc)
            self.dialog.content.add_widget(
                Button(
                text='Cancel',
                size_hint= [0.2, 0.07],
                pos_hint= {'center_x': 0.88,'y': 0.02},
                on_release= self.dialog.dismiss
                    ),
                )
            self.dialog.content.add_widget(
                Button(
                text='Select',
                size_hint= [0.2, 0.07],
                pos_hint= {'center_x': 0.66,'y': 0.02},
                on_release=self.select
                    ),
                )
        self.dialog.open()
    def select(self,instance):
        if len(self.fc.selection)==1:
            selection=self.fc.selection[0]
            self.parent.parent.parent.choose[self.widget]=selection
            self.parent.parent.parent.labels[self.widget].text=selection.split('\\')[-1] 
            self.parent.parent.parent.labels[self.widget].text_size=self.parent.parent.parent.labels[self.widget].size
            self.parent.parent.parent.labels[self.widget].halign='left'
            self.dialog.dismiss()
        

if __name__=='__main__':
    pass