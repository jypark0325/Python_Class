import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import base64

# ==== 설정 ====
IMAGE_CAPTION_API_URL = "https://ftapi.pythonanywhere.com/caption"  # 예시 API URL
TRANSLATION_API_URL = "https://libretranslate.com/translate"

# ==== 이미지 설명 생성 함수 ====
def generate_image_caption(image_path):
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    headers = {
        "Content-Type": "application/json",
    }

    json_data = {
        "image": img_b64
    }

    try:
        response = requests.post(IMAGE_CAPTION_API_URL, headers=headers, json=json_data)
        response.raise_for_status()
        data = response.json()
        caption = data.get("caption", "이미지 설명을 생성할 수 없습니다.")
        return caption
    except Exception as e:
        return f"❌ 이미지 설명 생성 실패: {e}"

# ==== 번역 함수 ====
def translate_text(text, source_lang="en", target_lang="ko"):
    headers = {
        "Content-Type": "application/json",
    }

    json_data = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "text"
    }

    try:
        response = requests.post(TRANSLATION_API_URL, headers=headers, json=json_data)
        response.raise_for_status()
        data = response.json()
        translated_text = data.get("translatedText", "번역을 수행할 수 없습니다.")
        return translated_text
    except Exception as e:
        return f"❌ 번역 실패: {e}"

# ==== GUI 관련 함수 ====
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("이미지 파일", "*.png *.jpg *.jpeg *.bmp")])
    if file_path:
        load_and_show_image(file_path)
        description_text.set("이미지 설명 생성 중...")
        root.update()

        caption = generate_image_caption(file_path)
        description_text.set("번역 중...")
        root.update()

        translated_caption = translate_text(caption)
        description_text.set(translated_caption)

def load_and_show_image(path):
    img = Image.open(path)
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

# ==== Tkinter GUI 설정 ====
root = tk.Tk()
root.title("시각장애인을 위한 이미지 묘사 프로그램")
root.geometry("600x700")
root.configure(bg="#B0E0E6")

title = tk.Label(root, text="이미지 묘사 프로그램", font=("Helvetica", 24, "bold"), bg="#B0E0E6", fg="#003366")
title.pack(pady=15)

btn = tk.Button(root, text="이미지 선택하기", font=("Helvetica", 16), bg="#4682B4", fg="white", command=select_image)
btn.pack(pady=10)

image_label = tk.Label(root, bg="#B0E0E6")
image_label.pack(pady=20)

description_text = tk.StringVar()
desc_label = tk.Label(root, textvariable=description_text, font=("Helvetica", 16), bg="#B0E0E6", fg="#003366", wraplength=550, justify="left")
desc_label.pack(pady=20)

root.mainloop()
