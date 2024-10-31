from kivymd.uix.screen import MDScreen
from widgets import *
from kivymd.uix.button import MDButton,MDButtonText
from kivy.uix.textinput import TextInput
from kivy.graphics import Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.fitimage import FitImage
class UserLabel(Label):
    pass

class base(MDScreen):
    def __init__(self, *args, **kwargs):
        self.user='Guest'
        self.dialog = None
        super().__init__(*args, **kwargs)
    def get_pdfs(self,i,instance):
        self.ids['pdfs'].sem=i
        self.ids['nd'].current='pdfs' 
    def open(self):
        if self.user == 'Admin' or self.user == 'admin':
            self.ids['aboutus'].add_widget(
                MDButton(MDButtonText(text='Admin Previlages'),
                pos_hint= {'center_x': 0.85,'y': 0.85},
                on_release=self.admin
                    ),
                )
            self.ids['nav_drawer'].set_state('toggle')
        if self.user != 'Guest':
            self.ids['nav_drawer'].set_state('toggle') 
    def admin(self,instance):
        self.ids['nd'].current='admin'
        self.ids['admin'].ids['page1'].active=True
    def admin_content(self):
        self.ids['admin'].ids['content'].clear_widgets()
        if self.ids['admin'].ids['page1'].active:
            content=[
                Label(text='Subject Name :       ',pos_hint= {'x': 0,'center_y': 0.9},size_hint=[0.3,0.1],color='black'),
                TextInput(pos_hint= {'x': 0.3,'center_y': 0.9},size_hint=[0.3,0.1]),
                Label(text='Upload Folder :        ',pos_hint= {'x': 0,'center_y': 0.75},size_hint=[0.3,0.1],color='black'),
                Label(text='',pos_hint= {'x': 0.51,'center_y': 0.75},size_hint=[0.4,0.1],color='black'),
                Upload_admin(text='Upload',color= 'white',background_color= '#15616d',pos_hint= {'x': 0.3,'center_y': 0.75},size_hint=[0.2,0.1],widget='examfolder'),
                Label(text='Upload Key(.csv) :  ',pos_hint= {'x': 0,'center_y': 0.6},size_hint=[0.3,0.1],color='black'),
                Label(text='',pos_hint= {'x': 0.51,'center_y': 0.6},size_hint=[0.4,0.1],color='black'),
                Upload_admin(text='Upload',color= 'white',background_color= '#15616d',pos_hint= {'x': 0.3,'center_y': 0.6},size_hint=[0.2,0.1],widget='examfile'),
                Label(markup=True,text='[b]INSTRUCTIONS :-[/b]\n\nfolder requirements.\n     - Should be Subject name.\n     - Not have any special characters.\nfile requirements.\n     - It should be .csv file.\n     - First column should contain\n       question numbers.\n     - second column should contain\n       lowercase Alphabets(a,b,c,d).',pos_hint= {'x': 0.8,'top': 0.9},size_hint=[0.2,0.5],color='black',font_size=24),
                Button(text='Apply',color= 'white',background_color= '#9e2a2b',pos_hint= {'center_x': 0.5,'center_y': 0.45},size_hint=[0.2,0.1],on_release=self.ids['admin'].apply_button),
                ]
            self.ids['admin'].labels['examfile']=content[6]
            self.ids['admin'].labels['examfolder']=content[3]
        elif self.ids['admin'].ids['page2'].active:
            content=[
                Label(text='Subject Name :       ',pos_hint= {'x': 0,'center_y': 0.9},size_hint=[0.3,0.1],color='black'),
                TextInput(pos_hint= {'x': 0.3,'center_y': 0.9},size_hint=[0.3,0.1]),
                Label(text='Upload file :              ',pos_hint= {'x': 0,'center_y': 0.75},size_hint=[0.3,0.1],color='black'),
                Label(text='',pos_hint= {'x': 0.51,'center_y': 0.75},size_hint=[0.45,0.1],color='black'),
                Upload_admin(text='Upload',color= 'white',background_color= '#15616d',pos_hint= {'x': 0.3,'center_y': 0.75},size_hint=[0.2,0.1],widget='stmfile'),
                Label(markup=True,text='[b]INSTRUCTIONS :-[/b]\n\n- Subject name should be as specified\n  in Syllabus.\n- Study Material should be .pdf format.',pos_hint= {'x': 0.8,'top': 0.9},size_hint=[0.2,0.5],color='black',font_size=24),
                Button(text='Apply',color= 'white',background_color= '#9e2a2b',pos_hint= {'center_x': 0.5,'center_y': 0.45},size_hint=[0.2,0.1],on_release=self.ids['admin'].apply_button),
                ]
            self.ids['admin'].labels['stmfile']=content[3]
        elif self.ids['admin'].ids['page3'].active:
            content=[]
            a=ScrollView(do_scroll_y=True,size_hint=[1,1],pos_hint= {'center_x': 0.5,'center_y': 0.5})
            content.append(a)
            a.add_widget(BoxLayout(orientation= 'vertical',size_hint=[1,0.1*len(handler().get_users())],spacing=15))
            for i in handler().get_users():
                a.children[0].add_widget(UserLabel(text=i,size_hint= [0.3,0.3],color='white',font_size=25))
        self.ids['admin'].content=content
        for i in range(len(content)):
            self.ids['admin'].ids['content'].add_widget(content[i])
        
    def createuser(self):
        if self.ids['profile'].ids['user'].text not in ['Guest','guest','']:
            self.user = self.ids['profile'].ids['user'].text
            self.ids['nd'].current='home'
            self.updatedata()  
    def updatedata(self):
        db=handler()
        if self.user in db.score_out().keys():
            arr=db.score_out()[self.user]
            for i in range(len(arr)):
                self.ids['nd'].current_screen.add_exam_row([str(i+1),arr[i]['subjectname'],str(arr[i]['date_time']),str(arr[i]['Marks'])+'/'+str(arr[i]['max_marks'])])
        if self.user in db.Practice_out().keys():
            arr=db.Practice_out()[self.user]
            for i in range(len(arr)):
                self.ids['nd'].current_screen.add_practice_row([str(i+1),arr[i]['subject_name'],str(arr[i]['entry_date_time']),str(arr[i]['duration'])])

    
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = Popup(title='Choose Profile',content=FloatLayout(size_hint= [1, 1],
                pos_hint= {'center_x': 0.5,'center_y': 0.5},
                ),
                size_hint= [0.6, 0.8],
                pos_hint= {'center_x': 0.5,'center_y': 0.5},
                )
            self.fc=FileChooserIconView(
                    path="../" , # Set initial directory (optional)
                    filters = ['*.png','*.jpg','*.jpeg','.bmp'],
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
        selection=self.fc.selection
        if len(selection):
            fl=self.ids['profile'].ids['pic']
            fl.canvas.add(Ellipse(size=[fl.size[0],fl.size[0]], pos=fl.pos, color=(0.92, 0.92, 1, 1)))
            fl.canvas.add(Ellipse(size=[fl.size[0],fl.size[0]], source=selection[0],pos=fl.pos))
            self.dialog.dismiss()
