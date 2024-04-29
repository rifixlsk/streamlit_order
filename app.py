import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="O'slo Archive 주문조회",
    page_icon="./images/아카이브.png"
)

# 데이터 파일 경로
DATA_FILE = "orders.csv"

# 초기 데이터 로드
def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['주문번호', '상품명', '구매자', '전화번호', '금액', '주문상태', '택배사', '운송장번호'])
    return df

# 데이터 저장
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Streamlit 애플리케이션 생성
def main():
    df = load_data()  # 초기 데이터 로드
    
    st.image("./images/1.png")
    st.title(" Check Your Orders ")
    
    # 입력칸 생성
    input_type = st.radio("조회 유형 선택:", ['주문번호', '전화번호'])
    order_input = st.text_input(f"{input_type}를 입력하세요:")
    st.markdown("*※전화번호 입력하실 때 -(하이픈) 입력해 주세요.*")
    
    # 관리자 모드
    admin_phone_number = '01058518570'
    if order_input == admin_phone_number:
        admin_mode = True
    else:
        admin_mode = False
    
    if admin_mode:
        st.title('관리자 모드')
        
        # 관리자 모드에서 주문 데이터 추가
        st.subheader('새로운 주문 데이터 추가')
        new_order_data = {'주문번호': '', '상품명': '', '구매자': '', '전화번호': '', '금액': '', '주문상태': '', '택배사': '', '운송장번호': ''}
        new_order_data['주문번호'] = st.text_input('주문번호')
        new_order_data['상품명'] = st.text_input('상품명')
        new_order_data['구매자'] = st.text_input('구매자')
        new_order_data['전화번호'] = st.text_input('전화번호')
        new_order_data['금액'] = st.text_input('금액')
        new_order_data['주문상태'] = st.radio('주문상태 선택:', ['결제 대기중', '결제 완료', '해외 현지 배송중', '국내로 배송중', '국내 배송중', '배송완료'], index=0)
        if new_order_data['주문상태'] == '국내 배송중':
            new_order_data['택배사'] = st.text_input('택배사')
            new_order_data['운송장번호'] = st.text_input('운송장번호')
        
        if st.button('주문 추가하기'):
            df = pd.concat([df, pd.DataFrame([new_order_data])], ignore_index=True)
            save_data(df)  # 데이터 저장
            st.success('주문이 성공적으로 추가되었습니다.')
        
        # 관리자 모드에서 주문 데이터 리스트 확인, 수정, 삭제
        st.subheader('주문 데이터 리스트')
        
        # 주문 데이터 표시
        st.write(df)
        
        # 주문 데이터 수정
        st.subheader('주문 상태 수정')
        selected_order_index = st.number_input('수정할 주문의 인덱스를 입력하세요:', min_value=0, max_value=len(df)-1)
        selected_order = df.iloc[selected_order_index]
        st.write(selected_order)
        new_order_status = st.radio('새로운 주문상태를 선택하세요:', ['결제 대기중', '결제 완료', '해외 현지 배송중', '국내로 배송중', '국내 배송중', '배송완료'], index=['결제 대기중', '결제 완료', '해외 현지 배송중', '국내로 배송중', '국내 배송중', '배송완료'].index(selected_order['주문상태']))
        if new_order_status != selected_order['주문상태']:
            df.loc[selected_order_index, '주문상태'] = new_order_status
            if new_order_status == '국내 배송중':
                if '택배사' not in df.columns:
                    df['택배사'] = ''
                if '운송장번호' not in df.columns:
                    df['운송장번호'] = ''
                df.loc[selected_order_index, '택배사'] = st.text_input('택배사', value=selected_order.get('택배사', ''))
                df.loc[selected_order_index, '운송장번호'] = st.text_input('운송장번호', value=selected_order.get('운송장번호', ''))
                if st.button('확인'):
                    save_data(df)
                    st.success('주문이 성공적으로 수정되었습니다.')
            else:
                save_data(df)
                st.success('주문이 성공적으로 수정되었습니다.')
        
        # 주문 데이터 삭제
        st.subheader('주문 데이터 삭제')
        selected_order_index_delete = st.number_input('삭제할 주문의 인덱스를 입력하세요:', min_value=0, max_value=len(df)-1)
        if st.button('삭제하기'):
            df = df.drop(index=selected_order_index_delete).reset_index(drop=True)
            save_data(df)
            st.success('주문이 성공적으로 삭제되었습니다.')
                
    else:
        # 일반 사용자 모드
        if st.button('조회하기'):
            if order_input:
                result = df[(df['주문번호'].astype(str) == order_input) | (df['전화번호'] == order_input)]
                if not result.empty:
                    st.write(result)
                else:
                    st.write("해당하는 주문이 없습니다.")
            else:
                st.write("주문번호 또는 전화번호를 입력해주세요.")

if __name__ == '__main__':
    main()
