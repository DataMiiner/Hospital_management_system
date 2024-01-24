import streamlit as st
import mysql.connector
import pandas as pd
from streamlit_login_auth_ui.widgets import __login__


st.set_page_config(page_icon='🏥',
                            page_title="Hospital Management System")


if 'login' not in st.session_state:
    st.session_state.login = False

 
__login__obj = __login__(auth_token="courier_auth_token",
                    company_name="Shims",
                    width=200, height=250,
                    logout_button_name='Logout', hide_menu_bool=False,
                    hide_footer_bool=False,
                    lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')


st.session_state.login = __login__obj.build_login_ui()


if st.session_state.login:

    # Get the user name.
    fetched_cookies = __login__obj.cookies
    if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
        st.session_state["username"] = fetched_cookies['__streamlit_login_signup_ui_username__']
    
    
    
  
    a = mysql.connector.connect(host="bpoepuvaeqtlyk4lv7zg-mysql.services.clever-cloud.com", user="ubdcaqgk8cowwmtv", password="gg6ZOCFe8kFFyl1ERfc6",database="bpoepuvaeqtlyk4lv7zg")

    cur=a.cursor()
    #cur.execute(f"create database if NOT EXISTS  hospital_{st.session_state['username']}")
    #cur.execute(f"use hospital_{st.session_state['username']}")
    cur.execute(f"create table  if not exists patient_{st.session_state['username']}(id int ,mobile_no char(10) ,name varchar(50),doct_name varchar(100),descp varchar(120),primary key(id,mobile_no))")
    cur.execute(f"create table if not exists appointment_{st.session_state['username']}(id int primary key,name varchar(50),mob char(10),doct varchar(50),date varchar(10),time varchar(10),descp varchar(200))")

    #addition of details
    def pat_add(id,name,mob,doct_name,descp):
      try:
        cur.execute(f"insert into patient_{st.session_state['username']}(id,mobile_no, name, doct_name, descp) values(%s,%s,%s,%s,%s)",(id,mob, name, doct_name, descp))
        a.commit()
        st.success(f"Detail of {name} are added")
      except:
        st.warning("OOPs!,There is some error")  
    
    #deletion of details
    def delete(id,name):
        try:
            cur.execute(f"delete from patient_{st.session_state['username']} where id=%s and name=%s",(id,name))
            a.commit()
            st.success(f"Record of {name} is deleted")
        except:
            st.warning("OOPs!,There is some error")  
    
    #search by id
    def search(id):
          cur.execute(f"select * from patient_{st.session_state['username']} where id=%s",(id,))
          ret=cur.fetchall()
          li=list(ret)
          st.session_state["mob"]=li[0][1]
          st.session_state["name"]=li[0][2]
          st.session_state["doct_name"]=li[0][3]
          st.session_state["descp"]=li[0][4]
          
          #st.session_state
          data=pd.DataFrame(ret,columns=["id","mobile_no", "name", "doct_name", "description"])
          return data
    #search by mobile no
    def search_mob(mob):
          cur.execute(f"select * from patient_{st.session_state['username']} where mobile_no=%s",(mob,))
          ret=cur.fetchall()
          #st.session_state
          data=pd.DataFrame(ret,columns=["id","mobile_no", "name", "doct_name", "description"])
          return data






    #display of record
    def display():
        cur.execute(f"select * from patient_{st.session_state['username']}")
        ret=cur.fetchall()
        data=pd.DataFrame(ret,columns=["id","mobile_no", "name", "doct_name", "description"])
        return data

    #update record
    def  update(id,name,mob,doct_name,descp):
        try:
          cur.execute(f"update patient_{st.session_state['username']} set name=%s,mobile_no=%s,doct_name=%s,descp=%s where id=%s",(name,mob,doct_name,descp,id))
          a.commit()
          st.success(f"Records of id {id} updated successfully")
        except:
          st.warning("OOPs!,There is some error") 

    #appoinment_table
    def appointment(id,name,mob,doct,date,time,descp):
        try:
          cur.execute(f"insert into appointment_{st.session_state['username']}(id,name,mob,doct,date,time,descp) values(%s,%s,%s,%s,%s,%s,%s)",(id,name,mob,doct,date,time,descp))
          a.commit()
          st.success("Appointment is Booked")
        except:
          st.warning("OOPs!,There is some error")   
    #appointment_table fetch
    def fetch():
        try:
          cur.execute(f"select * from appointment_{st.session_state['username']}")
          re=cur.fetchall()
          data=pd.DataFrame(re,columns=["Id","Name","Mobile no","Doct_name","Date(DD/MM/YY)","Time(HH-MM)","Description"])     
          st.write(data)
        except:
          st.warning("OOPs!,There is some error")
          
    #appointment_del
    def dele_app(id):
        try:
          cur.execute(f"delete from appointment_{st.session_state['username']} where id=%s",(id,))
          a.commit()
          st.success("Appointment deleted")
        except:
            st.warning("OOPs!,There is some error")
        #main function     
    def main():

        if "name" not in st.session_state:
            st.session_state["name"]="NA"
        elif "id" not in st.session_state:   
            st.session_state["id"]="NA"
        elif "mob" not in st.session_state:   
            st.session_state["mob"]="NA"
        elif "doct_name" not in st.session_state:   
            st.session_state["doct_name"]="NA"
        elif "descp" not in st.session_state:   
            st.session_state["descp"]="NA"


        side_bar=st.sidebar.radio("Select the Features from below:",["Home","Search Patient Data","Show Patient list","Add New patient details","Update patient Details","Delete Patient Detail","Add appoinment","Show Appointments","Delete Appoinment"])




        if  side_bar=="Home":
          st.title("Hospital Management System")
          st.write("Select the Query from side bar")
          st.success(f"Welcome {st.session_state['username']}")
          st.image("hospital.png",width=300)
          
        elif side_bar=="Add New patient details":
            c1,c2=st.columns([1,5])
            c2.subheader("Patients Records")
            c1.image("patient.png",width=100)
            st.write("  ")
            st.write("Enter Patient Records:")
            st.session_state["id"]=st.text_input("Enter Patient id:")
            st.session_state["name"]=st.text_input("Enter Patient Name:")
            st.session_state["mob"]=st.text_input("Enter Patient Mobile No.:")
            st.session_state["doct_name"]=st.text_input("Enter Doctor Name:")
            st.session_state["descp"]=st.text_area("Description:")
            st.session_state["butt"]=st.button("Add")
            if st.session_state["butt"]==True:
              st.session_state["butt"]=False
              pat_add(st.session_state["id"],st.session_state["name"],st.session_state["mob"],st.session_state["doct_name"],st.session_state["descp"]) 

        elif side_bar=="Show Patient list":
          col1,col2=st.columns([1,5])
          col1.image("medical-record.png",width=100)
          col2.subheader("Patient Records")
          r=display()
          st.write(r)

        elif side_bar=="Delete Patient Detail" :
          st.subheader("Delete Patient Records")
          st.write("Enter name of ")
          st.session_state["del_name"]=st.text_input("Enter name:")
          st.session_state["id"]=st.text_input("Enter id:")
          st.session_state['del']=st.button("Delete")
          if st.session_state['del']==True:
              st.session_state['del']=False
              delete(st.session_state["id"],st.session_state["del_name"])
              
        elif side_bar=="Update patient Details":
            st.subheader("Update Patient Records")
            st.session_state["id"]=st.text_input("Enter Id Of Patient:")
            if st.session_state["id"]:
              search(st.session_state["id"])
            st.session_state["update_records"]=st.multiselect("Select What you have to Update:",["name","mob","doct_name","desc"])
            
            for i in st.session_state["update_records"]:
              st.session_state[f"{i}"]=st.text_input(f"Enter Patient {i}:")
            st.session_state['but_up']=st.button("Update")
            if st.session_state['but_up']==True:
              st.session_state['but_up']=False
              update(st.session_state["id"],st.session_state["name"],st.session_state["mob"],st.session_state["doct_name"],st.session_state["descp"])

        elif side_bar=="Search Patient Data":
          col1,col2=st.columns([1,5])
          col1.image("find.png",width=100)
          col2.subheader("Search patient Data")
          st.session_state["searchby"]=st.selectbox("Search By:",["Id","Mobile no."])
          if st.session_state["searchby"]=="Id":
                  st.session_state["id"]=st.text_input("Enter Patient id:")
                  st.session_state["search"]=st.button("Search")
                  if st.session_state["search"]:
                      st.session_state["search"]=False
                      data=search(st.session_state["id"])
                      st.write(data)
          elif st.session_state["searchby"]=="Mobile no.":
                  st.session_state["mob"]=st.text_input("Enter Patient Mobile no.:")
                  st.session_state["search"]=st.button("Search")
                  if st.session_state["search"]:
                      st.session_state["search"]=False
                      data=search_mob(st.session_state["mob"])
                      st.write(data)    

        elif side_bar=="Add appoinment":
            
          col1,col2=st.columns([1,5])
          col1.image("appointment.png",width=100)
          col2.subheader("Take Appoinment") 
          st.session_state["id_a"]=st.text_input("Enter id:") 
          st.session_state["name_a"]=st.text_input("Enter Name of Patient:")
          st.session_state["Mobile_a"]=st.text_input("Enter Mobile no.:")
          st.session_state["Doctor_a"]=st.text_input("Enter Doctor name:")
          st.session_state["Time"]=st.text_input("Enter Time(HH-MM):")
          st.session_state["Date"]=st.text_input("Enter Date (DD/MM/YY):")
          st.session_state["descp"]=st.text_input("Enter description:")
          st.session_state["app_but"]=st.button("Book Appoinment")
          if st.session_state["app_but"]:
            st.session_state["app_but"]=False
            appointment(st.session_state["id_a"],st.session_state["name_a"],st.session_state["Mobile_a"],st.session_state["Doctor_a"],st.session_state["Date"],st.session_state["Time"],st.session_state["descp"])
        elif side_bar=="Show Appointments":

          st.subheader("Appointments")
          fetch()
        elif side_bar=="Delete Appoinment":
          st.subheader("Delete Appointment")
          st.session_state["id_a"]=st.text_input("Enter id of Appointment to be deleted:") 
          st.session_state["app_but_del"]=st.button("Delete Appoinment")
          if st.session_state["app_but_del"]:
            st.session_state["app_but_del"]=False 
            dele_app(st.session_state["id_a"])
            
                  
                  
    if __name__=="__main__":    
              main()  
