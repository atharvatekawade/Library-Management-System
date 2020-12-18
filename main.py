from tkinter import *
from tkinter import messagebox
import mysql.connector
from datetime import date, timedelta, datetime
from credentials import *  
import mysql.connector
import numpy as np
import smtplib,ssl
mydb=mysql.connector.connect(host='localhost', port=poort, user=admin, passwd=passwd, database=database)

port=465

def adduser():
    mycursor=mydb.cursor()
    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    for i in range(0,len(result)):
        if result[i][3]==str(username.get()):
            messagebox.showerror("Error","Username already taken")
            user_name.delete(0,END)
            username.delete(0,END)
            email.delete(0,END)
            password.delete(0,END)
            clicked_user_type.set('Students')
        #print(i)

    sql = "INSERT INTO users (name,username,email,password,user_type) VALUES (%s, %s, %s, %s, %s)"
    valid_email=str(email.get())
    if('@' in valid_email):
        val = (str(user_name.get()),str(username.get()),str(email.get()),str(password.get()),str(clicked_user_type.get()))
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success","User added")
    else:
        messagebox.showerror("Error","This is not a valid email")
    user_name.delete(0,END)
    username.delete(0,END)
    email.delete(0,END)
    password.delete(0,END)
    clicked_user_type.set('Students')

def saveuser(username,name,email,password,user_type,top):
    mycursor = mydb.cursor()
    sql = "UPDATE users SET name = %s, email = %s, password = %s, user_type = %s WHERE username = %s"
    val = (str(name.get()),str(email.get()),str(password.get()),str(user_type),str(username))
    mycursor.execute(sql, val)
    mydb.commit()
    messagebox.showinfo("Success","User updated")

def edituser(value,top):
    edit_user_name=Entry(top,width=30)
    edit_user_name.grid(row=5,column=1,padx=20)
    edit_user_name_label=Label(top,text="Name")
    edit_user_name_label.grid(row=5,column=0)
    edit_user_name.insert(0,value[1])
    edit_email=Entry(top,width=30)
    edit_email.grid(row=6,column=1)
    edit_email_label=Label(top,text="Email")
    edit_email_label.grid(row=6,column=0)
    edit_email.insert(0,value[2])
    edit_password=Entry(top,width=30)
    edit_password.grid(row=7,column=1)
    edit_password_label=Label(top,text="Password")
    edit_password_label.grid(row=7,column=0)
    edit_password.insert(0,value[5])
    options=["Students", "Faculty", "Staff", "Guest"]
    edit_clicked_user_type=StringVar()
    edit_clicked_user_type.set(value[4])
    user_type=OptionMenu(top,edit_clicked_user_type,*options)
    user_type.grid(row=8,column=1)
    user_type_label=Label(top,text='Type')
    user_type_label.grid(row=8,column=0)
    add_user=Button(top,text='Save User',command = lambda: saveuser(value[3],edit_user_name,edit_email,edit_password,str(edit_clicked_user_type.get()),top))
    add_user.grid(row=9,column=0,columnspan=2,pady=10,padx=10,ipadx=100)

def deleteuser(username,id):
    mycursor = mydb.cursor()
    c=0
    mycursor.execute("select * from book_borrow")
    result=mycursor.fetchall()
    for i in result:
        if(i[1]==id and i[4]=="Not"):
            c=1
            break
    mycursor.execute("select * from periodical_borrow")
    result=mycursor.fetchall()
    for i in result:
        if(i[1]==id and i[4]=="Not"):
            c=1
            break
    
    
    current_date = date.today().isoformat()
    current_date=str(current_date)
    current_date=current_date.split('-')
    end=date(int(current_date[0]),int(current_date[1]),int(current_date[2]))
    mycursor.execute("select * from users")
    d={}
    result=mycursor.fetchall()
    for i in result:
        if(i[4]=='Faculty'):
            d[i[0]]=30
        elif(i[4]=='Guest'):
            d[i[0]]=7
        elif(i[4]=='Staff'):
            d[i[0]]=30
        elif(i[4]=='Students'):
            d[i[0]]=15
    span=int(d[id])
    due=0
    mycursor.execute("select * from book_borrow")
    result=mycursor.fetchall()
    for i in result:
        if(i[1]==id):
            issue=str(i[3])
            date_time_obj = datetime.strptime(issue, '%Y-%m-%d')
            a=date_time_obj.date()
            days_after = (a+timedelta(days=span)).isoformat()
            days_after=str(days_after)
            b=days_after.split('-')
            start = date(int(b[0]),int(b[1]),int(b[2]))
            days=np.busday_count(start,end)
            days=int(days)
            if(days<0):
                days=0
            due=due+days
    mycursor.execute("select * from periodical_borrow")
    result=mycursor.fetchall()
    for i in result:
        if(i[1]==id):
            issue=str(i[3])
            date_time_obj = datetime.strptime(issue, '%Y-%m-%d')
            a=date_time_obj.date()
            days_after = (a+timedelta(days=span)).isoformat()
            days_after=str(days_after)
            b=days_after.split('-')
            start = date(int(b[0]),int(b[1]),int(b[2]))
            days=np.busday_count(start,end)
            days=int(days)
            if(days<0):
                days=0
            due=due+days

    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    amt=0
    for i in result:
        if(i[0]==id):
            amt=i[6]
    fine=due-amt




    if(c==1):
        messagebox.showerror("Error","User still has some books or periodicals in his possession")
    elif(fine!=0):
        print(fine)
        messagebox.showerror("Error","Clear user balance...")
    else:
        sql = "DELETE FROM book_borrow WHERE user_id = %s"
        adr = (id,)
        mycursor.execute(sql, adr)
        mydb.commit()
        sql = "DELETE FROM periodical_borrow WHERE user_id = %s"
        adr = (id,)
        mycursor.execute(sql, adr)
        mydb.commit()
        sql = "DELETE FROM waiting WHERE user_id = %s"
        adr = (id,)
        mycursor.execute(sql, adr)
        mydb.commit()
        sql = "DELETE FROM users WHERE id = %s"
        adr = (id,)
        mycursor.execute(sql, adr)
        mydb.commit()
        messagebox.showinfo("Success","User deleted")

def borrowbooksubmit(value,top,book):

    c=0
    d={"Students":3, "Faculty":6, "Staff":4, "Guest":2}
    mycursor=mydb.cursor()
    mycursor.execute("select * from book_borrow")
    result=mycursor.fetchall()
    for i in result:
        if(i[1]==value[0] and i[4]=='Not'):
            c=c+1
    if(c==d[value[4]]):
        msg="You already have "+str(c)+" books"
        messagebox.showerror("Error",msg)
    else:
        current_date = date.today().isoformat()
        issue=str(current_date)
        #book=int(book)
        sql = "INSERT INTO book_borrow (user_id,book_id,issue) VALUES (%s, %s, %s)"
        val = (int(value[0]),int(book.get()),str(issue))
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success","Book Borrowed")

def borrowperiodicalsubmit(value,top,periodical):

    c=0
    d={"Students":3, "Faculty":6, "Staff":4, "Guest":2}
    mycursor=mydb.cursor()
    mycursor.execute("select * from periodical_borrow")
    result=mycursor.fetchall()
    for i in result:
        if(i[1]==value[0] and i[4]=='Not'):
            c=c+1
    if(c==d[value[4]]):
        msg="You already have "+str(c)+" periodicals"
        messagebox.showerror("Error",msg)
    else:
        current_date = date.today().isoformat()
        issue=str(current_date)
        #book=int(book)
        sql = "INSERT INTO periodical_borrow (user_id,periodical_id,issue) VALUES (%s, %s, %s)"
        val = (int(value[0]),int(periodical.get()),str(issue))
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success","Periodical Borrowed")




def borrowbook(value,top):
    mycursor=mydb.cursor()
    mycursor.execute("select * from book")
    result=mycursor.fetchall()
    mycursor.execute("select * from book_borrow")
    result_1=mycursor.fetchall()
    borrowed=[]
    for i in result_1:
        if(i[4]=='Not'):
            borrowed.append(i[2])
    options=[]
    for i in result:
        if(i[0] not in borrowed and i[3]=='Not'):
            options.append(i[0])
    clicked_book=IntVar()
    clicked_book.set(options[0])
    book_borrow_id=OptionMenu(top,clicked_book,*options)
    book_borrow_id.grid(row=6,column=1,pady=20)
    book_borrow_id_label=Label(top,text='Book')
    book_borrow_id_label.grid(row=6,column=0)
    borrow_book_btn=Button(top,text='Borrow',command = lambda: borrowbooksubmit(value,top,clicked_book))
    borrow_book_btn.grid(row=7,column=0)
def borrowperiodical(value,top):
    mycursor=mydb.cursor()
    mycursor.execute("select * from periodical")
    result=mycursor.fetchall()
    mycursor.execute("select * from periodical_borrow")
    result_1=mycursor.fetchall()
    borrowed=[]
    for i in result_1:
        if(i[4]=='Not'):
            borrowed.append(i[2])
    options=[]
    for i in result:
        if(i[0] not in borrowed and i[3]=='Not'):
            options.append(i[0])
    clicked_periodical=IntVar()
    clicked_periodical.set(options[0])
    periodical_borrow_id=OptionMenu(top,clicked_periodical,*options)
    periodical_borrow_id.grid(row=6,column=1,pady=20)
    periodical_borrow_id_label=Label(top,text='Periodical')
    periodical_borrow_id_label.grid(row=6,column=0)
    borrow_periodical_btn=Button(top,text='Borrow',command = lambda: borrowperiodicalsubmit(value,top,clicked_periodical))
    borrow_periodical_btn.grid(row=7,column=0)

def givebook(a,top):
    top.destroy()
    current_date = date.today().isoformat()
    current_date=str(current_date)
    current_date=current_date.split('-')
    end=date(int(current_date[0]),int(current_date[1]),int(current_date[2]))
    #messagebox.showinfo('Success','Book returned')
    mycursor=mydb.cursor()
    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    d={}
    for i in result:
        if(i[4]=='Faculty'):
            d[i[0]]=30
        elif(i[4]=='Guest'):
            d[i[0]]=7
        elif(i[4]=='Staff'):
            d[i[0]]=30
        elif(i[4]=='Students'):
            d[i[0]]=15
        
    mycursor=mydb.cursor()
    mycursor.execute("select * from book_borrow")
    result=mycursor.fetchall()
    issue=''
    for i in result:
        if(i[0]==a):
            id=i[1]
            issue=i[3]
            break
    span=d[id]
    date_time_obj = datetime.strptime(issue, '%Y-%m-%d')
    e=date_time_obj.date()
    days_after = (e+timedelta(days=span)).isoformat()
    days_after=str(days_after)
    b=days_after.split('-')
    start=date(int(b[0]),int(b[1]),int(b[2]))
    days=np.busday_count(start,end)
    if(int(days)<=0):
        days=0
    days=str(days)
    show='Book returned. Fine of Rs.'+days
    current_date = date.today().isoformat()
    current_date=str(current_date)
    sql = "UPDATE book_borrow SET deposit = %s WHERE id = %s"
    val = (current_date,a)
    mycursor.execute(sql, val)
    mydb.commit()
    #print(a)
    messagebox.showinfo('Success',show)
    
    
    

def returnbook(id):
    current_date = date.today().isoformat()
    current_date=str(current_date)
    current_date=current_date.split('-')
    end=date(int(current_date[0]),int(current_date[1]),int(current_date[2]))
    mycursor=mydb.cursor()
    mycursor.execute("select * from users")
    d={}
    result=mycursor.fetchall()
    for i in result:
        if(i[4]=='Faculty'):
            d[i[0]]=30
        elif(i[4]=='Guest'):
            d[i[0]]=7
        elif(i[4]=='Staff'):
            d[i[0]]=30
        elif(i[4]=='Students'):
            d[i[0]]=15

    mycursor.execute("select * from book_borrow") 
    borrowed=[]
    result=mycursor.fetchall()
    for i in result:
        if(i[1]==id and i[4]=='Not'):
            borrowed.append(i)
    if(len(borrowed)==0):
        messagebox.showinfo('Message','You do not have any books in your possession currently')
    else:
        top_25=Toplevel()
        c=0
        for i in borrowed:
            c=c+1
            my_btn=Button(top_25,text='Book id: '+str(i[2]),command = lambda: givebook(i[0],top_25))
            issue=str(i[3])
            span=int(d[i[1]])
            date_time_obj = datetime.strptime(issue, '%Y-%m-%d')
            a=date_time_obj.date()
            days_after = (a+timedelta(days=span)).isoformat()
            days_after=str(days_after)
            b=days_after.split('-')
            start = date(int(b[0]),int(b[1]),int(b[2]))
            days=np.busday_count(start,end)
            if(int(days)<=0):
                days=0
            days=str(days)
            my_btn.grid(row=c,column=0)
            s='Due on : '+days_after
            my_label=Label(top_25,text=s)
            my_label.grid(row=c,column=1)
            s='Fine : Rs. '+days
            my_label=Label(top_25,text=s)
            my_label.grid(row=c,column=2)

def giveperiodical(a,top):
    top.destroy()
    current_date = date.today().isoformat()
    current_date=str(current_date)
    current_date=current_date.split('-')
    end=date(int(current_date[0]),int(current_date[1]),int(current_date[2]))
    #messagebox.showinfo('Success','Book returned')
    mycursor=mydb.cursor()
    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    d={}
    for i in result:
        if(i[4]=='Faculty'):
            d[i[0]]=30
        elif(i[4]=='Guest'):
            d[i[0]]=7
        elif(i[4]=='Staff'):
            d[i[0]]=30
        elif(i[4]=='Students'):
            d[i[0]]=15
        
    mycursor=mydb.cursor()
    mycursor.execute("select * from periodical_borrow")
    result=mycursor.fetchall()
    issue=''
    for i in result:
        if(i[0]==a):
            id=i[1]
            issue=i[3]
            break
    span=d[id]
    date_time_obj = datetime.strptime(issue, '%Y-%m-%d')
    e=date_time_obj.date()
    days_after = (e+timedelta(days=span)).isoformat()
    days_after=str(days_after)
    b=days_after.split('-')
    start=date(int(b[0]),int(b[1]),int(b[2]))
    days=np.busday_count(start,end)
    if(int(days)<=0):
        days=0
    days=str(days)
    show='Periodical returned. Fine of Rs.'+days
    current_date = date.today().isoformat()
    current_date=str(current_date)
    sql = "UPDATE periodical_borrow SET deposit = %s WHERE id = %s"
    val = (current_date,a)
    mycursor.execute(sql, val)
    mydb.commit()
    #print(a)
    messagebox.showinfo('Success',show)




def returnperiodical(id):
    id=int(id)
    current_date = date.today().isoformat()
    current_date=str(current_date)
    current_date=current_date.split('-')
    end=date(int(current_date[0]),int(current_date[1]),int(current_date[2]))
    mycursor=mydb.cursor()
    mycursor.execute("select * from users")
    d={}
    result=mycursor.fetchall()
    for i in result:
        if(i[4]=='Faculty'):
            d[i[0]]=30
        elif(i[4]=='Guest'):
            d[i[0]]=7
        elif(i[4]=='Staff'):
            d[i[0]]=30
        elif(i[4]=='Students'):
            d[i[0]]=15
    span=int(d[id])
    mycursor.execute("select * from book_borrow") 
    result=mycursor.fetchall()
    current_date = date.today().isoformat()
    current_date=str(current_date)


    mycursor.execute("select * from periodical_borrow") 
    borrowed=[]
    result=mycursor.fetchall()
    for i in result:
        if(i[1]==id and i[4]=='Not'):
            borrowed.append(i)
    if(len(borrowed)==0):
        messagebox.showinfo('Message','You do not have any periodical in your possession currently')
    else:
        top_25=Toplevel()
        c=0
        for i in borrowed:
            c=c+1
            my_btn=Button(top_25,text='Periodical id: '+str(i[2]),command = lambda: giveperiodical(i[0],top_25))
            issue=str(i[3])
            span=int(d[i[1]])
            date_time_obj = datetime.strptime(issue, '%Y-%m-%d')
            a=date_time_obj.date()
            days_after = (a+timedelta(days=span)).isoformat()
            days_after=str(days_after)
            b=days_after.split('-')
            start = date(int(b[0]),int(b[1]),int(b[2]))
            days=np.busday_count(start,end)
            if(int(days)<=0):
                days=0
            days=str(days)
            my_btn.grid(row=c,column=0)
            s='Due on : '+days_after
            my_label=Label(top_25,text=s)
            my_label.grid(row=c,column=1)
            s='Fine : Rs. '+days
            my_label=Label(top_25,text=s)
            my_label.grid(row=c,column=2)


def message(id):
    pass
    


def pay(amt,id,fine):
    mycursor=mydb.cursor()
    mycursor.execute("select * from users") 
    result=mycursor.fetchall()
    a=0
    for i in result:
        if(i[0]==id):
            a=int(i[6])+amt
            break

    sql = "UPDATE users SET paid = %s WHERE id = %s"
    val = (a, id)
    mycursor.execute(sql, val)
    mydb.commit()
    if(fine!=a):
        txt='Amount of Rs. '+str(amt)+' is paid successfully. You still have to pay Rs. '+str(fine-a)+' ...'
    else:
        txt='Amount of Rs. '+str(amt)+' is paid successfully. You dues are cleared'

    messagebox.showinfo('Info',txt)






def viewuser(value,top):
    #messagebox.showinfo("Success",value)
    flag=-1
    mycursor=mydb.cursor()
    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    for i in range(0,len(result)):
        if(result[i][3]==value):
            flag=i
            break
    for i in result:
        if(i[3]==value):
            flag=i
            break
        
    if(flag==-1):
        messagebox.showerror("Error","No user with this username")
    else:
        id=int(flag[0])
        mycursor.execute("select * from users")
        d={}
        result=mycursor.fetchall()
        for i in result:
            if(i[4]=='Faculty'):
                d[i[0]]=30
            elif(i[4]=='Guest'):
                d[i[0]]=7
            elif(i[4]=='Staff'):
                d[i[0]]=30
            elif(i[4]=='Students'):
                d[i[0]]=15
        span=int(d[id])
        due=0
        mycursor.execute("select * from book_borrow")
        result=mycursor.fetchall()
        for i in result:
            if(i[1]==id):
                issue=str(i[3])
                date_time_obj = datetime.strptime(issue, '%Y-%m-%d')
                a=date_time_obj.date()
                days_after = (a+timedelta(days=span)).isoformat()
                days_after=str(days_after)
                b=days_after.split('-')
                start = date(int(b[0]),int(b[1]),int(b[2]))
                if(i[4]=='Not'):
                    current_date = date.today().isoformat()
                    current_date=str(current_date)
                    current_date=current_date.split('-')
                    end=date(int(current_date[0]),int(current_date[1]),int(current_date[2]))
                    days=np.busday_count(start,end)
                else:
                    dt=i[4].split('-')
                    #print('Hello world returned')
                    end=date(int(dt[0]),int(dt[1]),int(dt[2]))
                    days=np.busday_count(start,end)
                days=int(days)
                if(days<0):
                    days=0
                due=due+days
        mycursor.execute("select * from periodical_borrow")
        result=mycursor.fetchall()
        for i in result:
            if(i[1]==id):
                issue=str(i[3])
                date_time_obj = datetime.strptime(issue, '%Y-%m-%d')
                a=date_time_obj.date()
                days_after = (a+timedelta(days=span)).isoformat()
                days_after=str(days_after)
                b=days_after.split('-')
                start = date(int(b[0]),int(b[1]),int(b[2]))
                if(i[4]=='Not'):
                    current_date = date.today().isoformat()
                    current_date=str(current_date)
                    current_date=current_date.split('-')
                    end=date(int(current_date[0]),int(current_date[1]),int(current_date[2]))
                    days=np.busday_count(start,end)
                else:
                    dt=i[4].split('-')
                    end=date(int(dt[0]),int(dt[1]),int(dt[2]))
                    days=np.busday_count(start,end)
                #days=np.busday_count(start,end)
                days=int(days)
                if(days<0):
                    days=0
                due=due+days

        mycursor.execute("select * from users")
        result=mycursor.fetchall()
        amt=0
        for i in result:
            if(i[0]==id):
                amt=i[6]
        fine=due-amt
        fine=str(fine)
        
                







        view_user_label=Label(top,text=flag[3])
        view_user_label.grid(row=2,column=0,padx=5,pady=2)
        edit_user=Button(top,text='Edit User',command = lambda: edituser(flag,top))        
        edit_user.grid(row=2,column=0)
        delete_user=Button(top,text='Delete User',command=lambda: deleteuser(str(flag[3]),int(flag[0])))
        delete_user.grid(row=2,column=1)
        borrow_book=Button(top,text='Borrow Book',command = lambda: borrowbook(flag,top))
        borrow_book.grid(row=3,column=0)
        borrow_periodical=Button(top,text='Borrow Periodical',command = lambda: borrowperiodical(flag,top))
        borrow_periodical.grid(row=3,column=1)
        borrowed_label=Label(top,text="#Books issued currently")
        borrowed_label.grid(row=100,column=0,padx=5,pady=10)
        c=0
        d=0
        am=0
        bm=0
        id=flag[0]
        mycursor.execute("select * from book_borrow")
        result=mycursor.fetchall()
        for i in result:
            if(i[1]==id):
                c=c+1
                if(i[4]=='Not'):
                    d=d+1
        mycursor.execute("select * from periodical_borrow")
        result=mycursor.fetchall()
        for i in result:
            if(i[1]==id):
                bm=bm+1
                if(i[4]=='Not'):
                    am=am+1
        borrowed_label=Label(top,text=str(d))
        borrowed_label.grid(row=100,column=1,padx=5,pady=2)
        borrowed_label=Label(top,text="#Books issued")
        borrowed_label.grid(row=101,column=0,padx=5,pady=2)
        borrowed_label=Label(top,text=str(c))
        borrowed_label.grid(row=101,column=1,padx=5,pady=2)
        borrowed_label=Label(top,text="#Periodicals issued currently")
        borrowed_label.grid(row=102,column=0,padx=5,pady=2)
        borrowed_label=Label(top,text=str(am))
        borrowed_label.grid(row=102,column=1,padx=5,pady=2)
        borrowed_label=Label(top,text="#Periodicals issued")
        borrowed_label.grid(row=103,column=0,padx=5,pady=2)
        borrowed_label=Label(top,text=str(bm))
        borrowed_label.grid(row=103,column=1,padx=5,pady=2)
        borrowed_label=Label(top,text="Due Fine:")
        borrowed_label.grid(row=104,column=0,padx=5,pady=2)
        borrowed_label=Label(top,text='Rs. '+fine)
        borrowed_label.grid(row=104,column=1,padx=5,pady=2)
        fumes=Entry(top,width=30)
        fumes.grid(row=105,column=0,padx=20)
        borrowed_label=Button(top,text='Pay Fine',command = lambda: pay(int(fumes.get()),id,int(due)))
        borrowed_label.grid(row=105,column=1,padx=5,pady=2)
        return_book=Button(top,text='Return Books',command = lambda: returnbook(id))        
        return_book.grid(row=106,column=0)
        return_periodical=Button(top,text='Return Periodicals',command = lambda: returnperiodical(id))        
        return_periodical.grid(row=106,column=1)

def open_view_user():
    top_1=Toplevel()
    top_1.title('View User')
    #global view_username
    view_username=Entry(top_1,width=30)
    view_username.grid(row=0,column=1,padx=20)
    view_username_label=Label(top_1,text='Serch for User')
    view_username_label.grid(row=0,column=0)
    view_user=Button(top_1,text='View User',command = lambda: viewuser(str(view_username.get()),top_1))
    view_user.grid(row=1,column=0,columnspan=2,pady=10,padx=10,ipadx=100)
    

def open_add_user():
    #global my_label
    top=Toplevel()
    top.title('Add User')
    global user_name
    global username
    global email
    global password
    global user_type
    global clicked_user_type
    user_name=Entry(top,width=30)
    user_name.grid(row=0,column=1,padx=20)
    username=Entry(top,width=30)
    username.grid(row=1,column=1)
    email=Entry(top,width=30)
    email.grid(row=2,column=1)
    password=Entry(top,width=30)
    password.grid(row=3,column=1)
    options=["Students", "Faculty", "Staff", "Guest"]
    clicked_user_type=StringVar()
    clicked_user_type.set("Students")
    user_type=OptionMenu(top,clicked_user_type,*options)
    user_type.grid(row=4,column=1)
    name_label=Label(top,text='Name')
    name_label.grid(row=0,column=0)
    user_label=Label(top,text='Username')
    user_label.grid(row=1,column=0)
    email_label=Label(top,text='Email')
    email_label.grid(row=2,column=0)
    password_label=Label(top,text='Password')
    password_label.grid(row=3,column=0)
    user_type_label=Label(top,text='Type')
    user_type_label.grid(row=4,column=0)
    add_user=Button(top,text='Add User',command=adduser)
    add_user.grid(row=6,column=0,columnspan=2,pady=10,padx=10,ipadx=100)

def submit():
    mycursor=mydb.cursor()
    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    msg1="#Users :  "+str(len(result))
    label_1=Label(root,text=msg1)
    label_1.grid(row=1001,column=0)
    #mycursor=mydb.cursor()
    mycursor.execute("select * from author")
    result=mycursor.fetchall()
    msg2="#Authors :  "+str(len(result))
    label_2=Label(root,text=msg2)
    label_2.grid(row=1002,column=0)
    #mycursor=mydb.cursor()
    mycursor.execute("select * from book")
    result=mycursor.fetchall()
    msg3="#Books :  "+str(len(result))
    label_3=Label(root,text=msg3)
    label_3.grid(row=1003,column=0)
    mycursor.execute("select * from periodical")
    result=mycursor.fetchall()
    msg4="#Periodicals :  "+str(len(result))
    label_4=Label(root,text=msg4)
    label_4.grid(row=1004,column=0)

def addauthor(author,top):
    naam=str(author.get())
    mycursor=mydb.cursor()
    sql = "INSERT INTO author (name) VALUES (%s)"
    val=(naam,)
    mycursor.execute(sql, val)
    mydb.commit()
    messagebox.showinfo("Success","Author Added")
    author.delete(0,END)
def viewauthor(author,top):
    mycursor=mydb.cursor()
    mycursor.execute("select * from author")
    result=mycursor.fetchall()
    if(True):
        ids=[]
        for i in result:
            if(i[1]==author):
                ids.append(i[0])
        if(len(ids)==0):
            messagebox.showwarning("Error","No such author")
        else:
            mycursor.execute("select * from book_author")
            result=mycursor.fetchall()
            isbns=[]
            for i in result:
                if(i[1] in ids):
                    isbns.append(i[2])
            if(len(isbns)==0):
                label=Label(top,text="No books by this author")
                label.grid(row=3,column=0)
            else:
                mycursor.execute("select * from book_edition")
                result=mycursor.fetchall()
                c=0
                for i in result:
                    s=''
                    if(i[0] in isbns):
                        c=c+1
                        s=str(c)+'.'+str(i[2])
                        label=Label(top,text=s,anchor='w')
                        label.grid(row=c+2,column=0)
        





def open_view_author():
    top_5=Toplevel()
    top_5.title('View Books by this author')
    #global view_username
    view_author=Entry(top_5,width=30)
    view_author.grid(row=0,column=1,padx=20)
    view_author_label=Label(top_5,text='')
    view_author_label.grid(row=0,column=0)
    view_author_btn=Button(top_5,text='View Books by this author',command = lambda: viewauthor(str(view_author.get()),top_5))
    view_author_btn.grid(row=1,column=0,columnspan=2,pady=10,padx=10,ipadx=100)

def open_add_author():
    top_2=Toplevel()
    top_2.title('Add Author')
    author=Entry(top_2,width=30)
    author.grid(row=0,column=1,padx=20)
    author_label=Label(top_2,text='Author Name')
    author_label.grid(row=0,column=0)
    author_submit_btn=Button(top_2,text='Add Author',command = lambda: addauthor(author,top_2))
    author_submit_btn.grid(row=3,column=0,pady=2)

    #mycursor=mydb.cursor()
    #sql = "INSERT INTO author (name) VALUES (%s)"
    #val=(,)
    #mycursor.execute(sql, val)
    #mydb.commit()

def add_particular_book(book):
    mycursor=mydb.cursor()
    d=date.today().isoformat()
    sql = "INSERT INTO book (isbn,arrival) VALUES (%s, %s)"
    val=(book,d)
    mycursor.execute(sql, val)
    mycursor.execute("select * from book")
    result=mycursor.fetchall()
    c=0
    for i in result:
        if(i[1]==book):
            c=c+1
    
    mydb.commit()
    s="Book is added. Currently you have "+str(c)+" such books."
    messagebox.showinfo("Success",s)

def viewbook(book,top):
    book=int(book.get())
    mycursor=mydb.cursor()
    sql = "SELECT * FROM book_edition WHERE isbn = %s"
    adr = (book,)
    mycursor.execute(sql, adr)
    result = mycursor.fetchall()
    if(len(result)==0):
        messagebox.showerror("Error","No such book exists")
    else:
        publisher_id=result[0][1]
        sql = "SELECT * FROM publisher WHERE id = %s"
        adr = (publisher_id,)
        mycursor.execute(sql, adr)
        p_name=mycursor.fetchall()
        p_name=p_name[0][1]
        a=[]
        sql = "SELECT * FROM book WHERE isbn = %s"
        adr = (result[0][0],)
        mycursor.execute(sql, adr)
        tot = mycursor.fetchall()
        ids=[]
        for i in tot:
            ids.append(i[0])
        a.append(str(len(tot)))
        mycursor.execute("select * from book_borrow")
        borrowed=mycursor.fetchall()
        c=0
        for i in borrowed:
            if(i[2] in ids and i[4]=='Not'):
                c=c+1
        a.append(str(len(tot)-c))
        s=''
        mycursor.execute("select * from book_author")
        authors=mycursor.fetchall()
        t=[]
        for i in authors:
            if(i[2]==book):
                t.append(i[1])
        mycursor.execute("select * from author")
        last=mycursor.fetchall()
        for i in last:
            if(i[0] in t):
                s=s+i[1]+','+' '
        s=s[:-2]
        
        arr=['isbn:','Publisher:','Title:','Pages:','Number of copies in library:','Number of copies currently available:']
        for i in range(1,6):
            if(i==1):
                label=Label(top,text=arr[i])
                label.grid(row=5,column=0)
                label=Label(top,text=p_name)
                label.grid(row=5,column=1)
            elif(i<4):
                label=Label(top,text=arr[i])
                label.grid(row=i+4,column=0)
                label=Label(top,text=result[0][i])
                label.grid(row=i+4,column=1)
            else:
                label=Label(top,text=arr[i])
                label.grid(row=i+4,column=0)
                label=Label(top,text=a[i-4])
                label.grid(row=i+4,column=1)
        label=Label(top,text=s)
        label.grid(row=10,column=1)
        label=Label(top,text="Authors:")
        label.grid(row=10,column=0)
        label=Label(top,text="Add a copy of this book:")
        label.grid(row=11,column=0)
        add_particular_book_btn=Button(top,text='Add',command = lambda: add_particular_book(book))
        add_particular_book_btn.grid(row=11,column=1)




def open_view_book():
    top_7=Toplevel()
    top_7.title('View Book')
    book=Entry(top_7,width=30)
    book.grid(row=0,column=1,padx=20)
    book_label=Label(top_7,text='Book ISBN')
    book_label.grid(row=0,column=0)
    book_submit_btn=Button(top_7,text='View Book Details',command = lambda: viewbook(book,top_7))
    book_submit_btn.grid(row=3,column=0,pady=2)

def addbook(isbn,publisher,title,pages,authors,discipline,top):
    mycursor=mydb.cursor()
    isbn=int(isbn.get())
    publisher=str(publisher.get())
    title=str(title.get())
    pages=int(pages.get())
    discipline=str(discipline.get())
    authors=str(authors.get())
    authors=authors.split(',')
    a=[]
    mycursor.execute("select * from author")
    result=mycursor.fetchall()
    for i in authors:
        for j in result:
            if(j[1]==i):
                a.append(j[0])
                break
    if(len(authors)==len(a)):
        sql = "INSERT INTO book_edition (isbn,publisher_id,title,pages,discipline) VALUES (%s, %s, %s, %s, %s)"
        val = (isbn,publisher,title,pages,discipline)
        mycursor.execute(sql, val)
        mydb.commit()
        for id in a:
            sql = "INSERT INTO book_author (author_id,book_isbn) VALUES (%s, %s)"
            val = (id,isbn)
            mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success","Book Edition added")
    else:
        messagebox.showerror("Error","Make sure all authors are in database")




def open_add_book():
    mycursor=mydb.cursor()
    top_9=Toplevel()
    top_9.title('Add Book Edition')
    isbn=Entry(top_9,width=30)
    isbn.grid(row=0,column=1,padx=20)
    isbn_label=Label(top_9,text='Book ISBN')
    isbn_label.grid(row=0,column=0)
    options=[]
    mycursor.execute("select * from publisher")
    result=mycursor.fetchall()
    for i in result:
        options.append(i[0])
    clicked_publisher=IntVar()
    clicked_publisher.set(options[0])
    publisher_id=OptionMenu(top_9,clicked_publisher,*options)
    publisher_id.grid(row=1,column=1,pady=20)
    publisher_id_label=Label(top_9,text='Publisher')
    publisher_id_label.grid(row=1,column=0)
    title=Entry(top_9,width=30)
    title.grid(row=2,column=1,padx=20)
    title_label=Label(top_9,text='Book title')
    title_label.grid(row=2,column=0)
    pages=Entry(top_9,width=30)
    pages.grid(row=3,column=1,padx=20)
    pages_label=Label(top_9,text='Number of Pages')
    pages_label.grid(row=3,column=0)
    authors=Entry(top_9,width=30)
    authors.grid(row=4,column=1,padx=20)
    authors_label=Label(top_9,text='Authors(Enter in comma separated format)')
    authors_label.grid(row=4,column=0)
    o=["CSE", "ME", "CE", "Math", "Phy", "EE", "Hindi"]
    clicked_discipline=StringVar()
    clicked_discipline.set(o[0])
    discipline=OptionMenu(top_9,clicked_discipline,*o)
    discipline.grid(row=5,column=1,pady=20)
    discipline_label=Label(top_9,text='Discipline')
    discipline_label.grid(row=5,column=0)
    book_submit_btn=Button(top_9,text='Add Book Edition',command = lambda: addbook(isbn,clicked_publisher,title,pages,authors,clicked_discipline,top_9))
    book_submit_btn.grid(row=6,column=0,pady=2)

def view_logs(duration):
    top_10=Toplevel()
    top_10.title('View Logs')
    mycursor=mydb.cursor()
    duration=int(duration.get())
    dates=[]
    a=[]
    b=[]
    g=[]
    f=[]
    mycursor.execute("select * from book_borrow")
    result_1=mycursor.fetchall()
    mycursor.execute("select * from periodical_borrow")
    result_2=mycursor.fetchall()
    current_date = date.today().isoformat()
    for i in range(0,duration):
        days_before = (date.today()-timedelta(days=i)).isoformat()
        dates.append(days_before)
    for i in dates:
        for j in result_1:
            if(j[3]==i):
                a.append(j)
            if(j[4]==i):
                b.append(j)
        for k in result_2:
            if(k[3]==i):
                g.append(k)
            if(k[3]==i):
                f.append(k)
    d={}
    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    for i in result:
        d[i[0]]=i[3]
    label=Label(top_10,text='Borrowed Books:')
    label.grid(row=9,column=0)
    c=0
    e=0
    if(len(a)==0):
        label=Label(top_10,text="No books borrowed in the requested duration....")
        label.grid(row=10+c,column=0)
    else:
        c=c+1
        
        label=Label(top_10,text="S.N")
        label.grid(row=10+c,column=0)
        label=Label(top_10,text="Username")
        label.grid(row=10+c,column=1)
        label=Label(top_10,text="Book ID")
        label.grid(row=10+c,column=2)
        label=Label(top_10,text="Borrow Date")
        label.grid(row=10+c,column=3)
        for i in a:
            e=e+1
            c=c+1
            label=Label(top_10,text=str(e)+" .")
            label.grid(row=10+c,column=0)
            label=Label(top_10,text=d[i[1]])
            label.grid(row=10+c,column=1)
            label=Label(top_10,text=i[2])
            label.grid(row=10+c,column=2)
            label=Label(top_10,text=i[3])
            label.grid(row=10+c,column=3)
    label=Label(top_10,text='Returned Books:')
    label.grid(row=11+c,column=0)
    e=0
    if(len(b)==0):
        label=Label(top_10,text='No books returned in requested duration....')
        label.grid(row=12+c,column=0)
    else:
        c=c+1
        label=Label(top_10,text="S.N")
        label.grid(row=10+c,column=0)
        label=Label(top_10,text="Username")
        label.grid(row=10+c,column=1)
        label=Label(top_10,text="Book ID")
        label.grid(row=10+c,column=2)
        label=Label(top_10,text="Return Date")
        label.grid(row=10+c,column=3)
        for i in b:
            e=e+1
            c=c+1
            label=Label(top_10,text=str(e)+" .")
            label.grid(row=12+c,column=0)
            label=Label(top_10,text=d[i[1]])
            label.grid(row=12+c,column=1)
            label=Label(top_10,text=i[2])
            label.grid(row=12+c,column=2)
            label=Label(top_10,text=i[4])
            label.grid(row=12+c,column=3)
    label=Label(top_10,text='Borrowed Periodicals:')
    label.grid(row=13+c,column=0)
    e=0
    if(len(g)==0):
        label=Label(top_10,text='No borrowed periodicals in requested duration....')
        label.grid(row=14+c,column=0)
    else:
        c=c+1
        label=Label(top_10,text="S.N")
        label.grid(row=10+c,column=0)
        label=Label(top_10,text="Username")
        label.grid(row=10+c,column=1)
        label=Label(top_10,text="Periodical ID")
        label.grid(row=10+c,column=2)
        label=Label(top_10,text="Borrow Date")
        label.grid(row=10+c,column=3)
        for i in g:
            e=e+1
            c=c+1
            label=Label(top_10,text=str(e)+" .")
            label.grid(row=14+c,column=0)
            label=Label(top_10,text=d[i[1]])
            label.grid(row=14+c,column=1)
            label=Label(top_10,text=i[2])
            label.grid(row=14+c,column=2)
            label=Label(top_10,text=i[3])
            label.grid(row=14+c,column=3)
    label=Label(top_10,text='Returned Periodicals:')
    label.grid(row=15+c,column=0)
    e=0
    if(len(f)==0):
        label=Label(top_10,text='No periodicals returned in requested duration.....')
        label.grid(row=16+c,column=0)
    else:
        c=c+1
        label=Label(top_10,text="S.N")
        label.grid(row=10+c,column=0)
        label=Label(top_10,text="Username")
        label.grid(row=10+c,column=1)
        label=Label(top_10,text="Periodical ID")
        label.grid(row=10+c,column=2)
        label=Label(top_10,text="Returned Date")
        label.grid(row=10+c,column=3)
        for i in f:
            e=e+1
            c=c+1
            label=Label(top_10,text=str(e)+" .")
            label.grid(row=16+c,column=0)
            label=Label(top_10,text=d[i[1]])
            label.grid(row=16+c,column=1)
            label=Label(top_10,text=i[2])
            label.grid(row=16+c,column=2)
            label=Label(top_10,text=i[4])
            label.grid(row=16+c,column=3)

def add_particular_periodical(book):
    d=date.today().isoformat() 
    mycursor=mydb.cursor()
    sql = "INSERT INTO periodical (isbn,arrival) VALUES (%s, %s)"
    val=(book,d)
    mycursor.execute(sql, val)
    mycursor.execute("select * from periodical")
    result=mycursor.fetchall()
    c=0
    for i in result:
        if(i[1]==book):
            c=c+1
    mydb.commit()
    s="Periodical is added. Currently you have "+str(c)+" such periodicals."
    messagebox.showinfo("Success",s)
def viewperiodical(book,top):
    book=int(book.get())
    mycursor=mydb.cursor()
    sql = "SELECT * FROM periodical_edition WHERE isbn = %s"
    adr = (book,)
    mycursor.execute(sql, adr)
    result = mycursor.fetchall()
    if(len(result)==0):
        messagebox.showerror("Error","No such periodical exists")
    else:
        publisher_id=result[0][3]
        sql = "SELECT * FROM publisher WHERE id = %s"
        adr = (publisher_id,)
        mycursor.execute(sql, adr)
        p_name=mycursor.fetchall()
        p_name=p_name[0][1]
        a=[]
        sql = "SELECT * FROM periodical WHERE isbn = %s"
        adr = (result[0][0],)
        mycursor.execute(sql, adr)
        tot = mycursor.fetchall()
        ids=[]
        for i in tot:
            ids.append(i[0])
        a.append(str(len(tot)))
        mycursor.execute("select * from periodical_borrow")
        borrowed=mycursor.fetchall()
        c=0
        for i in borrowed:
            if(i[2] in ids and i[4]=='Not'):
                c=c+1
        a.append(str(len(tot)-c))
        arr=['isbn:','Publisher:','Title:','Pages:','Number of copies in library:','Number of copies currently available:']
        for i in range(1,6):
            if(i==1):
                label=Label(top,text=arr[i])
                label.grid(row=5,column=0)
                label=Label(top,text=p_name)
                label.grid(row=5,column=1)
            elif(i<4):
                label=Label(top,text=arr[i])
                label.grid(row=i+4,column=0)
                label=Label(top,text=result[0][i])
                label.grid(row=i+4,column=1)
            else:
                label=Label(top,text=arr[i])
                label.grid(row=i+4,column=0)
                label=Label(top,text=a[i-4])
                label.grid(row=i+4,column=1)
        label=Label(top,text="Add a copy of this periodical:")
        label.grid(row=11,column=0)
        add_particular_book_btn=Button(top,text='Add',command = lambda: add_particular_periodical(book))
        add_particular_book_btn.grid(row=11,column=1)
    

def open_periodical():
    top_12=Toplevel()
    top_12.title('View Periodical')
    book=Entry(top_12,width=30)
    book.grid(row=0,column=1,padx=20)
    book_label=Label(top_12,text='Periodical ISBN')
    book_label.grid(row=0,column=0)
    book_submit_btn=Button(top_12,text='View Periodical Details',command = lambda: viewperiodical(book,top_12))
    book_submit_btn.grid(row=3,column=0,pady=2)

def addperiodical(isbn,year,volume,publisher,title,top):
    mycursor=mydb.cursor()
    isbn=int(isbn.get())
    year=str(year.get())
    volume=str(volume.get())
    title=str(title.get())
    publisher=int(publisher.get())
    if(True):
        sql = "INSERT INTO periodical_edition (isbn,year,volume,publisher_id,title) VALUES (%s, %s, %s, %s, %s)"
        val = (isbn,year,volume,publisher,title)
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success","Periodical Edition added")




def open_add_periodical():
    mycursor=mydb.cursor()
    top_13=Toplevel()
    top_13.title('Add Periodical Edition')
    isbn=Entry(top_13,width=30)
    isbn.grid(row=0,column=1,padx=20)
    isbn_label=Label(top_13,text='Periodical ISBN')
    isbn_label.grid(row=0,column=0)
    options=[]
    mycursor.execute("select * from publisher")
    result=mycursor.fetchall()
    for i in result:
        options.append(i[0])
    clicked_publisher=IntVar()
    clicked_publisher.set(options[0])
    publisher_id=OptionMenu(top_13,clicked_publisher,*options)
    publisher_id.grid(row=1,column=1,pady=20)
    publisher_id_label=Label(top_13,text='Publisher')
    publisher_id_label.grid(row=1,column=0)
    year=Entry(top_13,width=30)
    year.grid(row=2,column=1,padx=20)
    year_label=Label(top_13,text='Periodical year')
    year_label.grid(row=2,column=0)
    volume=Entry(top_13,width=30)
    volume.grid(row=3,column=1,padx=20)
    volume_label=Label(top_13,text='Volume No.')
    volume_label.grid(row=3,column=0)
    title=Entry(top_13,width=30)
    title.grid(row=4,column=1,padx=20)
    title_label=Label(top_13,text='Title')
    title_label.grid(row=4,column=0)
    book_submit_btn=Button(top_13,text='Add Periodical Edition',command = lambda: addperiodical(isbn,year,volume,clicked_publisher,title,top_13))
    book_submit_btn.grid(row=5,column=0,pady=2)

def viewpaper(paper,top):
    paper=str(paper.get())
    mycursor=mydb.cursor()
    sql = "SELECT * FROM paper WHERE name = %s"
    adr = (paper,)
    mycursor.execute(sql, adr)
    result = mycursor.fetchall()
    if(len(result)==0):
        messagebox.showerror("Error","No such paper exists")
    else:
        c=0
        s=''
        mycursor.execute("select * from paper_author")
        authors=mycursor.fetchall()
        mycursor.execute("select * from author")
        a=mycursor.fetchall()
        for i in result:
            s=''
            c=c+1
            s='Paper '+str(c)+" :"
            paper_label=Label(top,text=s)
            paper_label.grid(row=c,column=0)
            isbn=i[2]
            sql = "SELECT * FROM periodical_edition WHERE isbn = %s"
            adr = (isbn,)
            mycursor.execute(sql, adr)
            result_1 = mycursor.fetchall()
            s='Periodical : '+str(result_1[0][4])+'('+str(isbn)+')'
            label=Label(top,text=s)
            label.grid(row=c+1,column=0)
            id=i[0]
            s='Authors: '
            ids=[]
            for j in authors:
                if(j[2]==id):
                    ids.append(j[1])
            for i in a:
                if(i[0] in ids):
                    s=s+str(i[1])+", "
            s=s[:-2]
            label=Label(top,text=s)
            label.grid(row=c+2,column=0)
            
            




def open_paper():
    top_14=Toplevel()
    top_14.title('View Paper')
    paper=Entry(top_14,width=30)
    paper.grid(row=0,column=1,padx=20)
    paper_label=Label(top_14,text='Paper Title')
    paper_label.grid(row=0,column=0)
    paper_submit_btn=Button(top_14,text='View Paper Details',command = lambda: viewpaper(paper,top_14))
    paper_submit_btn.grid(row=1000,column=0,pady=2)

def addpaper(name,clicked_periodical,authors,top_15):
    mycursor=mydb.cursor()
    periodical=int(clicked_periodical.get())
    name=str(name.get())
    authors=str(authors.get())
    authors=authors.split(',')
    a=[]
    mycursor.execute("select * from author")
    result=mycursor.fetchall()
    for i in authors:
        for j in result:
            if(j[1]==i):
                a.append(j[0])
                break
    if(len(authors)==len(a)):
        sql = "INSERT INTO paper (name,periodical_isbn) VALUES (%s, %s)"
        val = (name,periodical)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.execute("select * from paper")
        result=mycursor.fetchall()
        req=0
        for i in result:
            if(i[0]>req):
                req=i[0]
        for id in a:
            sql = "INSERT INTO paper_author (author_id,paper_id) VALUES (%s, %s)"
            val = (id,req)
            mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success","Paper added")
    else:
        messagebox.showerror("Error","Make sure all authors are in database")





def open_add_paper():
    mycursor=mydb.cursor()
    top_15=Toplevel()
    top_15.title('Add Paper')
    name=Entry(top_15,width=30)
    name.grid(row=0,column=1,padx=20)
    name_label=Label(top_15,text='Paper Name')
    name_label.grid(row=0,column=0)
    options=[]
    mycursor.execute("select * from periodical_edition")
    result=mycursor.fetchall()
    for i in result:
        options.append(i[0])
    clicked_periodical=IntVar()
    clicked_periodical.set(options[0])
    periodical_id=OptionMenu(top_15,clicked_periodical,*options)
    periodical_id.grid(row=1,column=1,pady=20)
    periodical_id_label=Label(top_15,text='Periodical')
    periodical_id_label.grid(row=1,column=0)
    authors=Entry(top_15,width=30)
    authors.grid(row=4,column=1,padx=20)
    authors_label=Label(top_15,text='Authors(Enter in comma separated format)')
    authors_label.grid(row=4,column=0)
    book_submit_btn=Button(top_15,text='Add Paper',command = lambda: addpaper(name,clicked_periodical,authors,top_15))
    book_submit_btn.grid(row=5,column=0,pady=2)

def view_new(duration):
    mycursor=mydb.cursor()
    top_16=Toplevel()
    top_16.title('New Additions')
    duration=int(duration.get())
    dates=[]
    for i in range(duration):
        days_before = (date.today()-timedelta(days=i)).isoformat()
        dates.append(days_before)
    mycursor.execute("select * from book")
    books=mycursor.fetchall()
    mycursor.execute("select * from periodical")
    periodicals=mycursor.fetchall()
    book_label=Label(top_16,text="New book additions:")
    book_label.grid(row=0,column=0)
    a=[]
    b=[]
    t=0
    for i in dates:
        for j in books:
            if(j[2]==i):
                a.append(j)
        for k in periodicals:
            if(k[2]==i):
                b.append(k)
    if(len(a)==0):
        book_label=Label(top_16,text="No new book additions in requested duration")
        book_label.grid(row=1,column=0)
    else:
        u=0
        t=t+1
        label=Label(top_16,text="S.N.")
        label.grid(row=t,column=0)
        label=Label(top_16,text="Book ISBN")
        label.grid(row=t,column=1)
        label=Label(top_16,text="Arrival")
        label.grid(row=t,column=2)
        for i in a:
            u=u+1
            t=t+1
            label=Label(top_16,text=str(u))
            label.grid(row=t,column=0)
            label=Label(top_16,text=str(i[1]))
            label.grid(row=t,column=1)
            label=Label(top_16,text=str(i[2]))
            label.grid(row=t,column=2)
    t=t+1
    book_label=Label(top_16,text="New periodicals additions:")
    book_label.grid(row=t,column=0)
    if(len(b)==0):
        t=t+1
        book_label=Label(top_16,text="No new periodical additions")
        book_label.grid(row=t,column=0)
    else:
        u=0
        t=t+1
        label=Label(top_16,text="S.N.")
        label.grid(row=t,column=0)
        label=Label(top_16,text="Periodical ISBN")
        label.grid(row=t,column=1)
        label=Label(top_16,text="Arrival")
        label.grid(row=t,column=2)
        for i in b:
            u=u+1
            t=t+1
            label=Label(top_16,text=str(u))
            label.grid(row=t,column=0)
            label=Label(top_16,text=str(i[1]))
            label.grid(row=t,column=1)
            label=Label(top_16,text=str(i[2]))
            label.grid(row=t,column=2)

def deletebook(isbn,top):
    mycursor=mydb.cursor()
    isbn=int(isbn.get())
    mycursor.execute("select * from book")
    result=mycursor.fetchall()
    arr=[]
    for i in result:
        if(i[1]==isbn and i[3]=='Not'):
            arr.append(i[0])
    if(len(arr)==0):
        messagebox.showerror('Error','No such book exists')
    else:
        mycursor.execute("select * from book_borrow")
        result=mycursor.fetchall()
        flag=0
        for i in result:
            if(i[2] in arr and i[4]=='Not'):
                flag=1
                break
        if(flag==1):
            messagebox.showwarning('Warning','Some copies of this book are yet not returned')
        else:
            current_date = date.today().isoformat() 
            sql = "UPDATE book SET del = %s WHERE isbn = %s"
            val = (str(current_date), isbn)
            mycursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo('Success','All copies of this book were deleted')


def delete_particular_book(id,top):
    mycursor=mydb.cursor()
    id=int(id.get())
    mycursor.execute("select * from book")
    result=mycursor.fetchall()
    flag=0
    for i in result:
        if(i[0]==id and i[3]=='Not'):
            flag=1
            break
    if(flag==0):
        messagebox.showerror('Error','This book does not exist')
    else:
        mycursor.execute("select * from book_borrow")
        result=mycursor.fetchall()
        c=0
        for i in result:
            if(i[2]==id and i[4]=='Not'):
                c=1
                break
        if(c==1):
            messagebox.showwarning('Warning','This book is currently issued')
        else:
            current_date = date.today().isoformat() 
            sql = "UPDATE book SET del = %s WHERE id = %s"
            val = (str(current_date), id)
            mycursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo('Success','This book was deleted')


def deleteperiodical(isbn,top):
    mycursor=mydb.cursor()
    isbn=int(isbn.get())
    mycursor.execute("select * from periodical")
    result=mycursor.fetchall()
    arr=[]
    for i in result:
        if(i[1]==isbn and i[3]=='Not'):
            arr.append(i[0])
    if(len(arr)==0):
        messagebox.showerror('Error','No such periodical exists')
    else:
        mycursor.execute("select * from periodical_borrow")
        result=mycursor.fetchall()
        flag=0
        for i in result:
            if(i[2] in arr and i[4]=='Not'):
                flag=1
                break
        if(flag==1):
            messagebox.showwarning('Warning','Some copies of this periodical are yet not returned')
        else:
            current_date = date.today().isoformat() 
            sql = "UPDATE periodical SET del = %s WHERE isbn = %s"
            val = (str(current_date), isbn)
            mycursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo('Success','All copies of this periodical were deleted')



def delete_particular_periodical(id,top):
    mycursor=mydb.cursor()
    id=int(id.get())
    mycursor.execute("select * from book")
    result=mycursor.fetchall()
    flag=0
    for i in result:
        if(i[0]==id and i[3]=='Not'):
            flag=1
            break
    if(flag==0):
        messagebox.showerror('Error','This book does not exist')
    else:
        mycursor.execute("select * from periodical_borrow")
        result=mycursor.fetchall()
        c=0
        for i in result:
            if(i[2]==id and i[4]=='Not'):
                c=1
                break
        if(c==1):
            messagebox.showwarning('Warning','This periodical is currently issued')
        else:
            current_date = date.today().isoformat() 
            sql = "UPDATE periodical SET del = %s WHERE id = %s"
            val = (str(current_date), id)
            mycursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo('Success','This periodical was deleted')



    

def open_delete_book():
    top_17=Toplevel()
    top_17.title('Delete Book')
    isbn=Entry(top_17,width=30)
    isbn.grid(row=0,column=1,padx=20)
    isbn_label=Label(top_17,text='Delete by ISBN')
    isbn_label.grid(row=0,column=0)
    isbn_btn=Button(top_17,text='Go',command = lambda: deletebook(isbn,top_17))
    isbn_btn.grid(row=0,column=2,pady=2,padx=4)
    id=Entry(top_17,width=30)
    id.grid(row=1,column=1,padx=20)
    id_label=Label(top_17,text='Delete by ID')
    id_label.grid(row=1,column=0)
    isbn_btn=Button(top_17,text='Go',command = lambda: delete_particular_book(id,top_17))
    isbn_btn.grid(row=1,column=2,pady=2,padx=4)

    


def open_delete_periodical():
    top_18=Toplevel()
    top_18.title('Delete Periodical')
    isbn=Entry(top_18,width=30)
    isbn.grid(row=0,column=1,padx=20)
    isbn_label=Label(top_18,text='Delete by ISBN')
    isbn_label.grid(row=0,column=0)
    isbn_btn=Button(top_18,text='Go',command = lambda: deleteperiodical(isbn,top_18))
    isbn_btn.grid(row=0,column=2,pady=2,padx=4)
    id=Entry(top_18,width=30)
    id.grid(row=1,column=1,padx=20)
    id_label=Label(top_18,text='Delete by ID')
    id_label.grid(row=1,column=0)
    isbn_btn=Button(top_18,text='Go',command = lambda: delete_particular_periodical(id,top_18))
    isbn_btn.grid(row=1,column=2,pady=2,padx=4)


def reservebook(isbn,user,top):
    mycursor=mydb.cursor()
    username=str(user.get())
    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    id=0
    for i in result:
        if(i[3]==username):
            id=i[0]
            break
    sql = "INSERT INTO waiting (user_id, book_isbn, request) VALUES (%s, %s, %s)"
    val = (int(id),int(isbn),"Not")
    mycursor.execute(sql, val)
    mydb.commit()
    messagebox.showinfo('Info','Book Reserved. It will be issued to you when available')



def reserveperiodical(isbn,user,top):
    return


def searchbook(isbn,top):
    mycursor=mydb.cursor()
    isbn=int(isbn.get())
    mycursor.execute("select * from book")
    result=mycursor.fetchall()
    ids=[]
    for i in result:
        if(i[1]==isbn and i[3]=='Not'):
            ids.append(i[0])
    if(len(ids)==0):
        messagebox.showerror('Error','This book does not exist')
    else:
        mycursor.execute("select * from book_borrow")
        result=mycursor.fetchall()
        arr=[]
        diff=[]
        for i in result:
            if(i[2] in ids and i[4]=='Not'):
                arr.append(i[2])
        for i in ids:
            if(i not in arr):
                diff.append(i)
        diff.sort()
        if(len(diff)==0):
            notice=Label(top,text="Sorry all books are currently issued")
            notice.grid(row=1,column=0)
            user=Entry(top,width=30)
            user.grid(row=2,column=1,padx=20)
            user_label=Label(top,text='Username')
            user_label.grid(row=2,column=0)
            user_btn=Button(top,text='Reserve',command = lambda: reservebook(isbn,user,top))
            user_btn.grid(row=2,column=2,pady=2,padx=4)
        else:
            s='Currently available: '
            for i in diff:
                s=s+str(i)+", "
            s=s[:-2]
            notice=Label(top,text=s)
            notice.grid(row=1,column=0)




def searchperiodical(isbn,top):
    mycursor=mydb.cursor()
    isbn=int(isbn.get())
    mycursor.execute("select * from periodical")
    result=mycursor.fetchall()
    ids=[]
    for i in result:
        if(i[1]==isbn and i[3]=='Not'):
            ids.append(i[0])
    if(len(ids)==0):
        messagebox.showerror('Error','This periodical does not exist')
    else:
        mycursor.execute("select * from periodical_borrow")
        result=mycursor.fetchall()
        arr=[]
        diff=[]
        for i in result:
            if(i[2] in ids and i[4]=='Not'):
                arr.append(i[2])
        for i in ids:
            if(i not in arr):
                diff.append(i)
        diff.sort()
        if(len(diff)==0):
            notice=Label(top,text="Sorry all periodicals are currently issued")
            notice.grid(row=1,column=0)
            
        else:
            s='Currently available: '
            for i in diff:
                s=s+str(i)+", "
            s=s[:-2]
            notice=Label(top,text=s)
            notice.grid(row=1,column=0)





def open_book_available():
    top_19=Toplevel()
    top_19.title('Search for book')
    isbn=Entry(top_19,width=30)
    isbn.grid(row=0,column=1,padx=20)
    isbn_label=Label(top_19,text='Search for book(ISBN)')
    isbn_label.grid(row=0,column=0)
    isbn_btn=Button(top_19,text='Go',command = lambda: searchbook(isbn,top_19))
    isbn_btn.grid(row=0,column=2,pady=2,padx=4)

def open_periodical_available():
    top_20=Toplevel()
    top_20.title('Search for periodical')
    isbn=Entry(top_20,width=30)
    isbn.grid(row=0,column=1,padx=20)
    isbn_label=Label(top_20,text='Search for periodical(ISBN)')
    isbn_label.grid(row=0,column=0)
    isbn_btn=Button(top_20,text='Go',command = lambda: searchperiodical(isbn,top_20))
    isbn_btn.grid(row=0,column=2,pady=2,padx=4)

def viewbookdues(dues):
    current_date = date.today().isoformat()
    current_date=str(current_date)
    current_date=current_date.split('-')
    end=date(int(current_date[0]),int(current_date[1]),int(current_date[2]))
    mycursor=mydb.cursor()
    top_24=Toplevel()
    top_24.title('View book dues')
    dues=int(dues.get())
    dates=[]
    for i in range(0,dues):
        days_before=(date.today()-timedelta(days=i)).isoformat()
        dates.append(str(days_before))
    d={}
    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    for i in result:
        if(i[4]=='Faculty'):
            d[i[0]]=(i[3],30)
        elif(i[4]=='Guest'):
            d[i[0]]=(i[3],7)
        elif(i[4]=='Staff'):
            d[i[0]]=(i[3],30)
        elif(i[4]=='Students'):
            d[i[0]]=(i[3],15)
    mycursor.execute("select * from book_borrow")
    result=mycursor.fetchall()
    arr=[]
    for i in dates:
        for j in result:
            if(j[4]=='Not'):
                print(j)
                issue=str(j[3])
                span=int(d[j[1]][1])
                date_time_obj = datetime.strptime(issue, '%Y-%m-%d')
                a=date_time_obj.date()
                days_after = (a+timedelta(days=span)).isoformat()
                days_after=str(days_after)
                if(i==days_after):
                    b=days_after.split('-')
                    start = date(int(b[0]),int(b[1]),int(b[2]))
                    days=np.busday_count(start,end)
                    days=int(days)
                    entry=(j[2],d[j[1]][0],days_after,days)
                    arr.append(entry)
    
    if(len(arr)==0):
        msg=Label(top_24,text='No book dues')
        msg.grid(row=0,column=0)
    else:
        msg=Label(top_24,text='S.N.')
        msg.grid(row=0,column=0)
        msg=Label(top_24,text='Book(id)')
        msg.grid(row=0,column=1)
        msg=Label(top_24,text='Username')
        msg.grid(row=0,column=2)
        msg=Label(top_24,text='Due Date')
        msg.grid(row=0,column=3)
        msg=Label(top_24,text='Fine(Rs.)')
        msg.grid(row=0,column=4)
        c=0
        for i in arr:
            c=c+1
            msg=Label(top_24,text=str(c)+".")
            msg.grid(row=c,column=0)
            msg=Label(top_24,text=i[0])
            msg.grid(row=c,column=1)
            msg=Label(top_24,text=i[1])
            msg.grid(row=c,column=2)
            msg=Label(top_24,text=i[2])
            msg.grid(row=c,column=3)
            msg=Label(top_24,text=i[3])
            msg.grid(row=c,column=4)










                 




      
    

def viewperiodicaldues(dues):
    current_date = date.today().isoformat()
    current_date=str(current_date)
    current_date=current_date.split('-')
    end=date(int(current_date[0]),int(current_date[1]),int(current_date[2]))
    mycursor=mydb.cursor()
    top_24=Toplevel()
    top_24.title('View periodical dues')
    dues=int(dues.get())
    dates=[]
    for i in range(0,dues):
        days_before=(date.today()-timedelta(days=i)).isoformat()
        dates.append(str(days_before))
    d={}
    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    for i in result:
        if(i[4]=='Faculty'):
            d[i[0]]=(i[3],30)
        elif(i[4]=='Guest'):
            d[i[0]]=(i[3],7)
        elif(i[4]=='Staff'):
            d[i[0]]=(i[3],30)
        elif(i[4]=='Students'):
            d[i[0]]=(i[3],15)
    mycursor.execute("select * from periodical_borrow")
    result=mycursor.fetchall()
    arr=[]
    for i in dates:
        for j in result:
            if(j[4]=='Not'):
                issue=str(j[3])
                span=int(d[j[1]][1])
                date_time_obj = datetime.strptime(issue, '%Y-%m-%d')
                a=date_time_obj.date()
                days_after = (a+timedelta(days=span)).isoformat()
                days_after=str(days_after)
                if(i==days_after):
                    b=days_after.split('-')
                    start = date(int(b[0]),int(b[1]),int(b[2]))
                    days=np.busday_count(start,end)
                    days=int(days)
                    entry=(j[2],d[j[1]][0],days_after,days)
                    arr.append(entry)
    
    if(len(arr)==0):
        msg=Label(top_24,text='No periodical dues')
        msg.grid(row=0,column=0)
    else:
        msg=Label(top_24,text='S.N.')
        msg.grid(row=0,column=0)
        msg=Label(top_24,text='Periodical(id)')
        msg.grid(row=0,column=1)
        msg=Label(top_24,text='Username')
        msg.grid(row=0,column=2)
        msg=Label(top_24,text='Due Date')
        msg.grid(row=0,column=3)
        msg=Label(top_24,text='Fine(Rs.)')
        msg.grid(row=0,column=4)
        c=0
        for i in arr:
            c=c+1
            msg=Label(top_24,text=str(c)+".")
            msg.grid(row=c,column=0)
            msg=Label(top_24,text=i[0])
            msg.grid(row=c,column=1)
            msg=Label(top_24,text=i[1])
            msg.grid(row=c,column=2)
            msg=Label(top_24,text=i[2])
            msg.grid(row=c,column=3)
            msg=Label(top_24,text=i[3])
            msg.grid(row=c,column=4)


def issue_reserve():
    current_date = date.today().isoformat()
    current_date=str(current_date)
    mycursor=mydb.cursor()
    arr=[]
    d={}
    mycursor.execute("select * from book_edition")
    result=mycursor.fetchall()
    for i in result:
        d[i[0]]=[]
    mycursor.execute("select * from waiting")
    result=mycursor.fetchall()
    for i in result:
        if(i[3]=='Not'):
            arr.append(i)
    arr.sort(key = lambda x: x[0])
    ids=[]
    b=[]
    mycursor.execute("select * from book_borrow")
    result=mycursor.fetchall()
    for i in result:
        b.append(i)
        if(i[4]=='Not'):
            ids.append(i[2])
    mycursor.execute("select * from book")
    result=mycursor.fetchall()
    for i in result:
        if(i[3]=='Not' and i[0] not in ids):
            d[i[1]].append(i[0])
    #print(d)
    f={}
    p={}
    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    for i in result:
        p[i[0]]=i[2]
    for i in result:
        c=0
        for j in b:
            if(j[1]==i[0] and j[4]=='Not'):
                c=c+1
        if(i[4]=='Faculty'):
            f[i[0]]=(c,6)
        elif(i[4]=='Guest'):
            f[i[0]]=(c,2)
        elif(i[4]=='Staff'):
            f[i[0]]=(c,4)
        elif(i[4]=='Students'):
            f[i[0]]=(c,3)


    current_date=str(current_date)
    for i in arr:
        if(len(d[i[2]])>0):
            give=d[i[2]][0]
            #if(f[i[1]][0]!=f[i[1]][1]):
            if(True):
                #sql = "INSERT INTO book_borrow (user_id,book_id,issue,deposit) VALUES (%s, %s, %s, %s)"
                #val = (i[1],give,current_date,'Not')
                #mycursor.execute(sql, val)
                isbn=i[2]
                message="Book request for "+str(isbn)+'\n'+'\n'+'Hi, the book you requested is available as of now....Hurry!!!'
                receive=str(p[i[1]])
                context=ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com',port,context=context) as server:
                    server.login(sender,password)
                    server.sendmail(sender,receive,message)
                sql = "UPDATE waiting SET request = %s WHERE id = %s"
                val = (current_date,i[0])
                mycursor.execute(sql, val)
                mydb.commit()
                #d[i[2]].remove(give)
    mydb.commit()
    messagebox.showinfo('Info','Books issued')



def issue_dues():
    mycursor=mydb.cursor()
    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    d={}
    p={}
    for i in result:
        p[i[0]]=i[2]
        if(i[4]=='Faculty'):
            d[i[0]]=30
        elif(i[4]=='Guest'):
            d[i[0]]=7        
        elif(i[4]=='Staff'):
            d[i[0]]=30
        elif(i[4]=='Students'):
            d[i[0]]=15
    mycursor.execute("select * from book_borrow")
    result=mycursor.fetchall()
    f={}
    current_date = date.today().isoformat()
    current_date=str(current_date)
    for i in result:
        if(i[4]=='Not'):
            issue=str(i[3])
            span=int(d[i[1]])
            date_time_obj = datetime.strptime(issue, '%Y-%m-%d')
            a=date_time_obj.date()
            days_after = (a+timedelta(days=span)).isoformat()
            days_after=str(days_after)
            if(current_date==days_after):
                if(i[1] not in f):
                    f[i[1]]=[]
                    f[i[1]].append(i[2])
                else:
                    f[i[1]].append(i[2])
    for i in f:
        s=''
        for j in f[i]:
            s=s+str(j)+' '
        s=s[:-1]
        receive=str(p[i])
        message="Subject:Reminder... "+'\n'+'\n'+'Hi there. This is a reminder for you to return books today: '+s
        context=ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',port,context=context) as server:
            server.login(sender,password)
            server.sendmail(sender,receive,message)
    
    #mydb.commit()
    messagebox.showinfo('Info','Mails sent..')



def issue_dues_periodicals():
    mycursor=mydb.cursor()
    mycursor.execute("select * from users")
    result=mycursor.fetchall()
    d={}
    p={}
    for i in result:
        p[i[0]]=i[2]
        if(i[4]=='Faculty'):
            d[i[0]]=30
        elif(i[4]=='Guest'):
            d[i[0]]=7        
        elif(i[4]=='Staff'):
            d[i[0]]=30
        elif(i[4]=='Students'):
            d[i[0]]=15
    mycursor.execute("select * from periodical_borrow")
    result=mycursor.fetchall()
    f={}
    current_date = date.today().isoformat()
    current_date=str(current_date)
    for i in result:
        if(i[4]=='Not'):
            issue=str(i[3])
            span=int(d[i[1]])
            date_time_obj = datetime.strptime(issue, '%Y-%m-%d')
            a=date_time_obj.date()
            days_after = (a+timedelta(days=span)).isoformat()
            days_after=str(days_after)
            if(current_date==days_after):
                if(i[1] not in f):
                    f[i[1]]=[]
                    f[i[1]].append(i[2])
                else:
                    f[i[1]].append(i[2])
    for i in f:
        s=''
        for j in f[i]:
            s=s+str(j)+' '
        s=s[:-1]
        receive=str(p[i])
        message="Subject:Reminder... "+'\n'+'\n'+'Hi there. This is a reminder for you to return periodicals today: '+s
        context=ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',port,context=context) as server:
            server.login(sender,password)
            server.sendmail(sender,receive,message)
    
    #mydb.commit()
    messagebox.showinfo('Info','Mails sent..')


def tags_books(vars,d,top,c):
    arr=[]
    b=[]
    for i in vars:
        arr.append(i.get())
    cntr=-1
    isbns=[]
    f={}
    for i in d:
        cntr=cntr+1
        if(arr[cntr]==1):
            b.append(i)
    mycursor=mydb.cursor()
    mycursor.execute("select * from book_tags")
    result=mycursor.fetchall()
    for i in result:
        if(i[1] in f):
            f[i[1]].append(i[2])
        else:
            f[i[1]]=[]
            f[i[1]].append(i[2])
    for i in f:
        if(set(f[i])==set(b)):
            isbns.append(i)
    #print(isbns)
    r={}
    for i in set(isbns):
        r[i]=0
    borrowed=[]
    mycursor.execute("select * from book_borrow")
    result=mycursor.fetchall()
    for i in result:
        if(i[4]=='Not'):
            borrowed.append(i[2])
    mycursor.execute("select * from book")
    result=mycursor.fetchall()
    for i in result:
        if(i[3]=='Not' and i[1] in isbns and i[0] not in borrowed):
            r[i[1]]=r[i[1]]+1
    label=Label(top,text="Books with requested Tags:")
    label.grid(row=c+3,column=0)
    c=c+1
    if(len(r)==0):
        top.destroy()
        messagebox.showinfo('Info','No books with requested tags')
    else:
        label=Label(top,text="ISBN:")
        label.grid(row=c+3,column=0)
        label=Label(top,text="#Available Copies")
        label.grid(row=c+3,column=1)
        s=0
        for i in r:
            c=c+1
            s=s+r[i]
            label=Label(top,text=str(i))
            label.grid(row=c+3,column=0)
            label=Label(top,text=str(r[i]))
            label.grid(row=c+3,column=1)
        if(s==0):
            label=Label(top,text="All books with these tags are issued. Try reserving them")
            label.grid(row=c+100,column=0)


def tags_periodicals(vars,d,top,c):
    arr=[]
    b=[]
    for i in vars:
        arr.append(i.get())
    cntr=-1
    isbns=[]
    f={}
    for i in d:
        cntr=cntr+1
        if(arr[cntr]==1):
            b.append(i)
    mycursor=mydb.cursor()
    mycursor.execute("select * from periodical_tags")
    result=mycursor.fetchall()
    for i in result:
        if(i[1] in f):
            f[i[1]].append(i[2])
        else:
            f[i[1]]=[]
            f[i[1]].append(i[2])
    for i in f:
        if(set(f[i])==set(b)):
            isbns.append(i)
    #print(isbns)
    r={}
    for i in set(isbns):
        r[i]=0
    borrowed=[]
    mycursor.execute("select * from periodical_borrow")
    result=mycursor.fetchall()
    for i in result:
        if(i[4]=='Not'):
            borrowed.append(i[2])
    mycursor.execute("select * from periodical")
    result=mycursor.fetchall()
    for i in result:
        if(i[3]=='Not' and i[1] in isbns and i[0] not in borrowed):
            r[i[1]]=r[i[1]]+1
    label=Label(top,text="Books with requested Tags:")
    label.grid(row=c+3,column=0)
    c=c+1
    if(len(r)==0):
        top.destroy()
        messagebox.showinfo('Info','No periodicals with requested tags')
    else:
        label=Label(top,text="ISBN:")
        label.grid(row=c+3,column=0)
        label=Label(top,text="#Available Copies")
        label.grid(row=c+3,column=1)
        s=0
        for i in r:
            c=c+1
            s=s+r[i]
            label=Label(top,text=str(i))
            label.grid(row=c+3,column=0)
            label=Label(top,text=str(r[i]))
            label.grid(row=c+3,column=1)
        if(s==0):
            label=Label(top,text="All books with these tags are issued. Try reserving them")
            label.grid(row=c+100,column=0)

    



    


    






def search_book_tags():
    top_50=Toplevel()
    d={}
    mycursor=mydb.cursor()
    mycursor.execute("select * from tag")
    result=mycursor.fetchall()
    for i in result:
        d[i[0]]=i[1]
    vars = []
    l=len(d)
    c=2
    for i in d:
        c=c+1
        r=IntVar()
        vars.append(r)
        radio=Checkbutton(top_50,text=d[i],variable=r)
        radio.grid(row=c,column=0,pady=2)
    btn_2=Button(top_50,text='Search',command = lambda: tags_books(vars,d,top_50,c))
    btn_2.grid(row=c+2,column=0,pady=2)



def search_periodical_tags():
    top_51=Toplevel()
    d={}
    mycursor=mydb.cursor()
    mycursor.execute("select * from tag")
    result=mycursor.fetchall()
    for i in result:
        d[i[0]]=i[1]
    vars = []
    l=len(d)
    c=2
    for i in d:
        c=c+1
        r=IntVar()
        vars.append(r)
        radio=Checkbutton(top_51,text=d[i],variable=r)
        radio.grid(row=c,column=0,pady=2)
    btn_2=Button(top_51,text='Search',command = lambda: tags_periodicals(vars,d,top_51,c))
    btn_2.grid(row=c+2,column=0,pady=2)  




            


    



root=Tk()
root.title('LMS')
root.geometry("600x550")
btn_1=Button(root,text='Check Inventory',command=submit)
btn_1.grid(row=1000,column=0,pady=10,padx=30,columnspan=2)







btn_2=Button(root,text='Add User',command=open_add_user)
btn_2.grid(row=0,column=0,pady=2)
btn_3=Button(root,text='View User',command=open_view_user)
btn_3.grid(row=0,column=1,pady=2)
btn_4=Button(root,text='Add Author',command=open_add_author)
btn_4.grid(row=1,column=1,pady=2)
btn_5=Button(root,text='View Author information',command=open_view_author)
btn_5.grid(row=1,column=0,pady=2)
btn_6=Button(root,text='View Book Information',command=open_view_book)
btn_6.grid(row=2,column=0,pady=2)
btn_7=Button(root,text='Add Book Edition',command=open_add_book)
btn_7.grid(row=2,column=1,pady=2)
label=Label(root,text="View Logs(In days)")
btn_9=Button(root,text='View Periodical',command=open_periodical)
btn_9.grid(row=3,column=0,pady=2,padx=4)
btn_10=Button(root,text='Add Periodical',command=open_add_periodical)
btn_10.grid(row=3,column=1,pady=2,padx=4)
btn_9=Button(root,text='View Paper',command=open_paper)
btn_9.grid(row=4,column=0,pady=2,padx=4)
btn_10=Button(root,text='Add Paper',command=open_add_paper)
btn_10.grid(row=4,column=1,pady=2,padx=4)
label.grid(row=5,column=0)
duration=Entry(root,width=30)
duration.grid(row=5,column=1)
btn_8=Button(root,text='View Logs',command = lambda: view_logs(duration))
btn_8.grid(row=5,column=2,pady=2,padx=4)
my_label=Label(root,text='New Aditions!!')
my_label.grid(row=6,column=0)
duration_books=Entry(root,width=30)
duration_books.grid(row=6,column=1)
btn_8=Button(root,text='View New Additions',command = lambda: view_new(duration_books))
btn_8.grid(row=6,column=2,pady=2,padx=4)
label_8=Label(root,text='View Book Dues:(In days)')
label_8.grid(row=7,column=0)
dues=Entry(root,width=30)
dues.grid(row=7,column=1)
btn_16=Button(root,text='View Dues',command = lambda: viewbookdues(dues))
btn_16.grid(row=7,column=2,pady=2,padx=4)
dues_1=Entry(root,width=30)
dues_1.grid(row=8,column=1)
label_9=Label(root,text='View Periodical Dues:(In days)')
label_9.grid(row=8,column=0)
btn_16=Button(root,text='View Dues',command = lambda: viewperiodicaldues(dues_1))
btn_16.grid(row=8,column=2,pady=2,padx=4)
btn_12=Button(root,text='Delete Book',command = open_delete_book)
btn_12.grid(row=9,column=0,pady=2,padx=4)
btn_13=Button(root,text='Delete Periodical',command = open_delete_periodical)
btn_13.grid(row=9,column=1,pady=2,padx=4)
btn_14=Button(root,text='Check Book Availability',command = open_book_available)
btn_14.grid(row=10,column=0,pady=4,padx=4)
btn_15=Button(root,text='Check Periodical Availability',command = open_periodical_available)
btn_15.grid(row=10,column=1,pady=4,padx=4)
btn_16=Button(root,text='Issue book requests',command = issue_reserve)
btn_16.grid(row=11,column=0,pady=4,padx=4)
btn_17=Button(root,text='Issue book dues',command = issue_dues)
btn_17.grid(row=11,column=1,pady=4,padx=4)
btn_17=Button(root,text='Issue periodicals dues',command = issue_dues_periodicals)
btn_17.grid(row=11,column=2,pady=4,padx=4)
btn_17=Button(root,text='Search book by tags',command = search_book_tags)
btn_17.grid(row=12,column=0,pady=4,padx=4)
btn_17=Button(root,text='Search periodical by tags',command = search_periodical_tags)
btn_17.grid(row=12,column=1,pady=4,padx=4)
#btn_7=Button(root,text='Add Book',command=open_add_particular_book)
#btn_7.grid(row=2,column=2,padx=60, pady=10)
root.mainloop()