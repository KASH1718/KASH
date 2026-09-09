import streamlit as st
import mysql.connector
st.markdown(f"""<style>
    .stApp{{
    background-image:url("https://i.imgur.com/T3qLPlw.png");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}
</style>
    """,unsafe_allow_html=True)
mydb=mysql.connector.connect(host=st.secrets['mysql']['host'],port=st.secrets['mysql']['port'],user=st.secrets['mysql']['user'],password=st.secrets['mysql']['pass'],ssl_ca='isrgrootx1.pem',ssl_verify_cert=True,use_pure=True)
mycursor=mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS KASH")
mydb.commit()
mycursor.execute("CREATE DATABASE IF NOT EXISTS CSMATH")
mydb.commit()
mycursor.execute("CREATE DATABASE IF NOT EXISTS BIOMATH")
mydb.commit()
mycursor.execute("CREATE DATABASE IF NOT EXISTS BIOCS")
mydb.commit()
mycursor.execute("CREATE DATABASE IF NOT EXISTS STAR_WARS")
mydb.commit()
mycursor.execute("USE KASH")
def register(stream,adno):
    if stream=="CS-MATH":
        mycursor.execute("USE CSMATH")
        qc="""CREATE TABLE IF NOT EXISTS {} (
                     PHY INT,
                    CHEM INT,
                    MATH INT,
                      CS INT,
                      ENG INT)"""
        mycursor.execute(qc.format(adno))
        mydb.commit()
    elif stream=="BIO-MATH":
        mycursor.execute("USE BIOMATH")
        qc="""CREATE TABLE IF NOT EXISTS{}(
                PHY INT,
                CHEM INT,
                MATH INT,
                BIO INT,
                ENG INT)"""
        mycursor.execute(qc.format(adno))
        mydb.commit()
    elif stream=="BIO-CS":
        mycursor.execute("USE BIOCS")
        qc="""CREATE TABLE IF NOT EXISTS {} (
                PHY INT,
                CHEM INT,
                BIO INT,
                CS INT,
                ENG INT)"""
        mycursor.execute(qc.format(adno))
        mydb.commit()
st.logo("KASH.png")
st.divider()
col1,col2,col3=st.columns(3)
with col2:
    st.image("REGISTER.png")
st.markdown("""<center><h1>REGISTRATION</h1></center>""",unsafe_allow_html=True)
st.divider()
col1,col2=st.columns(2)
with col1:
    if st.toggle("ROLE OF REGISTRATION"):
        st.markdown("`TEACHER REGISTRATION`")
        with col2:#TEACHER
            with st.form("TEACHER_REGISTER",clear_on_submit=True):
                r_tn=st.text_input("ENTER YOUR NAME")
                r_ti=st.text_input("ENTER YOUR TEACHER ID")
                r_ts=st.selectbox("ENTER YOUR SUBJECT",["PHYSICS","CHEMISTRY","MATHEMATICS","COMPUTER SCIENCE","BIOLOGY","ENGLISH"],index=None,placeholder="ENTER YOUR SUBJECT")
                r_tp=st.text_input("ENTER YOUR PASSWORD",type="password")
                r_tcp=st.text_input("CONFIRM YOUR PASSWORD",type="password")
                data=(r_tn,r_ti,r_ts,r_tp,r_tcp)
                if st.form_submit_button("REGISTER"):
                    c=0
                    for i in data:
                        if i is not None:
                            c+=1
                    if c==5:
                        if r_tp==r_tcp:
                            data_db=(r_tn,r_ti,r_ts,r_tp)
                            mycursor.execute("""CREATE TABLE IF NOT EXISTS TEACHER (
                                                NAME CHAR(15),
                                                TEACH_ID CHAR(10),
                                                SUBJECT CHAR(20),
                                                PASSWORD VARCHAR(20))""")
                            q="INSERT INTO TEACHER VALUES{}"
                            mycursor.execute(q.format(data_db))
                            mydb.commit()
                            st.success("REGISTERED SUCCESSFULLY")
                        else:
                            st.error("CONFIRM PASSWORD DOES NOT MATCH PASSWORD")
                    else:
                        st.warning("PLEASE ENTER ALL THE REQIURED INFORMATION")
    else:
        st.markdown("`STUDENT REGISTRATION`")
        with col2:#STUDENT
            with st.form("STUDENT_REGISTER",clear_on_submit=True):
                r_n=st.text_input("ENTER YOUR NAME")
                r_c=st.text_input("ENTER YOUR CLASS NAME")
                r_a=st.text_input("ENTER STUDENT ID")
                r_s=st.selectbox("STREAM",["CS-MATH","BIO-MATH","BIO-CS"],index=None,placeholder="ENTER YOUR STREAM")
                r_p=st.text_input("ENTER YOUR PASSWORD",type="password")
                r_cp=st.text_input("CONFIRM YOUR PASSWORD",type="password")
                data=(r_n,r_c,r_a,r_s,r_p,r_cp)
                if st.form_submit_button("REGISTER"):
                    c=0
                    for i in data:
                        if i is not None:
                            c+=1
                    if c==6:
                        if r_p==r_cp:
                            mycursor.execute("""CREATE TABLE IF NOT EXISTS STUDENT(
                                                NAME CHAR(25),
                                                CLASS CHAR(10),
                                                ADNO CHAR(10),
                                                STREAM CHAR(10),
                                                PASSWORD CHAR(50),
                                                SUB_1 FLOAT(4,1) DEFAULT 0,
                                                SUB_2 FLOAT(4,1) DEFAULT 0,
                                                SUB_3 FLOAT(4,1) DEFAULT 0,
                                                SUB_4 FLOAT(4,1) DEFAULT 0,
                                                SUB_5  FLOAT(4,1) DEFAULT 0,
                                                PERC FLOAT(4,1) DEFAULT 0,
                                                FEED_BACK CHAR(100))""")
                            q="INSERT INTO STUDENT(NAME,CLASS,ADNO,STREAM,PASSWORD) VALUES{}"
                            mycursor.execute(q.format((r_n,r_c,r_a,r_s,r_p)))
                            mydb.commit()
                            register(r_s,r_a)
                            st.success("REGISTERED SUCCESSFULLY")
                        else:
                            st.error("CONFIRM PASSWORD DOES NOT MATCH PASSWORD")
                    else:
                        st.warning("PLEASE ENTER ALL REQUIRED INFORMATION")
