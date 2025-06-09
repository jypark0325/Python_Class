import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import base64

# ==== 설정 ====
API_KEY = "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"
MODEL_IMAGE_DESC = "moonshotai/kimi-vl-a3b-thinking:free"
MODEL_TRANSLATE = "openai/gpt-3.5-turbo"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ==== 이미지 설명 API 호출 ====
def call_image_desc_api(image_path):
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "이 이미지를 자세히 설명해줘."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
            ],
        }
    ]

    json_data = {
        "model": MODEL_IMAGE_DESC,
        "messages": messages,
        "stream": False,
    }

    response = requests.post(API_URL, headers=headers, json=json_data)
    if response.status_code == 200:
        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except:
            return "❗ 이미지 설명 파싱 실패"
    else:
        return f"❗ 이미지 설명 API 호출 실패: {response.status_code}"

# ==== 번역 API 호출 ====
def call_translation_api(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = f"다음 영어 문장을 시각장애인을 위해 자연스럽고 쉽게 이해할 수 있도록 한국어로 번역해줘:\n\n{text}"

    json_data = {
        "model": MODEL_TRANSLATE,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }

    response = requests.post(API_URL, headers=headers, json=json_data)
    if response.status_code == 200:
        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except:
            return "❗ 번역 결과 파싱 실패"
    else:
        return f"❗ 번역 API 호출 실패: {response.status_code}"

# ==== 이미지 선택 및 처리 ====
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("이미지 파일", "*.png *.jpg *.jpeg *.bmp")])
    if file_path:
        load_and_show_image(file_path)
        description_text.set("이미지 설명 생성 중...")
        root.update()

        english_desc = call_image_desc_api(file_path)
        description_text.set("번역 중...")
        root.update()

        translated = call_translation_api(english_desc)
        description_text.set(translated)

# ==== 이미지 표시 ====
def load_and_show_image(path):
    img = Image.open(path)
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

# ==== GUI 세팅 ====
root = tk.Tk()
root.title("시각장애인 이미지 묘사 프로그램 (2단계 무료 AI)")
root.geometry("600x700")
root.configure(bg="#B0E0E6")

tk.Label(root, text="이미지 묘사 프로그램", font=("Helvetica", 24, "bold"), bg="#B0E0E6", fg="#003366").pack(pady=15)
tk.Button(root, text="이미지 선택하기", font=("Helvetica", 16), bg="#4682B4", fg="white", command=select_image).pack(pady=10)

image_label = tk.Label(root, bg="#B0E0E6")
image_label.pack(pady=20)

description_text = tk.StringVar()
tk.Label(root, textvariable=description_text, font=("Helvetica", 16), bg="#B0E0E6", fg="#003366", wraplength=550, justify="left").pack(pady=20)

root.mainloop()
