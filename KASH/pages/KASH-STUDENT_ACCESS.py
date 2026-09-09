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
        """, unsafe_allow_html=True)
mydb = mysql.connector.connect(host="localhost", user="root", passwd="1708", database="KASH")
mycursor = mydb.cursor()
st.logo("KASH.png")
if "logged_ins" not in st.session_state:
    st.session_state.logged_ins = False
if "flow" not in st.session_state:
    st.session_state.flow=False
if "class_flash" not in st.session_state:
    st.session_state.class_flash=False
if "trace" not in st.session_state:
    st.session_state.trace=False
if "buddy_battle" not in st.session_state:
    st.session_state.buddy_battle=False
if "info_hub" not in st.session_state:
    st.session_state.info_hub=False
if "name" not in st.session_state:
    st.session_state.name = ""
if "stream" not in st.session_state:
    st.session_state.stream = ""
if "sid" not in st.session_state:
    st.session_state.sid = ""
if "clas" not in st.session_state:
    st.session_state.clas = ""
def info_hub(stream,sid):
    mycursor.execute("USE KASH")
    q="SELECT * FROM NOTICEBOARD"
    mycursor.execute(q)
    a=mycursor.fetchall()
    notice=a[::-1]
    notice=notice[:5]
    tn=[]
    n=[]
    data={"TEACHER-NAME":tn,"NOTICE":n}
    for i in notice:
        tn.append(i[1])
        n.append(i[0])
    df=pd.DataFrame(data)
    with col1:
        st.subheader("NOTICE-BOARD")
        st.table(df)
    q="SELECT SUB_1,SUB_2,SUB_3,SUB_4,SUB_5,PERC FROM STUDENT WHERE ADNO=%s"
    mycursor.execute(q, (sid,))
    p_list=mycursor.fetchone()
    if stream=="CS-MATH":
        sub_p=["PHYSICS","CHEMISTRY","MATHEMATICS","COMPUTER SCIENCE","ENGLISH","OVERALL PERCENTAGE"]
    elif stream=="BIO-MATH":
        sub_p=["PHYSICS","CHEMISTRY","MATHEMATICS","BIOLOGY","ENGLISH","OVERALL PERCENTAGE"]
    elif stream=="BIO-CS":
        sub_p=["PHYSICS","CHEMISTRY","BIOLOGY","COMPUTER SCIENCE","ENGLISH","OVERALL PERCENTAGE"]
    data_P={"SUBJECT":sub_p,"PERCENTAGE":p_list}
    df=pd.DataFrame(data_P)
    with col2:
        st.subheader("SCORE-BOARD")
        st.table(df)
def flow(stream,sid):
    db_stream=stream.replace("-","")
    q=f"USE {db_stream}"
    mycursor.execute(q)
    q=f"SELECT * FROM {sid}"
    mycursor.execute(q)
    a=mycursor.fetchall()
    if len(a)==0:#metric
        st.warning("SCORES NOT YET ADDED")
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
        mycursor.execute("USE KASH")
        q="SELECT FEED_BACK FROM STUDENT WHERE ADNO=%s"
        mycursor.execute(q, (sid,))
        a=mycursor.fetchone()
        feed_back=a[0]
        st.text(f"FEED BACK FROM TEACHER:  {feed_back}")
        q="USE {}"
        mycursor.execute(q.format(stream.replace("-","")))
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
def buddy_battle(stream,sid):
    b1=sid
    b2=st.text_input("ENTER BUDDY'S STUDENT ID")
    mycursor.execute("SELECT STREAM FROM STUDENT WHERE ADNO=%s", (b2,))
    s=mycursor.fetchone()
    if b2 and (b2!=b1):
        if s is not None:
            if s[0] != stream:
                st.warning("BUDDY NOT FOUND IN YOUR STREAM")
            else:
                st.divider()
                q="SELECT SUB_1,SUB_2,SUB_3,SUB_4,SUB_5,PERC FROM STUDENT WHERE ADNO=%s"
                mycursor.execute(q,(b2,))
                s2=mycursor.fetchone()    
                mycursor.execute(q, (b1,))
                s1=mycursor.fetchone()
                if stream=="CS-MATH":
                    subj=["PHYSICS","CHEMISTRY","MATHEMATICS","COMPUTER SCIENCE","ENGLISH","OVERALL"]
                elif stream=="BIO-MATH":
                    subj=["PHYSICS","CHEMISTRY","MATHEMATICS","BIOLOGY","ENGLISH","OVERALL"]
                elif stream=="BIO-CS":
                    subj=["PHYSICS","CHEMISTRY","BIOLOGY","COMPUTER SCIENCE","ENGLISH","OVERALL"]
                data_bb=pd.DataFrame({"YOUR SCORES":s1,"BUDDY SCORES":s2,"SUBJECTS":subj})
                col1,col2=st.columns(2)
                colors=[(0,255,0),(255,0,0)]
                with col1:
                    st.bar_chart(data_bb,color=colors,x="SUBJECTS",stack=False,sort=False)
                data_bt=pd.DataFrame({"SUBJECTS":subj,"YOUR SCORES":s1,"BUDDY'S SCORES":s2})
                with col2:
                    st.table(data_bt)
        else:
            st.warning("BUDDY NOT YET REGISTERED")
    else:
        if b2==b1:
            st.warning("PLEASE CHECK THE STUDENT ID OF YOUR'S AND BUDDY'S")
        else:
            st.warning("PLEASE ENTER YOUR BUDDY'S STUDENT ID")
def class_flash(stream,sid,clas):
    if stream=="CS-MATH":
        subj=["PHYSICS","CHEMISTRY","MATHEMATICS","COMPUTER SCIENCE","ENGLISH","OVERALL"]
    elif stream=="BIO-MATH":
        subj=["PHYSICS","CHEMISTRY","MATHEMATICS","BIOLOGY","ENGLISH","OVERALL"]
    elif stream=="BIO-CS":
        subj=["PHYSICS","CHEMISTRY","BIOLOGY","COMPUTER SCIENCE","ENGLISH","OVERALL"]  
    q="SELECT SUB_1,SUB_2,SUB_3,SUB_4,SUB_5,PERC FROM STUDENT WHERE ADNO=%s"
    mycursor.execute(q, (sid,))
    ms=list(mycursor.fetchone())
    qc="SELECT AVG(SUB_1),AVG(SUB_2),AVG(SUB_3),AVG(SUB_4),AVG(SUB_5),AVG(PERC)FROM STUDENT WHERE STREAM=%s AND CLASS=%s"
    mycursor.execute(qc, (stream,clas))
    cs=list(mycursor.fetchone())
    data=({"SUBJECTS":subj,"YOUR AVERAGES":ms,"CLASS AVERGE":cs})
    colors=[(0,255,0),(255,0,0)]
    st.markdown(f"<h2><center>CLASS-FLASH:{clas}</center></h2>",unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        st.bar_chart(data,x="SUBJECTS",color=colors,stack=False,sort=False)
    data_ct=({"SUBJECTS":subj,"YOUR AVERAGES":ms,"CLASS AVERAGES":cs})
    with col2:
        st.table(data)
def trace(stream,sid):
    col1,col2=st.columns(2)
    db=stream.replace("-","")
    mycursor.execute(f"USE {db}")
    mycursor.execute(f"SELECT * FROM {sid}")
    a=mycursor.fetchall()
    if len(a) != 0:
        if stream=="CS-MATH":
            subj=["PHYSICS","CHEMISTRY","MATHEMATICS","COMPUTER SCIENCE","ENGLISH"]
        elif stream=="BIO-MATH":
            subj=["PHYSICS","CHEMISTRY","MATHEMATICS","BIOLOGY","ENGLISH"]
        elif stream=="BIO-CS":
            subj=["PHYSICS","CHEMISTRY","BIOLOGY","COMPUTER SCIENCE","ENGLISH"]
        g=st.selectbox("TRACE-",subj,index=None,placeholder="ENTER SUBJECT TO TRACED")
        st.markdown("""**The scores `T-Raced` here is the scores of the `last seven tests`,if you have scores
                       for _seven or more_ tests. Otherwise the total scores will be `T-Raced`.**""")
        if g:
            st.divider()
            col1,col2,col3=st.columns(3)
            mycursor.execute(f"SELECT * FROM {sid}")
            a=mycursor.fetchall()
            if len(a)>=7:
                test=["TEST-1","TEST-2","TEST-3","TEST-4","TEST-5","TEST-6","TEST-7"]
                dat=a[-7:]
            else:
                test=[]
                for i in range(1,len(a)+1):
                    test.append("TEST-"+str(i))
                dat=a
            sub_1=[]
            sub_2=[]
            sub_3=[]
            sub_4=[]
            sub_5=[]
            for i in a:
                sub_1.append(i[0])
                sub_2.append(i[1])
                sub_3.append(i[2])
                sub_4.append(i[3])
                sub_5.append(i[4])
            if g==subj[0]:
                data=pd.DataFrame({"TEST":test,"SCORES":sub_1})
            elif g==subj[1]:
                data=pd.DataFrame({"TEST":test,"SCORES":sub_2})
            elif g==subj[2]:
                data=pd.DataFrame({"TEST":test,"SCORES":sub_3})
            elif g==subj[3]:
                data=pd.DataFrame({"TEST":test,"SCORES":sub_4})
            elif g==subj[4]:
                data=pd.DataFrame({"TEST":test,"SCORES":sub_5})
            h=len(a)
            with col1:
                st.bar_chart(data,y="SCORES",x="TEST")
            if len(a)<7:
                with col2:
                    st.caption(f"You have attended {h} tests and all scores are T-Raced")
            else:
                with col2:
                    st.caption(f"You have attended {h} tests and recent 7 from them are T-Raced ")
            with col3:
                st.table(data)
        else:
            st.warning("PLEASE ENTER SUBJECT TO BE T-RACED")

    else:
        st.warning("SCORES NOT YET ADDED")
placeholder = st.empty()
if not st.session_state.logged_ins:
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("STUDENT1.webp", width=360)
    st.divider()
    st.markdown("<center><h1>STUDENT ACCESS</h1></center>", unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns(3)  
    with col2:#login
        sid = st.text_input("ENTER YOUR STUDNET ID")
        s = st.selectbox("STREAM", ["CS-MATH","BIO-MATH","BIO-CS"], index=None, placeholder="ENTER YOUR STREAM")
        p = st.text_input("ENTER YOUR PASSWORD", type="password")
        if st.button("LOGIN"):
            if sid and (p and s):
                q = "SELECT PASSWORD FROM STUDENT WHERE ADNO=%s AND STREAM=%s"
                mycursor.execute(q, (sid,s))
                a = mycursor.fetchone()
                if a:
                    db_password = a[0]
                    if db_password == p:
                        st.session_state.logged_ins = True
                        st.session_state.sid = sid
                        st.session_state.stream = s
                        q="SELECT NAME,CLASS FROM STUDENT WHERE ADNO=%s"
                        mycursor.execute(q, (sid,))
                        b = mycursor.fetchone()
                        st.session_state.name= b[0]
                        st.session_state.clas=b[1]
                        st.rerun()
                    else:
                        st.error("INCORRECT PASSWORD")
                else:
                    st.error("USER NOT FOUND IN STREAM")
            else:
                st.warning("PLEASE ENTER ALL YOUR LOGIN CREDENTIALS")
else:
    if st.sidebar.button("Logout"):
        st.session_state.logged_ins = False
        st.session_state.name = ""
        st.session_state.stream = ""
        st.session_state.sid=""
        st.session_state.flow=False
        st.session_state.info_hub=False
        st.session_state.class_flash=False
        st.session_state.trace=False
        st.session_state.buddy_battle=False
        st.rerun()
    with placeholder.container():
        col1, col2, col3 = st.columns(3)
        with col2:
            st.image("STUDENT1.webp", width=360)
        st.divider()
        st.markdown("<center><h1>STUDENT ACCESS</h1></center>", unsafe_allow_html=True)
        st.markdown("""Here you can view your `FLOW` and you can compete with your friends
                    using `BUDDY BATTLE`.You can also **T-Race** your progress and
                    view your level compared to the class with the help of _CLASS-FLASH_""")
        st.divider()
        col1,col2,col3=st.columns(3)
        with col1:
            st.image("flow.png")
            if st.button("FLOW",type="primary"):
                st.session_state.flow=True
                st.session_state.class_flash=False
                st.session_state.trace=False
                st.session_state.buddy_battle=False
                st.session_state.info_hub=False
            st.image("buddybattle.png")
            if st.button("BUDDY-BATTLE"):
                st.session_state.flow=False
                st.session_state.class_flash=False
                st.session_state.trace=False
                st.session_state.buddy_battle=True
                st.session_state.info_hub=False
        with col2:
            st.image("KASHSTAR.png")
            st.subheader(f"Welcome KASH STAR {st.session_state.name}!")
            st.text(f"Class -{st.session_state.clas}")
            st.text(f"Student ID -{st.session_state.sid}")
            st.text(f"Stream - {st.session_state.stream}")
            if st.button("INFO-HUB",type="primary"):
                st.session_state.flow=False
                st.session_state.info_hub=True
                st.session_state.class_flash=False
                st.session_state.trace=False
                st.session_state.buddy_battle=False
        with col3:
            st.image("classflash.png")
            if st.button("CLASS-FLASH",type="primary"):
                st.session_state.flow=False
                st.session_state.class_flash=True
                st.session_state.info_hub=False
                st.session_state.trace=False
                st.session_state.buddy_battle=False
            st.image("TRACE.png")
            if st.button("T-RACE"):
                st.session_state.flow=False
                st.session_state.class_flash=False
                st.session_state.trace=True
                st.session_state.buddy_battle=False
                st.session_state.info_hub=False
        st.divider()
        col1,col2=st.columns(2)
        if st.session_state.flow:
            flow(st.session_state.stream,st.session_state.sid)
        if st.session_state.class_flash:
            class_flash(st.session_state.stream,st.session_state.sid,st.session_state.clas)
        if st.session_state.trace:
            trace(st.session_state.stream,st.session_state.sid)
        if st.session_state.buddy_battle:
            buddy_battle(st.session_state.stream,st.session_state.sid)
        if st.session_state.info_hub:
            info_hub(st.session_state.stream,st.session_state.sid)
        if not (st.session_state.info_hub or(st.session_state.buddy_battle or st.session_state.trace )):
            if not (st.session_state.class_flash or st.session_state.flow):
                st.success("ENTER THE FEATURE TO BE DONE")
