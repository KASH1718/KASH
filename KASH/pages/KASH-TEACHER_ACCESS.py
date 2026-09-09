import streamlit as st
import pandas as pd
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
mydb=mysql.connector.connect(host="localhost",user="root",passwd="1708")
mycursor=mydb.cursor()
mycursor.execute("USE KASH")
st.logo("KASH.png")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_add_scores" not in st.session_state:
    st.session_state.show_add_scores = False
if "show_students" not in st.session_state:
    st.session_state.show_students = False
if "show_flow" not in st.session_state:
    st.session_state.show_flow = False
if "notice" not in st.session_state:
    st.session_state.notice=False
if "declare_war" not in st.session_state:
    st.session_state.declare_war=False
if "name" not in st.session_state:
    st.session_state.name = ""
if "tid" not in st.session_state:
    st.session_state.tid = ""
if "subject" not in st.session_state:
    st.session_state.subject = ""
def star_wars():
    mycursor.execute("USE STAR_WARS")
    sub=st.selectbox("ENTER YOUR WAR SUBJECT",["PHYSICS","CHEMISTRY","MATHEMATICS","COMPUTERSCIENCE","BIOLOGY","ENGLISH"],index=None,placeholder="ENTER YOUR SUBJECT")
    st.divider()
    if sub:
        q=f"""CREATE TABLE IF NOT EXISTS {sub}(
            QUESTION TEXT,
            OPT_A VARCHAR(50),
            OPT_B VARCHAR(50),
            OPT_C VARCHAR(50),
            OPT_D VARCHAR(50),
            CORRECT_OPT CHAR(1))"""
        mycursor.execute(q)
        mydb.commit()
        mycursor.execute(f"SELECT * FROM {sub}")
        questions=mycursor.fetchall()
        question_count=len(questions)
        if  question_count<10:
            st.info(f"Questions Added: {question_count}/10")
            with st.form(f"WAR PREPERATION", clear_on_submit=True):
                q=st.text_input(f"ENTER QUESTION {question_count+1}: ")
                a=st.text_input("ENTER OPTION A:")
                b=st.text_input("ENTER OPTION B:")
                c=st.text_input("ENTER OPTION C:")
                d=st.text_input("ENTER OPTION D:")
                corr_op=st.text_input("ENTER CORRECT OPTION:")
                submitted=st.form_submit_button("DECLARE")
                if submitted :
                    if sub=="PHYSICS":
                        col="KPQ"
                    elif sub=="CHEMISTRY":
                        col="KCQ"
                    elif sub=="MATHEMATICS":
                        col="KMQ"
                    elif sub=="COMPUTERSCIENCE":
                        col="KCSQ"
                    elif sub=="BIOLOGY":
                        col="KBQ"
                    elif sub=="ENGLISH":
                        col="KEQ"
                    up=f"UPDATE WAR SET {col}=0"
                    mycursor.execute(up)
                    mydb.commit() 
                    val=f"INSERT INTO {sub} VALUES(%s,%s,%s,%s,%s,%s)"
                    mycursor.execute(val, (q,a,b,c,d,corr_op))
                    mydb.commit()
                    st.rerun()
        elif question_count>=10:
            col1=st.columns(1)
            col1,col2=st.columns(2)
            with col1:
                st.warning("WAR CREATED:CEASE WAR TO DELARE ANOTHER ONE")
            with col2:
                if st.button("CEASE WAR",type="primary"):
                    q=f"DELETE FROM {sub}"
                    mycursor.execute(q)
                    mydb.commit()
                    if sub=="PHYSICS":
                        col="KPQ"
                    elif sub=="CHEMISTRY":
                        col="KCQ"
                    elif sub=="MATHEMATICS":
                        col="KMQ"
                    elif sub=="COMPUTERSCIENCE":
                        col="KCSQ"
                    elif sub=="BIOLOGY":
                        col="KBQ"
                    elif sub=="ENGLISH":
                        col="KEQ"
                    up=f"UPDATE WAR SET {col}=-1"
                    mycursor.execute(up)
                    mydb.commit()
    else:
        st.warning("PLEASE ENTER SUBJECT TO DECLARE WAR")
def flow(stream):
    col1,col2,col3=st.columns(3)
    with col2:
        mycursor.execute("USE KASH")
        sid=st.text_input("ENTER STUDENT ID",placeholder='ENTER STUDNET ID')
        q="SELECT ADNO FROM STUDENT WHERE STREAM=%s"
        mycursor.execute(q, (stream,))
        a=mycursor.fetchall()
    if sid:
        if (sid,) in a:
            q="USE {}"
            mycursor.execute(q.format(stream.replace("-","")))
            q="SELECT * FROM {}"
            mycursor.execute(q.format(sid))
            a=mycursor.fetchall()
            if len(a)==0:#metric
                with col2:
                    st.subheader("ADD SCORES TO STUDENT")
            else:
                dif=[]
                c_scores=a[-1]
                if len(a)==1:
                    p_scores=[0,0,0,0,0]
                else:
                    p_scores=a[-2]
                for i in range(5):
                    dif.append(c_scores[i]-p_scores[i])
                if stream=="CS-MATH":
                    sub=["PHYSICS","CHEMISTRY","MATHEMATICS","COMPUTER SCIENCE","ENGLISH"]
                elif stream=="BIO-MATH":
                    sub=["PHYSICS","CHEMISTRY","MATHEMATICS","BIOLOGY","ENGLISH"]
                elif stream=="BIO-CS":
                    sub=["PHYSICS","CHEMISTRY","BIOLOGY","COMPUTER SCIENCE","ENGLISH"]
                cols=st.columns(5)
                for i in range(0,5):
                    with cols[i]:
                        st.metric(sub[i],c_scores[i],delta=dif[i])
            q=f"SELECT COUNT(*) FROM {sid}"
            mycursor.execute(q)
            a=mycursor.fetchone()
            if a[0]>0:#table
                q="SELECT * FROM {}"
                mycursor.execute(q.format(sid))
                score_board=mycursor.fetchall()
                s1=[]
                s2=[]
                s3=[]
                s4=[]
                s5=[]
                data_m={sub[0]:s1,sub[1]:s2,sub[2]:s3,sub[3]:s4,sub[4]:s5}
                for test in score_board:
                    for j in range(5):
                        subject=sub[j]
                        score=test[j]
                        data_m[subject].append(score)
                df_m=pd.DataFrame(data_m)
                st.table(df_m)
        else:
            st.warning("STUDENT NOT FOUND IN STREM")
    else:
        st.warning("PLEASE ENTER STUDENT ID")        

def student(stream):
    mycursor.execute("USE KASH")
    try:
        q="SELECT NAME, CLASS,ADNO FROM STUDENT WHERE STREAM=%s"
        mycursor.execute(q, (stream,))
        name_list=mycursor.fetchall()
        name=[]
        clas=[]
        SID=[]
        for j in name_list:
            name.append(j[0])
            clas.append(j[1])
            SID.append(j[2])
        data_n={"NAME":name,'CLASS':clas,'STUDENT ID':SID}
        df=pd.DataFrame(data_n)
        st.table(df)
    except :
        name=[]
        clas=[]
        SID=[]
        data_n={"NAME":name,'CLASS':clas,'STUDENT ID':SID}
        df=pd.DataFrame(data_n)
        st.table(df)
def notice(name):
    tn=name
    with st.form("NOTICE_BOARD",clear_on_submit=True):
        notice=st.text_area("ENTER NOTICE IN NOTICE BOARD",value="")
        if  st.form_submit_button("SUBMIT NOTICE"):
            mycursor.execute("USE KASH")
            q="""CREATE TABLE IF NOT EXISTS NOTICEBOARD(
                 NOTICE CHAR(75),
                 TEACHER CHAR(20))"""
            mycursor.execute(q)
            mydb.commit()
            q="INSERT INTO NOTICEBOARD(NOTICE,TEACHER) VALUES(%s,%s)"
            mycursor.execute(q, (notice,tn))
            mydb.commit()
            st.success("NOTICE ADDED!!")
def add_scores(stream):
    with st.form("SCORE_BOARD", clear_on_submit=True):
        if stream=="CS-MATH":
            warning="SCORE ORDER:PHY,CHEM,MATH,CS,ENG"
            sub=["PHY","CHEM","MATH","CS","ENG"]
            q="USE CSMATH"
        elif stream=="BIO-MATH":
            warning="SCORE ORDER:PHY,CHEM,MATH,BIO,ENG"
            sub=["PHY","CHEM","MATH","BIO","ENG"]
            q="USE BIOMATH"
        elif stream=="BIO-CS":
            warning="SCORE ORDER:PHY,CHEM,BIO,CS,ENG"
            sub=["PHY","CHEM","BIO","CS","ENG"]
            q="USE BIOCS"
        st.warning(warning)
        sid = st.text_input("ENTER STUDENT ID",key="sid",placeholder='ENTER STUDENT ID')
        m1 = st.number_input("ENTER SCORE 1", min_value=0, max_value=100)   
        m2 = st.number_input("ENTER SCORE 2", min_value=0, max_value=100)
        m3 = st.number_input("ENTER SCORE 3", min_value=0, max_value=100)
        m4 = st.number_input("ENTER SCORE 4", min_value=0, max_value=100)
        m5 = st.number_input("ENTER SCORE 5", min_value=0, max_value=100)
        feed_back=st.text_area("ENTER YOUR FEEDBACK ABOUT THE STUDENT",value="")
        submitted = st.form_submit_button("Add Scores")
        if submitted:
           mycursor.execute(q)
           mydb.commit()
           t=sid
           q=f"INSERT INTO {t} VALUES(%s,%s,%s,%s,%s)"
           mycursor.execute(q, (m1,m2,m3,m4,m5))
           mydb.commit()
           AVG=[]
           for i in sub:
               mycursor.execute(f"SELECT AVG({i}) FROM {t}")
               a=mycursor.fetchone()
               AVG.append(a[0])
           mycursor.execute("USE KASH")
           for i in range(1,6):
               C="SUB_"+str(i)
               V=AVG[i-1]
               q=f"UPDATE STUDENT SET {C}={V} WHERE ADNO=%s"
               mycursor.execute(q, (sid,))
               mydb.commit()
           q=f"UPDATE STUDENT SET FEED_BACK=%s WHERE ADNO=%s"
           mycursor.execute(q, (feed_back,sid))
           mydb.commit()
           perc=sum(AVG)/5
           q="UPDATE STUDENT SET PERC=%s WHERE ADNO=%s"
           mycursor.execute(q, (perc,sid))
           mydb.commit()
           st.success("SCORES ADDED: ADD SCORE TO NEXT STUDENT")
placeholder=st.empty()
if not st.session_state.logged_in:
    col1,col2,col3=st.columns(3)
    with col2:
        st.image("TEACHER.jpg",width=360)
    st.divider()
    col1=st.columns(1)
    st.markdown("""
    <center><h1>TEACHER ACCESS</h1>
    </center>
    """,unsafe_allow_html=True)
    st.divider()
    col1,col2,col3=st.columns(3)#Login
    with col2:
        tid=st.text_input("ENTER YOUR TEACHER ID")
        tp=st.text_input("ENTER YOUR PASSWORD",type="password")
        if st.button("LOGIN"):
                if tid and tp:
                    q="SELECT NAME,SUBJECT,PASSWORD FROM TEACHER WHERE TEACH_ID=%s"
                    mycursor.execute(q, (tid,))
                    a=mycursor.fetchone()
                    if a:
                        db_password = a[2]
                        tn=a[0]
                        ts=a[1]
                        if db_password == tp:
                            st.session_state.logged_in = True
                            st.session_state.tid =tid
                            st.session_state.name = tn.upper()
                            st.session_state.subject=ts.upper()
                            st.rerun()
                        else:
                            st.error("INCORRECT PASSWORD")
                    else:
                        st.error("TEACHER NOT YET REGISTERED")
                else:
                    st.warning("PLEASE ENTER TEACHER_ID AND PASSWORD")
else:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.show_add_scores = False
        st.session_state.show_students = False
        st.session_state.show_flow = False
        st.session_state.notice=False
        st.session_state.name=""
        st.session_state.declare_war=False
        st.rerun()
    with placeholder.container():
        col1,col2,col3=st.columns(3)
        with col2:
            st.image("TEACHER.jpg",width=360)
        st.divider()
        col1=st.columns(1)
        st.markdown("""
        <center><h1>TEACHER ACCESS</h1>
        ENTER THE STREAM OF STUDENTS AND VIWE THE STUDENT LIST TO ACCESS
        STUDENT ID AND ADD SCORES,VIEW THEIR PROGGESS,ADD NOTICE AND EVEN
        GIVE THEM A SUBJECT WAR THROUGH STAR-WARS.
        </center>
        """,unsafe_allow_html=True)
        st.divider()
        col1,col2,col3=st.columns(3)
        with col1:
            st.image("addscore.png",width=360)
            if st.button("+Add Scores", type="primary"):
                st.session_state.show_add_scores = True
                st.session_state.show_students = False
                st.session_state.show_flow = False
                st.session_state.notice=False
                st.session_state.declare_war=False
            st.image("studentlist.png")
            if st.button("CLICK TO GET STUDENT LIST"):
                st.session_state.show_students = True
                st.session_state.show_add_scores = False
                st.session_state.show_flow = False
                st.session_state.notice=False
                st.session_state.declare_war=False
        with col2:
            st.image("STAR_WARS.png")
            if st.button("DECLARE WAR",type="primary"):
                st.session_state.show_students = False
                st.session_state.show_add_scores = False
                st.session_state.show_flow = False
                st.session_state.notice=False
                st.session_state.declare_war=True
            st.subheader(f'WELCOME {st.session_state.name}')
            st.text(f"Teacher ID -{st.session_state.tid}")
            st.text(f"Techer Subject-{st.session_state.subject}")
            stream=st.selectbox("STREAM",["CS-MATH","BIO-MATH","BIO-CS"],index=None,placeholder="ENTER STREAM")
        with col3:
            st.image("flow.png")
            if st.button("Flow", type="primary"):
                st.session_state.show_flow= True
                st.session_state.show_add_scores = False
                st.session_state.show_students = False
                st.session_state.notice=False
                st.session_state.declare_war=False
            st.image("noticeboard.png")
            if st.button("NOTICE_BOARD"):
                st.session_state.notice=True
                st.session_state.show_students = False
                st.session_state.show_add_scores = False
                st.session_state.show_flow = False
                st.session_state.declare_war=False
        col1=st.columns(1)
        st.divider()
        if st.session_state.declare_war:
                star_wars()
        if st.session_state.notice:
                notice(st.session_state.name)
        if stream:
            if not (st.session_state.show_flow or(st.session_state.show_add_scores or st.session_state.show_students)):
                st.success("NOW ENTER THE FEATURE")
            if st.session_state.show_flow:
                flow(stream)
            if st.session_state.show_add_scores:
                add_scores(stream)
            if st.session_state.show_students:
                student(stream)
        if not stream and (not st.session_state.declare_war and not st.session_state.notice):
            st.warning("PLEASE ENTER THE STREAM")
            st.session_state.show_flow= False
            st.session_state.show_add_scores = False
            st.session_state.show_students = False
