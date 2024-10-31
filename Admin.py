from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar,MDSnackbarText,MDSnackbarActionButton,MDSnackbarActionButtonText,MDSnackbarButtonContainer
from kivymd.uix.widget import Widget
import shutil
from databasehandling import *


class AdminScreen(MDScreen):
    choose={'examfile':'','examfolder':'','stmfile':''}
    labels={'examfile':'','examfolder':'','stmfile':''}
    def csv_reader(self,path):
        fd=open(path,'r')
        csv={int(i.replace('\n','').split(',')[0]): i.replace('\n','').split(',')[1] for i in fd.readlines()}
        return csv
    def apply_button(self,instance):
        text=MDSnackbarText(text='')
        snackbar=MDSnackbar(text,pos_hint={"center_x": 0.5,'center_y':0.2},size_hint_x=0.5,duration=1)
        if self.ids['page1'].active:
            if self.content[1].text != '' and self.content[3].text != '' and self.content[6].text != '':
                if not self.content[6].text.endswith('.csv'):
                    text.text='Choose .csv files Only'
                    snackbar.open()
                elif not self.content[3].text.replace(' ','').isalnum():
                    text.text='Selected Folder name should not contain special characters'
                    snackbar.open()
                else:
                    self.sure=MDSnackbar(
                                MDSnackbarText(
                                    text="Are You Sure !!!",
                                ),
                                MDSnackbarButtonContainer(
                                    Widget(),
                                    MDSnackbarActionButton(
                                        MDSnackbarActionButtonText(
                                            text="Yes"
                                        ),
                                        on_release=self.access
                                    ),
                                    MDSnackbarActionButton(
                                        MDSnackbarActionButtonText(
                                            text="No"
                                        ),
                                        on_release=self.dismiss
                                    ),
                                ),
                                pos_hint={"center_x": 0.5,'center_y':0.2},
                                size_hint_x=0.6,
                                duration=100
                            )
                    self.sure.open()
            else:
                text.text='Invalid details'
                snackbar.open()
        if self.ids['page2'].active:
            if self.content[1].text != '' and self.content[3].text != '':
                if not self.content[3].text.endswith('.pdf'):
                    text.text='Choose .pdf files Only'
                    snackbar.open()
                else:
                    self.sure=MDSnackbar(
                                MDSnackbarText(
                                    text="Are You Sure !!!",
                                ),
                                MDSnackbarButtonContainer(
                                    Widget(),
                                    MDSnackbarActionButton(
                                        MDSnackbarActionButtonText(
                                            text="Yes"
                                        ),
                                        on_release=self.access
                                    ),
                                    MDSnackbarActionButton(
                                        MDSnackbarActionButtonText(
                                            text="No"
                                        ),
                                        on_release=self.dismiss
                                    ),
                                ),
                                pos_hint={"center_x": 0.5,'center_y':0.2},
                                size_hint_x=0.6,
                                duration=100
                            )
                    self.sure.open()
            else:
                text.text='Invalid details'
                snackbar.open()
    def dismiss(self,instance):
        self.sure.dismiss(instance)
    
    def access(self,instance):
        if self.ids['page1'].active:
            sub_name=self.content[1].text
            path=self.choose['examfolder']
            csv=self.csv_reader(self.choose['examfile'])
            shutil.rmtree('_internal/QuestionPapers/'+sub_name)
            shutil.copytree(path,'_internal/QuestionPapers/'+sub_name)
            a=handler()
            a.insert_exam(sub_name,csv)
        elif self.ids['page2'].active:
            sub_name=self.content[1].text
            pdfpath=self.choose['stmfile']
            a=handler()
            try:
                shutil.copy(pdfpath,'_internal/pdfs/'+pdfpath.split('\\')[-1])
            except:
                pass
            a.insert_stm(sub_name,pdfpath.split('\\')[-1])
        self.dismiss(instance)
        



        
