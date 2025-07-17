import json
import os
import datetime
import random
import streamlit as st

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

# 파일 경로 (Streamlit Cloud에서는 로컬 파일 시스템이 임시적이므로 데이터 지속성을 위한 다른 방안 고려 필요)
# 여기서는 예시를 위해 현재 디렉토리에 저장하도록 함. 실제 서비스에서는 DB 연동 고려.
history_file = "waste_history.json"
settings_file = "settings.json"

messages = {
    "ko": {
        "welcome": "🌿 환경을 위한 작은 실천, 시작합니다!",
        "select_menu": "\n1. 쓰레기 입력\n2. 오늘 배출량 및 점수 확인\n3. 하루 목표 설정\n4. 종료\n선택하세요: ",
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
        "invalid_language_choice": "❌ 잘못된 선택입니다. 기본값: 한국어로 설정됩니다."
    },
    "en": {
        "welcome": "🌿 Let's start a small action for the environment!",
        "select_menu": "\n1. Enter waste\n2. View today's emissions and score\n3. Set daily target\n4. Exit\nChoose: ",
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
        "invalid_language_choice": "❌ Invalid choice. Default: Korean will be set."
    },
    "zh": {
        "welcome": "🌿 开始为环境做一点小改变吧！",
        "select_menu": "\n1. 输入垃圾\n2. 查看今日排放量和分数\n3. 设置每日目标\n4. 退出\n请选择: ",
        "goodbye": "👋 感谢您的使用！",
        "invalid_number": "❌ 请输入数字。",
        "invalid_menu": "❌ 菜单编号无效。",
        "input_count": "多少{unit}？",
        "daily_target_prompt": "请输入每日CO₂排放目标(公斤): ",
        "target_set": "✅ 目标已设置。",
        "over_target": "⚠️ 超过每日目标({target}公斤)！",
        "available_waste_types": "可用垃圾种类:",
        "enter_waste_type": "请输入垃圾类型:", # Changed from "选择" to "输入" for text input
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
        "invalid_language_choice": "❌ 选择无效。默认：将设置为韩语。"
    }
}

# Streamlit 세션을 사용하여 언어 설정 유지
if 'current_language' not in st.session_state:
    st.session_state.current_language = "ko" # 기본값

def load_history():
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"daily_target": None}

def save_settings(settings):
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)

def calculate_impact(waste_key, count):
    data = waste_data[waste_key]
    weight_kg = count * data["unit_weight"]
    co2 = weight_kg * data["co2_per_kg"]

    decompose = ""
    if "decompose_years" in data:
        decompose = f"{data['decompose_years']}년" if st.session_state.current_language == "ko" else \
                    f"{data['decompose_years']} years" if st.session_state.current_language == "en" else \
                    f"{data['decompose_years']}年"
    elif "decompose_months" in data:
        decompose = f"{data['decompose_months']}개월" if st.session_state.current_language == "ko" else \
                    f"{data['decompose_months']} months" if st.session_state.current_language == "en" else \
                    f"{data['decompose_months']}个月"
    elif "decompose_weeks" in data:
        decompose = f"{data['decompose_weeks']}주" if st.session_state.current_language == "ko" else \
                    f"{data['decompose_weeks']} weeks" if st.session_state.current_language == "en" else \
                    f"{data['decompose_weeks']}周"

    return {
        "waste_key": waste_key,
        "count": count,
        "unit": data["unit"][st.session_state.current_language],
        "weight_kg": weight_kg,
        "co2_emitted": co2,
        "decompose_time": decompose,
        "eco_tip": data["eco_alternative"][st.session_state.current_language],
        "date": datetime.datetime.today().strftime("%Y-%m-%d")
    }

def show_result(result):
    lang = st.session_state.current_language
    name = waste_data[result['waste_key']]['names'][lang]
    count = result['count']
    unit = result['unit']
    weight = result['weight_kg']
    co2 = result['co2_emitted']
    decompose = result['decompose_time']
    eco_tip = result['eco_tip']

    st.subheader(messages[lang]["result_title"])
    st.write(f"{messages[lang]['name_label']} {name}: {count} {unit}")
    st.write(f"{messages[lang]['weight_label']} {weight:.3f} kg")
    st.write(f"{messages[lang]['co2_emitted_label']} {co2:.2f} kg")
    st.write(f"{messages[lang]['decompose_time_label']} {decompose}")
    st.write(f"{messages[lang]['eco_tip_label']} {eco_tip}")

def get_today_co2_and_score(history):
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    today_records = [r for r in history if r["date"] == today]
    total_co2 = sum(r["co2_emitted"] for r in today_records)
    eco_score = max(0, 100 - total_co2 * 5)
    return total_co2, eco_score

def select_language():
    lang_options = {
        "ko": messages["ko"]["lang_ko"],
        "en": messages["en"]["lang_en"],
        "zh": messages["zh"]["lang_zh"]
    }
    
    selected_lang_name = st.sidebar.selectbox(
        messages[st.session_state.current_language]["select_language_title"],
        options=list(lang_options.values()),
        index=list(lang_options.keys()).index(st.session_state.current_language),
        key="language_selector"
    )
    
    for key, value in lang_options.items():
        if value == selected_lang_name:
            st.session_state.current_language = key
            break

def main():
    st.set_page_config(layout="centered", page_title="Eco Tracker")
    
    select_language()
    
    st.title(messages[st.session_state.current_language]["welcome"])
    st.write(random.choice(eco_quotes))

    history = load_history()
    settings = load_settings()

    menu_options = {
        "ko": ["쓰레기 입력", "오늘 배출량 및 점수 확인", "하루 목표 설정"],
        "en": ["Enter waste", "View today's emissions and score", "Set daily target"],
        "zh": ["输入垃圾", "查看今日排放量和分数", "设置每日目标"]
    }
    
    choice = st.sidebar.radio(
        messages[st.session_state.current_language]["select_menu"],
        menu_options[st.session_state.current_language]
    )

    if choice == menu_options[st.session_state.current_language][0]: # 쓰레기 입력 / Enter waste / 输入垃圾
        st.header(messages[st.session_state.current_language]["available_waste_types"])
        waste_names_for_select = [data['names'][st.session_state.current_language] for data in waste_data.values()]
        
        selected_waste_name = st.selectbox(
            messages[st.session_state.current_language]["enter_waste_type"],
            options=waste_names_for_select
        )

        waste_key = None
        for k, v in waste_data.items():
            if selected_waste_name == v["names"][st.session_state.current_language]:
                waste_key = k
                break

        if waste_key:
            count = st.number_input(
                messages[st.session_state.current_language]["input_count"].format(unit=waste_data[waste_key]["unit"][st.session_state.current_language]),
                min_value=0.0,
                value=1.0,
                step=0.1
            )
            
            if st.button(messages[st.session_state.current_language]["select_menu"].split('\n')[0].replace('1. ', '')): # "쓰레기 입력" 버튼
                if count < 0:
                    st.error(messages[st.session_state.current_language]["enter_positive_number"])
                else:
                    result = calculate_impact(waste_key, count)
                    history.append(result)
                    save_history(history)
                    show_result(result)

                    today_co2, eco_score = get_today_co2_and_score(history)
                    st.metric(label=messages[st.session_state.current_language]["today_co2_emission"], value=f"{today_co2:.2f} kg")
                    st.metric(label=messages[st.session_state.current_language]["today_score"], value=f"{eco_score:.1f} / 100")

                    if settings.get("daily_target") and today_co2 > settings["daily_target"]:
                        st.warning(messages[st.session_state.current_language]["over_target"].format(target=settings["daily_target"]))
        else:
            st.error(messages[st.session_state.current_language]["waste_not_registered"])


    elif choice == menu_options[st.session_state.current_language][1]: # 오늘 배출량 및 점수 확인 / View today's emissions and score / 查看今日排放量和分数
        st.header(messages[st.session_state.current_language]["today_co2_emission"].replace(':', ''))
        today_co2, eco_score = get_today_co2_and_score(history)
        st.metric(label=messages[st.session_state.current_language]["today_co2_emission"], value=f"{today_co2:.2f} kg")
        st.metric(label=messages[st.session_state.current_language]["today_score"], value=f"{eco_score:.1f} / 100")

    elif choice == menu_options[st.session_state.current_language][2]: # 하루 목표 설정 / Set daily target / 设置每日目标
        st.header(messages[st.session_state.current_language]["daily_target_prompt"].replace(':', ''))
        current_target = settings.get("daily_target", 0.0)
        target = st.number_input(
            messages[st.session_state.current_language]["daily_target_prompt"],
            min_value=0.0,
            value=float(current_target if current_target is not None else 0.0), # None일 경우 0.0으로 초기화
            step=0.1,
            format="%.2f"
        )
        if st.button(messages[st.session_state.current_language]["select_menu"].split('\n')[2].replace('3. ', '')): # "하루 목표 설정" 버튼
            settings["daily_target"] = target
            save_settings(settings)
            st.success(messages[st.session_state.current_language]["target_set"])
            
    # "종료" 메뉴는 웹 앱에서는 필요 없으므로 제거 (혹은 "종료" 대신 "정보" 등으로 대체)

if __name__ == "__main__":
    main()