import tkinter as tk
import random
import os
import json
from datetime import datetime
from tkinter import messagebox

# 색상 테마
BG_COLOR = "#FFEFD5"
TEXT_COLOR = "#8B0000"
BUTTON_COLOR = "#FFDAB9"
HIGHLIGHT_COLOR = "#FF4500"

# 통계 파일 경로
stats_file = "stroop_game_stats.json"

# 게임 관련 변수
colors = ["빨간색", "파란색", "초록색", "노란색"]
color_map = {
    "빨간색": "red",
    "파란색": "blue",
    "초록색": "green",
    "노란색": "yellow"
}

level = 1
max_level = 10
current_answer = ""
countdown_id = None
countdown_seconds = 5
score = 0

# 통계 함수
def load_stats():
    if os.path.exists(stats_file):
        with open(stats_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"plays": 0, "correct": 0, "incorrect": 0, "best_level": 0, "last_play": None}

def save_stats(stats):
    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)

# 게임 초기화
def reset_game():
    global level, score
    level = 1
    score = 0
    start_round()

# 카운트다운 시작
def start_countdown(seconds):
    global countdown_id
    timer_label.config(text=f"남은 시간: {seconds} 초")
    if seconds > 0:
        countdown_id = root.after(1000, start_countdown, seconds - 1)
    else:
        handle_timeout()

# 시간 초과 처리
def handle_timeout():
    stats = load_stats()
    stats["plays"] += 1
    stats["incorrect"] += 1
    stats["last_play"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_stats(stats)
    messagebox.showinfo("시간 초과", "입력 시간이 초과되었습니다. 다시 시도하세요!")
    reset_game()

# 새 라운드 시작
def start_round():
    global current_answer, countdown_id
    if countdown_id:
        root.after_cancel(countdown_id)
        countdown_id = None

    timer_label.config(text="")
    word = random.choice(colors)
    display_color = color_map[random.choice(colors)]
    current_answer = display_color

    draw_word_with_outline(word, display_color)
    start_countdown(countdown_seconds)

# 버튼 클릭 시 정답 확인
def check_answer(selected_color):
    global level, score, countdown_id
    if countdown_id:
        root.after_cancel(countdown_id)

    stats = load_stats()
    stats["plays"] += 1
    stats["last_play"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if selected_color == current_answer:
        stats["correct"] += 1
        level += 1
        score += 1
        if stats.get("best_level", 0) < level:
            stats["best_level"] = level
        save_stats(stats)

        if level > max_level:
            messagebox.showinfo("🎉 성공", f"최고 단계 달성! 총 점수: {score}")
            reset_game()
        else:
            start_round()
    else:
        stats["incorrect"] += 1
        save_stats(stats)
        messagebox.showinfo("실패", f"틀렸어요! 정답은 {current_answer} 입니다.\n현재 점수: {score}\n최고 기록 단계: {stats['best_level']}단계")
        reset_game()

# UI 시작 함수
def start_main_ui():
    global root, word_label, timer_label, draw_word_with_outline
    root = tk.Tk()
    root.title("🧠 스트룹 테스트 게임")
    root.geometry("500x400")
    root.configure(bg=BG_COLOR)

    title = tk.Label(root, text="색깔-단어 구별 게임", font=("Helvetica", 20, "bold"),
                     bg=BG_COLOR, fg=TEXT_COLOR)
    title.pack(pady=20)

    canvas = tk.Canvas(root, width=300, height=80, bg=BG_COLOR, highlightthickness=0)
    canvas.pack(pady=30)
    word_label = canvas

    def draw_word_with_outline(text, fill_color):
        canvas.delete("all")
        canvas.create_rectangle(20, 10, 280, 70, fill="white", outline="gray")
        x, y = 150, 40
        outline_color = "black"
        font_spec = ("Helvetica", 32, "bold")
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            canvas.create_text(x+dx, y+dy, text=text, font=font_spec, fill=outline_color)
        canvas.create_text(x, y, text=text, font=font_spec, fill=fill_color)

    timer_label = tk.Label(root, text="", font=("Helvetica", 16), bg=BG_COLOR, fg="red")
    timer_label.pack(pady=5)

    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)

    for color_name in colors:
        tk.Button(button_frame, text=color_name, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=("Helvetica", 14), width=10,
                  command=lambda c=color_map[color_name]: check_answer(c)).pack(side="left", padx=5)

    reset_game()
    root.mainloop()

def launch_game():
    global intro
    intro = tk.Tk()
    intro.title("게임 규칙 안내")
    intro.geometry("500x350")
    intro.configure(bg=BG_COLOR)

    rules = (
    """    🧠 스트룹 테스트 게임 규칙 🧠
    

    1. 화면에 색깔 이름이 표시됩니다.

    2. 글자의 실제 색깔을 기준으로 선택하세요.

    3. 텍스트 내용과 색상이 다를 수 있으니 주의하세요.

    4. 제한 시간 내에 정답을 선택해야 합니다.

    5. 단계가 올라갈수록 시간이 줄어들고 점수가 오릅니다.
    
    준비되셨다면 시작 버튼을 눌러 시작하세요."""
)

    rule_label = tk.Label(intro, text=rules, font=("Helvetica", 13), justify="left",
                          bg=BG_COLOR, fg=TEXT_COLOR, padx=20, pady=20)
    rule_label.pack()

    start_button = tk.Button(intro, text="게임 시작하기", font=("Helvetica", 14),
                             bg=BUTTON_COLOR, fg="black", command=lambda: [intro.destroy(), start_main_ui()])
    start_button.pack(pady=10)

    intro.mainloop()


# 모듈 단독 실행 시 테스트용
if __name__ == "__main__":
    launch_game()