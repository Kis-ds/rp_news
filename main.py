

# https://pension-news.streamlit.app/
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf
from datetime import datetime

def make_clickable(get_list):
    link, title = get_list[0], get_list[1]
    # text = link.split('=')[1]
    return f'<a target="aboutlink" href="{link}">{title}</a>'

# def loadPickle(path):
#     with open(path, 'rb') as fr:
#         df = pickle.load(fr)
#     return df


# 페이지 설정
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

################# Style option
left_mg = 0
right_mg = 10
top_mg = 0
btm_mg = 10

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            .col_heading {text-align: center !important}
            </style>
            """

################# DATA LOAD

# DATA LOAD
# df = loadPickle('./resource/04_UPLOAD.pkl')  # all_full_db_060708

df = pd.read_excel('./resource/04_UPLOAD.xlsx')
df['날짜'] = (pd.to_datetime(df['날짜']).dt.strftime('%Y-%m-%d'))
df['날짜'] = df['날짜'].astype(str)

# 사이드바에 내용 추가
st.sidebar.header("Side Bar")

white_space_1, data_space, white_space_2 = st.columns([0.1, 0.8, 0.1])

with white_space_1:
    st.empty()

with data_space:
    ######################### HEAD
    # 메인 콘텐츠 영역에 내용 추가
    st.title(":newspaper:퇴직연금 동향 뉴스")
    st.write("다음은 금일 수집한 퇴직연금 관련 뉴스 리스트입니다. (조회일자 기준 최근 7일 기사 확인이 가능합니다.)")
    ''
    ''
    ######################### 차트 화면
    st.subheader('뉴스 분석',
                 help="수집한 결과를 차트로 파악하기 쉽게 도식화 해두었습니다.\n- 주별뉴스현황 : 카테고리별로 기사 발행 현황에 대해 막대차트로 확인가능합니다.\n- 기업관련 기사 조회 : 기업별로 발행한 퇴직연금 관련 기사 수를 파이차트로 비중을 도식화 하였습니다. ")
    subject_chart, company_chart = st.columns(2, gap="large")

    ##### CHAT01. 뉴스 주제별 bar chat
    with subject_chart:
        st.markdown(
            '<div style = "color:white; font-size: 16px; text-align:center; background-color: #2d3d4a">주별 뉴스 현황</div>',
            # #403466  2d3d4a
            unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
        df_pivot = pd.pivot_table(df, index='날짜',
                                  columns='분류',
                                  values='제목', aggfunc='count').fillna(0)

        fig_amt = df_pivot.iplot(kind='bar', barmode='stack', asFigure=True, dimensions=(400, 400),
                                 colors=('#7f999f', '#a2a9cd', '#77adda', '#85d3e6', '#0eccfb', '#2ebbc9'))

        fig_amt.update_layout(margin_l=left_mg, margin_r=right_mg, margin_t=top_mg, margin_b=btm_mg,
                              plot_bgcolor='white', paper_bgcolor='white', font_color="black",
                              legend=dict(bgcolor='#e7f6fa', yanchor='top', y=-0.1, xanchor='left',
                                          x=0.015, orientation='h', font=dict(color='black'))  # orientation='h'
                              )

        fig_amt.update_xaxes(showgrid=True, gridcolor='#adb0c2', tickfont_color='black')
        fig_amt.update_yaxes(showgrid=True, gridcolor='#adb0c2', tickfont_color='black')  # 332951
        st.plotly_chart(fig_amt, use_container_width=True)

    with company_chart:
        st.markdown(
            '<div style = "color:white; font-size: 16px; text-align:center; background-color: #2d3d4a">기업관련 기사 조회</div>',
            # #403466  2d3d4a
            unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)

        pie_chart_df = pd.DataFrame(df[df.기업명 != '-'].기업명.value_counts()).reset_index()[:10]
        pie_chart_df.columns = ['기업명', '카운트']

        fig_pie = pie_chart_df.iplot(kind='pie', labels='기업명', values='카운트', asFigure=True, dimensions=(400, 350),
                                     colors=('#a2b4cd', '#a2a9cd', '#77adda', '#0eccfb', '#85d3e6',
                                             '#2ebbc9'))  # '#ff4388', '#fe7e22', '#fbc120', '#4b1a84'

        fig_pie.update_layout(margin_l=left_mg, margin_r=right_mg, margin_t=top_mg, margin_b=btm_mg,
                              plot_bgcolor='white', paper_bgcolor='white', font_color="black",
                              # plot_bgcolor='#151121', paper_bgcolor='#0e1117',font_color="blue",
                              legend=dict(bgcolor='#e7f6fa', orientation='v', font=dict(color='black'))
                              # orientation='h' #d9d9d9

                              )

        st.plotly_chart(fig_pie, use_container_width=True)

    ''
    ''
    ######################### 뉴스보여주기
    st.subheader('오늘의 이슈',
                 help="전체 기사를 조회할 수 있는 화면입니다. 각 컬럼별 설명은 아래와 같습니다.\n- 날짜 : 각 기사가 발행된 날짜 \n- 분류 : 학습된 AI를 활용하여 카테고리를 크게 사회동향, 타사동향 및 이벤트, 상품, 제도를 구분지었습니다. \n- 기업명 : 해당 기사가 어떤 기업에 관한 내용인지 나타냅니다.\n- 제목 : 제목 선택시 해당 기사 페이지로 바로 넘어가도록 하이퍼링크가 구현되어있습니다. \n- 본문요약 : 학습된 AI가 기사 전체의 본문을 3줄 이내로 요약하여 요점을 쉽게 파악할 수 있습니다. ")
    st.text(
        f'전체 수집된 기사 중 유의미 하다고 판단된 기사는 총 {df.shape[0]}건이며, 금일 기준 ({df.날짜.max()}) 수집된 주요 기사는 총 {df[df.날짜 == df.날짜.max()].shape[0]}건 입니다.')
    ''
    df2 = df[['날짜', '분류', '기업명', '제목', '본문요약', 'url']]

    title_list = []
    for idx, row in df2.iterrows():
        tmp = make_clickable([row['url'], row['제목']])
        title_list.append(tmp)

    df2['기사제목'] = title_list

    df2.index = df2.index + 1

    ###################
    df2 = df2[['날짜', '분류', '기업명', '기사제목', '본문요약']]

    ## 라디오 추가
    radio_sel = st.multiselect(f"수집 뉴스 조회", list(df2.분류.unique()), default=list(df2.분류.unique()), key='part2_1',
                               max_selections=4)
    tmp1 = df2[(df2['분류'].isin(radio_sel))].reset_index(drop=True)
    tmp1.index = tmp1.index + 1
    ################### 가운데 정렬 설정
    # df2.style.set_properties(**{'text-align': 'center'}).set_table_styles(
    #     [{'selector': 'th', 'props': [('text-align', 'center')]}])
    # st.markdown('<style>.col_heading{text-align: center;}</style>', unsafe_allow_html=True)
    # df2.columns = ['<div class="col_heading">' + col + '</div>' for col in df2.columns]
    # st.write(tmp1.to_html(escape=False), unsafe_allow_html=True)

    tmp1.style.set_properties(**{'text-align': 'center'}).set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'center')]}])
    st.markdown('<style>.col_heading{text-align: center;}</style>', unsafe_allow_html=True)
    tmp1.columns = ['<div class="col_heading">' + col + '</div>' for col in tmp1.columns]
    st.write(tmp1.to_html(escape=False), unsafe_allow_html=True)

with white_space_2:
    st.empty()

############################ 참고 사이트
# 이모지 찾기 :  https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# extra : https://extras.streamlit.app/Dataframe%20explorer%20UI
# iplot 스타일 설정 : https://wikidocs.net/186155 (iplot쓰려면 import plotly.graph_objects as go / # import cufflinks as cf  두개 필수 )
# pie chart 참고 : https://sks8410.tistory.com/35
# 색상 추천 사이트 : https://www.colorhexa.com/34b5d5

# https://yeomss.tistory.com/301
# streamlit dataframe header center정렬 :  https://discuss.streamlit.io/t/center-dataframe-header/51193/4



#-------------------------------------------------------------------------------------
# # import pickle
# # import streamlit as st
# # from streamlit_lottie import st_lottie
# # from PIL import Image
# # import matplotlib.pyplot as plt
# # from wordcloud import WordCloud
# # import collections
# import datetime
# import pandas as pd
# import streamlit as st
# from st_aggrid import AgGrid
# import numpy
# import plotly.express as px
# import plotly.graph_objects as go
# import cufflinks as cf


# def make_clickable(get_list):
#     link, title = get_list[0], get_list[1]
#     # text = link.split('=')[1]
#     return f'<a target="aboutlink" href="{link}">{title}</a>'


# # 페이지 설정
# st.set_page_config(
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ################# Style option
# left_mg = 0
# right_mg = 10
# top_mg = 0
# btm_mg = 10

# hide_table_row_index = """
#             <style>
#             thead tr th:first-child {display:none}
#             tbody th {display:none}
#             .col_heading {text-align: center !important}
#             </style>
#             """

# ################# DATA LOAD
# df = pd.read_excel('./resource/05_2023-10-04_final_object_find.xlsx')  # 06_2023-09-15_complete.xlsx
# df['날짜'] = (pd.to_datetime(df['날짜']).dt.strftime('%Y-%m-%d'))
# df['날짜'] = df['날짜'].astype(str)

# # 사이드바에 내용 추가
# st.sidebar.header("Side Bar")

# white_space_1, data_space, white_space_2 = st.columns([0.1, 0.8, 0.1])

# with white_space_1:
#     st.empty()

# with data_space:
#     ######################### HEAD
#     # 메인 콘텐츠 영역에 내용 추가
#     st.title(":newspaper:퇴직연금 동향 뉴스")
#     st.write("다음은 금일 수집한 퇴직연금 관련 뉴스 리스트입니다. (조회일자 기준 최근 7일 기사 확인이 가능합니다.)")
#     ''
#     ''
#     ######################### 차트 화면
#     st.subheader('뉴스 분석',
#                  help="수집한 결과를 차트로 파악하기 쉽게 도식화 해두었습니다.\n- 주별뉴스현황 : 카테고리별로 기사 발행 현황에 대해 막대차트로 확인가능합니다.\n- 기업관련 기사 조회 : 기업별로 발행한 퇴직연금 관련 기사 수를 파이차트로 비중을 도식화 하였습니다. ")
#     subject_chart, company_chart = st.columns(2, gap="large")

#     ##### CHAT01. 뉴스 주제별 bar chat
#     with subject_chart:
#         st.markdown(
#             '<div style = "color:white; font-size: 16px; text-align:center; background-color: #2d3d4a">주별 뉴스 현황</div>',
#             # #403466  2d3d4a
#             unsafe_allow_html=True)
#         st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)
#         df_pivot = pd.pivot_table(df, index='날짜',
#                                   columns='분류',
#                                   values='제목', aggfunc='count').fillna(0)

#         fig_amt = df_pivot.iplot(kind='bar', barmode='stack', asFigure=True, dimensions=(400, 400),
#                                  colors=('#7f999f', '#a2a9cd', '#77adda', '#85d3e6', '#0eccfb', '#2ebbc9'))

#         fig_amt.update_layout(margin_l=left_mg, margin_r=right_mg, margin_t=top_mg, margin_b=btm_mg,
#                               plot_bgcolor='white', paper_bgcolor='white', font_color="black",
#                               legend=dict(bgcolor='#e7f6fa', yanchor='top', y=-0.1, xanchor='left',
#                                           x=0.015, orientation='h', font=dict(color='black'))  # orientation='h'
#                               )

#         fig_amt.update_xaxes(showgrid=True, gridcolor='#adb0c2', tickfont_color='black')
#         fig_amt.update_yaxes(showgrid=True, gridcolor='#adb0c2', tickfont_color='black')  # 332951
#         st.plotly_chart(fig_amt, use_container_width=True)

#     with company_chart:
#         st.markdown(
#             '<div style = "color:white; font-size: 16px; text-align:center; background-color: #2d3d4a">기업관련 기사 조회</div>',
#             # #403466  2d3d4a
#             unsafe_allow_html=True)
#         st.markdown('<h3 style="text-align:center">   </h3>', unsafe_allow_html=True)

#         pie_chart_df = pd.DataFrame(df[df.기업명 != '-'].기업명.value_counts()).reset_index()[:10]
#         pie_chart_df.columns = ['기업명', '카운트']

#         fig_pie = pie_chart_df.iplot(kind='pie', labels='기업명', values='카운트', asFigure=True, dimensions=(400, 350),
#                                      colors=('#a2b4cd', '#a2a9cd', '#77adda', '#0eccfb', '#85d3e6',
#                                              '#2ebbc9'))  # '#ff4388', '#fe7e22', '#fbc120', '#4b1a84'

#         fig_pie.update_layout(margin_l=left_mg, margin_r=right_mg, margin_t=top_mg, margin_b=btm_mg,
#                               plot_bgcolor='white', paper_bgcolor='white', font_color="black",
#                               # plot_bgcolor='#151121', paper_bgcolor='#0e1117',font_color="blue",
#                               legend=dict(bgcolor='#e7f6fa', orientation='v', font=dict(color='black'))
#                               # orientation='h' #d9d9d9

#                               )

#         st.plotly_chart(fig_pie, use_container_width=True)

#     ''
#     ''
#     ######################### 뉴스보여주기
#     st.subheader('오늘의 이슈',
#                  help="전체 기사를 조회할 수 있는 화면입니다. 각 컬럼별 설명은 아래와 같습니다.\n- 날짜 : 각 기사가 발행된 날짜 \n- 분류 : 학습된 AI를 활용하여 카테고리를 크게 사회동향, 타사동향 및 이벤트, 상품, 제도를 구분지었습니다. \n- 기업명 : 해당 기사가 어떤 기업에 관한 내용인지 나타냅니다.\n- 제목 : 제목 선택시 해당 기사 페이지로 바로 넘어가도록 하이퍼링크가 구현되어있습니다. \n- 본문요약 : 학습된 AI가 기사 전체의 본문을 3줄 이내로 요약하여 요점을 쉽게 파악할 수 있습니다. ")
#     st.text(
#         f'전체 수집된 기사 중 유의미 하다고 판단된 기사는 총 {df.shape[0]}건이며, 금일 기준 ({df.날짜.max()}) 수집된 주요 기사는 총 {df[df.날짜 == df.날짜.max()].shape[0]}건 입니다.')
#     ''
#     df2 = df[['날짜', '분류', '기업명', '제목', '본문요약', 'url']]

#     title_list = []
#     for idx, row in df2.iterrows():
#         tmp = make_clickable([row['url'], row['제목']])
#         title_list.append(tmp)

#     df2['기사제목'] = title_list

#     ### 이건 추후에 지울것
#     df2 = df2.drop([133, 141], axis=0).reset_index(drop=True)
#     ###
#     df2.index = df2.index + 1



#     ###################
#     df2 = df2[['날짜', '분류', '기업명', '기사제목', '본문요약']]

#     ## 라디오 추가
#     radio_sel = st.multiselect(f"수집 뉴스 조회",list(df2.분류.unique()) , default=list(df2.분류.unique()), key='part2_1',
#                                   max_selections=4)
#     tmp1 = df2[(df2['분류'].isin(radio_sel))].reset_index(drop=True)
    
#     ################### 가운데 정렬 설정
#     # df2.style.set_properties(**{'text-align': 'center'}).set_table_styles(
#     #     [{'selector': 'th', 'props': [('text-align', 'center')]}])
#     # st.markdown('<style>.col_heading{text-align: center;}</style>', unsafe_allow_html=True)
#     # df2.columns = ['<div class="col_heading">' + col + '</div>' for col in df2.columns]
#     # st.write(tmp1.to_html(escape=False), unsafe_allow_html=True)

#     tmp1.style.set_properties(**{'text-align': 'center'}).set_table_styles(
#         [{'selector': 'th', 'props': [('text-align', 'center')]}])
#     st.markdown('<style>.col_heading{text-align: center;}</style>', unsafe_allow_html=True)
#     tmp1.columns = ['<div class="col_heading">' + col + '</div>' for col in tmp1.columns]
#     st.write(tmp1.to_html(escape=False), unsafe_allow_html=True)


# with white_space_2:
#     st.empty()

# ############################ 참고 사이트
# # 이모지 찾기 :  https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# # extra : https://extras.streamlit.app/Dataframe%20explorer%20UI
# # iplot 스타일 설정 : https://wikidocs.net/186155 (iplot쓰려면 import plotly.graph_objects as go / # import cufflinks as cf  두개 필수 )
# # pie chart 참고 : https://sks8410.tistory.com/35
# # 색상 추천 사이트 : https://www.colorhexa.com/34b5d5

# # https://yeomss.tistory.com/301
# # streamlit dataframe header center정렬 :  https://discuss.streamlit.io/t/center-dataframe-header/51193/4
