import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="ACL 術後康復分析系統", layout="wide")

# 初始化 session_state 儲存資料
if "data" not in st.session_state:
    st.session_state.data = []

st.title("🦵 ACL 重建術後康復評估系統")

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
swelling = st.selectbox("膝關節是否腫脹", ["無", "有"])
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

# 評估 RTS 是否達標
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
        "RTS 符合": "是" if rts_qualified and rts_complete == "是" else "否"
    })
    st.success("資料已儲存 ✅")

st.header("📊 資料總覽與下載")

if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df)
    st.header("📈 資料分析報告")

    # 平均值計算
    st.subheader("📊 平均值統計")
    st.write(f"平均 IKDC 分數：{df['IKDC'].mean():.2f}")
    st.write(f"平均股四頭肌肌力：{df['股四頭肌力'].mean():.2f} kg")
    st.write(f"平均 ACL-RSI 分數：{df['ACL-RSI'].mean():.2f}")
    st.write(f"平均 ROM：{df['ROM'].mean():.2f}°")

    # RTS 符合率
    st.subheader("✅ RTS 合格分析")
    rts_rate = (df["RTS 符合"] == "是").mean() * 100
    st.write(f"RTS 合格比例：{rts_rate:.1f}%")

    # Giveaway 發生頻率統計
    st.subheader("⚠️ Giveaway 發生頻率")
    giveaway_counts = df["Giveaway"].value_counts()
    st.bar_chart(giveaway_counts)

    # 性別與 RTS 比例交叉比對
    st.subheader("📌 性別與 RTS 成功比率")
    gender_rts = pd.crosstab(df["性別"], df["RTS 符合"], normalize='index') * 100
    st.dataframe(gender_rts.round(1))
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📥 下載所有資料 (CSV)", csv, "ACL_Recovery_Data.csv", "text/csv")
else:
    st.info("尚無儲存資料")
