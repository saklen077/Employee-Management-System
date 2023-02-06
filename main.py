from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import requests
from pymongo import *
from pymongo import MongoClient
import re
from geopy.geocoders import Nominatim
import csv
import pandas as pd
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
def add1():
    root.withdraw()
    aw.deiconify()
def add2():
    aw.withdraw()
    root.deiconify()
def add3():
    con=None
    try:
        con=MongoClient("mongodb://localhost:27017")
        db=con["mongo"]
        coll=db["sky"]
        id=add_ent_id.get()
#-------------------id validation for add------------------------------------------------------------------------------
        if re.search("^[@_!#$%^&*()<>?/\|}{~:]+$", id):
            raise Exception("id does not contain special letter") 
        elif (len(id)==0):
            raise Exception("id can not be empty")
        elif any(ch.isalpha() for ch in id):
            raise Exception("id does not contain alphabet")
        elif (int(id)<=0):
            raise Exception("enter only positive integers") 
        else:
            pass
#-------------------Name validation for add---------------------------------------------------------------------------
        name=add_ent_name.get()
        if name.strip() == "":
            raise Exception("Name cannot be empty.")
        if re.search("^[a-zA-Z]+$", name):
            pass
        else:
            raise Exception( "Name contains only alphabets.")
        min_alphabet = 2	
        if len(name)>=min_alphabet:
            pass
        else:
            raise Exception("Name should  be greater than 2")
#------------------Salary validation for add--------------------------------`---------------------------------------------------
        salary=add_ent_salary.get()
        if re.search("^[@_!#$%^&*()<>?/\|}{~:]+$", salary):
            raise Exception("Salary does not contain special letter") 
        elif salary.strip() == "":
            raise Exception("Salary cannot be empty.")
        elif any(ch.isalpha() for ch in salary):
            raise Exception("Salary does not contain alphabet")
        elif float(salary) <0:
            raise Exception("Salary should not be negatives")
        elif(float(salary) <= 8000):
            raise Exception("minimum salary should be 8000")
        else:
            pass
        count=coll.count_documents({"_id":id})
        if count==1:
            showerror("Error","already exists")
        else:
            info={"_id":id,"name":name,"salary":salary}
            coll.insert_one(info)
            showinfo("success","record created")
    except Exception as e:
        showerror("Failed",e)
    finally:
        if con is not None:
            con.close()
        add_ent_id.delete(0,END)
        add_ent_name.delete(0,END)
        add_ent_salary.delete(0,END)
        add_ent_id.focus()
def view1():
    root.withdraw()
    vw.deiconify()
    vw_st_data.delete(1.0,END)
    con=None
    try:
        con=MongoClient("mongodb://localhost:27017")
        db=con["mongo"]
        coll=db["sky"]
        data=coll.find()
        info=""
        for d in data:
            info="id=" + str(d["_id"]) + " name=" + str(d["name"]) + " salary=" + str(d["salary"]) + "\n"
            vw_st_data.insert(INSERT,info)
    except Exception as e:
        showerror("issue",e)
    finally:
        if con is not None:
            con.close()
        
def view2():
    vw.withdraw()
    root.deiconify()
def update1():
    root.withdraw()
    uw.deiconify()
def update2():
    uw.withdraw()
    root.deiconify()
def update3():
    con=None
    try:
        con=MongoClient("mongodb://localhost:27017")
        db=con["mongo"]
        coll=db["sky"]
        id=update_ent_id.get()
        if re.search("^[@_!#$%^&*()<>?/\|}{~:]+$", id):
            raise Exception("id does not contain special letter") 
        elif (len(id)==0):
            raise Exception("id can not be empty")
        elif any(ch.isalpha() for ch in id):
            raise Exception("id does not contain alphabet")
        elif (int(id)<=0):
            raise Exception("id contain positive numbers") 
        else:
            pass
        count=coll.count_documents({"_id":id})
        if count == 1:
            info={}
            name=update_ent_name.get()
            if name.strip() == "":
                raise Exception("Name cannot be empty.")
            if re.search("^[a-zA-Z]+$", name):
                pass
            else:
                raise Exception( "name contains only alphabets.")
            min_alphabet = 2	
            if len(name)>=min_alphabet:
                pass
            else:
                raise Exception("name should  be greater than 2")
            salary=update_ent_salary.get()
            if re.search("^[@_!#$%^&*()<>?/\|}{~:]+$", salary):
               raise Exception("Salary does not contain special letter") 
            elif salary.strip() == "":
               raise Exception("Salary cannot be empty.")
            elif any(ch.isalpha() for ch in salary):
               raise Exception("Salary does not contain alphabet")
            elif float(salary) <0:
               raise Exception("salary should not be negatives")
            elif float(salary) <= 8000:
               raise Exception("minimum salary should be 8000")
            else:
               pass
            info["name"]= name
            info["salary"]=salary
            ndata={"$set":info}
            coll.update_one({"_id":id},ndata)
            showinfo("success","record updated")
        else:
            showerror("Error","id does not exists")
    except Exception as e:
        showerror("issue",e)
    finally:
            if con is not None:
                con.close()
                update_ent_id.delete(0,END)
                update_ent_name.delete(0,END)
                update_ent_salary.delete(0,END)
                update_ent_id.focus()
def delete1():
    root.withdraw()
    dw.deiconify()
def delete2():
    dw.withdraw()
    root.deiconify()
def delete3():
    con=None
    try:
        con=MongoClient("mongodb://localhost:27017")
        db=con["mongo"]
        coll=db["sky"]
        id=delete_ent_id.get()
        if re.search("^[@_!#$%^&*()<>?/\|}{~:]+$", id):
            raise Exception("id does not contain special letter") 
        elif (len(id)==0):
            raise Exception("id can not be empty")
        elif any(ch.isalpha() for ch in id):
            raise Exception("id does not contain alphabet")
        elif (int(id)<=0):
            raise Exception("enter only positive integers") 
        else:
            pass
        count= coll.count_documents({"_id":id})
        if count == 1:
            coll.delete_one({"_id":id})
            showinfo("success","deleted")   
        else:
            showerror("Error","id does not exist") 
    except Exception as e:
        showerror("issue",e)
    finally:
        if con is not None:
            con.close()
            delete_ent_id.delete(0,END)
            delete_ent_id.focus()
def chart():
    try:
        con=MongoClient("mongodb://localhost:27017")
        db=con["mongo"]
        coll=db["sky"]
        data = list(coll.find())
        df = pd.DataFrame(data)
        df.to_csv("saklen.csv")
        df = pd.read_csv("saklen.csv")
        df = df.sort_values("salary", ascending=False)
        df.to_csv("sorted_data.csv", index=False)
        top_5 = df.head(5)
        plt.bar(top_5.name, top_5['salary'])
        plt.xlabel("name")
        plt.ylabel("salary")
        plt.title("Top 5 highest earning salaried employee")
        plt.show()
    except Exception as e:
        showerror("Wrong",e)


############## ROOT SECTION ########################################################################################
root = Tk()
root.title("E.M.S")
root.geometry("500x600+100+10")
root['bg']='lightgreen'
root.iconbitmap("image.ico")
f=("Simsun",30,"bold")
a=("Simsun",30)

root_add_btn=Button(root,text="Add",font=f,width=9,command=add1)
root_view_btn=Button(root,text="View",font=f,width=9,command=view1)
root_update_btn=Button(root,text="Update",font=f,width=9,command=update1)
root_delete_btn=Button(root,text="Delete",font=f,width=9,command=delete1)
root_charts_btn=Button(root,text="Charts",font=f,width=9,command=chart)
loc_lab=Label(root,text="Location:",font=("Simsun",20),bg="lightgreen")
temp_lab=Label(root,text="Temp:",font=("Simsun",20),bg="lightgreen")
text_msg=Entry(root,text="",font=("Simsun",20),width=10,bg="lightgreen")
try:
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode("kalyan")
    temp=round(getLoc.latitude,2)
    temp2=round(getLoc.longitude,2)
    final=temp,temp2
    text_msg.insert(INSERT,final)
except Exception as e:
    print("issue",e)
text_msg2=Entry(root,text="",font=("Simsun",20),width=10,bg="lightgreen")
try:
    api_key = '57eed7b63035c325212cf0a74f191eef'
    city = 'kalyan,maharashtra'
    endpoint =f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(endpoint)
    data = response.json()
    temp=data['main']['temp'] - 273.15
    res=round(temp,2)
    text_msg2.insert(INSERT,res)
 
except Exception as e:
    print("issue",e)
root_add_btn.pack(pady=5)
root_view_btn.pack(pady=5)
root_update_btn.pack(pady=5)
root_delete_btn.pack(pady=5)
root_charts_btn.pack(pady=5)
loc_lab.place(x=6,y=470)
temp_lab.place(x=300,y=470)
text_msg.place(x=135,y=475)
text_msg2.place(x=370,y=475)

#################### ADD SECTION ####################################################################################
aw=Toplevel(root)
aw.title("Add Student")
aw.geometry("500x600+100+10")
aw.configure(bg='lightblue')

add_lab_id=Label(aw,text="enter id:",font=a,bg="lightblue")
add_ent_id=Entry(aw,font=a)
add_lab_name=Label(aw,text="enter name:",font=a,bg="lightblue")
add_ent_name=Entry(aw,font=a)
add_lab_salary=Label(aw,text="enter salary:",font=a,bg="lightblue")
add_ent_salary=Entry(aw,font=a)
add_save_btn=Button(aw,text="Add",font=f,width=9,bg="green",activebackground="deeppink",command=add3)
add_back_btn=Button(aw,text="Back",font=f,width=9,bg="black",fg="cyan",activebackground="deeppink",command=add2)

add_lab_id.pack(pady=10)
add_ent_id.pack(pady=10)
add_lab_name.pack(pady=10)
add_ent_name.pack(pady=10)
add_lab_salary.pack(pady=10)
add_ent_salary.pack(pady=10)
add_save_btn.pack(pady=10)
add_back_btn.pack(pady=5)

aw.withdraw()
###############  VIEW SECTION #######################################################################################
vw=Toplevel(root)
vw.title("View Student")
vw.geometry("570x600+100+10")
vw['bg']='orange2'
vw_st_data=ScrolledText(vw,width=40,height=10,font=("Simsun",25),bg="orange2",bd=2)
vw_btn_back=Button(vw,text="Back",font=f,command=view2)
vw_st_data.pack(pady=10)
vw_btn_back.pack(pady=10)
vw.withdraw()

############# UPDATE SECTION ########################################################################################
uw=Toplevel(root)
uw.title("Update Student")
uw.geometry("500x600+100+10")
uw.configure(bg='lightsalmon')

update_lab_id=Label(uw,text="enter id:",font=a,bg='lightsalmon')
update_ent_id=Entry(uw,font=a)
update_lab_name=Label(uw,text="enter name:",font=a,bg='lightsalmon')
update_ent_name=Entry(uw,font=a)
update_lab_salary=Label(uw,text="enter salary:",font=a,bg='lightsalmon')
update_ent_salary=Entry(uw,font=a)
update_update_btn=Button(uw,text="Update",font=f,width=9,command=update3)
update_back_btn=Button(uw,text="Back",font=f,width=9,command=update2)

update_lab_id.pack(pady=10)
update_ent_id.pack(pady=10)
update_lab_name.pack(pady=10)
update_ent_name.pack(pady=10)
update_lab_salary.pack(pady=10)
update_ent_salary.pack(pady=10)
update_update_btn.pack(pady=10)
update_back_btn.pack(pady=5)
uw.withdraw()

################# DELETE SECTION #####################################################################################
dw=Toplevel(root)
dw.title("Delete Student")
dw.geometry("500x600+100+10")
dw.configure(bg='MediumPurple2')

delete_lab_id=Label(dw,text="enter id:",font=a,bg="MediumPurple2")
delete_ent_id=Entry(dw,font=a)
delete_update_btn=Button(dw,text="Delete",font=f,width=9,command=delete3)
delete_back_btn=Button(dw,text="Back",font=f,width=9,command=delete2)

delete_lab_id.pack(pady=10)
delete_ent_id.pack(pady=10)
delete_update_btn.pack(pady=10)
delete_back_btn.pack(pady=5)
dw.withdraw()
root.mainloop()
