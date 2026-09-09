import streamlit as st
import random
st.markdown(f"""<style>
    .stApp{{
    background-image:url("https://i.imgur.com/ih1NRjp.jpeg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}
</style>
    """,unsafe_allow_html=True)
st.image("KASH.png",width=1080)
st.logo("KASH.png")
st.markdown("""
<center><h1>KASH</h1>
        <h4>Knowledge Analysing Star Hatcher</h4>
</center>
""",unsafe_allow_html=True)
st.divider()
st.markdown("""The **KASH** will analyse the students knowledge in each subject and make them hatch from thier steriotyped _egg_-_THE LOW MARKS_
               and make them as a **`STAR`** with _GREAT marks_.The KASH is intended to allow educators and learners to easily assess and track progress across key areas of the curriculum,
               offering a clear and data-driven view of areas of strength and areas for development. KASH goes beyond traditional grading systems, using `clear data visualizations`
               and `structured performance metrics`. It actively fosters the
               student potential as a nurturing incubator to guide each learner to achieve academic excellence and help shape the _stars_ of tomorrow.""")
st.divider()
a=random.randint(1,6)
if a==1:
    st.markdown("""<marquee>Genius is 10% inspiration, 90% perspiration
                                                -Thomas Edison</marquee>""",unsafe_allow_html=True)
elif a==2:
    st.markdown("<marquee>Focus on progress, not perfection</marquee>",unsafe_allow_html=True)
elif a==3:
    st.markdown("<marquee>Finish the small, win the big</marquee>",unsafe_allow_html=True)
elif a==4:
    st.markdown("""<marquee>Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time
                                                                                                - Thomas Edison</marquee>""",unsafe_allow_html=True)
elif a==5:
    st.markdown("""<marquee>The harder I work, the more luck I seem to have.
                                                    — Thomas Jefferson</marquee>""",unsafe_allow_html=True)
elif a==6:
    st.markdown("""<marquee>The important thing is to never stop questioning.
                                       — Albert Einstein</marquee>""",unsafe_allow_html=True)
def sa():
    st.divider()
    col1,col2,col3=st.columns(3)
    with col1:#student access
        st.image("STUDENT1.webp",width=360)
    with col2:
        st.subheader("STUDENT ACCESS")
        st.caption("""The Student Access will let you view your marks,you can see the
    difference in your scores.Click the below button to login as STUDENT!!!!!!!""")
    with col3:
        if st.button("STUDENT ACCESS",type="primary"):
            st.switch_page("pages/KASH-STUDENT_ACCESS.py")
def ta():
    st.divider()
    col1,col2,col3=st.columns(3)
    with col1:#teacher access
        st.image("TEACHER.jpg",width=360)
    with col2:
        st.subheader("TEACHER ACCESS")
        st.caption("""The Teacher Access will let the teachers to enter the marks
    of each student. They can see individual performance of each
    and every student.Click the below button to login as TEACHER!!!!!!!""")
    with col3:
        if st.button("TEACHER ACCESS",type="primary"):
            st.switch_page("pages/KASH-TEACHER_ACCESS.py")
def reg():
    st.divider()
    col1,col2,col3=st.columns(3)
    with col1:#registration
        st.image("REGISTER.png",width=360)
    with col2:
        st.subheader("REGISTRATION")
        st.caption("""Click the below REGISTER button to register yourself
                      in KASH,so that you can LOGIN through your respective accesses and
                        become and create a star using KASH!!!!!!!! """)
    with col3:
        if st.button("REGISTER IN KASH",type="primary"):
            st.switch_page("pages/KASH-REGISTRATION.py")
def sw():
    st.divider()
    col1,col2,col3=st.columns(3)
    with col1:
        st.image("STAR_WARS.png",width=360)
    with col2:
        st.subheader("STAR WARS")
        st.caption("""Click the below button to do a academic war with your friends
                    with score board and points!!!!!!""")
    with col3:
        if st.button("STAR WARS",type="primary"):
            st.switch_page("pages/KASH-STAR_WARS.py")
reg()
ta()
sa()
sw()
