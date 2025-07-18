import json
import os
import datetime
import random

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

#퀴즈 데이터
quiz_data = [
    {
        "question": {
            "ko": "플라스틱 병이 분해되려면 몇 년이 걸릴까요?",
            "en": "How many years does it take for a plastic bottle to decompose?",
            "zh": "一个塑料瓶需要多少年才能分解？"
        },
        "answer": "450"
    },
    {
        "question": {
            "ko": "종이가 분해되려면 몇 주가 걸릴까요?",
            "en": "How many weeks does it take for a paper to decompose?",
            "zh": "纸张需要几周才能分解？"
        },
        "answer": "4"
    },
    {
        "question": {
            "ko": "담배꽁초가 분해되려면 몇 년이 걸릴까요?",
            "en": "How many years does it take for a cigarette butt to decompose?",
            "zh": "一个烟蒂需要多少年才能分解？"
        },
        "answer": "12"
    },
    {
        "question": {
            "ko": "유리가 분해되려면 몇 년이 걸릴까요?",
            "en": "How many years does it take for a glass to decompose?",
            "zh": "玻璃需要多少年才能分解?"
        },
        "answer": "1000000"
    },
    {
        "question": {
            "ko": "환경 보호의 3R 중 첫 번째는 무엇인가요? (줄이기/재사용/재활용)",
            "en": "What is the first of the 3Rs for the environment? (Reduce/Reuse/Recycle)",
            "zh": "环保3R中的第一个是什么？（减少/重复使用/回收）"
        },
        "answer": {
            "ko": "줄이기",
            "en": "Reduce",
            "zh": "减少"
        }
    },
    {
        "question": {
            "ko": "지구의 대체 행성이 있다(O/X)?",
            "en": "Is there an alternative planet to Earth? (O/X)",
            "zh": "地球有替代行星吗？（O/X）"
        },
        "answer": "X"
    },
    {
        "question": {
            "ko": "전기 대신 자연광을 이용하는 행동은 에너지를 (절약한다/낭비한다)?",
            "en": "Using natural light instead of electricity (saves/wastes) energy?",
            "zh": "使用自然光代替电能是（节约/浪费）能源？"
        },
        "answer": {
            "ko": "절약한다",
            "en": "saves",
            "zh": "节约"
        }
    },
    {
        "question": {
            "ko": "비닐봉지의 평균 분해 기간은 약 몇 년인가요?",
            "en": "About how many years does it take for a plastic bag to decompose?",
            "zh": "一个塑料袋大约需要多少年才能分解？"
        },
        "answer": "1000"
    },
    {
        "question": {
            "ko": "지구의 해수면 상승 주요 원인은? (빙하가 녹음/비가 많이 옴/화산 폭발)",
            "en": "Main cause of rising sea levels? (Melting glaciers/More rain/Volcano eruption)",
            "zh": "海平面上升的主要原因？（冰川融化/降雨多/火山爆发）"
        },
        "answer": {
            "ko": "빙하가 녹음",
            "en": "Melting glaciers",
            "zh": "冰川融化"
        }
    },
    {
        "question": {
            "ko": "기후 변화의 주요 원인 중 하나는? (이산화탄소/질소/수소)",
            "en": "One main cause of climate change? (Carbon dioxide/Nitrogen/Hydrogen)",
            "zh": "气候变化的主要原因之一？（二氧化碳/氮气/氢气）"
        },
        "answer": {
            "ko": "이산화탄소",
            "en": "Carbon dioxide",
            "zh": "二氧化碳"
        }
    },
    {
        "question": {
            "ko": "가장 환경 친화적인 운송 수단은? (자전거/자동차/비행기)",
            "en": "Which is the most eco-friendly transport? (Bicycle/Car/Airplane)",
            "zh": "最环保的交通方式是？（自行车/汽车/飞机）"
        },
        "answer": {
            "ko": "자전거",
            "en": "Bicycle",
            "zh": "自行车"
        }
    },
    {
        "question": {
            "ko": "에너지를 아끼는 행동은? (대기전력 차단/에어컨 계속 켜기/TV 켜두기)",
            "en": "Which action saves energy? (Unplug devices/Keep AC on/Leave TV on)",
            "zh": "节约能源的做法是？（拔掉插头/一直开空调/开着电视）"
        },
        "answer": {
            "ko": "대기전력 차단",
            "en": "Unplug devices",
            "zh": "拔掉插头"
        }
    },
    {
        "question": {
            "ko": "휴지를 대신할 수 있는 친환경 대안은?",
            "en": "What is an eco-friendly alternative to tissues?",
            "zh": "替代纸巾的环保选择是什么？"
        },
        "answer": {
            "ko": "손수건",
            "en": "Handkerchief",
            "zh": "手帕"
        }
    }
]
# 파일 경로
base_dir = os.path.dirname(os.path.abspath(__file__))
history_file = os.path.join(base_dir, "waste_history.json")
settings_file = os.path.join(base_dir, "settings.json")

# 기본 설정
current_language = "ko"

messages = {
    "ko": {
        "welcome": "🌿 환경을 위한 작은 실천, 시작합니다!",
        "select_menu": "\n1. 쓰레기 입력\n2. 오늘 배출량 및 점수 확인\n3. 하루 목표 설정\n4. 환경 퀴즈\n5. 종료\n선택하세요: ",
        "goodbye": "👋 이용해 주셔서 감사합니다!",
        "invalid_number": "❌ 숫자를 입력해주세요.",
        "invalid_menu": "❌ 올바른 메뉴 번호를 선택해주세요.",
        "input_count": "몇 {unit}를 버렸나요? ",
        "daily_target_prompt": "하루 CO₂ 배출 목표(kg)를 입력하세요: ",
        "target_set": "✅ 목표가 설정되었습니다.",
        "over_target": "⚠️ 설정한 목표({target} kg)를 초과했습니다!"
    },
    "en": {
        "welcome": "🌿 Let's start a small action for the environment!",
        "select_menu": "\n1. Enter waste\n2. View today's emissions and score\n3. Set daily target\n4. Eco Quiz\n5. Exit\nChoose: ",
        "goodbye": "👋 Thank you for using!",
        "invalid_number": "❌ Please enter a number.",
        "invalid_menu": "❌ Invalid menu number.",
        "input_count": "How many {unit}? ",
        "daily_target_prompt": "Enter daily CO₂ target (kg): ",
        "target_set": "✅ Target set.",
        "over_target": "⚠️ Over daily target ({target} kg)!"
    },
    "zh": {
        "welcome": "🌿 开始为环境做一点小改变吧！",
        "select_menu": "\n1. 输入垃圾\n2. 查看今日排放量和分数\n3. 设置每日目标\n4. 环保测验\n5. 退出\n请选择: ",
        "goodbye": "👋 感谢您的使用！",
        "invalid_number": "❌ 请输入数字。",
        "invalid_menu": "❌ 菜单编号无效。",
        "input_count": "多少{unit}？",
        "daily_target_prompt": "请输入每日CO₂排放目标(公斤): ",
        "target_set": "✅ 目标已设置。",
        "over_target": "⚠️ 超过每日目标({target}公斤)！"
    }
}

eco_quotes = [
    "The Earth is what we all have in common. - Wendell Berry",
    "작은 변화가 큰 변화를 만듭니다.",
    "지구는 우리가 물려받은 것이 아니라, 빌려온 것입니다.",
    "There is no Planet B.",
    "One planet, one chance."
]

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
        decompose = f"{data['decompose_years']}년" if current_language=="ko" else \
                    f"{data['decompose_years']} years" if current_language=="en" else \
                    f"{data['decompose_years']}年"
    elif "decompose_months" in data:
        decompose = f"{data['decompose_months']}개월" if current_language=="ko" else \
                    f"{data['decompose_months']} months" if current_language=="en" else \
                    f"{data['decompose_months']}个月"
    elif "decompose_weeks" in data:
        decompose = f"{data['decompose_weeks']}주" if current_language=="ko" else \
                    f"{data['decompose_weeks']} weeks" if current_language=="en" else \
                    f"{data['decompose_weeks']}周"

    return {
        "waste_key": waste_key,
        "count": count,
        "unit": data["unit"][current_language],
        "weight_kg": weight_kg,
        "co2_emitted": co2,
        "decompose_time": decompose,
        "eco_tip": data["eco_alternative"][current_language],
        "date": datetime.datetime.today().strftime("%Y-%m-%d")
    }

def show_result(result):
    lang = current_language
    name = waste_data[result['waste_key']]['names'][lang]
    count = result['count']
    unit = result['unit']
    weight = result['weight_kg']
    co2 = result['co2_emitted']
    decompose = result['decompose_time']
    eco_tip = result['eco_tip']

    if lang == "ko":
        print("\n📊 결과")
        print(f"- {name}: {count} {unit}")
        print(f"- 무게: {weight:.3f} kg")
        print(f"- 배출된 CO₂: {co2:.2f} kg")
        print(f"- 분해 시간: {decompose}")
        print(f"- 🌱 친환경 대안: {eco_tip}")
    elif lang == "en":
        print("\n📊 Result")
        print(f"- {name}: {count} {unit}")
        print(f"- Weight: {weight:.3f} kg")
        print(f"- CO₂ Emitted: {co2:.2f} kg")
        print(f"- Decompose Time: {decompose}")
        print(f"- 🌱 Eco Tip: {eco_tip}")
    else: # zh
        print("\n📊 结果")
        print(f"- {name}: {count} {unit}")
        print(f"- 重量: {weight:.3f} kg")
        print(f"- 排放的 CO₂: {co2:.2f} kg")
        print(f"- 分解时间: {decompose}")
        print(f"- 🌱 环保建议: {eco_tip}")

def get_today_co2_and_score(history):
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    today_records = [r for r in history if r["date"] == today]
    total_co2 = sum(r["co2_emitted"] for r in today_records)
    eco_score = max(0, 100 - total_co2 * 5)
    return total_co2, eco_score

def eco_quiz():
    quiz = random.choice(quiz_data) 
    q_text = quiz["question"][current_language]
    
    print("\n🌱 " + q_text)
    user_answer = input({
        "ko": "정답을 입력하세요: ",
        "en": "Enter your answer: ",
        "zh": "请输入答案: "
    }[current_language]).strip()

    correct = quiz["answer"]
    if isinstance(correct, dict):
        correct = correct[current_language]

    if user_answer == str(correct):
        print({
            "ko": "✅ 정답입니다! 잘 하셨어요!",
            "en": "✅ Correct! Well done!",
            "zh": "✅ 正确！做得好！"
        }[current_language])
    else:
        print({
            "ko": f"❌ 아쉽지만 오답입니다. 정답: {correct}",
            "en": f"❌ Incorrect. The correct answer: {correct}",
            "zh": f"❌ 答错了。正确答案是: {correct}"
        }[current_language])


def select_language():
    global current_language
    print("\n🌐 언어를 선택하세요:")
    print("1. 한국어\n2. English\n3. 中文")
    choice = input("선택: ")
    if choice == "1":
        current_language = "ko"
    elif choice == "2":
        current_language = "en"
    elif choice == "3":
        current_language = "zh"
    else:
        print("❌ 잘못된 선택입니다. 기본값: 한국어로 설정됩니다.")
        current_language = "ko"


def main():
    select_language()
    print("\n" + random.choice(eco_quotes))
    print(messages[current_language]["welcome"])

    history = load_history()
    settings = load_settings()

    while True:
        choice = input(messages[current_language]["select_menu"])

        if choice == "1":
            print("\n" + (
                "가능한 쓰레기 종류:" if current_language == "ko"
                else "Available waste types:" if current_language == "en"
                else "可用垃圾种类:"
            ))

            for key, data in waste_data.items():
                print(f"- {data['names'][current_language]} ({data['unit'][current_language]})")

            name_input = input({
                "ko": "쓰레기 종류를 입력하세요: ",
                "en": "Enter waste type: ",
                "zh": "请输入垃圾类型: "
            }[current_language]).strip()

            waste_key = None
            for k, v in waste_data.items():
                if name_input == v["names"][current_language]:
                    waste_key = k
                    break
            if not waste_key:
                print({
                    "ko": "❌ 등록되지 않은 쓰레기 종류입니다.",
                    "en": "❌ Not registered waste type.",
                    "zh": "❌ 未注册垃圾类型。"
                }[current_language])
                continue

            try:
                count = float(input(messages[current_language]["input_count"].format(unit=waste_data[waste_key]["unit"][current_language])))
                if count < 0:
                    print({
                        "ko": "❌ 0 이상의 숫자를 입력하세요.",
                        "en": "❌ Enter a number >= 0.",
                        "zh": "❌ 输入大于等于0的数字。"
                    }[current_language])
                    continue
            except ValueError:
                print(messages[current_language]["invalid_number"])
                continue

            result = calculate_impact(waste_key, count)
            history.append(result)
            save_history(history)
            show_result(result)

            today_co2, eco_score = get_today_co2_and_score(history)
            print(f"\n📝 { {'ko':'오늘 누적 CO₂ 배출량:', 'en':'Today\'s CO₂ Emissions:', 'zh':'今日累计CO₂排放量:'}[current_language]} {today_co2:.2f} kg")
            print(f"🏆 { {'ko':'오늘 점수:', 'en':'Score:', 'zh':'分数:'}[current_language]} {eco_score:.1f} / 100")

            if settings.get("daily_target") and today_co2 > settings["daily_target"]:
                print(messages[current_language]["over_target"].format(target=settings["daily_target"]))

        elif choice == "2":
            today_co2, eco_score = get_today_co2_and_score(history)
            print(f"\n📝 { {'ko':'오늘 누적 CO₂ 배출량:', 'en':'Today\'s CO₂ Emissions:', 'zh':'今日累计CO₂排放量:'}[current_language]} {today_co2:.2f} kg")
            print(f"🏆 { {'ko':'오늘 점수:', 'en':'Score:', 'zh':'分数:'}[current_language]} {eco_score:.1f} / 100")

        elif choice == "3":
            try:
                target = float(input(messages[current_language]["daily_target_prompt"]))
                settings["daily_target"] = target
                save_settings(settings)
                print(messages[current_language]["target_set"])
            except ValueError:
                print(messages[current_language]["invalid_number"])

        elif choice == "4": # Moved eco_quiz to be a direct menu option
            eco_quiz()

        elif choice == "5":
            print(messages[current_language]["goodbye"])
            break

        else:
            print(messages[current_language]["invalid_menu"])

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
