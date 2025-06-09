import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import game1 as game1
import game2 as game2
import game3 as game3

# 색상 테마
BACKGROUND_COLOR = "#F0F8FF"
BUTTON_COLOR = "#87CEEB"
TEXT_COLOR = "#003366"

def start_order_game():
    root.destroy()
    game1.launch_game()

def start_color_game():
    root.destroy()
    game2.launch_game()

def start_word_game():
    root.destroy()
    game3.launch_game()

# 메인 윈도우
root = tk.Tk()
root.title("기억해!GAME")
root.geometry("500x400")
root.configure(bg=BACKGROUND_COLOR)

# 타이틀
title = tk.Label(root, text="🧠 기억해!GAME 🧠", font=("Helvetica", 24, "bold"),
                 fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
title.pack(pady=30)

# 버튼 생성 함수
def make_button(text, command):
    return tk.Button(root, text=text, command=command,
                     font=("Helvetica", 16), bg=BUTTON_COLOR, fg=TEXT_COLOR,
                     activebackground="#B0E0E6", width=25, height=2)

# 게임 버튼 추가
make_button("🧩 순서 기억 게임", start_order_game).pack(pady=10)
make_button("🧠 색깔 기억 게임", start_color_game).pack(pady=10)
make_button("🔤 단어 기억 게임", start_word_game).pack(pady=10)

root.mainloop()
