import streamlit as st
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

st.set_page_config(page_title="ACL 術後康復分析系統", layout="wide")

# 初始化 session_state
if "data" not in st.session_state:
    st.session_state.data = []

# 加入範例資料（僅一次）
if not st.session_state.data:
    st.session_state.data = [
        {
            "ID": "P001", "年齡": 25, "性別": "男", "術側": "左膝", "再次重建": "否",
            "運動類型": "籃球", "身高(cm)": 180, "體重(kg)": 75, "BMI": 23.15,
            "受傷日": date(2024, 1, 1), "手術日": date(2024, 1, 20), "延遲日數": 19,
            "復健週數": 1, "膝穩定度": 50, "IKDC": 45, "股四頭肌力": 40.0,
            "疼痛VAS": 6, "腫脹": "有", "Giveaway": "偶爾", "運動表現": "不佳",
            "臀中肌張力": "不足", "ROM": 80, "MMT": "3",
            "單腳跳比值": 60, "肌力比值": 65, "ACL-RSI": 40,
            "RTS 完成": "否", "RTS 符合": "否", "記錄日期": date(2024, 1, 27)
        },
        {
            "ID": "P001", "年齡": 25, "性別": "男", "術側": "左膝", "再次重建": "否",
            "運動類型": "籃球", "身高(cm)": 180, "體重(kg)": 75, "BMI": 23.15,
            "受傷日": date(2024, 1, 1), "手術日": date(2024, 1, 20), "延遲日數": 19,
            "復健週數": 4, "膝穩定度": 70, "IKDC": 60, "股四頭肌力": 60.0,
            "疼痛VAS": 3, "腫脹": "有", "Giveaway": "偶爾", "運動表現": "普通",
            "臀中肌張力": "正常", "ROM": 110, "MMT": "4",
            "單腳跳比值": 80, "肌力比值": 85, "ACL-RSI": 55,
            "RTS 完成": "是", "RTS 符合": "否", "記錄日期": date(2024, 2, 17)
        },
        {
            "ID": "P001", "年齡": 25, "性別": "男", "術側": "左膝", "再次重建": "否",
            "運動類型": "籃球", "身高(cm)": 180, "體重(kg)": 75, "BMI": 23.15,
            "受傷日": date(2024, 1, 1), "手術日": date(2024, 1, 20), "延遲日數": 19,
            "復健週數": 8, "膝穩定度": 85, "IKDC": 85, "股四頭肌力": 85.0,
            "疼痛VAS": 1, "腫脹": "無", "Giveaway": "無", "運動表現": "優秀",
            "臀中肌張力": "正常", "ROM": 135, "MMT": "5",
            "單腳跳比值": 95, "肌力比值": 95, "ACL-RSI": 80,
            "RTS 完成": "是", "RTS 符合": "是", "記錄日期": date(2024, 3, 15)
        }
    ]

st.title("🦵 ACL 重建術後康復評估系統")

# 輸入欄位
st.header("📋 基本資料")
patient_id = st.text_input("患者 ID")
age = st.number_input("年齡", 10, 100)
sex = st.selectbox("性別", ["男", "女"])
side = st.selectbox("術側", ["左膝", "右膝"])
revision = st.selectbox("是否為再次重建手術", ["否", "是"])

st.header("🏃 術前資訊")
sport_type = st.text_input("術前運動類型")
height = st.number_input("身高 (cm)", 100, 250)
weight = st.number_input("體重 (kg)", 30.0, 200.0)
bmi = round(weight / ((height / 100) ** 2), 2) if height else 0
st.write(f"✅ 自動計算 BMI：{bmi}")

st.header("🩹 術後資訊")
injury_date = st.date_input("受傷日期", value=date(2024, 1, 1))
surgery_date = st.date_input("手術日期", value=date.today())
delay_days = (surgery_date - injury_date).days
st.write(f"📆 手術延遲天數：{delay_days} 天")

st.header("💪 恢復指標")
rehab_weeks = st.number_input("復健週數", 0, 100)
knee_stability = st.slider("膝關節穩定度分數", 0, 100)
ikdc_score = st.slider("IKDC 分數", 0, 100)
quads_strength = st.number_input("股四頭肌肌力（kg）", 0.0, 200.0)
pain_vas = st.slider("術後疼痛指數 (VAS)", 0, 10)
swelling = st.selectbox("膝關節水腫程度", ["無", "輕微", "中度", "重度"])
giveaway = st.selectbox("Giveaway 發生頻率", ["無", "偶爾", "經常"])
performance = st.selectbox("運動表現", ["優秀", "普通", "不佳"])
glute_tone = st.selectbox("臀中肌張力（幗旁肌）", ["正常", "過高", "不足"])
knee_rom = st.number_input("膝關節活動度 ROM（°）", 0, 150)
knee_mmt = st.selectbox("膝關節 MMT 等級", ["0", "1", "2", "3", "4", "5"])

st.header("🏅 RTS（回運動）模組")
hop_test = st.number_input("單腳跳測試左右比值（%）", 0, 150)
strength_ratio = st.number_input("股四頭肌力左右比值（%）", 0, 150)
acl_rsi = st.slider("ACL-RSI 分數", 0, 100)
rts_complete = st.selectbox("是否完成 RTS 測試流程", ["否", "是"])

# RTS 評估
rts_qualified = (hop_test >= 90) and (strength_ratio >= 90) and (acl_rsi >= 65)
if rts_qualified and rts_complete == "是":
    st.success("✅ 建議：符合回運動條件，可進行進階運動訓練。")
else:
    st.warning("⚠️ 尚未符合 RTS 標準，建議繼續復健與追蹤。")

if st.button("✅ 儲存本筆資料"):
    st.session_state.data.append({
        "ID": patient_id,
        "年齡": age,
        "性別": sex,
        "術側": side,
        "再次重建": revision,
        "運動類型": sport_type,
        "身高(cm)": height,
        "體重(kg)": weight,
        "BMI": bmi,
        "受傷日": injury_date,
        "手術日": surgery_date,
        "延遲日數": delay_days,
        "復健週數": rehab_weeks,
        "膝穩定度": knee_stability,
        "IKDC": ikdc_score,
        "股四頭肌力": quads_strength,
        "疼痛VAS": pain_vas,
        "腫脹": swelling,
        "Giveaway": giveaway,
        "運動表現": performance,
        "臀中肌張力": glute_tone,
        "ROM": knee_rom,
        "MMT": knee_mmt,
        "單腳跳比值": hop_test,
        "肌力比值": strength_ratio,
        "ACL-RSI": acl_rsi,
        "RTS 完成": rts_complete,
        "RTS 符合": "是" if rts_qualified and rts_complete == "是" else "否",
        "記錄日期": date.today()
    })
    st.success("資料已儲存 ✅")

st.header("📊 資料總覽與分析")

if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df)

    st.subheader("📈 平均值分析")
    st.write(f"平均 IKDC 分數：{df['IKDC'].mean():.2f}")
    st.write(f"平均股四頭肌肌力：{df['股四頭肌力'].mean():.2f} kg")
    st.write(f"平均 ACL-RSI 分數：{df['ACL-RSI'].mean():.2f}")
    st.write(f"平均 ROM：{df['ROM'].mean():.2f}°")

    st.subheader("✅ RTS 合格率")
    rts_rate = (df["RTS 符合"] == "是").mean() * 100
    st.write(f"RTS 合格比例：{rts_rate:.1f}%")

    st.subheader("⚠️ Giveaway 發生頻率統計")
    st.bar_chart(df["Giveaway"].value_counts())

    st.subheader("📌 性別與 RTS 成功率")
    st.dataframe(pd.crosstab(df["性別"], df["RTS 符合"], normalize='index') * 100)

    st.subheader("📊 個別患者追蹤趨勢圖")
    selected_id = st.selectbox("選擇要查看的患者 ID", df["ID"].unique())
    patient_data = df[df["ID"] == selected_id].sort_values("記錄日期")

    if not patient_data.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(patient_data["記錄日期"], patient_data["IKDC"], label="IKDC")
        ax.plot(patient_data["記錄日期"], patient_data["股四頭肌力"], label="股四頭肌力")
        ax.plot(patient_data["記錄日期"], patient_data["ACL-RSI"], label="ACL-RSI")
        ax.plot(patient_data["記錄日期"], patient_data["ROM"], label="ROM")
        ax.set_ylabel("分數/度數")
        ax.set_title(f"📉 {selected_id} 康復指標趨勢圖")
        ax.legend()
        st.pyplot(fig)

    # 下載資料
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📥 下載所有資料 (CSV)", csv, "ACL_Recovery_Data.csv", "text/csv")
else:
    st.info("尚無儲存資料")
