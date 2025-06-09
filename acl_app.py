import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="ACL 術後康復分析系統", layout="wide")

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
ikdc_score = st.slider("IKDC 分數", 0, 100)
quads_strength = st.number_input("股四頭肌肌力（kg）", 0.0, 200.0)
pain_vas = st.slider("術後疼痛指數 (VAS)", 0, 10)
swelling = st.selectbox("膝關節是否水腫", ["無", "輕微", "中度", "嚴重"])
giveaway = st.text_input("Giveaway 發生頻率（自由輸入）")
performance = st.selectbox("運動表現主觀評價", ["優秀", "普通", "不佳"])
hamstring_tightness = st.selectbox("Hamstring 肌肉張力", ["正常", "輕度緊繃", "中度緊繃", "嚴重緊繃"])
knee_rom = st.number_input("膝關節活動度 ROM（°）", 0, 150)
knee_mmt = st.selectbox("膝關節 MMT 等級", ["0", "1", "2", "3", "4", "5"])

st.header("🏅 運動表現（Hop Tests 比值計算）")

def calc_ratio(right, left):
    return round((right / left) * 100, 1) if left else 0

# 輸入 + 自動比值
left_single = st.number_input("單腳跳遠（左腳 cm）", 0.0, 500.0)
right_single = st.number_input("單腳跳遠（右腳 cm）", 0.0, 500.0)
ratio_single = calc_ratio(right_single, left_single)
st.write(f"👉 單腳跳遠比值（右/左）：{ratio_single}%")

left_triple = st.number_input("三級跳遠（左腳 cm）", 0.0, 1000.0)
right_triple = st.number_input("三級跳遠（右腳 cm）", 0.0, 1000.0)
ratio_triple = calc_ratio(right_triple, left_triple)
st.write(f"👉 三級跳遠比值（右/左）：{ratio_triple}%")

left_crossover = st.number_input("交叉跳遠（左腳 cm）", 0.0, 1000.0)
right_crossover = st.number_input("交叉跳遠（右腳 cm）", 0.0, 1000.0)
ratio_crossover = calc_ratio(right_crossover, left_crossover)
st.write(f"👉 交叉跳遠比值（右/左）：{ratio_crossover}%")

left_timed = st.number_input("6 公尺計時跳（左腳 sec）", 0.0, 20.0)
right_timed = st.number_input("6 公尺計時跳（右腳 sec）", 0.0, 20.0)
ratio_timed = calc_ratio(left_timed, right_timed)  # 小於 100 表現較佳
st.write(f"👉 6 公尺跳比值（左/右時間）：{ratio_timed}%")

st.header("📈 RTS 模組")
hop_test = st.number_input("單腳跳測試總比值（%）", 0, 150)
strength_ratio = st.number_input("股四頭肌力左右比值（%）", 0, 150)
acl_rsi = st.slider("ACL-RSI 分數", 0, 100)
rts_complete = st.selectbox("是否完成 RTS 測試流程", ["否", "是"])
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
        "IKDC": ikdc_score,
        "股四頭肌力": quads_strength,
        "疼痛VAS": pain_vas,
        "水腫": swelling,
        "Giveaway": giveaway,
        "運動表現": performance,
        "Hamstring張力": hamstring_tightness,
        "ROM": knee_rom,
        "MMT": knee_mmt,
        "單腳跳遠比值": ratio_single,
        "三級跳遠比值": ratio_triple,
        "交叉跳遠比值": ratio_crossover,
        "6公尺跳比值": ratio_timed,
        "單腳跳總比值": hop_test,
        "肌力比值": strength_ratio,
        "ACL-RSI": acl_rsi,
        "RTS 完成": rts_complete,
        "RTS 符合": "是" if rts_qualified and rts_complete == "是" else "否"
    })
    st.success("資料已儲存 ✅")

st.header("📊 資料總覽與分析")
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df)

    st.subheader("📈 資料分析")
    st.write(f"平均 IKDC：{df['IKDC'].mean():.2f}")
    st.write(f"平均股四頭肌力：{df['股四頭肌力'].mean():.2f} kg")
    st.write(f"平均 ACL-RSI：{df['ACL-RSI'].mean():.2f}")
    st.write(f"平均 ROM：{df['ROM'].mean():.2f}°")
    st.write(f"RTS 合格率：{(df['RTS 符合'] == '是').mean() * 100:.1f}%")

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📥 下載資料 (CSV)", csv, "ACL_Recovery.csv", "text/csv")
else:
    st.info("尚無資料")
