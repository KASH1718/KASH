import streamlit as st
import mysql.connector
import pandas as pd
st.markdown(f"""<style>
    .stApp{{
    background-image:url("https://i.imgur.com/vKCskUz.jpeg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}
</style>
    """,unsafe_allow_html=True)
st.logo("KASH.png")
mydb=mysql.connector.connect(host="localhost",user="root",passwd="1708")
mycursor=mydb.cursor()
mycursor.execute("USE KASH")
if "enter_war" not in st.session_state:
    st.session_state.enter_war=False
if "star_rank" not in st.session_state:
    st.session_state.star_rank=False
if "score_board" not in st.session_state:
    st.session_state.score_board=False
if "sid" not in st.session_state:
    st.session_state.sid=""
if "name" not in st.session_state:
    st.session_state.name=""
if "ans" not in st.session_state:
    st.session_state.ans=[]
if "war_sub" not in st.session_state:
    st.session_state.war_sub=""
def score_board(name,sid,ans,sub):
    mycursor.execute("USE STAR_WARS")
    mycursor.execute("SELECT SCORE_VIEWED FROM WAR WHERE ADNO=%s", (sid,))
    sv=mycursor.fetchone()
    if sv is not None:
        if ans and sv[0]==0:
            with st.container(border=True):
                col1,col2=st.columns(2)
                q=f"SELECT OPT_A,OPT_B,OPT_C,OPT_D,CORRECT_OPT FROM {sub}"
                mycursor.execute(q)
                corr_an=mycursor.fetchall()
                a=[]
                b=[]
                c=[]
                d=[]
                corr_ans=[]
                for i in corr_an:
                    a.append(i[0])
                    b.append(i[1])
                    c.append(i[2])
                    d.append(i[3])
                    corr_ans.append(i[4])
                score=10
                wa=[]
                for i in range(10):
                    if corr_ans[i]!=ans[i]:
                        score-=1
                        ca=corr_ans[i]
                        if ca=="A":
                            opt=a[i]
                        elif ca=="B":
                            opt=b[i]
                        elif ca=="C":
                            opt=c[i]
                        elif ca=="D":
                            opt=d[i]
                        wa.append(f"THE CORRECT OPTION FOR QUSESTION.{i+1} IS {corr_ans[i]}-{opt}")
                p="SELECT Q_COUNT,POINTS FROM WAR WHERE ADNO=%s"
                mycursor.execute(p, (sid,))
                q=mycursor.fetchone()
                c=q[0]
                pnt=q[1]
                points=score/2
                t_points=pnt+points
                nc=c+1
                up=f"UPDATE WAR SET SCORE={score},POINTS={t_points},Q_COUNT={nc},SCORE_VIEWED=1 WHERE ADNO=%s"
                mycursor.execute(up, (sid,))
                mydb.commit()
                with col1:    
                    st.subheader(f"PLAYER NAME:{name}")
                    st.subheader(f"PLAYER ID:{sid}")
                    st.subheader(f"SCORE:{score}/10")
                    st.subheader(f"POINTS ADDED:{points}")
                    st.subheader(f"TOTAL POINTS:{t_points}")
                for i in wa:
                    st.text(i)    
        else:
            if sv[0]==1:
                q="SELECT Q_COUNT,SCORE,POINTS FROM WAR WHERE ADNO=%s"
                mycursor.execute(q, (sid,))
                a=mycursor.fetchone()
                with st.container(border=True):
                    st.subheader(f"PLAYER NAME:{name}")
                    st.subheader(f"PLAYER ID :{sid}")
                    st.subheader(f"QUIZ-COUNT:{a[0]}")
                    st.subheader(f"PREVIOUS SCORE:{a[1]}")
                    st.subheader(f"TOTAL-POINTS:{a[2]}")
    else:
        st.warning("PLEASE ENTER WAR AND ATTACK TO VIEW SCORE")
def war(sid,name):
    col1,col2,col3=st.columns(3)
    with col2:
        war=st.selectbox("ENTER WAR SUBJECT",["PHYSICS","CHEMISTRY","MATHEMATICS","COMPUTERSCIENCE","BIOLOGY","ENGLISH"],index=None,placeholder="ENTER WAR SUBJECT")
        st.session_state.war_sub=war
    st.divider()
    if war:
        war_sub=(st.session_state.war_sub.lower(),)
        q="SHOW TABLES" 
        mycursor.execute(q)
        t=mycursor.fetchall()
        if war_sub in t:
            q=f"SELECT * FROM {war}"
            mycursor.execute(q)
            w=mycursor.fetchall()
            if war=="PHYSICS":
                col="KPQ"
            elif war=="CHEMISTRY":
                col="KCQ"
            elif war=="MATHEMATICS":
                col="KMQ"
            elif war=="COMPUTERSCIENCE":
                col="KCSQ"
            elif war=="BIOLOGY":
                col="KBQ"
            elif war=="ENGLISH":
                col="KEQ"
            check=f"SELECT {col} FROM WAR WHERE ADNO=%s"
            mycursor.execute(check, (sid,))
            ch=mycursor.fetchone()
            if len(w)==10 and ch[0]==0:
                col1,col2,col3=st.columns(3)
                q=f"SELECT QUESTION,OPT_A,OPT_B,OPT_C,OPT_D FROM {war}"
                mycursor.execute(q)
                qp=mycursor.fetchall()
                qs=[]
                oa=[]
                ob=[]
                oc=[]
                od=[]
                for i in qp:
                    qs.append(i[0])
                    oa.append(i[1])
                    ob.append(i[2])
                    oc.append(i[3])
                    od.append(i[4])
                with col1:
                     with st.container(border=True):
                         st.subheader("QUESTION-PAPER")
                         for i in range(1,6):
                            st.write(f"Q{i}.",qs[i-1])
                            st.write("OPTION-A:",oa[i-1])
                            st.write("OPTION-B:",ob[i-1])
                            st.write("OPTION-C:",oc[i-1])
                            st.write("OPTION-D:",od[i-1])
                            st.divider()
                with col2:
                    with st.container(border=True):
                        st.subheader("QUESTION-PAPER")
                        for i in range(6,11):
                            st.write(f"Q{i}.",qs[i-1])
                            st.write("OPTION-A:",oa[i-1])
                            st.write("OPTION-B:",ob[i-1])
                            st.write("OPTION-C:",oc[i-1])
                            st.write("OPTION-D:",od[i-1])
                            st.divider()
                with col3:
                    ans=[]  
                    with st.form("ANSWER_SHEET",clear_on_submit=True):
                        st.subheader("ANSWER SHEET")
                        for i in range(1,11):
                            a=st.radio(f"ENTER OPTION FOR QUESTION {i}",["A","B","C","D"],index=None,horizontal=True)
                            ans.append(a)
                        submitted=st.form_submit_button("ATTCAK")
                        if submitted and len(ans)==10:
                            if st.session_state.war_sub=="PHYSICS":
                                col="KPQ"
                            elif st.session_state.war_sub=="CHEMISTRY":
                                col="KCQ"
                            elif st.session_state.war_sub=="MATHEMATICS":
                                col="KMQ"
                            elif st.session_state.war_sub=="COMPUTERSCIENCE":
                                col="KCSQ"
                            elif st.session_state.war_sub=="BIOLOGY":
                                col="KBQ"
                            elif st.session_state.war_sub=="ENGLISH":
                                col="KEQ"
                            up=f"UPDATE WAR SET {col}=1,SCORE_VIEWED=0 WHERE ADNO=%s"
                            mycursor.execute(up, (sid,))
                            mydb.commit()
                            st.session_state.ans=ans
                            st.session_state.score_board = True
                            st.session_state.enter_war = False
                            st.session_state.star_rank = False
                            st.rerun()
            else:
                st.warning("WAR HAS CEASED OR ALREADY ATTEMPTED")
        else:
            st.warning("WAR DOES NOT CRAETED")
    else:
        st.warning("PLEASE ENTER SUBJECT TO ENTER WAR")
def enter_war(name,sid):
    mycursor.execute("USE STAR_WARS")
    q="""CREATE TABLE IF NOT EXISTS WAR(
        ADNO CHAR(10) PRIMARY KEY,
        NAME CHAR(20),
        SCORE_VIEWED INT(1) DEFAULT 1,
        SCORE FLOAT DEFAULT 0,
        POINTS INT DEFAULT 0,
        Q_COUNT INT DEFAULT 0,
        KPQ INT DEFAULT -1,
        KCQ INT DEFAULT -1,
        KMQ INT DEFAULT -1,
        KCSQ INT DEFAULT -1,
        KBQ INT DEFAULT -1,
        KEQ INT DEFAULT -1)"""
    mycursor.execute(q)
    mydb.commit()
    q="SELECT ADNO FROM WAR"
    mycursor.execute(q)
    a=mycursor.fetchall()
    if (sid,) not in a:
        q="INSERT INTO WAR(ADNO,NAME) VALUES(%s,%s)"
        mycursor.execute(q, (sid,name))
        mydb.commit()
        sub=["PHYSICS","CHEMISTRY","MATHEMATICS","COMPUTERSCIENCE","BIOLOGY","ENGLISH"]
        l=[]
        for i in sub:
            q=f"SELECT * FROM {i}"
            mycursor.execute(q)
            a=mycursor.fetchall()
            if len(a)==10:
                l.append(i)
        for i in l:
            if i=="PHYSICS":
                col="KPQ"
            elif i=="CHEMISRTY":
                col="KCQ"
            elif i=="MATHEMATICS":
                col="KMQ"
            elif i=="COMPUTERSCIENCE":
                col="KCSQ"
            elif i=="BIOLOGY":
                col="=KBQ"
            elif i=="ENGLISH":
                col="KEQ"
            up=f"UPDATE WAR SET {col}=0 WHERE ADNO={sid}"
            mycursor.execute(up)
            mydb.commit()
        war(sid,name)
    else:
        war(sid,name)
def star_rank(name,sid):
    mycursor.execute("USE STAR_WARS")
    if not st.toggle("RANKED BASED ON"):
        st.markdown("`POINTS`")
        q="SELECT ADNO,NAME,POINTS FROM WAR ORDER BY POINTS DESC"
        mycursor.execute(q)
        lis=mycursor.fetchall()
        c=len(lis)
        sidl=[]
        namel=[]
        pointsl=[]
        rank=[":1st_place_medal:-KASH_LEGEND",":2nd_place_medal:-KASH_ELITE",":3rd_place_medal:-KASH_CHAMPION"
              ,"\U0001F31F-RISING_STAR",":star:-FUTURE_STAR",":sparkles:-BRIGHT_SPAKS",":phoenix:-KASH_PHOENIX","💯-MIND_MASTER",
              ":brain:-BRAIN_BOOSTER","⚡-SPRAK_MIND"]
        for i in lis:
            sidl.append(i[0])
            namel.append(i[1])
            pointsl.append(i[2])
        if c>=10:
            s=sidl[:10]
            n=namel[:10]
            p=pointls[:10]
            rl=rank[:10]
        else:
            s=sidl[:c]
            n=namel[:c]
            p=pointsl[:c]
            rl=rank[:c]
        data=pd.DataFrame({"RANK":rl,"PLAYER-ID":s,"PLAYER NAME":n,"POINTS":p})
        st.table(data)
        i=sidl.index(sid)
        rankp=int(i)+1
        st.info(f"YOUR RANK-{rankp}")
    else:
        st.markdown("`QUIZ_COUNT`")
        q="SELECT ADNO,NAME,Q_COUNT FROM WAR ORDER BY Q_COUNT DESC"
        mycursor.execute(q)
        lis=mycursor.fetchall()
        c=len(lis)
        sidl=[]
        namel=[]
        qcl=[]
        rank=[":1st_place_medal:-KASH_LEGEND",":2nd_place_medal:-KASH_ELITE",":3rd_place_medal:-KASH_CHAMPION",
              "\U0001F31F-RISING_STAR",":star:-FUTURE_STAR",":sparkles:-BRIGHT_SPAKS",":phoenix:-KASH_PHOENIX","💯-MIND_MASTER",
              ":brain:-BRAIN_BOOSTER","⚡-SPRAK_MIND"]
        for i in lis:
            sidl.append(i[0])
            namel.append(i[1])
            qcl.append(i[2])
        if c>=10:
            s=sidl[:10]
            n=namel[:10]
            qc=qcl[:10]
            rl=rank[:10]
        else:
            s=sidl[:c]
            n=namel[:c]
            qc=qcl[:c]
            rl=rank[:c]
        data=pd.DataFrame({"RANK":rl,"PLAYER-ID":s,"PLAYER NAME":n,"QUIZ_COUNT":qc})
        t=st.table(data)
        i=sidl.index(sid)
        rankp=int(i)+1
        st.info(f"YOUR RANK-{rankp}")
col1,col2,col3=st.columns(3)
with col2:
    st.image("STAR_WARS.png")
    sid=st.text_input("ENTER YOUR STUDENT ID")
    st.image("scoreboard.png")
    if st.button("SCORE BOARD"):
        st.session_state.score_board=True
        st.session_state.enter_war=False
        st.session_state.star_rank=False
with col3:
    st.image("starrank.jpeg")
    if st.button("STAR RANK"):
        st.session_state.enter_war=False
        st.session_state.star_rank=True
        st.session_state.score_board=False
with col1:
    st.image("enterwar.png")
    if st.button("ENTER WAR"):
        st.session_state.enter_war=True
        st.session_state.star_rank=False
        st.session_state.score_board=False
st.divider()
if sid:
    q="SELECT NAME FROM STUDENT WHERE ADNO=%s"
    mycursor.execute(q, (sid,))
    a=mycursor.fetchone()
    if a==None:
        st.warning("STUDENT NOT YET REGISTERED")
    else:
        st.session_state.name=a[0].upper()
        st.session_state.sid=sid
    if st.session_state.enter_war:
        enter_war(st.session_state.name,st.session_state.sid)
    if st.session_state.star_rank:
        star_rank(st.session_state.name,st.session_state.sid)
    if st.session_state.score_board:
        score_board(st.session_state.name,st.session_state.sid,st.session_state.ans,st.session_state.war_sub)
    if not(st.session_state.enter_war or (st.session_state.star_rank or st.session_state.score_board)) and a!=None:
        st.success("NOW ENTER THE WAR")
else:
    st.warning("PLEASE ENTER YOUR STUDENT ID TO ENTER WAR")
