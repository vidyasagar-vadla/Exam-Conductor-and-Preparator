import mysql.connector
class handler():
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="optimus",
            password="Vidyasagar2005@",
            database="exambuilder"
        )
        self.mycursor = self.mydb.cursor()

    def get_subject(self):
        self.mycursor.execute("select sname, cimg from subjects")
        subjects ={}
        for i in self.mycursor.fetchall():
            subjects[i[0]] = i[1]
        return subjects        
    def get_sem_pdfs(self,i):
        self.mycursor.execute("select * from syllabus where Semester = {}".format(i))
        subjects= {}
        for i in self.mycursor.fetchall():
            subjects[i[1]]={'abbrev':i[0],'filename':i[3]}
        return subjects
    def create_ans(self,arr,sub):
        for i in range(len(arr)):
            self.mycursor.execute("INSERT INTO answers(sno,sname,opt) VALUES({},'{}','{}')".format(i+1,sub,arr[i]))
        if input('confirm yes//no')=='yes':
            self.mydb.commit()


    def get_answers(self,subject):
        self.mycursor.execute("select * from answers a where a.sname='{}'".format(subject))
        keys = {}
        for i in self.mycursor.fetchall():
            keys[i[0]] = i[2]
        return keys
    

    def score_in_db(self,user,sub,score,max_marks):
        self.mycursor.execute("INSERT INTO userscores(username,subject_name,Marks,max_marks,date_time) VALUES('{}','{}',{},{}, now())".format(user,sub,score,max_marks))
        self.mydb.commit()


    def score_out(self):
        users={}
        self.mycursor.execute('select * from userscores')
        for i in self.mycursor.fetchall():
            try:
                a={'s_no':i[0],'subjectname':i[2],'Marks':i[3],'max_marks':i[4],'date_time':i[5].strftime("%d-%m-%Y, %I:%M %p")}
                if i[1] in users.keys():
                    users[i[1]]+=[a]
                else:
                    users[i[1]]=[a]
            except:
                pass        
        return users
    
    def Practice_out(self):
        users={}
        self.mycursor.execute('select * from practice')
        for i in self.mycursor.fetchall():
            try:
                a={'s_no':i[0],'subject_name':i[2],'entry_date_time':i[3].strftime("%d-%m-%Y, %I:%M %p"),'duration':str(i[4])}
                if i[1] in users.keys():
                    users[i[1]]+=[a]
                else:
                    users[i[1]]=[a]
            except:
                pass
        return users
    

    def Practice_in_db(self,user,sub,entry,dur):
        self.mycursor.execute("insert into practice(username,subject_name,entry_date_time,duration) values('{}','{}','{}','{}')".format(user,sub,entry,dur))
        self.mydb.commit()
    
    def last_out(self,table,user):
        #userscores, practice
        self.mycursor.execute("select count(username) from {} where username='{}'".format(table,user))
        return self.mycursor.fetchall()[0][0]
    
    def insert_exam(self,sub,csv):
        self.mycursor.execute("select sname from answers where sname='{}'".format(sub))
        if len(self.mycursor.fetchall())>0:
            self.mycursor.execute("delete from answers where sname='{}'".format(sub))
        for i,j in csv.items():
            self.mycursor.execute("insert into answers values({},'{}','{}')".format(i,sub,j))
        self.mydb.commit()
    
    def insert_stm(self,sub,pdfpath):
        self.mycursor.execute("select subject_name from syllabus where subject_name='{}'".format(sub))
        if len(self.mycursor.fetchall())>0:
            self.mycursor.execute("update syllabus set pdfpath='{}' where subject_name='{}'".format(pdfpath,sub))
        self.mydb.commit()

    def get_users(self):
        user= set(list(self.Practice_out().keys())+list(self.score_out().keys()))
        if 'admin' in user:
            user.remove('admin')
        if 'admin' in user:
            user.remove('Admin')
        return user


if __name__ == "__main__":
    a = handler()
    print(a.get_users())
