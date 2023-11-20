import os
import streamlit as st
import pandas as pd
import matplotlib as mpl
import plotly.express as px
import base64
import pickle
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# -*- coding: utf-8-sig -*-

# 사용자 계정 정보
accounts = {
    'kmac_dx': 'kmac_dx',
    'databank279': 'databank2615',
    'databank196': 'databank4259',
    'databank105': 'databank1963',
    'databank003': 'databank5554',
    'databank165': 'databank2562',
    'databank078': 'databank3023',
    'databank009': 'databank1514',
    'databank264': 'databank0145',
    'databank015': 'databank8102',
    'databank021': 'databank8012',
    'databank082': 'databank5722',
    'databank275': 'databank8437',
    'databank072': 'databank6596',
    'databank229': 'databank8208',
    'databank100': 'databank8874',
    'databank052': 'databank3111',
    'databank067': 'databank1689',
    'databank079': 'databank8929',
    'databank053': 'databank5530',
    'databank133': 'databank8560',
    'databank190': 'databank7554',
    'databank159': 'databank1530',
    'databank007': 'databank2524',
    'databank004': 'databank2071',
    'databank084': 'databank6974',
    'databank125': 'databank3588',
    'databank031': 'databank5306',
    'databank020': 'databank1555',
    'databank080': 'databank5535',
    'databank006': 'databank5990',
    'databank025': 'databank5242',
    'databank063': 'databank9922',
    'databank062': 'databank2638',
    'databank226': 'databank2570',
    'databank011': 'databank5471',
    'databank032': 'databank7104',
    'databank029': 'databank1550',
    'databank017': 'databank0970',
    'databank248': 'databank230 ',
    'databank145': 'databank4742',
    'databank276': 'databank4200',
    'databank221': 'databank4481',
    'databank061': 'databank5325',
    'databank111': 'databank0378',
    'databank008': 'databank9906',
    'databank126': 'databank5563',
    'databank094': 'databank3083',
    'databank136': 'databank1760',
    'databank074': 'databank3881',
    'databank092': 'databank7666',
    'databank010': 'databank7754',
    'databank253': 'databank5728',
    'databank224': 'databank1089',
    'databank225': 'databank1089',
    'databank107': 'databank2753',
    'databank012': 'databank2258',
    'databank034': 'databank3524',
    'databank086': 'databank6565',
    'databank081': 'databank4708',
    'databank055': 'databank1592',
    'databank277': 'databank5995',
    'databank095': 'databank1318',
    'databank070': 'databank6506',
    'databank040': 'databank7973',
    'databank036': 'databank1155',
    'databank051': 'databank8182',
    'databank026': 'databank2203',
    'databank104': 'databank6574',
    'databank047': 'databank0339',
    'databank073': 'databank8700',
    'databank161': 'databank6138',
    'databank146': 'databank6806',
    'databank103': 'databank4500',
    'databank065': 'databank8698',
    'databank075': 'databank8356',
    'databank098': 'databank2002',
    'databank278': 'databank6536',
    'databank043': 'databank0923',
    'databank200': 'databank6032',
    'databank049': 'databank0064',
    'databank033': 'databank6170',
    'databank219': 'databank7978',
    'databank088': 'databank5911',
    'databank071': 'databank4363',
    'databank192': 'databank7213',
    'databank102': 'databank8387',
    'databank163': 'databank-394',
    'databank030': 'databank7111',
    'databank258': 'databank9595',
    'databank046': 'databank9974',
    'databank252': 'databank8297',
    'databank039': 'databank2848',
    'databank068': 'databank7693',
    'databank093': 'databank8096',
    'databank035': 'databank9111',
    'databank054': 'databank8176',
    'databank045': 'databank5180',
    'databank131': 'databank3538',
    'databank016': 'databank6531',
    'databank083': 'databank2739',
    'databank267': 'databank7765',
    'databank230': 'databank1091',
    'databank193': 'databank7779',
    'databank223': 'databank9979',
    'databank090': 'databank3959',
    'databank134': 'databank7588',
    'databank005': 'databank4917',
    'databank024': 'databank9686',
    'databank042': 'databank1500',
    'databank280': 'databank5057',
    'databank091': 'databank9129',
    'databank001': 'databank1290',
    'databank060': 'databank2951',
    'databank137': 'databank1106',
    'databank140': 'databank1106',
    'databank202': 'databank0752',
    'databank089': 'databank2798',
    'databank194': 'databank4924',
    'databank087': 'databank6121',
    'databank002': 'databank6895',
    'databank097': 'databank2122',
    'databank022': 'databank6487',
    'databank201': 'databank5918',
    'databank066': 'databank3334',
    'databank027': 'databank6016',
    'databank058': 'databank0369',
    'databank019': 'databank2829',
    'databank041': 'databank1865',
    'databank251': 'databank1361',
    'databank023': 'databank5809',
    'databank099': 'databank4335',
    'databank096': 'databank7817',
    'databank014': 'databank3366',
    'databank118': 'databank6627',
    'databank044': 'databank4440',
    'databank228': 'databank5225',
    'databank101': 'databank0396',
    'databank064': 'databank3223',
    'databank109': 'databank2753',
    'databank037': 'databank9729',
    'databank028': 'databank8975',
    'databank069': 'databank6245',
    'databank013': 'databank5694',
    'databank050': 'databank2347'
    }

# 로그인 함수
@st.cache_data(experimental_allow_widgets=True)
def check_login(username, password):
    return accounts.get(username) == password

# 로그인 세션 상태 관리
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 로그인 화면 표시
def login_ui():
    with st.container():
        st.title("로그인")
        username = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        if st.button("로그인"):
            if check_login(username, password):
                st.session_state['logged_in'] = True
                st.success("로그인에 성공했습니다.")
            else:
                st.error("아이디 혹은 비밀번호가 잘못되었습니다.")

# EDA 완료 상태를 설정하는 함수

def set_eda_complete():
    st.session_state.eda_complete = True  # EDA 완료 상태를 True로 설정

def start_setup():
    st.session_state.setup_started = True  # Setup 시작 상태를 True로 설정

# 메인 앱 콘텐츠
def main_app():
    try:
        # 페이지 제목
        st.title('📍AutoML을 활용한 데이터 분석')

        # 페이지 설명
        st.write('''
            자동화된 머신러닝(AutoML) 기법을 사용하여 데이터를 분석하고, 모델을 비교, 최적화할 수 있습니다. 
            데이터를 업로드하고, 관심 있는 결과를 얻어보세요.
        ''')

        st.sidebar.title('문제해결은행🏛️')

        # 데이터 파일 업로드
        uploaded_file = st.sidebar.file_uploader("데이터 파일 업로드 (CSV, Excel, Pickle)", type=['csv', 'xlsx', 'pickle'])
        df = None

        # 업로드된 파일로부터 데이터프레임 로드
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith(('.pkl', '.pickle')):
                df = pickle.load(uploaded_file, encoding='utf-8-sig')

        # 모델 종류 선택
        model_type = st.sidebar.selectbox("모델 종류 선택", ["분류", "예측", "군집분석", "시계열", "이상치 탐지"])
        st.session_state['model_type'] = model_type  # 세션 상태에 모델 종류 저장

        # 초기화
        datetime_column = None
        target_column = None

        # 시간 변수 선택 (시계열)
        if model_type == "시계열" and df is not None:
            datetime_column = st.sidebar.selectbox("시간 변수 선택", df.columns)
            if df[datetime_column].dtype != 'datetime64[ns]':
                try:
                    df[datetime_column] = pd.to_datetime(df[datetime_column])
                except Exception as e:
                    st.error(f"시간 변수를 datetime 형식으로 변환하는 데 실패했습니다: {e}")

            available_columns_for_target = df.columns.drop(datetime_column)
            target_column = st.sidebar.selectbox("타겟 변수 선택", available_columns_for_target)

        # 타겟 변수 선택 (군집분석 및 이상치 탐지 제외)
        elif model_type not in ["군집분석", "이상치 탐지"] and df is not None:
            target_column = st.sidebar.selectbox("타겟 변수 선택", df.columns)

        # 활용 컬럼 선택
        selected_columns = []
        if df is not None:
            # 타겟 변수와 날짜/시간 컬럼을 제외한 컬럼들만 선택 가능하도록 설정
            selectable_columns = [col for col in df.columns if col != target_column and col != datetime_column]
            selected_columns = st.sidebar.multiselect("분석에 사용할 컬럼 선택", selectable_columns, default=selectable_columns)

        # 메인 콘텐츠 영역
        tab1, tab2, tab3, tab4 = st.tabs(['데이터 EDA' , '분석 모델링', '모델 성능 평가', '모델 활용'])

        with tab1:
            st.markdown('## 📊 데이터 EDA')
            st.write('데이터 EDA는 데이터에 대해 확인하는 데이터 분석을 위한 준비절차입니다.')
            
            # 필터링된 데이터프레임 초기화
            filtered_df = pd.DataFrame()

            # 필터링된 컬럼 리스트
            if selected_columns:
                filtered_columns = selected_columns + ([target_column] if target_column else []) + ([datetime_column] if datetime_column else [])
            else:
                filtered_columns = ([target_column] if target_column else []) + ([datetime_column] if datetime_column else [])

            # df가 None이 아닐 때만 필터링된 데이터프레임 생성
            if df is not None:
                filtered_df = df[filtered_columns].copy()                
            else:
            # df가 None일 경우 안전하게 처리
                filtered_df = pd.DataFrame(columns=filtered_columns)

            if df is not None:
                # 세션 상태에서 모델 타입을 참조
                model_type = st.session_state['model_type']

                # 모델 클래스 인스턴스화 및 세션 상태에 저장
                if st.session_state['model_type'] == "분류":
                    from AutoML_Classification import Classification
                    st.session_state['model'] = Classification(None, target_column)
                elif model_type == "예측":
                    from AutoML_Regression import Regression
                    st.session_state['model'] = Regression(None, target_column)
                elif model_type == "군집분석":
                    from AutoML_Clustering import Clustering
                    st.session_state['model'] = Clustering(None, target_column)
                elif model_type == "시계열":
                    from AutoML_TimeSeries import TimeSeries
                    st.session_state['model'] = TimeSeries(None, target_column)
                elif model_type == "이상치 탐지":
                    from AutoML_AnomalyDetection import AnomalyDetection
                    st.session_state['model'] = AnomalyDetection(None, target_column)   

                # 모델 데이터 로드
                if df is not None:
                    st.session_state['model'].load_data(dataframe=filtered_df)

                # 데이터프레임 필터링 옵션
                if st.session_state['model_type'] == "분류":# in ["분류"]:
                    if st.checkbox("타겟 변수에 대한 데이터만 보기"):
                        filtered_value = st.selectbox("타겟 변수 값 선택", df[target_column].unique())
                        st.dataframe(df[df[target_column] == filtered_value])
                    else:
                        st.dataframe(df)

                elif model_type in ["예측"]:
                    if st.checkbox("범위로 데이터 필터링"):
                        min_val, max_val = st.slider("범위 선택", float(df[target_column].min()), float(df[target_column].max()), (float(df[target_column].min()), float(df[target_column].max())))
                        st.dataframe(df[df[target_column].between(min_val, max_val)])
                    else:
                        st.dataframe(df)

                elif model_type in ["군집분석"]:
                    st.dataframe(df)

                elif model_type in ["시계열"]:
                    if st.checkbox("타겟 변수에 대한 데이터만 보기"):
                        filtered_value = st.selectbox("타겟 변수 값 선택", df[target_column].unique())
                        st.dataframe(df[df[target_column] == filtered_value])
                    else:
                        st.dataframe(df)   

                elif model_type in ["이상치 탐지"]:
                    st.dataframe(df)

                data_hash = st.session_state['model'].hash_data()

                # 메소드 호출
                if 'model' in st.session_state:
                    st.markdown("### 수치형 데이터 통계")
                    data_description = st.session_state['model'].explore_data(data_hash)
                    st.write(data_description)

                    st.markdown("### 수치형 데이터 분포")
                    numerical_figs = st.session_state['model'].visualize_numerical_distribution(data_hash)
                    for fig in numerical_figs:
                        st.pyplot(fig)

                    categorical_figs = st.session_state['model'].visualize_categorical_distribution(data_hash)
                    if categorical_figs:
                        st.markdown("### 범주형 데이터 분포")
                        for fig in categorical_figs:
                            st.pyplot(fig)
                    else:
                        st.markdown("### 범주형 데이터 분포")
                        st.warning("이 데이터셋에는 범주형 변수가 없습니다.")      

                # 결측치 분포 시각화
                if 'model' in st.session_state:
                    st.markdown("### 결측치 분포")
                    st.write('''이 차트는 데이터셋의 각 변수에서 결측치의 비율을 보여줍니다. 
                            높은 결측치 비율을 가진 변수는 주의 깊게 살펴볼 필요가 있습니다.''')
                    missing_df, missing_fig = st.session_state['model'].visualize_missing_distribution(data_hash)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.dataframe(missing_df, height=300)  # 데이터 프레임 높이 조절
                    with col2:
                        st.pyplot(missing_fig)

                # 시계열 모델이 아닐 경우에만 결측치 처리 및 시각화 실행
                if model_type != '시계열':
                    missing_threshold = st.sidebar.slider("결측치 처리 임계값", 0, 100, 30)
                    cleaned_missing_df, cleaned_missing_fig = st.session_state['model'].handle_and_visualize_missing(data_hash, threshold=missing_threshold)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.dataframe(cleaned_missing_df, height=300)  # 데이터 프레임 높이 조절
                    with col2:
                        st.pyplot(cleaned_missing_fig)

                # 수치형 변수 상관계수 시각화
                if 'model' in st.session_state:
                    numerical_corr_fig = st.session_state['model'].numerical_correlation(data_hash)
                    # st.pyplot(numerical_corr_fig)
                    
                    # 범주형 변수 상관계수 시각화
                    categorical_corr_fig = st.session_state['model'].categorical_correlation(data_hash)
                    # st.pyplot(categorical_corr_fig)
                    st.markdown("### 변수 간 상관계수")
                    st.write("변수 간의 상관관계를 나타내는 히트맵입니다. 값이 높을수록 강한 상관관계를 나타냅니다.")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### 수치형 변수 상관계수")
                        st.pyplot(numerical_corr_fig)
                    with col2:
                        st.markdown("#### 범주형 변수 상관계수")
                        st.pyplot(categorical_corr_fig)

                if model_type == '시계열':
                    st.write('\n')
                    st.markdown("### 시계열 데이터 확인")
                    
                    # 시계열 그래프 플로팅
                    fig = px.line(df, x=datetime_column, y=target_column, title='시간에 따른 타겟 변수 변화')
        
                    # Plotly 그래프를 Streamlit에 표시
                    st.plotly_chart(fig)
                    set_eda_complete()  # EDA 완료 상태 설정
        
            if "eda_complete" in st.session_state and st.session_state.eda_complete:
                st.write('\n')
                st.write('\n')
                st.write('-------------------------------------------------')
                st.write(' #### ❗️데이터 EDA를 마쳤습니다.')
                st.write(''' 
                        다음으로 분석 모델링을 진행해볼까요?    
                        상단의 **분석 모델링 탭**을 클릭해주세요!
                        ''')

        with tab2:
            st.markdown('## 💡분석 모델링')
            if df is not None:

                # 필터링된 데이터프레임
                include = selected_columns + ([target_column] if target_column else []) + ([datetime_column] if datetime_column else [])
                filtered_df = df[include].copy()

                # 모델 설정 옵션
                st.markdown('### 모델 설정 옵션')

                # 모델 종류별 옵션
                if st.session_state['model_type'] == "분류": #model_type == "분류":
                    model = Classification(None, target_column)
                    # model = st.session_state['model']
                    model.load_data(dataframe=filtered_df)

                    remove_outliers = st.checkbox("이상치 제거", value=False, help="데이터에서 이상치를 제거할지 여부.")
                    remove_multicollinearity = st.checkbox("다중공선성 제거", value=True, help="변수 간 고도의 상관관계(다중공선성) 제거 여부.")
                    multicollinearity_threshold = st.slider("다중공선성 임계값", 0.0, 1.0, 0.9, help="다중공선성을 제거할 상관관계 임계값.")
                    train_size = st.slider("훈련 데이터 크기", 0.1, 1.0, 0.7, help="전체 데이터 중 훈련 데이터로 사용할 비율.")
                    fold_strategy = st.selectbox("교차 검증 전략", ['stratifiedkfold', 'kfold'], index=0, help="교차 검증 시 사용할 전략, 예: stratifiedkfold, kfold.")
                    fold = st.number_input("교차 검증 폴드 수", min_value=2, max_value=10, value=3, help="교차 검증 시 데이터를 나눌 폴드의 수.")
                    profile = st.checkbox("프로파일링 활성화", value=True, help="데이터 프로파일링 기능 활성화 여부.")
                    session_id = st.number_input("세션 ID", value=786, help="실험의 재현성을 위한 세션 ID.")
                    fix_imbalance = st.checkbox("데이터 불균형 처리", value=True, help="클래스 불균형이 존재하는 데이터셋에 대한 처리 여부.")
                    fix_imbalance_method = st.selectbox("불균형 처리 방법 ", ['SMOTE', 'None'], index=0, help="데이터 불균형 처리 방법 선택, 예: SMOTE.")

                    # setup 시작 버튼
                    if st.button("Setup 시작", on_click=start_setup):
                        # setup 메서드 실행
                        _, setup_results=model.setup(fix_imbalance=fix_imbalance, 
                                    fix_imbalance_method=fix_imbalance_method, 
                                    remove_outliers=remove_outliers, 
                                    remove_multicollinearity=remove_multicollinearity,
                                    multicollinearity_threshold=multicollinearity_threshold,
                                    train_size=train_size,
                                    fold_strategy=fold_strategy,
                                    fold=fold,
                                    profile=profile,
                                    session_id=session_id, 
                                    verbose=False
                                    )
                        st.success("Setup 완료!")

                        # setup 결과 표시
                        st.table(setup_results)
                
                    st.write('\n')
                    # 모델 비교 및 최적화 설정
                    if "setup_started" in st.session_state and st.session_state.setup_started:
                        
                        st.markdown('### 모델 비교 및 최적화 설정')

                        st.write('\n')
                        if st.button("모델 비교 및 최적화 시작"):
                            with st.spinner('모델을 비교하고 최적화하는 중...'):
                                # 모델 비교 및 최적화
                                model_dict, tuned_models, compare_result, optimization_results = model.compare_and_optimize_models(n_select=3, n_iter=10)
                                st.session_state['models_dict'] = model_dict
                                st.success('모델 비교 및 최적화 완료!')

                                # 결과 표시 및 세션 상태 업데이트
                                st.session_state['optimization_completed'] = True
                                st.write('\n')
                                st.write('모델 성능 비교 결과')
                                st.dataframe(compare_result)

                                # 최적화된 모델 결과 표시
                                st.write('##### 최적화된 모델 결과')
                                for i, (tuned_model, result_df) in enumerate(zip(tuned_models, optimization_results)):
                                    st.markdown(f'**모델 {i+1}:** {str(tuned_model)}')
                                    st.dataframe(result_df)  # 각 모델의 최적화 결과를 데이터 프레임 형태로 표시합니다.
                        
                    if st.session_state.get('optimization_completed', False):
            
                        # 최고 성능 모델 선택
                        st.write('\n')
                        st.markdown('### 최고 성능 모델 선택')
                        best_model_optimize = st.selectbox("최고 성능 모델 선택 기준", ['Accuracy', 'Recall', 'Precision', 'F1'], index=0)
                        if st.button("최고 성능 모델 선택"):
                            with st.spinner('최고 성능 모델을 선택하는 중...'):
                                best_model = model.select_best_model(optimize=best_model_optimize)
                                st.session_state['models_dict']['최고 성능 모델'] = best_model
                                st.success('최고 성능 모델 선택 완료!')
                                # st.dataframe(result_df)

                                # 최고 성능 모델 정보 표시
                                st.write('\n')
                                st.markdown('##### 선택된 최고 성능 모델')
                                st.write(f'**{str(best_model)}**')
                                
                                # 세션 상태 업데이트
                                st.session_state['model_selected'] = True

                        # 모델 저장
                        if st.session_state.get('model_selected', False):
                            st.write('\n')
                            st.markdown('### 모델 저장 설정')
                            model_name = st.text_input("저장할 모델의 이름을 입력하세요", "classification_model")
                            save_path = st.text_input("모델을 저장할 경로를 입력하세요", "C:/Users/Desktop")

                            if st.button("모델 저장하기"):
                                with st.spinner('모델을 저장하는 중...'):
                                    model.save_model(model_name, save_path)
                                    st.success('모델 저장 완료!')
                                    st.write(f"'{save_path}' 경로에 모델 '{model_name}'을 저장했습니다.")
            
                elif model_type == "예측":
                    model = Regression(None, target_column)
                    model.load_data(dataframe=filtered_df)

                    remove_outliers = st.checkbox("이상치 제거", value=False, help="데이터에서 이상치를 제거할지 여부.")
                    remove_multicollinearity = st.checkbox("다중공선성 제거", value=True, help="변수 간 고도의 상관관계(다중공선성) 제거 여부.")
                    multicollinearity_threshold = st.slider("다중공선성 임계값", 0.0, 1.0, 0.9, help="다중공선성을 제거할 상관관계 임계값.")
                    train_size = st.slider("훈련 데이터 크기", 0.1, 1.0, 0.7, help="전체 데이터 중 훈련 데이터로 사용할 비율.")
                    # fold_strategy = st.selectbox("교차 검증 전략", ['kfold'], index=0, help="교차 검증 시 사용할 전략, 예: kfold.")
                    fold = st.number_input("교차 검증 폴드 수", min_value=2, max_value=10, value=3, help="교차 검증 시 데이터를 나눌 폴드의 수.")
                    # profile = st.checkbox("프로파일링 활성화", value=True, help="데이터 프로파일링 기능 활성화 여부.")
                    session_id = st.number_input("세션 ID", value=786, help="실험의 재현성을 위한 세션 ID.")
                    normalize = st.checkbox("데이터 정규화", value=True, help="데이터 정규화 여부.")
                    normalize_method = st.selectbox("정규화 방법", ['zscore', 'minmax', 'maxabs', 'robust'], index=0, help="데이터 정규화 방법 선택, 예: zscore.")
                    feature_selection = st.checkbox("변수 선택 여부", value=False, help="변수 선택 여부.")
                    feature_selection_method = st.selectbox("변수 선택 방법", ['classic', 'univariate', 'sequential'], index=0, help="변수 선택 방법 선택, 예: classic.")
                    feature_selection_estimator = st.selectbox("변수 선택 알고리즘", ['lr', 'rf', 'lightgbm', 'xgboost', 'catboost'], index=0, help="변수 선택 알고리즘 선택, 예: lr.")
                    # verbose = st.checkbox("상세 출력", value=False, help="모델 설정 및 훈련 과정에서 상세 정보 출력 여부.")

                    # setup 시작 버튼
                    if st.button("Setup 시작", on_click=start_setup):
                        # setup 메서드 실행
                        _, setup_results=model.setup(remove_outliers=remove_outliers, 
                                    remove_multicollinearity=remove_multicollinearity,
                                    multicollinearity_threshold=multicollinearity_threshold,
                                    train_size=train_size,
                                    fold_strategy='kfold',
                                    fold=fold,
                                    session_id=session_id,
                                    normalize=normalize,
                                    normalize_method=normalize_method,
                                    feature_selection=feature_selection,
                                    feature_selection_method=feature_selection_method,
                                    feature_selection_estimator=feature_selection_estimator,
                                    verbose=False
                                    )
                        st.success("Setup 완료!")

                        # setup 결과 표시
                        st.table(setup_results)

                        # setup이 시작되었다는 것을 st.session_state에 기록
                        st.session_state.setup_started = True  # 상태 추가

                    st.write('\n')
                    # 모델 비교 및 최적화 설정
                    if st.session_state.get('setup_started', False):
                        st.markdown('### 모델 비교 및 최적화 설정')

                        if st.button("모델 비교 및 최적화 시작"):
                            with st.spinner('모델을 비교하고 최적화하는 중...'):
                                # 모델 비교 및 최적화
                                model_dict, tuned_models, compare_result, optimization_results = model.compare_and_optimize_models(n_select=3, n_iter=10)
                                st.session_state['models_dict'] = model_dict
                                st.success('모델 비교 및 최적화 완료!')

                                # 결과 표시 및 세션 상태 업데이트
                                st.session_state['optimization_completed'] = True
                                st.write('\n')
                                st.write('모델 성능 비교 결과')
                                st.dataframe(compare_result)

                                # 최적화된 모델 결과 표시
                                st.write('##### 최적화된 모델 결과')
                                for i, (tuned_model, result_df) in enumerate(zip(tuned_models, optimization_results)):
                                    st.markdown(f'**모델 {i+1}:** {str(tuned_model)}')
                                    st.dataframe(result_df)  # 각 모델의 최적화 결과를 데이터 프레임 형태로 표시합니다.
                
                        if st.session_state.get('optimization_completed', False):
                            # 최고 성능 모델 선택
                            st.markdown('### 최고 성능 모델 선택')
                            best_model_optimize = st.selectbox("최고 성능 모델 선택 기준", ['MAE', 'MSE', 'RMSE', 'R2', 'RMSLE', 'MAPE'], index=0)
                            if st.button("최고 성능 모델 선택"):
                                with st.spinner('최고 성능 모델을 선택하는 중...'):
                                    best_model = model.select_best_model(optimize=best_model_optimize)
                                    st.session_state['models_dict']['최고 성능 모델'] = best_model
                                    st.success('최고 성능 모델 선택 완료!')

                                    # 최고 성능 모델 정보 표시
                                    st.markdown('##### 선택된 최고 성능 모델')
                                    st.write(f'**{str(best_model)}**')
                                    st.session_state['model_selected'] = True

                            # 모델 저장
                            if st.session_state.get('model_selected', False):
                                st.markdown('### 모델 저장 설정')
                                model_name = st.text_input("저장할 모델의 이름을 입력하세요", "regression_model")
                                save_path = st.text_input("모델을 저장할 경로를 입력하세요", "C:/Users/Desktop")

                                if st.button("모델 저장하기"):
                                    with st.spinner('모델을 저장하는 중...'):
                                        model.save_model(model_name, save_path)
                                        st.success('모델 저장 완료!')
                                        st.write(f"'{save_path}' 경로에 모델 '{model_name}'을 저장했습니다.")

                elif model_type == "군집분석":
                    model = Clustering(None, target_column)
                    model.load_data(dataframe=filtered_df)

                    remove_outliers = st.checkbox("이상치 제거", value=False, help="데이터에서 이상치를 제거할지 여부.")
                    session_id = st.number_input("세션 ID", value=786, help="실험의 재현성을 위한 세션 ID.")
                    normalize = st.checkbox("데이터 정규화", value=True, help="데이터 정규화 여부.")
                    normalize_method = st.selectbox("정규화 방법", ['zscore', 'minmax', 'maxabs', 'robust'], index=0, help="데이터 정규화 방법 선택, 예: zscore.")

                    # setup 시작 버튼
                    if st.button("Setup 시작", on_click=start_setup):
                        
                        # setup 메서드 실행
                        _, setup_results = model.setup(
                            session_id=session_id, 
                            normalize=normalize,
                            normalize_method=normalize_method,
                            verbose=False)
                        st.success("Setup 완료!")

                        # setup 결과 표시
                        st.table(setup_results)  # setup_results는 ClusteringExperiment 객체일 수 있습니다. 이를 테이블로 표시할 수 있는지 확인해야 합니다.

                        # setup이 시작되었다는 것을 st.session_state에 기록
                        st.session_state.setup_started = True  # 상태 추가

                    st.write('\n')
                    # 모델 생성 및 군집 할당
                    if "setup_started" in st.session_state and st.session_state.setup_started:
                        st.markdown('### 모델 생성 및 군집 할당')
                        
                        # 모델 선택
                        model_name = st.selectbox("군집 모델 선택", ['kmeans'])
                        
                        # 클러스터 수 선택
                        num_clusters = st.slider("클러스터 수 선택", 2, 11, 3)
                        
                        # 모델 생성 버튼
                        if st.button("모델 생성"):
                            with st.spinner('모델 생성 중...'):
                                # create_model 메서드 실행
                                model_dict, created_model, model_results = model.create_model(model_name, num_clusters=num_clusters)
                                st.success('모델 생성 완료!')
                                
                                st.dataframe(model_results)  # 모델 생성 결과를 데이터 프레임 형태로 표시합니다.
                                st.write(f'생성된 모델: {str(created_model)}')  # 생성된 모델의 정보를 표시합니다.
                                st.session_state['models_dict'] = model_dict

                                st.session_state['optimization_completed'] = True  # 세션 상태 업데이트

                                # 군집 할당 및 데이터프레임 저장
                                clustered_data, clustered_result = model.assign_model(created_model)
                                st.session_state['clustered_data'] = clustered_data  # 군집화된 데이터를 세션 상태에 저장

                                st.session_state['model_selected'] = True

                        # 모델 저장
                        if st.session_state.get('model_selected', False):
                            st.write('\n')
                            st.markdown('### 모델 저장 설정')
                            model_name = st.text_input("저장할 모델의 이름을 입력하세요", "clustering_model")
                            save_path = st.text_input("모델을 저장할 경로를 입력하세요", "C:/Users/Desktop")

                            if st.button("모델 저장하기"):
                                with st.spinner('모델을 저장하는 중...'):
                                    model.save_model(model_name, save_path)
                                    st.success('모델 저장 완료!')
                                    st.write(f"'{save_path}' 경로에 모델 '{model_name}'을 저장했습니다.")

                elif model_type == "시계열":
                    model = TimeSeries(None, target_column)
                    model.load_data(dataframe=filtered_df)
                    filtered_df.index = filtered_df[datetime_column]
                    filtered_df.drop(columns=[datetime_column], inplace=True)
                    st.session_state['exog_vars'] = filtered_df[selected_columns]

                    # 사용자에게 주기(freq) 선택 옵션 표시
                    selected_freq = st.selectbox("데이터의 주기(freq)를 선택하세요. ('D' - 일, 'M' - 월, 'Q' - 분기, 'Y' - 년, 'H' - 시간, 'T' 또는 'min' - 분, 'S' - 초)", 
                                                 ["D", "M", "Q", "Y", "H", "T", "S"])
                    st.session_state['freq']=selected_freq

                    # 사용자가 주기(freq)를 선택하면 데이터 정제
                    if selected_freq:
                        new_index = pd.date_range(start=filtered_df.index.min(), end=filtered_df.index.max(), freq=selected_freq)
                        new_df = pd.DataFrame(index=new_index)
                        filtered_df = filtered_df.join(new_df)
                        filtered_df = filtered_df.fillna('null')

                    fold = st.number_input("교차 검증 폴드 수", min_value=2, max_value=10, value=3, help="교차 검증 시 데이터를 나눌 폴드의 수.")
                    fh = st.number_input("예측 지평(데이터의 25%에 해당되는 값까지 적용 가능)", min_value=1, max_value=365, value=12, help="모델이 예측할 기간의 범위.")
                    session_id = st.number_input("세션 ID", value=786, help="실험의 재현성을 위한 세션 ID.")                           
                    seasonal_period_input = st.text_input("계절성 주기 (옵션)", '', help="데이터의 계절성 주기를 입력합니다. 필요하지 않은 경우 비워 두세요.")
                    seasonal_period = int(seasonal_period_input) if seasonal_period_input else None
                    numeric_imputation_options = ["None", "drift", "linear", "nearest", "mean", "median", "backfill", "bfill", "pad", "ffill", "random"]
                    numeric_imputation_target = st.selectbox("변수의 결측치 처리 방법", numeric_imputation_options, index=1, help="변수의 누락된 값을 어떻게 처리할지 선택합니다.")
                    # 변수 스케일링 옵션
                    apply_scaling = st.checkbox("변수 스케일링 적용하기", value=True)
                    if apply_scaling:
                        scale_target_options = ["zscore", "minmax", "maxabs", "robust"]
                        scale_target = st.selectbox("변수의 스케일링 방법", scale_target_options, help="변수를 어떻게 스케일링할지 선택합니다.")
                    else:
                        scale_target = None
                        
                    st.session_state['fh'] = fh
                    st.session_state['session_id'] = session_id
                    st.session_state['numeric_imputation_target'] = numeric_imputation_target
                    st.session_state['numeric_imputation_exogenous'] = numeric_imputation_target
                    st.session_state['scale_target'] = scale_target
                    st.session_state['scale_exogenous'] = scale_target

                    # setup 시작 버튼
                    if st.button("Setup 시작", on_click=start_setup):
                        # setup 메서드 실행
                        _, setup_results = model.setup(
                            fold=fold,
                            fh=fh,
                            enforce_exogenous=False,
                            session_id=session_id,
                            seasonal_period=seasonal_period,
                            numeric_imputation_target=numeric_imputation_target,
                            numeric_imputation_exogenous=numeric_imputation_target,
                            scale_target=scale_target,
                            scale_exogenous=scale_target
                        )
                        st.success("Setup 완료!")

                        # setup 결과 표시
                        st.table(setup_results)

                        # setup이 시작되었다는 것을 st.session_state에 기록
                        st.session_state.setup_started = True  # 상태 추가
                    
                    st.write('\n')
                    # 모델 비교 및 최적화 설정
                    if st.session_state.get('setup_started', False):
                        st.markdown('### 모델 비교 및 최적화 설정')

                        if st.button("모델 비교 및 최적화 시작"):
                            with st.spinner('모델을 비교하고 최적화하는 중...'):
                                # 모델 비교 및 최적화
                                model_dict, tuned_models, compare_result, optimization_results = model.compare_and_optimize_models(n_select=3, n_iter=10)
                                st.session_state['models_dict'] = model_dict
                                st.success('모델 비교 및 최적화 완료!')

                                # 결과 표시 및 세션 상태 업데이트
                                st.session_state['optimization_completed'] = True
                                st.write('\n')
                                st.write('모델 성능 비교 결과')
                                st.dataframe(compare_result)

                                # 최적화된 모델 결과 표시
                                st.write('##### 최적화된 모델 결과')
                                for i, (tuned_model, result_df) in enumerate(zip(tuned_models, optimization_results)):
                                    st.markdown(f'**모델 {i+1}:** {str(tuned_model)}')
                                    st.dataframe(result_df)  # 각 모델의 최적화 결과를 데이터 프레임 형태로 표시합니다.
                
                        if st.session_state.get('optimization_completed', False):
                            # 최고 성능 모델 선택
                            st.markdown('### 앙상블 모델 생성')
                            best_model_optimize = st.selectbox("앙상블 모델 생성 기준", ['MASE', 'RMSSE', 'MAE', 'RMSE', 'MAPE', 'SMAPE', 'R2'], index=0)
                            if st.button("앙상블 모델 생성"):
                                with st.spinner('앙상블 모델을 생성하는 중...'):
                                    best_model = model.select_best_model(optimize=best_model_optimize)
                                    st.session_state['models_dict']['앙상블 모델'] = best_model
                                    st.success('모델 선택 완료!')

                                    # 최고 성능 모델 정보 표시
                                    st.markdown('##### 선택된 모델')
                                    st.write(f'**{str(best_model)}**')
                                    st.session_state['model_selected'] = True

                            # 모델 저장
                            if st.session_state.get('model_selected', False):
                                st.markdown('### 모델 저장 설정')
                                model_name = st.text_input("저장할 모델의 이름을 입력하세요", "timeseries_model")
                                save_path = st.text_input("모델을 저장할 경로를 입력하세요", "C:/Users/Desktop")

                                if st.button("모델 저장하기"):
                                    with st.spinner('모델을 저장하는 중...'):
                                        model.save_model(model_name, save_path)
                                        st.success('모델 저장 완료!')
                                        st.write(f"'{save_path}' 경로에 모델 '{model_name}'을 저장했습니다.")                              

                elif model_type == "이상치 탐지":
                    model = AnomalyDetection(None, target_column)
                    model.load_data(dataframe=filtered_df)
                    session_id = st.number_input("세션 ID", value=786, help="실험의 재현성을 위한 세션 ID.")                           
                    # 변수 스케일링 옵션
                    normalize = st.checkbox("변수 스케일링 적용하기", value=True)
                    if normalize:
                        normalize_method_options = ["zscore", "minmax", "maxabs", "robust"]
                        target = st.selectbox("변수의 스케일링 방법", normalize_method_options, help="변수를 어떻게 스케일링할지 선택합니다.")
                    else:
                        target = None

                    # setup 시작 버튼
                    if st.button("Setup 시작", on_click=start_setup):
                        # setup 메서드 실행
                        _, setup_results=model.setup(
                                    session_id=session_id,
                                    normalize=normalize,
                                    normalize_method=target
                                    )
                        st.success("Setup 완료!")

                        # setup 결과 표시
                        st.table(setup_results)

                        # setup이 시작되었다는 것을 st.session_state에 기록
                        st.session_state.setup_started = True  # 상태 추가

                    # 모델 비교 설정
                    if st.session_state.get('setup_started', False):
                        st.markdown('### 모델 비교')

                        if st.button("모델 비교"):
                            with st.spinner('모델을 비교하는 중...'):
                                # 모델 비교
                                best_model = model.create_models()
                                models_dict = model.get_models()
                                results = model.get_results()
                                st.session_state['models_dict'] = models_dict
                                st.session_state['results'] = results
                                st.session_state['optimization_completed'] = True
                                st.success('모델 비교 완료!')

                    # 모델 선택을 위한 selectbox 생성 (모델 비교가 완료된 경우에만 표시)
                    if st.session_state.get('optimization_completed', False):
                        model_names = list(st.session_state['results'].keys())
                        selected_model = st.selectbox('모델 선택', model_names)

                        # 선택된 모델의 결과 표시
                        if selected_model:
                            st.write(f'##### 결과 - {selected_model} 모델')
                            st.dataframe(st.session_state['results'][selected_model])  # 선택된 모델의 결과 표시

                            st.markdown('### 모델 저장 설정')
                            model_name = st.text_input("저장할 모델의 이름을 입력하세요", f"{selected_model}")
                            save_path = st.text_input("모델을 저장할 경로를 입력하세요", "C:/Users/Desktop")

                            if st.button("모델 저장하기"):
                                with st.spinner('모델을 저장하는 중...'):
                                    models_dict = st.session_state.get('models_dict', {})
                                    if selected_model in models_dict:
                                        model.save_model(selected_model, model_name, save_path)
                                        st.success('모델 저장 완료!')
                                        st.write(f"'{save_path}' 경로에 모델 '{model_name}'이(가) 저장되었습니다.")

        with tab3:
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.markdown('## 🔎 모델 성능 평가')

            # 모델 성능 평가 탭 설명
            st.write('''
                모델 성능 평가는 모델의 성능을 확인하고, 최적의 모델을 선택할 수 있도록 도와줍니다.
            ''')
            if st.session_state.get('optimization_completed', False):
                if 'model_type' in st.session_state:
                    if st.session_state['model_type'] == "분류":
                        # 모델이 '분류'인 경우
                    
                        # 모델 선택
                        model_options = list(st.session_state.get('models_dict', {}).keys())
                        selected_model_name = st.selectbox("분석할 모델 선택", model_options, index=None)  # 기본값 없음

                        if selected_model_name:
                            st.write(f"**{selected_model_name}** 모델을 선택했습니다.")
                            st.write(f"선택 모델 정보: {st.session_state['models_dict'][selected_model_name]}")
                            selected_model = st.session_state['models_dict'][selected_model_name]

                            # Confusion Matrix 생성
                            with st.spinner("Confusion Matrix 생성 중..."):
                                st.markdown('##### Confusion Matrix')
                                st.session_state['model'].visualize_model(selected_model, 'confusion_matrix')

                        # 기타 시각화 유형 선택
                        st.write('\n')
                        st.markdown('##### 성능 시각화')
                        plot_types = ['auc', 'pr', 'calibration', 'lift', 'gain', 'tree']
                        selected_plot = st.selectbox("추가 시각화 유형 선택", plot_types)

                        if st.button("시각화 보기") and selected_model_name:
                            with st.spinner(f"{selected_plot} 시각화 생성 중..."):
                                st.session_state['model'].visualize_model(selected_model, selected_plot)

                        # # 모델 해석
                        # st.write('\n')
                        # st.markdown('##### 모델 해석')
                        # interpret_types = ['summary', 'correlation', 'reason', 'pdp', 'msa', 'pfi']
                        # selected_interpret = st.selectbox("모델 해석 유형 선택", interpret_types)

                        # if st.button("해석 보기") and selected_model_name:
                        #     with st.spinner(f"{selected_interpret} 해석 생성 중..."):
                        #         try:
                        #             shap.initjs()
                        #             plt.figure(figsize=(20,10))
                        #             interpret_result = st.session_state['model'].interpret_model(selected_model, plot = selected_interpret)
                        #             st.pyplot(interpret_result)
                        #         except TypeError as e:
                        #             if "This function only supports tree based models for binary classification" in str(e):
                        #                 st.warning("선택한 모델은 해석 제공이 불가합니다.")
                        #             else:
                        #                 st.error(f"오류 발생: {e}")

                    elif st.session_state['model_type'] == "예측":
                    # 모델이 '예측'인 경우
                        # 모델 선택
                        model_options = list(st.session_state.get('models_dict', {}).keys())
                        selected_model_name = st.selectbox("분석할 모델 선택", model_options, index=None)  # 기본값 없음

                        if selected_model_name:
                            st.write(f"**{selected_model_name}** 모델을 선택했습니다.")
                            st.write(f"선택 모델 정보: {st.session_state['models_dict'][selected_model_name]}")
                            selected_model = st.session_state['models_dict'][selected_model_name]

                            # 기타 시각화 유형 선택
                            st.write('\n')
                            st.markdown('##### 성능 시각화')
                            plot_types = ['residuals', 'error', 'cooks', 'vc', 'rfe', 'learning', 'manifold', 'calibration', 'dimension', 'feature', 'feature_all', 'parameter', 'lift', 'gain', 'tree', 'ks']
                            selected_plot = st.selectbox("추가 시각화 유형 선택", plot_types)

                            if st.button("시각화 보기") and selected_model_name:
                                with st.spinner(f"{selected_plot} 시각화 생성 중..."):
                                    st.session_state['model'].visualize_model(selected_model, selected_plot)

                            # # 모델 해석
                            # st.write('\n')
                            # st.markdown('##### 모델 해석')
                            # interpret_types = ['summary', 'correlation', 'reason', 'shap']
                            # selected_interpret = st.selectbox("모델 해석 유형 선택", interpret_types)

                            # if st.button("해석 보기") and selected_model_name:
                            #     with st.spinner(f"{selected_interpret} 해석 생성 중..."):
                            #         try:
                            #             interpret_result = st.session_state['model'].interpret_model(selected_model, selected_interpret)
                            #             st.pyplot(interpret_result)
                            #         except TypeError as e:
                            #             if "This function only supports tree based models for binary classification" in str(e):
                            #                 st.warning("선택한 모델은 해석 제공이 불가합니다.")
                            #             else:
                            #                 st.error(f"오류 발생: {e}")

                    elif st.session_state['model_type'] == "군집분석":
                        # 모델이 '군집분석'인 경우
                        # 모델 선택
                        model_options = list(st.session_state.get('models_dict', {}).keys())
                        selected_model_name = st.selectbox("분석할 모델 선택", model_options, index=None)

                        if selected_model_name:
                            st.write(f"**{selected_model_name}** 모델을 선택했습니다.")
                            st.write(f"선택 모델 정보: {st.session_state['models_dict'][selected_model_name]}")
                            selected_model = st.session_state['models_dict'][selected_model_name]

                            # 선택한 모델의 할당된 군집 데이터 프레임을 표시하는 부분
                            if 'clustered_data' in st.session_state:
                                st.dataframe(st.session_state['clustered_data'])

                            # 시각화 보기 버튼
                            if st.button("시각화 보기"):
                                with st.spinner('군집 분포 시각화 중...'):
                                    # 모델 시각화 실행
                                    # plot_result = model.plot_model(selected_model, 'cluster')
                                    st.session_state['model'].visualize_model(selected_model, 'distribution')
                                    st.write('\n')

                                    st.session_state['model'].visualize_model(selected_model, 'cluster')
                                    st.write('\n')

                                    st.session_state['model'].visualize_model(selected_model, 'distance')
                                    st.write('\n')

                                    st.session_state['model'].visualize_model(selected_model, 'elbow')
                                    st.write('\n')

                                    st.session_state['model'].visualize_model(selected_model, 'silhouette')
                                    st.write('\n')

                                    # 상세 분석을 위한 상태 표시
                                    st.session_state['visualization_shown'] = True

                            if st.session_state.get('visualization_shown', False):
                                if st.button("군집 상세보기"):
                                    with st.spinner('군집 상세 분석 중...'):
                                        clustered_data_raw = st.session_state.get('clustered_data')

                                        if clustered_data_raw is not None:
                                            cluster_df = pd.DataFrame(clustered_data_raw)

                                            for cluster_id in sorted(cluster_df['Cluster'].unique()):
                                                st.markdown(f"#### Cluster {cluster_id}")

                                                # 수치형 변수 분석
                                                st.markdown("##### 수치형 분석")
                                                col1, col2 = st.columns(2)
                                                with col1:
                                                    numerical_stats, fig_num = Clustering.cluster_analysis_num(cluster_df, cluster_id)
                                                    st.dataframe(numerical_stats)
                                                with col2:
                                                    st.pyplot(fig_num)

                                                # 범주형 변수 분석
                                                st.markdown("##### 범주형 분석")
                                                col1, col2 = st.columns(2)
                                                with col1:
                                                    categorical_stats, figs_cat = Clustering.cluster_analysis_cat(cluster_df, cluster_id)
                                                    for col, stats in categorical_stats.items():
                                                        st.write(f"Distribution of {col} in Cluster {cluster_id}:")
                                                        st.dataframe(stats)
                                                with col2:
                                                    for fig in figs_cat.values():
                                                        st.pyplot(fig)
                                        else:
                                            st.error("군집화된 데이터가 없습니다.")

                                # # 기타 시각화 유형 선택
                                # st.write('\n')
                                # st.markdown('##### 성능 시각화')
                                # plot_types = ['cluster', 'distance', 'distribution']
                                # selected_plot = st.selectbox("시각화 유형 선택", plot_types)

                    elif st.session_state['model_type'] == "시계열":
                    # 모델이 '시계열'인 경우
                        # 모델 선택
                        model_options = list(st.session_state.get('models_dict', {}).keys())
                        selected_model_name = st.selectbox("분석할 모델 선택", model_options, index=None)  # 기본값 없음

                        if selected_model_name:
                            st.write(f"**{selected_model_name}** 모델을 선택했습니다.")
                            st.write(f"선택 모델 정보: {st.session_state['models_dict'][selected_model_name]}")
                            selected_model = st.session_state['models_dict'][selected_model_name]

                            # 시각화 plot 생성
                            with st.spinner("시각화 plot 생성 중..."):
                                st.write('\n')
                                st.markdown('##### 시각화 plot')
                                st.session_state['model'].plot_model(selected_model)

                        # 기타 시각화 유형 선택
                        st.write('\n')
                        st.markdown('##### 성능 시각화')
                        plot_types = ['diff', 'periodogram', 'ccf', 'decomp']
                        selected_plot = st.selectbox("추가 시각화 유형 선택", plot_types)

                        if st.button("시각화 보기") and selected_model_name:
                            with st.spinner(f"{selected_plot} 시각화 생성 중..."):
                                st.session_state['model'].visualize_model(selected_model, selected_plot)

                        st.write('\n')
                        st.markdown('##### 최종 예측')
                        if st.button("예측"):                            
                            if st.session_state.get('exog_vars') is not None and not st.session_state['exog_vars'].empty:
                                # 외생변수가 있는 경우

                                final_model = st.session_state['model'].finalize_model(selected_model)

                                # 예측 수행
                                exog_exps = []
                                exog_models = []

                                from pycaret.time_series import TSForecastingExperiment

                                exog_vars = st.session_state['exog_vars'].columns
                                for exog_var in exog_vars:
                                    exog_exp = TSForecastingExperiment()

                                    exog_exp.setup(
                                        data=st.session_state['exog_vars'],
                                        target=exog_var,
                                        fh=st.session_state['fh'],
                                        numeric_imputation_target=st.session_state['numeric_imputation_target'],
                                        numeric_imputation_exogenous=st.session_state['numeric_imputation_exogenous'],
                                        session_id=st.session_state['session_id'],
                                        verbose=False)
                                    
                                    best = exog_exp.compare_models(
                                        sort="mase",
                                        include=[
                                            "arima",
                                            "ets",
                                            "exp_smooth",
                                            "theta",
                                            "lightgbm_cds_dt",
                                        ],
                                        verbose=False,
                                    )

                                    final_exog_model = exog_exp.finalize_model(best)

                                    exog_exps.append(exog_exp)
                                    exog_models.append(final_exog_model)

                                future_exog = [
                                    exog_exp.predict_model(exog_model)
                                    for exog_exp, exog_model in zip(exog_exps, exog_models)
                                ]

                                future_exog = pd.concat(future_exog, axis=1)
                                future_exog.columns = exog_vars

                                exp_future = TSForecastingExperiment()
                                
                                future_preds = exp_future.predict_model(
                                    final_model,  # 모델 입력
                                    X=future_exog,  # 외생변수 입력
                                    fh=st.session_state['fh'],
                                    round=0
                                )

                                future_preds.index = future_preds.index.to_timestamp()

                                if not future_preds.empty:
                                    st.write(future_preds)
                                    fig = px.line(future_preds, x=future_preds.index, y=future_preds.columns[0])
                                    st.plotly_chart(fig)
                            else:
                                # 외생변수가 없는 경우

                                final_model = st.session_state['model'].finalize_model(selected_model)
                                predictions = st.session_state['model'].predict_model(final_model)
                                predictions.index = predictions.index.to_timestamp()

                                st.write(predictions)

                                # 예측 결과 시각화
                                if not predictions.empty:
                                    fig = px.line(predictions, x=predictions.index, y=predictions.columns[0])
                                    st.plotly_chart(fig)

                    elif st.session_state['model_type'] == "이상치 탐지":
                    # 모델이 '이상치 탐지'인 경우
                        # 모델 선택
                        model_options = list(st.session_state.get('models_dict', {}).keys())
                        selected_model_name = st.selectbox("분석할 모델 선택", model_options, index=None)  # 기본값 없음

                        if selected_model_name:
                            st.write(f"**{selected_model_name}** 모델을 선택했습니다.")
                            st.write(f"선택 모델 정보: {st.session_state['models_dict'][selected_model_name]}")
                            selected_model = st.session_state['models_dict'][selected_model_name]

                            # 기타 시각화 유형 선택
                            st.write('\n')
                            st.markdown('##### 시각화')
                            plot_types = ['tsne','umap']
                            selected_plot = st.selectbox("시각화 유형 선택", plot_types)
                            
                            try:
                                if st.button("시각화 보기") and selected_model_name:
                                    with st.spinner(f"{selected_plot} 시각화 생성 중..."):
                                        st.session_state['model'].visualize_model(selected_model, selected_plot)
                            except Exception:
                                st.write("지원하지 않는 모델입니다.")

            else:
                st.error("모델 비교 및 최적화를 먼저 완료해야 합니다.")

        with tab4:
            st.markdown('## 🪄 모델 활용')
            st.write("여기에서는 선택한 모델을 사용하여 새로운 데이터의 결과를 예측할 수 있습니다.")
            

            # 사용자가 모델 선택
            if 'models_dict' in st.session_state and st.session_state['models_dict']:
                model_options = list(st.session_state['models_dict'].keys())
                selected_model_name = st.selectbox("모델 선택", model_options, index=None)

                if selected_model_name:
                    if 'models_dict' in st.session_state:
                        st.write(f"**{selected_model_name}** 을 선택했습니다.")
                        st.write(f"선택 모델 정보: {st.session_state['models_dict'][selected_model_name]}")

                    selected_model_info = st.session_state['models_dict'][selected_model_name]
                    selected_model = selected_model_info


                    # 예측 방식 선택
                    st.write('\n')
                    st.write('-------------------------------------------------')
                    st.write('##### 예측 방식 선택')
                    predict_option = st.radio("", ("직접 입력", "파일 업로드"))

                    if model_type == "분류":
                        if predict_option == "직접 입력":
                            input_data = {}
                            for col in selected_columns:  # 'selected_columns'를 활용
                                input_data[col] = st.text_input(f"{col} 입력", "0")
                        
                            # 예측 버튼
                            if st.button("예측하기"):
                                # 데이터를 DataFrame으로 변환
                                input_df = pd.DataFrame([input_data])
                                # 예측 수행
                                predictions = st.session_state['model'].predict_data(selected_model, input_df)  # `predict_data` 메서드 사용
                                # 결과 표시
                                st.write(predictions)

                        elif predict_option == "파일 업로드":
                            st.write('\n')
                            st.write('-------------------------------------------------')
                            st.write('##### 예측할 데이터 ')
                            uploaded_file = st.file_uploader("파일 업로드 (CSV, Excel)", type=['csv', 'xlsx'])
                            if uploaded_file:
                                if uploaded_file.name.endswith('.csv'):
                                    df = pd.read_csv(uploaded_file)
                                elif uploaded_file.name.endswith('.xlsx'):
                                    df = pd.read_excel(uploaded_file)

                                # 타겟 데이터 컬럼 삭제
                                if target_column and target_column in df.columns:
                                    df = df.drop(target_column, axis=1)

                                if set(selected_columns) != set(df.columns):
                                    st.write("선택된 컬럼: ", selected_columns)
                                    st.write("파일 컬럼: ", df.columns.tolist())
                                    st.error("학습용 데이터와 동일한 형태의 파일을 제공해주세요.")
                                else:
                                    if st.button("예측하기"):
                                        # 예측 수행
                                        predictions = st.session_state['model'].predict_data(selected_model, data=df)
                                        st.write(predictions)

                    if model_type == "예측":
                        if predict_option == "직접 입력":
                            input_data = {}
                            for col in selected_columns:  # 'selected_columns'를 활용
                                input_data[col] = st.text_input(f"{col} 입력", "0")
                        
                            # 예측 버튼
                            if st.button("예측하기"):
                                # 데이터를 DataFrame으로 변환
                                input_df = pd.DataFrame([input_data])
                                # 예측 수행
                                predictions = st.session_state['model'].predict_data(selected_model, input_df)  # `predict_data` 메서드 사용
                                # 결과 표시
                                st.write(predictions)

                        elif predict_option == "파일 업로드":
                            st.write('\n')
                            st.write('-------------------------------------------------')
                            st.write('##### 예측할 데이터 ')
                            uploaded_file = st.file_uploader("파일 업로드 (CSV, Excel)", type=['csv', 'xlsx'])
                            if uploaded_file:
                                if uploaded_file.name.endswith('.csv'):
                                    df = pd.read_csv(uploaded_file)
                                elif uploaded_file.name.endswith('.xlsx'):
                                    df = pd.read_excel(uploaded_file)

                                # 타겟 데이터 컬럼 삭제
                                if target_column and target_column in df.columns:
                                    df = df.drop(target_column, axis=1)

                                if set(selected_columns) != set(df.columns):
                                    st.write("선택된 컬럼: ", selected_columns)
                                    st.write("파일 컬럼: ", df.columns.tolist())
                                    st.error("학습용 데이터와 동일한 형태의 파일을 제공해주세요.")
                                else:
                                    if st.button("예측하기"):
                                        # 예측 수행
                                        predictions = st.session_state['model'].predict_data(selected_model, data=df)
                                        st.write(predictions)
                        
                    if model_type == "군집분석":
                        if predict_option == "직접 입력":
                            input_data = {}
                            for col in selected_columns:  # 'selected_columns'를 활용
                                input_data[col] = st.text_input(f"{col} 입력", "0")

                            # 예측 버튼
                            if st.button("예측하기"):
                                # 데이터를 DataFrame으로 변환
                                input_df = pd.DataFrame([input_data])
                                # 예측 수행
                                predictions = st.session_state['model'].predict_data(selected_model, input_df)
                                # 결과 표시
                                st.write(predictions)

                        elif predict_option == "파일 업로드":
                            st.write('\n')
                            st.write('-------------------------------------------------')
                            st.write('##### 예측할 데이터 ')
                            uploaded_file = st.file_uploader("파일 업로드 (CSV, Excel)", type=['csv', 'xlsx'])
                            if uploaded_file:
                                if uploaded_file.name.endswith('.csv'):
                                    df = pd.read_csv(uploaded_file)
                                elif uploaded_file.name.endswith('.xlsx'):
                                    df = pd.read_excel(uploaded_file)

                                # 타겟 데이터 컬럼 삭제
                                if target_column and target_column in df.columns:
                                    df = df.drop(target_column, axis=1)

                                if set(selected_columns) != set(df.columns):
                                    st.write("선택된 컬럼: ", selected_columns)
                                    st.write("파일 컬럼: ", df.columns.tolist())
                                    st.error("학습용 데이터와 동일한 형태의 파일을 제공해주세요.")
                                else:
                                    if st.button("예측하기"):
                                        # 예측 수행
                                        predictions = st.session_state['model'].predict_data(selected_model, data=df)
                                        st.write(predictions)

                    if model_type == "시계열":
                        if predict_option == "파일 업로드":
                            st.write('\n')
                            st.write('-------------------------------------------------')
                            st.write('##### 예측할 데이터 ')
                            uploaded_file = st.file_uploader("파일 업로드 (CSV, Excel)", type=['csv', 'xlsx'])
                            if uploaded_file:
                                if uploaded_file.name.endswith('.csv'):
                                    df = pd.read_csv(uploaded_file)
                                elif uploaded_file.name.endswith('.xlsx'):
                                    df = pd.read_excel(uploaded_file)

                                # 인덱스로 사용될 컬럼 선택
                                index_column = st.selectbox("인덱스로 사용할 컬럼 선택", df.columns)
                                # 인덱스 설정
                                df.set_index(index_column, inplace=True)
                                df.index = pd.to_datetime(df.index)

                                if st.button("예측하기"):
                                    final_model = st.session_state['model'].finalize_model(selected_model)
                                    
                                    from pycaret.time_series import TSForecastingExperiment

                                    # 외생변수가 있는 경우
                                    if 'exog_vars' in st.session_state and not st.session_state['exog_vars'].empty:
                                        # 업로드된 데이터에서 외생변수 선택
                                        exog_exps = []
                                        exog_models = []

                                        exog_vars = st.session_state['exog_vars'].columns

                                        for exog_var in exog_vars:
                                            exog_exp = TSForecastingExperiment()

                                        exog_exp.setup(
                                                data=st.session_state['exog_vars'],
                                                target=exog_var,
                                                fh=st.session_state['fh'],
                                                numeric_imputation_target=st.session_state['numeric_imputation_target'],
                                                numeric_imputation_exogenous=st.session_state['numeric_imputation_exogenous'],
                                                session_id=st.session_state['session_id'],
                                                verbose=False
                                            )

                                        best = exog_exp.compare_models(
                                                sort="mase",
                                                include=[
                                                    "arima",
                                                    "ets",
                                                    "exp_smooth",
                                                    "theta",
                                                    "lightgbm_cds_dt",
                                                ],
                                                verbose=False
                                            )
                                        
                                        final_exog_model = exog_exp.finalize_model(best)

                                        exog_exps.append(exog_exp)
                                        exog_models.append(final_exog_model)

                                        future_exog = [
                                            exog_exp.predict_model(exog_model)
                                            for exog_exp, exog_model in zip(exog_exps, exog_models)
                                        ]

                                        future_exog = pd.concat(future_exog, axis=1)
                                        future_exog.columns = exog_vars
                            
                                        exp_future = TSForecastingExperiment()
                                        future_preds = exp_future.predict_model(
                                            final_model,  # 모델 입력
                                            X=future_exog,  # 외생변수 입력
                                            fh=st.session_state['fh'],
                                            round=0
                                        )

                                        future_preds.index = future_preds.index.to_timestamp()
                                        st.write(future_preds)

                                    # 외생변수가 없는 경우
                                    else:
                                        predictions = st.session_state['model'].predict_model(final_model, fh=st.session_state['fh'])
                                        predictions.index = predictions.index.to_timestamp()
                                        st.write(predictions)

                    if model_type == "이상치 탐지":
                        if predict_option == "직접 입력":
                            input_data = {}
                            for col in selected_columns:  # 'selected_columns'를 활용
                                input_data[col] = st.text_input(f"{col} 입력", "0")
                        
                            # 예측 버튼
                            if st.button("예측하기"):
                                # 데이터를 DataFrame으로 변환
                                input_df = pd.DataFrame([input_data])
                                # 예측 수행
                                predictions = st.session_state['model'].predict_data(selected_model, input_df)  # `predict_data` 메서드 사용
                                # 결과 표시
                                st.write(predictions)

                        elif predict_option == "파일 업로드":
                            st.write('\n')
                            st.write('-------------------------------------------------')
                            st.write('##### 예측할 데이터 ')
                            uploaded_file = st.file_uploader("파일 업로드 (CSV, Excel)", type=['csv', 'xlsx'])
                            if uploaded_file:
                                if uploaded_file.name.endswith('.csv'):
                                    df = pd.read_csv(uploaded_file)
                                elif uploaded_file.name.endswith('.xlsx'):
                                    df = pd.read_excel(uploaded_file)

                                # 타겟 데이터 컬럼 삭제
                                if target_column and target_column in df.columns:
                                    df = df.drop(target_column, axis=1)

                                if set(selected_columns) != set(df.columns):
                                    st.write("선택된 컬럼: ", selected_columns)
                                    st.write("파일 컬럼: ", df.columns.tolist())
                                    st.error("학습용 데이터와 동일한 형태의 파일을 제공해주세요.")
                                else:
                                    if st.button("예측하기"):
                                        # 예측 수행
                                        predictions = st.session_state['model'].predict_data(selected_model, data=df)
                                        st.write(predictions)

                                    # # CSV 파일 저장 버튼
                                    # if st.button("CSV 파일로 저장하기"):
                                    #     # CSV 파일로 저장
                                    #     csv = predictions.to_csv(index=False, encoding='utf-8-sig')
                                    #     b64 = base64.b64encode(csv.encode()).decode()  # 문자열로 인코딩
                                    #     href = f'<a href="data:file/csv;base64,{b64}" download="prediction_results.csv">Download CSV file</a>'
                                    #     st.markdown(href, unsafe_allow_html=True)
                                # # 예측 수행
                                # predictions = Classification.predict_data(selected_model, data=df)
                                # # 예측 결과를 원본 데이터프레임에 병합
                                # # df = pd.concat([df, predictions], axis=1)
                                # st.write(predictions)
                                
                                # # CSV 파일로 저장
                                # csv = df.to_csv(index=False, encoding='utf-8-sig')
                                # b64 = base64.b64encode(csv.encode()).decode()  # 문자열로 인코딩
                                # href = f'<a href="data:file/csv;base64,{b64}" download="prediction_results.csv">Download CSV file</a>'
                                # st.markdown(href, unsafe_allow_html=True)
                                
    except UnicodeDecodeError as e:
        st.error("업로드한 파일의 인코딩 형식이 올바르지 않습니다. UTF-8 인코딩 형식으로 파일을 저장해주세요.")
    except ValueError as e:
        if 'The least populated class in y has only 1 member' in str(e).lower():
            st.error('타겟 변수의 클래스가 너무 적습니다. 타겟 변수의 클래스가 2개 이상인지 확인해주세요.')
        else:
            st.error("입력 값이 올바르지 않습니다. 입력 형식을 확인해주세요.")
    except KeyError as e:
        st.error("선택된 컬럼이 없습니다. 컬럼을 선택해주세요.")
    except FileNotFoundError as e:
        st.error("지정된 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    except MemoryError as e:
        st.error("더 작은 데이터셋을 사용해주세요.")
    except ConnectionError as e:
        st.error("네트워크 연결에 문제가 있습니다. 인터넷 연결을 확인하고 다시 시도해주세요.")
    except Exception as e:
        st.error(f'예상치 못한 오류가 발생했습니다: {e} \n \n 화면을 캡쳐하여 Q&A 게시판에 질문을 남겨주세요.')
        
# 로그인 상태에 따라 다른 화면 표시
if not st.session_state['logged_in']:
    login_ui()
else:
    main_app()