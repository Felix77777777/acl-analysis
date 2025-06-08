import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="ACL 病歷分析系統", layout="wide")

# 初始化 Session State 資料表
if 'patients' not in st.session_state:
    st.session_state['patients'] = pd.DataFrame(columns=[
        'patient_id', 'age', 'gender', 'injury_date', 'surgery_date',
        'rehab_duration_weeks', 'return_to_sport', 'knee_stability_score'
    ])

st.title("🏥 ACL 病歷分析系統")

# 區塊 1：輸入病歷
with st.form("add_form"):
    st.subheader("➕ 新增患者資料")
    col1, col2 = st.columns(2)
    with col1:
        pid = st.text_input("患者 ID")
        age = st.number_input("年齡", min_value=0, step=1)
        gender = st.selectbox("性別", ["M", "F"])
        rehab_weeks = st.number_input("復健週數", min_value=0, step=1)
    with col2:
        injury_date = st.date_input("受傷日期", value=date.today())
        surgery_date = st.date_input("手術日期", value=date.today())
        return_sport = st.selectbox("是否回到運動", ["Yes", "No"])
        knee_score = st.slider("膝穩定度分數", 0.0, 100.0, step=0.1)

    submitted = st.form_submit_button("新增資料")
    if submitted:
        new_row = {
            'patient_id': pid,
            'age': age,
            'gender': gender,
            'injury_date': injury_date,
            'surgery_date': surgery_date,
            'rehab_duration_weeks': rehab_weeks,
            'return_to_sport': return_sport,
            'knee_stability_score': knee_score
        }
        st.session_state['patients'] = pd.concat([st.session_state['patients'], pd.DataFrame([new_row])], ignore_index=True)
        st.success("✅ 病歷資料新增成功！")

# 區塊 2：顯示所有資料
st.subheader("📋 所有患者資料")
st.dataframe(st.session_state['patients'], use_container_width=True)

# 區塊 3：統計分析
if not st.session_state['patients'].empty:
    st.subheader("📊 資料統計分析")
    df = st.session_state['patients']
    col1, col2 = st.columns(2)
    with col1:
        st.metric("平均年齡", f"{df['age'].mean():.1f} 歲")
        st.metric("平均復健週數", f"{df['rehab_duration_weeks'].mean():.1f} 週")
    with col2:
        st.metric("回運動人數", f"{(df['return_to_sport'] == 'Yes').sum()} 人")
        st.metric("平均膝穩定度", f"{df['knee_stability_score'].mean():.1f} 分")

# （可選）匯出資料
st.download_button("⬇️ 下載 CSV", data=st.session_state['patients'].to_csv(index=False),
                   file_name="acl_patients.csv", mime="text/csv")
