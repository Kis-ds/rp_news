# import json
# import pickle
# import streamlit as st
# from streamlit_lottie import st_lottie
# from PIL import Image
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# import collections
import datetime
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
import numpy
from streamlit_extras.dataframe_explorer import dataframe_explorer
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf


################# Style option
left_mg = 0
right_mg = 10
top_mg = 0
btm_mg = 10
#
# 06_2023-09-14_complete.xlsx

################# DATA LOAD
df = pd.read_excel('./resource/06_2023-09-15_complete.xlsx')
# st.dataframe(df)





# 페이지 설정
st.set_page_config(
    layout="wide",  # wide layout은 sidebar를 더 넓게 만듭니다.
    initial_sidebar_state="collapsed"  # 초기에 sidebar가 확장된 상태로 표시됩니다.
)

# 사이드바에 내용 추가
st.sidebar.header("Side Bar")

white_space_1, data_space, white_space_2 = st.columns([0.1, 0.8, 0.1])

with white_space_1:
    st.text('여백1')

with data_space :
    ######################### HEAD
    # 메인 콘텐츠 영역에 내용 추가
    st.title(":newspaper:퇴직연금 동향 뉴스")
    st.write("다음은 금일 조회한 퇴직연금 관련 뉴스 리스트입니다. (조회일자 기준 최근 7일 기사 확인가능)")
    ''
    ''
    ######################### 차트 화면
    st.subheader('뉴스 분석', help="수집한 결과를 차트로 파악하기 쉽게 도식화 해두었습니다.")
    subject_chart, company_chart = st.columns(2, gap="large")


    ##### CHAT01. 뉴스 주제별 bar chat
    with subject_chart:

        st.markdown(
            '<div style = "color:white; font-size: 16px; text-align:center; background-color: #2d3d4a">주별 뉴스 현황</div>', # #403466  2d3d4a
            unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
        df_pivot = pd.pivot_table(df, index='날짜',
                                  columns='분류',
                                  values='제목', aggfunc='count').fillna(0)

        fig_amt = df_pivot.iplot(kind='bar', barmode='stack', asFigure=True, dimensions=(400,400),
                                 colors=('#7f999f','#a2a9cd',  '#77adda', '#85d3e6', '#0eccfb', '#2ebbc9'))

        fig_amt.update_layout(margin_l=left_mg, margin_r=right_mg, margin_t=top_mg, margin_b=btm_mg,
                              plot_bgcolor='white', paper_bgcolor='white',font_color="black",
                              legend=dict(bgcolor='#e7f6fa', yanchor='top', y=-0.1, xanchor='left',
                                          x=0.015, orientation='h',font=dict( color='black')) #  orientation='h'
                              )


        fig_amt.update_xaxes(showgrid=True, gridcolor='#332951',tickfont_color='black')
        fig_amt.update_yaxes(showgrid=True, gridcolor='#332951',tickfont_color='black')
        st.plotly_chart(fig_amt, use_container_width=True)


    with company_chart:
        st.markdown(
            '<div style = "color:white; font-size: 16px; text-align:center; background-color: #2d3d4a">기업</div>',
            # #403466  2d3d4a
            unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)

        pie_chart_df = pd.DataFrame(df[df.기업명 != 'No_Company'].기업명.value_counts()).reset_index()[:10]
        pie_chart_df.columns = ['기업명', '카운트']

        fig_pie = pie_chart_df.iplot(kind='pie', labels='기업명', values='카운트', asFigure=True, dimensions=(400, 350),
                       colors=('#a2b4cd','#a2a9cd',  '#77adda',  '#0eccfb', '#85d3e6','#2ebbc9'))  # '#ff4388', '#fe7e22', '#fbc120', '#4b1a84'

        fig_pie.update_layout(margin_l=left_mg, margin_r=right_mg, margin_t=top_mg, margin_b=btm_mg,
                              plot_bgcolor='white', paper_bgcolor='white', font_color="black",      #plot_bgcolor='#151121', paper_bgcolor='#0e1117',font_color="blue",
                              legend=dict(bgcolor='#e7f6fa',orientation='v', font=dict(color='black'))  # orientation='h' #d9d9d9

        )

        st.plotly_chart(fig_pie, use_container_width=True)

    ######################### 뉴스보여주기
    st.subheader('오늘의 이슈', help="오늘 뉴스 조회화면")
    st.text(f'오늘 수집된 주요 기사는 총 {df[df.날짜 == df.날짜.max()].shape[0]}건 입니다.')
    filtered_df = dataframe_explorer(df, case=False)
    st.dataframe(filtered_df, use_container_width=True)
with white_space_2 :
    st.text('여백2')



############################ 참고 사이트
# 이모지 찾기 :  https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# extra : https://extras.streamlit.app/Dataframe%20explorer%20UI
# iplot 스타일 설정 : https://wikidocs.net/186155 (iplot쓰려면 import plotly.graph_objects as go / # import cufflinks as cf  두개 필수 )
# pie chart 참고 : https://sks8410.tistory.com/35
# 색상 추천 사이트 : https://www.colorhexa.com/34b5d5

# https://yeomss.tistory.com/301


