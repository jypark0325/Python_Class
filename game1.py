import tkinter as tk
import random
import time
import os
import json
from datetime import datetime
from tkinter import messagebox

# 색상 테마
BG_COLOR = "#FFFACD"
BUTTON_COLOR = "#FFD700"
FLASH_COLOR = "#FFFF00"
TEXT_COLOR = "#4B0082"

# 통계 파일 경로
stats_file = "order_game_stats.json"

# 전역 변수
sequence = []
user_input = []
buttons = []
start_time = 0
countdown_id = None
countdown_seconds = 2

# 통계 함수
def load_stats():
    if os.path.exists(stats_file):
        with open(stats_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"plays": 0, "correct": 0, "incorrect": 0, "best_level": 0, "last_play": None}

def save_stats(stats):
    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)

# 순서 리셋
def reset_game():
    global sequence, user_input, start_time
    sequence = []
    user_input = []
    timer_label.config(text="")
    root.after(1000, generate_sequence)  # 1초 후 시작

# 순서 생성 및 깜빡이기
def generate_sequence():
    global sequence, start_time, countdown_id
    if countdown_id:
        root.after_cancel(countdown_id)
        countdown_id = None
    timer_label.config(text="")
    if countdown_id:
        root.after_cancel(countdown_id)
        countdown_id = None
    new_index = random.randint(0, 3)
    sequence.append(new_index)
    flash_sequence()
    start_time = time.time()
    # countdown moved to start after flashing

# 버튼 깜빡임 (순차적으로)
def flash_sequence():
    for i, idx in enumerate(sequence):
        root.after(1000 * i, lambda idx=idx: flash_button(idx))
    total_flash_time = 1000 * len(sequence)
    root.after(total_flash_time, lambda: start_countdown(countdown_seconds + len(sequence)))

# 깜빡이는 효과 (밝은 색 → 원래 색)
def flash_button(index):
    btn = buttons[index]
    btn.config(bg=FLASH_COLOR)
    root.after(500, lambda: btn.config(bg=BUTTON_COLOR))

# 시간 초과 처리
def handle_timeout():
    stats = load_stats()
    stats["plays"] += 1
    stats["incorrect"] += 1
    stats["last_play"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_stats(stats)
    messagebox.showinfo("시간 초과", "입력 시간이 초과되었습니다. 다시 시도하세요!")
    reset_game()

# 카운트다운
def start_countdown(seconds):
    global countdown_id
    timer_label.config(text=f"남은 시간: {seconds} 초")
    if seconds > 0:
        countdown_id = root.after(1000, start_countdown, seconds - 1)
    else:
        handle_timeout()

# 버튼 클릭 시
def button_click(index):
    global user_input
    # 타이머 취소 제거하여 계속 흐르게 유지

    user_input.append(index)

    if user_input[len(user_input) - 1] != sequence[len(user_input) - 1]:
        record_result(False)
        reset_game()
        return

    if len(user_input) == len(sequence):
        if countdown_id:
            root.after_cancel(countdown_id)
        record_result(True)
        user_input = []
        generate_sequence()

# 결과 기록 및 통계 저장
def record_result(correct):
    global countdown_id
    if countdown_id:
        root.after_cancel(countdown_id)
        countdown_id = None
    end_time = time.time()
    elapsed = round(end_time - start_time, 2)
    stats = load_stats()
    stats["plays"] += 1
    stats["last_play"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if correct:
        stats["correct"] += 1
        current_level = len(sequence)
        if stats.get("best_level", 0) < current_level:
            stats["best_level"] = current_level
    else:
        stats["incorrect"] += 1

    save_stats(stats)
    messagebox.showinfo("현재 단계 결과", f"현재 도달 단계: {len(sequence)} 최고 기록 단계: {stats['best_level']}단계")

# 게임 UI 실행 함수
def start_main_ui():
    global root, title, buttons, timer_label

    root = tk.Tk()
    root.title("🧩 순서 기억 게임")
    root.geometry("400x500")
    root.configure(bg=BG_COLOR)

    title = tk.Label(root, text="순서 기억 게임", font=("Helvetica", 24, "bold"),
                     bg=BG_COLOR, fg=TEXT_COLOR)
    title.pack(pady=30)

    timer_label = tk.Label(root, text="", font=("Helvetica", 16), bg=BG_COLOR, fg="red")
    timer_label.pack(pady=5)

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack()

    buttons = []
    for i in range(4):
        btn = tk.Button(frame, text=f"{i+1}", font=("Helvetica", 18, "bold"),
                        bg=BUTTON_COLOR, width=10, height=4,
                        command=lambda i=i: button_click(i))
        btn.grid(row=i//2, column=i%2, padx=10, pady=10)
        buttons.append(btn)

    reset_game()  # 시작하자마자 게임 시작
    root.mainloop()

def launch_game():
    intro = tk.Tk()
    intro.title("게임 규칙 안내")
    intro.geometry("500x300")
    intro.configure(bg=BG_COLOR)

    rule_text = (
    """    🧠 게임 규칙 안내 🧠
    
    
    1. 버튼이 순서대로 깜빡입니다.
    
    2.  같은 순서로 클릭하여 기억을 테스트하세요.
    
    3. 단계가 올라갈수록 순서가 길어지고 제한 시간이 늘어납니다.
    
    4. 틀리거나 시간이 초과되면 처음부터 다시 시작됩니다!
    
    준비되셨다면 시작 버튼을 눌러 시작하세요."""
    )

    rule_label = tk.Label(intro, text=rule_text, font=("Helvetica", 12), justify="left",
                      bg=BG_COLOR, fg=TEXT_COLOR, padx=20, pady=20)
    rule_label.pack()

    start_btn_intro = tk.Button(intro, text="게임 시작하기", font=("Helvetica", 14),
                                bg=BUTTON_COLOR, fg="white", command=lambda: [intro.destroy(), start_main_ui()])
    start_btn_intro.pack(pady=10)

    intro.mainloop()

# main.py에서 직접 실행될 경우만
if __name__ == "__main__":
    launch_game()
