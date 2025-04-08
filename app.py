import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="구매대행 마진율 계산기(For JM)",
    page_icon="💰",
    layout="wide"
)

# 제목
st.title("💰 구매대행 마진율 계산기")

# 사이드바에 환율 입력
st.sidebar.header("환율 설정")
exchange_rate = st.sidebar.number_input(
    "CNY/원 환율",
    min_value=0.0,
    value=180.0,
    step=0.1,
    format="%.1f"
)

# 메인 컨테이너
col1, col2 = st.columns(2)

with col1:
    st.header("입력")
    
    # 판매 정보
    st.subheader("판매 정보")
    sell_price_won = st.number_input("판매가 (원)", min_value=0, value=89000)
    platform_fee_percent = st.number_input("플랫폼 수수료 (%)", min_value=0.0, value=12.0, step=0.1)
    
    # 상품 정보
    st.subheader("상품 정보")
    item_price_cny = st.number_input("상품가격 (CNY)", min_value=0.0, value=258.0, step=0.1)
    cn_delivery_cny = st.number_input("중국내 배송비 (CNY)", min_value=0.0, value=12.0, step=0.1)
    
    # 배송 정보
    st.subheader("배송 정보")
    intl_base_fee_per_kg = st.number_input("국제배송 단가 (원/kg)", min_value=0, value=8000)
    weight_kg = st.number_input("실중량 (kg)", min_value=0.0, value=1.2, step=0.1)
    local_delivery_won = st.number_input("국내배송비 (원)", min_value=0, value=3000)
    
    # 박스 크기
    st.subheader("박스 크기 (cm)")
    col_size1, col_size2, col_size3 = st.columns(3)
    with col_size1:
        length_cm = st.number_input("가로", min_value=0.0, value=30.0, step=0.1)
    with col_size2:
        width_cm = st.number_input("세로", min_value=0.0, value=25.0, step=0.1)
    with col_size3:
        height_cm = st.number_input("높이", min_value=0.0, value=15.0, step=0.1)

with col2:
    st.header("계산 결과")
    
    # 부피무게 계산
    volumetric_weight = (length_cm * width_cm * height_cm) / 6000
    shipping_weight = max(weight_kg, volumetric_weight)
    
    # 비용 계산
    item_total_cny = item_price_cny + cn_delivery_cny
    item_total_won = item_total_cny * exchange_rate
    intl_shipping_won = shipping_weight * intl_base_fee_per_kg
    total_cost = item_total_won + intl_shipping_won + local_delivery_won
    platform_fee = sell_price_won * (platform_fee_percent / 100)
    final_cost = total_cost + platform_fee
    
    # 이익 계산
    profit = sell_price_won - final_cost
    margin_rate = (profit / sell_price_won) * 100
    
    # 결과 표시
    st.metric("환율", f"{exchange_rate:,.1f} 원/CNY")
    st.metric("부피무게", f"{volumetric_weight:.2f} kg")
    st.metric("적용무게", f"{shipping_weight:.2f} kg")
    st.metric("총비용", f"{final_cost:,.0f} 원")
    st.metric("플랫폼 수수료", f"{platform_fee:,.0f} 원")
    st.metric("순이익", f"{profit:,.0f} 원")
    
    # 마진율 표시
    if margin_rate >= 0:
        st.success(f"마진율: {margin_rate:.1f}%")
    else:
        st.error(f"마진율: {margin_rate:.1f}%")
    
    # 상세 비용 내역
    st.subheader("상세 비용 내역")
    cost_details = pd.DataFrame({
        "항목": ["상품가격", "중국내 배송비", "국제배송비", "국내배송비", "플랫폼 수수료", "총비용"],
        "금액(원)": [
            f"{item_total_won:,.0f}",
            f"{cn_delivery_cny * exchange_rate:,.0f}",
            f"{intl_shipping_won:,.0f}",
            f"{local_delivery_won:,.0f}",
            f"{platform_fee:,.0f}",
            f"{final_cost:,.0f}"
        ]
    })
    st.table(cost_details)

# 푸터
st.markdown("---")
st.markdown("© 2025 구매대행 마진율 계산기") 
