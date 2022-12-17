import mysql.connector
import maskpass
import os
from tabulate import tabulate
import matplotlib.pyplot as plt

def calculateResult(t):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM STUDENTS")
    myresult = mycursor.fetchall()
    mycursor.execute("SELECT * FROM STUDENTS")
    myresult1 = mycursor.fetchall()
    mycursor.execute("DESCRIBE STUDENTS")
    myresult2 = mycursor.fetchall()
    if myresult[0][0]!=0:
        head = []
        temp = ''
        for i in myresult2[6:]:
            head.append(i[0])
        if head != []:
            for ele in head:
                temp += ele+'+'
        mycursor.execute("SELECT REG_NO, COALESCE(SUM({}),0) FROM STUDENTS GROUP BY REG_NO".format(temp[:-1]))
        myresult = mycursor.fetchall()
        for i in myresult:
            regNo = i[0]
            gTotal = i[1]
            noOfSub = len(head)
            per = (gTotal/(noOfSub*100))*100
            if per >= 91 and per<100:
                grade = 'A+'
            elif per >=81 and per<=90:
                grade='A'
            elif per >=71 and per<=80:
                grade='B'
            elif per >=61 and per<=70:
                grade='C'
            elif per >=51 and per<=60:
                grade='D'
            elif per >=41 and per<=50:
                grade='E'
            elif per<=40:
                grade='F'
            else:
                grade='NA'
            mycursor.execute("UPDATE STUDENTS SET G_TOTAL = {}, GRADE = \"{}\" WHERE REG_NO=\"{}\"".format(int(gTotal), grade, regNo))
            mydb.commit()
    else:
        print("")
    if t=='stats':
        os.system('cls')
        print("View stats".center(40))
        choice=input("\n1. View stats for a specific student.\nEnter choice: ")
        if choice=='1':
            regNo = input("Enter Registration Number of the student: ")
            temp = ""
            if regNo!='':
                if head!=[]:
                    for ele in head:
                        temp += ', '+ele
                else:
                    input("No subject found. Press Enter to go to main menu and add a subject.")
                    menu()
                mycursor.execute(('SELECT NAME {} FROM STUDENTS WHERE REG_NO = "'.format(temp))+(regNo)+('"'))
                student = mycursor.fetchall()
                if student!=[]:
                    print(student)
                    yAxis=[]
                    for i in student[0][1:]:
                        if i!=None:
                            yAxis.append(i)
                        else:
                            yAxis.append(0)
                    xAxis = head
                    plt.bar(xAxis,yAxis)
                    plt.title(student[0][0])
                    plt.xlabel("Subjects")
                    plt.ylabel("Marks")
                    plt.show()
                else:
                    print("No student found!")
            else:
                print("No input detected.")
        else:
            print("No input detected.")
        input("Press Enter to go to main menu.")
        menu()
        
    
def addSubject():
    os.system('cls')
    print("Add a Subject".center(40))
    subId = input("Enter Subject name/ID: ")
    if subId!="":
        try:
            sql = ("ALTER TABLE STUDENTS ADD COLUMN ")+subId.replace(" ","")+(" INT(50)")
            mycursor.execute(sql)
            print("Subject added.")
            temp = input("Press any key to go to main menu.")
        except Exception as f:
            subErr = str(f)
            if(subErr[14:36]=="Duplicate column name "):
                print("Subject already exists!")
                input("Press Enter to go to Main Menu")
                menu()
    else:
        input("No entry detected, press Enter to return to main menu.")
    menu()
    
def addStudent():
    os.system('cls')
    print("Add a Student".center(40))
    name = input("Enter Student Full name: ")
    regNo = input("Enter {}'s Registration Number: ".format(name))
    phNo = input("Enter {}'s Mobile Number: ".format(name))
    email = input("Enter {}'s email ID: ".format(name))
    try:
        if name!="" and regNo!="" and phNo!="" and email!="":
            sql = ("INSERT INTO STUDENTS(NAME, REG_NO, PH_NO, EMAIL) VALUES(%s, %s, %s, %s)")
            mycursor.execute(sql, (name, regNo, phNo, email))
            mydb.commit()
            print("Student added.")
            temp = input("Press any key to go to main menu.")
        else:
            print("Missing fields, press Enter to return to main menu.")
            input("")
    except Exception as e:
        sErr = str(e)
        if sErr[14:29]=="Duplicate entry":
            input("Duplicate registration number, press Enter to return to main menu.")
            menu()
    menu()
    
def viewStudentOrSubject(a):
    os.system('cls')
    if a==0:
        print("Student List".center(40))
        mycursor = mydb.cursor()
        mycursor.execute("SELECT COUNT(*) FROM STUDENTS")
        myresult = mycursor.fetchall()
        print("Total students: {}".format(myresult[0][0]))
        if myresult[0][0]!=0:
            print("\nSorted alphabetically.")
            mycursor.execute("SELECT * FROM STUDENTS ORDER BY NAME ASC")
            myresult = mycursor.fetchall()
            temp=1
            for x in myresult:
                print("{}. {}, Reg No.: {}".format(temp,x[0],x[1]))
                temp=temp+1
        else:
            print("No students found.")
    if a==1:
        print("Subject List".center(40))
        mycursor = mydb.cursor()
        mycursor.execute("DESCRIBE STUDENTS")
        myresult = mycursor.fetchall()
        if len(myresult)==6:
            print("No subjects added.")
        else:
            for x in myresult[6:]:
                print(x[0])
    input("Press any key to go to main menu.")
    menu()

def addOrModifyMarks(n):
    os.system('cls')
    if n==0:
        print("Add marks".center(40))
        regNo = input("Enter Registration Number of the student: ")
        if regNo!='':
            mycursor.execute(('SELECT NAME FROM STUDENTS WHERE REG_NO = "')+(regNo)+('"'))
            temp = mycursor.fetchall()
            if temp!=[]:
                print("\nEntering marks for available subjects for {}.\n".format(temp[0][0]))
                mycursor.execute("DESCRIBE STUDENTS")
                myresult = mycursor.fetchall()
                if len(myresult)==6:
                    input("No subjects added. Press Enter to go to Main Menu to add subjects.")
                    menu()
                else:
                    for i in myresult[6:]:
                        a=input("Enter marks for {}:".format(i[0]))
                        if a=='' or int(a)<0 or int(a)>100:
                            input("No input detected or invalid marks. \nMake sure the marks is <= 100 and >= 0.\nPress any key to go to main menu.")
                            menu()
                        else:
                            mycursor.execute("UPDATE STUDENTS SET {} = {} WHERE REG_NO=\"{}\"".format(i[0], int(a), regNo))
                            mydb.commit()
                            print("{} marks added for {}.".format(i[0], temp[0][0]))
            else:
                print("No student found!")
        else:
            print("No input detected.")
    if n==1:
        print("Modify marks".center(40))
        regNo = input("Enter Registration Number of the student: ")
        if regNo!='':
            mycursor.execute(('SELECT NAME FROM STUDENTS WHERE REG_NO = "')+(regNo)+('"'))
            temp = mycursor.fetchall()
            if temp!=[]:
                print("\nModifying marks of {}.\n".format(temp[0][0]))
                sub = input("Enter the subject name/ID to update: ")
                subId = sub.replace(" ","")
                mycursor.execute("DESCRIBE STUDENTS")
                myresult = mycursor.fetchall()
                subjects = []
                for i in myresult[6:]:
                    subjects.append(i[0])
                if subId=='':
                    input("No input detected .\nPress Enter to go to main menu.")
                    menu()
                elif subId.replace(" ","") in subjects:
                    a=input("Enter marks for {}:".format(subId))
                    if a=='' or int(a)<0 or int(a)>100:
                        input("No input detected or invalid marks. \nMake sure the marks is <= 100 and >= 0.\nPress Enter to go to main menu.")
                        menu()
                    else:
                        mycursor.execute("UPDATE STUDENTS SET {} = {} WHERE REG_NO=\"{}\"".format(subId.replace(" ",""), int(a), regNo))
                        mydb.commit()
                        print("{} marks modified for {}.".format(subId, temp[0][0]))
                else:
                    input("Subject not found. \nPress Enter to go to Main Menu to add subjects.")
                    menu()
            else:
                print("No student found!")
        else:
            print("No input detected.")
    input("Press Enter to go to Main Menu.")
    menu()

def deleteSubject():
    os.system('cls')
    print("Delete a subject".center(40))
    subId = input("Enter the subject name to delete: ")
    subId = subId.replace(" ","")
    if subId!='':
        os.system('color 4')
        temp = input('Please make sure deleting {} will delete all marks stored for the subject.\nPress Enter to delete the subject or type "NO" to go back to main menu.'.format(subId))
        if temp!="NO":
            try:
                sql = ("ALTER TABLE STUDENTS DROP ")+(subId.replace(" ",""))
                mycursor.execute(sql)
                os.system('color 7')
                print("Deleted subject {}.".format(subId))
                input("Press any key to go to Main Menu.")
                menu()
            except Exception as f:
                iErr = str(f)
                if iErr[14:]=="Can't DROP '{}'; check that column/key exists".format(subId):
                    input("Subject not found.\nPress Enter to go to Main Menu.")
                else:
                    input("Unknown error occured.\nPress Enter to go to Main Menu.")
        else:
            os.system('color 7')
            print("Going to main menu.")
    else:
        input("No input detected, press any key to go to main menu.")
    os.system('color 7')
    menu()

def deleteStudent():
    os.system('cls')
    print("Delete a student".center(40))
    regNo = input("Enter student's registration number: ")
    if regNo != '':
        mycursor.execute(('SELECT NAME FROM STUDENTS WHERE REG_NO = "')+(regNo)+('"'))
        name = mycursor.fetchall()
        print(name)
        if name==[]:
            input("No student found with Registration Number {}.\nPress Enter to go to Main Menu.".format(regNo))
            menu()
        else:
            os.system('color 4')
            temp = input('Please make sure deleting {}, Reg. No: {} will delete all details and marks stored for the student.\nPress Enter to delete the student from the database or type "NO" to go back to main menu.'.format(name[0][0], regNo))
            if temp!="NO":
                sql = ('DELETE FROM STUDENTS WHERE REG_NO = "')+(regNo)+('"')
                mycursor.execute(sql)
                mydb.commit()
                os.system('color 7')
                print("Deleted student: {}.".format(name))
                input("Press any key to go to Main Menu.")
                menu()
            else:
                os.system('color 7')
                print("Going to main menu.")
                menu()
    else:
        input("No input detected, press any key to go to main menu.")
        os.system('color 7')
        mennu()

def viewResult():
    os.system('cls')
    print("View Result".center(40))
    calculateResult(True)
    n=input("1. View results for all students.\n2. View result for a specific student.\nEnter choice: ")
    if n=='1':
        os.system('cls')
        print("View Result - All".center(40))
        mycursor = mydb.cursor()
        mycursor.execute("SELECT COUNT(*) FROM STUDENTS")
        myresult = mycursor.fetchall()
        mycursor.execute("DESCRIBE STUDENTS")
        myresult2 = mycursor.fetchall()
        if myresult[0][0]!=0:
            head = ['Name','Reg. No.','Ph. No.','Email ID']
            temp = ''
            for i in myresult2[6:]:
                head.append(i[0])
            for ele in head[4:]:
                temp += ','+ele
            print("\nSorted alphabetically.")
            mycursor.execute("SELECT NAME, REG_NO, PH_NO, EMAIL {}, G_TOTAL, GRADE FROM STUDENTS ORDER BY NAME ASC".format(temp))
            myresult = mycursor.fetchall()
            head.append("Total")
            head.append("Grade")
            print(tabulate(myresult, headers=head, tablefmt="grid"))
        else:
            print("No students found.")
        input("Press Enter to go to main menu.")
        menu()
    elif n=='2':
        regNo = input("Enter student's registration number: ")
        if regNo!='':
            mycursor = mydb.cursor()
            mycursor.execute(('SELECT NAME FROM STUDENTS WHERE REG_NO = "')+(regNo)+('"'))
            name = mycursor.fetchall()
            if name==[]:
                input("No student found with Registration Number {}.\nPress Enter to go to Main Menu.".format(regNo))
                menu()
            else:
                mycursor = mydb.cursor()
                mycursor.execute("SELECT COUNT(*) FROM STUDENTS")
                myresult = mycursor.fetchall()
                mycursor.execute("DESCRIBE STUDENTS")
                myresult2 = mycursor.fetchall()
                head = ['Name','Reg. No.','Ph. No.','Email ID']
                temp = ''
                for i in myresult2[6:]:
                    head.append(i[0])
                for ele in head[4:]:
                    temp += ','+ele
                mycursor.execute("SELECT NAME, REG_NO, PH_NO, EMAIL {}, G_TOTAL, GRADE FROM STUDENTS WHERE REG_NO = '{}'".format(temp, regNo))
                myresult = mycursor.fetchall()
                head.append("Total")
                head.append("Grade")
                print(tabulate(myresult, headers=head, tablefmt="grid"))
        else:
            print("No input detected.")
    else:
        input("Wrong choice. Press Enter to go to Main Menu.")
        menu()
    input("Press Enter to go to main menu.")
    menu()
    
def menu():
    while True:
        os.system('cls')
        print("Main Menu".center(40))
        print("\n\n")
        print("1. Add Subject")
        print("2. Add Student Member")
        print("3. View Subjects")
        print("4. View Students")
        print("5. Add marks")
        print("6. Modify marks")
        print("7. Delete Subject")
        print("8. Delete Student")
        print("9. View result")
        print("10: View stats")
        print("11. Exit")
        ch=input("Enter your choice: " )
        if ch!="":
            break
        else:
            print("Couldn't detect a valid choice!")
            input("Press <Enter> to return back to the menu.")
    if ch=='1':
        addSubject()
    if ch=="2":
        addStudent()
    if ch=="3":
        viewStudentOrSubject(1)
    if ch=="4":
        viewStudentOrSubject(0)
    if ch=='5':
        addOrModifyMarks(0)
    if ch=='6':
        addOrModifyMarks(1)
    if ch=="7":
        deleteSubject()
    if ch=='8':
        deleteStudent()
    if ch=='9':
        viewResult()
    if ch=='10':
        calculateResult('stats')
    if ch=='11':
        quit()
    
        
        
while(True):
    #uName = input("Enter MySQL Server username: ")
    #uPass = maskpass.askpass(prompt="Enter MySQL Server password: ", mask="#")
    uName = "rootsie"
    uPass = "qwerty123"
    sHost = "db4free.net"
    try:
        # mydb = mysql.connector.connect(
        # host="127.0.0.1",
        # user=uName,
        # passwd=uPass,
        # database="results"
        # )
        mydb = mysql.connector.connect(
        host=sHost,
        user=uName,
        passwd=uPass,
        database="results"
        )
        bit = True
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS STUDENTS(NAME VARCHAR(100), REG_NO VARCHAR(10) PRIMARY KEY, PH_NO VARCHAR(10), EMAIL VARCHAR(200), G_TOTAL INT, GRADE VARCHAR(3))")
        menu()
        break      
    
    except Exception as e:
        err = str(e)
        print(e)
        if(err[14:]=="Access denied for user '{}'@'{}' (using password: YES)".format(uName, sHost)):
            print("Wrong username/password.")
        elif(err[14:]=="Access denied for user 'root'@'localhost' (using password: NO)"):
            print("Please enter password:")
            break
        else:
            print("Error occurred, exiting the program.")
            break


