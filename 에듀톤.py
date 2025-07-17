import json
import os
import datetime
import random
import streamlit as st

# --- 1. 데이터 정의 (Data Definitions) ---

# 쓰레기 종류 다국어 버전
waste_data = {
    "plastic_bottle": {
        "names": {"ko": "플라스틱 병", "en": "plastic bottle", "zh": "塑料瓶"},
        "co2_per_kg": 6.0,
        "decompose_years": 450,
        "eco_alternative": {
            "ko": "텀블러를 사용하세요",
            "en": "Use a tumbler",
            "zh": "使用保温杯"
        },
        "unit": {"ko": "병", "en": "bottle", "zh": "瓶"},
        "unit_weight": 0.02
    },
    "food_waste": {
        "names": {"ko": "음식물 쓰레기", "en": "food waste", "zh": "厨余垃圾"},
        "co2_per_kg": 0.5,
        "decompose_months": 1,
        "eco_alternative": {
            "ko": "남기지 말고 적당량만 요리하세요",
            "en": "Cook just the right amount and don't leave leftovers",
            "zh": "适量烹饪，避免浪费"
        },
        "unit": {"ko": "인분", "en": "servings", "zh": "份"},
        "unit_weight": 0.3
    },
    "paper": {
        "names": {"ko": "종이", "en": "paper", "zh": "纸"},
        "co2_per_kg": 1.0,
        "decompose_weeks": 4,
        "eco_alternative": {
            "ko": "전자문서나 양면 인쇄를 사용하세요",
            "en": "Use electronic documents or double-sided printing",
            "zh": "使用电子文件或双面打印"
        },
        "unit": {"ko": "장", "en": "piece", "zh": "张"},
        "unit_weight": 0.005
    },
    "aluminum_can": {
        "names": {"ko": "알루미늄 캔", "en": "aluminum can", "zh": "铝罐"},
        "co2_per_kg": 10.0,
        "decompose_years": 200,
        "eco_alternative": {"ko": "재사용 가능한 물병을 사용하세요", "en": "Use a reusable water bottle", "zh": "请使用可重复使用的水瓶"},
        "unit": {"ko": "개", "en": "can", "zh": "个"},
        "unit_weight": 0.015
    },
    "cigarette": {
        "names": {"ko": "담배꽁초", "en": "cigarette butt" , "zh": "烟蒂"},
        "co2_per_kg": 3.0,
        "decompose_years": 12,
        "eco_alternative": {"ko": "금연하거나 친환경 필터를 사용하세요", "en": "Quit smoking or use eco-friendly filters", "zh": "戒烟或使用环保滤嘴"},
        "unit": {"ko": "개비", "en": "cigarette", "zh": "根"},
        "unit_weight": 0.001
    },
    "disposable_cup": {
        "names": {"ko": "일회용 컵", "en": "disposable cup", "zh": "一次性杯子"},
        "co2_per_kg": 4.0,
        "decompose_years": 450,
        "eco_alternative": {"ko": "텀블러나 머그컵을 사용하세요", "en": "Use a tumbler or mug", "zh": "请使用随行杯或马克杯"},
        "unit": {"ko": "개", "en": "cup", "zh": "个"},
        "unit_weight": 0.01
    },
    "plastic_bag": {
        "names": {"ko": "비닐봉지", "en": "plastic bag", "zh": "塑料袋"},
        "co2_per_kg": 6.0,
        "decompose_years": 1000,
        "eco_alternative": {"ko": "장바구니를 사용하세요", "en": "Use a shopping bag", "zh": "请使用购物袋"},
        "unit": {"ko": "봉지", "en": "bag", "zh": "袋"},
        "unit_weight": 0.005
    },
    "paper_cup": {
        "names": {"ko": "종이컵", "en": "paper cup" , "zh": "纸杯"},
        "co2_per_kg": 1.2,
        "decompose_years": 20,
        "eco_alternative": {"ko": "세척 가능한 컵을 사용하세요", "en": "Use a washable cup", "zh": "请使用可清洗的杯子"},
        "unit": {"ko": "컵", "en": "cup", "zh": "个"},
        "unit_weight": 0.012
    },
    "glass_bottle": {
        "names": {"ko": "유리병", "en": "glass bottle" , "zh": "玻璃瓶"},
        "co2_per_kg": 1.5,
        "decompose_years": 1000000,
        "eco_alternative": {"ko": "리필 스테이션을 이용하세요", "en": "Use refill stations", "zh": "请使用补充站"},
        "unit": {"ko": "개", "en": "bottle", "zh": "个"},
        "unit_weight": 0.4
    },
    "tissue": {
        "names": {"ko": "휴지", "en": "tissue", "zh": "纸巾"},
        "co2_per_kg": 0.6,
        "decompose_weeks": 3,
        "eco_alternative": {"ko": "손수건을 사용하세요", "en": "Use a handkerchief", "zh": "请使用手帕"},
        "unit": {"ko": "개", "en": "piece", "zh": "张"},
        "unit_weight": 0.005
    },
    "paper_pack": {
        "names": {"ko": "종이팩", "en": "paper pack", "zh": "纸盒"},
        "co2_per_kg": 1.1,
        "decompose_years": 5,
        "eco_alternative": {"ko": "리필팩을 사용하거나 재활용하세요", "en": "Use refill packs or recycle", "zh": "请使用补充装或回收利用"},
        "unit": {"ko": "개", "en": "pack", "zh": "个"},
        "unit_weight": 0.03
    }
}

# 다국어 메시지
messages = {
    "ko": {
        "welcome": "🌿 환경을 위한 작은 실천, 시작합니다!",
        "select_menu": "메뉴를 선택하세요:",
        "goodbye": "👋 이용해 주셔서 감사합니다!",
        "invalid_number": "❌ 숫자를 입력해주세요.",
        "invalid_menu": "❌ 올바른 메뉴 번호를 선택해주세요.",
        "input_count": "몇 {unit}를 버렸나요? ",
        "daily_target_prompt": "하루 CO₂ 배출 목표(kg)를 입력하세요: ",
        "target_set": "✅ 목표가 설정되었습니다.",
        "over_target": "⚠️ 설정한 목표({target} kg)를 초과했습니다!",
        "available_waste_types": "가능한 쓰레기 종류:",
        "enter_waste_type": "쓰레기 종류를 선택하세요:",
        "waste_not_registered": "❌ 등록되지 않은 쓰레기 종류입니다.",
        "enter_positive_number": "❌ 0 이상의 숫자를 입력하세요.",
        "today_co2_emission": "오늘 누적 CO₂ 배출량:",
        "today_score": "오늘 점수:",
        "result_title": "📊 결과",
        "name_label": "-",
        "weight_label": "- 무게:",
        "co2_emitted_label": "- 배출된 CO₂:",
        "decompose_time_label": "- 분해 시간:",
        "eco_tip_label": "- 🌱 친환경 대안:",
        "select_language_title": "🌐 언어를 선택하세요:",
        "lang_ko": "한국어",
        "lang_en": "영어",
        "lang_zh": "중국어",
        "invalid_language_choice": "❌ 잘못된 선택입니다. 기본값: 한국어로 설정됩니다.",
        "add_waste_button": "쓰레기 입력",
        "set_target_button": "목표 설정"
    },
    "en": {
        "welcome": "🌿 Let's start a small action for the environment!",
        "select_menu": "Select menu:",
        "goodbye": "👋 Thank you for using!",
        "invalid_number": "❌ Please enter a number.",
        "invalid_menu": "❌ Invalid menu number.",
        "input_count": "How many {unit}? ",
        "daily_target_prompt": "Enter daily CO₂ target (kg): ",
        "target_set": "✅ Target set.",
        "over_target": "⚠️ Over daily target ({target} kg)!",
        "available_waste_types": "Available waste types:",
        "enter_waste_type": "Select waste type:",
        "waste_not_registered": "❌ Not registered waste type.",
        "enter_positive_number": "❌ Enter a number >= 0.",
        "today_co2_emission": "Today's CO₂ Emissions:",
        "today_score": "Score:",
        "result_title": "📊 Result",
        "name_label": "-",
        "weight_label": "- Weight:",
        "co2_emitted_label": "- CO₂ Emitted:",
        "decompose_time_label": "- Decompose Time:",
        "eco_tip_label": "- 🌱 Eco Tip:",
        "select_language_title": "🌐 Select language:",
        "lang_ko": "Korean",
        "lang_en": "English",
        "lang_zh": "Chinese",
        "invalid_language_choice": "❌ Invalid choice. Default: Korean will be set.",
        "add_waste_button": "Add Waste",
        "set_target_button": "Set Target"
    },
    "zh": {
        "welcome": "🌿 开始为环境做一点小改变吧！",
        "select_menu": "请选择菜单:",
        "goodbye": "👋 感谢您的使用！",
        "invalid_number": "❌ 请输入数字。",
        "invalid_menu": "❌ 菜单编号无效。",
        "input_count": "多少{unit}？",
        "daily_target_prompt": "请输入每日CO₂排放目标(公斤): ",
        "target_set": "✅ 目标已设置。",
        "over_target": "⚠️ 超过每日目标({target}公斤)！",
        "available_waste_types": "可用垃圾种类:",
        "enter_waste_type": "请选择垃圾类型:",
        "waste_not_registered": "❌ 未注册垃圾类型。",
        "enter_positive_number": "❌ 输入大于等于0的数字。",
        "today_co2_emission": "今日累计CO₂排放量:",
        "today_score": "分数:",
        "result_title": "📊 结果",
        "name_label": "-",
        "weight_label": "- 重量:",
        "co2_emitted_label": "- 排放的 CO₂:",
        "decompose_time_label": "- 分解时间:",
        "eco_tip_label": "- 🌱 环保建议:",
        "select_language_title": "🌐 选择语言:",
        "lang_ko": "韩语",
        "lang_en": "英语",
        "lang_zh": "中文",
        "invalid_language_choice": "❌ 选择无效。默认：将设置为韩语。",
        "add_waste_button": "添加垃圾",
        "set_target_button": "设置目标"
    }
}

# 환경 관련 명언 (NameError 해결을 위해 전역 범위에 정의)
eco_quotes = [
    "The Earth is what we all have in common. - Wendell Berry",
    "작은 변화가 큰 변화를 만듭니다.",
    "지구는 우리가 물려받은 것이 아니라, 빌려온 것입니다.",
    "There is no Planet B.",
    "One planet, one chance."
]

# --- 2. 파일 경로 및 세션 상태 관리 (File Paths & Session State) ---

# 파일 경로 (Streamlit Cloud에서는 로컬 파일 시스템이 임시적이므로 데이터 지속성을 위한 다른 방안 고려 필요)
# 여기서는 예시를 위해 현재 디렉토리에 저장하도록 함. 실제 서비스에서는 DB 연동 고려.
history_file = "waste_history.json"
settings_file = "settings.json"

# Streamlit 세션을 사용하여 언어 설정 유지
if 'current_language' not in st.session_state:
    st.session_state.current_language = "ko" # 기본값

# --- 3. 데이터 로드/저장 함수 (Data Load/Save Functions) ---

def load_history():
    """쓰레기 배출 기록을 JSON 파일에서 로드합니다."""
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    """쓰레기 배출 기록을 JSON 파일에 저장합니다."""
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def load_settings():
    """설정 데이터를 JSON 파일에서 로드합니다."""
    if os.path.exists(settings_file):
        with open(settings_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"daily_target": None}

def save_settings(settings):
    """설정 데이터를 JSON 파일에 저장합니다."""
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)

# --- 4. 핵심 로직 함수 (Core Logic Functions) ---

def calculate_impact(waste_key, count):
    """
    쓰레기 종류와 수량을 바탕으로 CO2 배출량 및 분해 시간 등을 계산합니다.
    """
    data = waste_data[waste_key]
    weight_kg = count * data["unit_weight"]
    co2 = weight_kg * data["co2_per_kg"]

    decompose_time_str = ""
    if "decompose_years" in data:
        decompose_time_str = f"{data['decompose_years']}년" if st.session_state.current_language == "ko" else \
                             f"{data['decompose_years']} years" if st.session_state.current_language == "en" else \
                             f"{data['decompose_years']}年"
    elif "decompose_months" in data:
        decompose_time_str = f"{data['decompose_months']}개월" if st.session_state.current_language == "ko" else \
                             f"{data['decompose_months']} months" if st.session_state.current_language == "en" else \
                             f"{data['decompose_months']}个月"
    elif "decompose_weeks" in data:
        decompose_time_str = f"{data['decompose_weeks']}주" if st.session_state.current_language == "ko" else \
                             f"{data['decompose_weeks']} weeks" if st.session_state.current_language == "en" else \
                             f"{data['decompose_weeks']}周"

    return {
        "waste_key": waste_key,
        "count": count,
        "unit": data["unit"][st.session_state.current_language],
        "weight_kg": weight_kg,
        "co2_emitted": co2,
        "decompose_time": decompose_time_str,
        "eco_tip": data["eco_alternative"][st.session_state.current_language],
        "date": datetime.datetime.today().strftime("%Y-%m-%d")
    }

def show_result(result):
    """계산된 쓰레기 배출 결과를 Streamlit에 표시합니다."""
    lang = st.session_state.current_language
    name = waste_data[result['waste_key']]['names'][lang]
    count = result['count']
    unit = result['unit']
    weight = result['weight_kg']
    co2 = result['co2_emitted']
    decompose = result['decompose_time']
    eco_tip = result['eco_tip']

    st.subheader(messages[lang]["result_title"])
    st.markdown(f"**{messages[lang]['name_label']}** {name}: {count} {unit}")
    st.markdown(f"**{messages[lang]['weight_label']}** {weight:.3f} kg")
    st.markdown(f"**{messages[lang]['co2_emitted_label']}** {co2:.2f} kg")
    st.markdown(f"**{messages[lang]['decompose_time_label']}** {decompose}")
    st.info(f"**{messages[lang]['eco_tip_label']}** {eco_tip}")

def get_today_co2_and_score(history):
    """오늘의 총 CO2 배출량과 환경 점수를 계산합니다."""
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    today_records = [r for r in history if r["date"] == today]
    total_co2 = sum(r["co2_emitted"] for r in today_records)
    # 점수 계산: CO2 배출량이 0이면 100점, 20kg이면 0점 (CO2 1kg당 5점 감점)
    eco_score = max(0, 100 - total_co2 * 5)
    return total_co2, eco_score

# --- 5. Streamlit UI 구성 함수 (Streamlit UI Functions) ---

def select_language_ui():
    """언어 선택 드롭다운을 사이드바에 표시합니다."""
    lang_options = {
        "ko": messages["ko"]["lang_ko"],
        "en": messages["en"]["lang_en"],
        "zh": messages["zh"]["lang_zh"]
    }
    
    # 현재 설정된 언어에 따라 selectbox의 기본값 설정
    current_lang_display = lang_options[st.session_state.current_language]
    
    selected_lang_name = st.sidebar.selectbox(
        messages[st.session_state.current_language]["select_language_title"],
        options=list(lang_options.values()),
        index=list(lang_options.values()).index(current_lang_display),
        key="language_selector"
    )
    
    # 선택된 언어에 따라 세션 상태 업데이트
    for key, value in lang_options.items():
        if value == selected_lang_name:
            st.session_state.current_language = key
            break

def display_today_stats(history, settings):
    """오늘의 CO2 배출량과 점수를 표시합니다."""
    lang = st.session_state.current_language
    today_co2, eco_score = get_today_co2_and_score(history)
    
    st.header(messages[lang]["today_co2_emission"].replace(':', ''))
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=messages[lang]["today_co2_emission"], value=f"{today_co2:.2f} kg")
    with col2:
        st.metric(label=messages[lang]["today_score"], value=f"{eco_score:.1f} / 100")

    if settings.get("daily_target") and today_co2 > settings["daily_target"]:
        st.warning(messages[lang]["over_target"].format(target=settings["daily_target"]))

# --- 6. 메인 애플리케이션 로직 (Main Application Logic) ---

def main():
    """Streamlit 애플리케이션의 메인 함수."""
    # 페이지 기본 설정
    st.set_page_config(layout="centered", page_title="Eco Tracker")
    
    # 언어 선택 UI (사이드바)
    select_language_ui()
    
    # 앱 제목 및 랜덤 명언 표시
    st.title(messages[st.session_state.current_language]["welcome"])
    st.markdown(f"*{random.choice(eco_quotes)}*") # 명언을 이탤릭체로 표시

    history = load_history()
    settings = load_settings()

    # 사이드바 메뉴 옵션
    menu_options = [
        messages[st.session_state.current_language]["add_waste_button"],
        messages[st.session_state.current_language]["today_co2_emission"].replace(':', ''), # '오늘 누적 CO₂ 배출량'
        messages[st.session_state.current_language]["set_target_button"]
    ]
    
    choice = st.sidebar.radio(
        messages[st.session_state.current_language]["select_menu"],
        menu_options
    )

    # --- 메뉴별 화면 구성 ---

    if choice == menu_options[0]: # 쓰레기 입력 / Add Waste / 添加垃圾
        st.header(messages[st.session_state.current_language]["available_waste_types"])
        
        # 쓰레기 종류 드롭다운 선택
        waste_names_for_select = [data['names'][st.session_state.current_language] for data in waste_data.values()]
        selected_waste_name = st.selectbox(
            messages[st.session_state.current_language]["enter_waste_type"],
            options=waste_names_for_select,
            key="waste_type_selector"
        )

        waste_key = None
        for k, v in waste_data.items():
            if selected_waste_name == v["names"][st.session_state.current_language]:
                waste_key = k
                break

        if waste_key:
            # 수량 입력 (number_input 사용)
            count = st.number_input(
                messages[st.session_state.current_language]["input_count"].format(unit=waste_data[waste_key]["unit"][st.session_state.current_language]),
                min_value=0.0,
                value=1.0,
                step=0.1,
                format="%.1f", # 소수점 한자리까지 표시
                key="waste_count_input"
            )
            
            # 쓰레기 입력 버튼
            if st.button(messages[st.session_state.current_language]["add_waste_button"]):
                if count < 0: # 음수 입력 방지 (min_value로 이미 방지되지만, 명시적 확인)
                    st.error(messages[st.session_state.current_language]["enter_positive_number"])
                else:
                    result = calculate_impact(waste_key, count)
                    history.append(result)
                    save_history(history)
                    show_result(result)
                    st.success("✅ " + selected_waste_name + " " + str(count) + " " + waste_data[waste_key]["unit"][st.session_state.current_language] + " " + ("입력 완료!" if st.session_state.current_language == "ko" else "added!"))

                    # 입력 후 오늘의 통계 업데이트 표시
                    display_today_stats(history, settings)
        else:
            st.error(messages[st.session_state.current_language]["waste_not_registered"])

    elif choice == menu_options[1]: # 오늘 배출량 및 점수 확인 / View today's emissions and score / 查看今日排放量和分数
        display_today_stats(history, settings)

    elif choice == menu_options[2]: # 하루 목표 설정 / Set daily target / 设置每日目标
        st.header(messages[st.session_state.current_language]["daily_target_prompt"].replace(':', ''))
        
        # 현재 설정된 목표를 기본값으로 표시
        current_target = settings.get("daily_target")
        target_value = float(current_target) if current_target is not None else 0.0

        target = st.number_input(
            messages[st.session_state.current_language]["daily_target_prompt"],
            min_value=0.0,
            value=target_value,
            step=0.1,
            format="%.2f",
            key="daily_target_input"
        )
        if st.button(messages[st.session_state.current_language]["set_target_button"]):
            settings["daily_target"] = target
            save_settings(settings)
            st.success(messages[st.session_state.current_language]["target_set"])
            # 목표 설정 후 오늘의 통계 업데이트 표시 (선택 사항)
            display_today_stats(history, settings)

# --- 7. 앱 실행 (Run App) ---

if __name__ == "__main__":
    main()
