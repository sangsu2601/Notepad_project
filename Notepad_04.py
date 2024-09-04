from customtkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# https://ysyblog.tistory.com/296 참고해서 구글 세팅 완료하십쇼
# 아주 중요함 - API키 받고, 구글 드라이브 API 활성화, 사용자 리스트에 본인 이메일 추가해놓기
# 처음 프로그램 시작하기 전에 아래 있는 주석처리된 auth 인증부분 실행하기
# 한번 인증 하면 앞으로 안해도 됨 ㅇㅇ

# Google Drive 인증 및 드라이브 객체 생성
#gauth = GoogleAuth()
#gauth.LocalWebserverAuth()  # 인증을 위한 웹 서버 열기
#drive = GoogleDrive(gauth)

# 전역 변수로 파일 경로를 저장할 변수
saved_file_id = None

def saveFile():
    global saved_file_id
    text = entry.get(1.0, END)
    
    if saved_file_id is None:
        # 새 파일을 Google Drive에 업로드
        new_file = drive.CreateFile({'title': 'new_note.txt', 'mimeType': 'text/plain'})
        new_file.SetContentString(text)
        new_file.Upload()
        saved_file_id = new_file['id']  # 파일 ID 저장
        print(f"File uploaded to Google Drive with ID: {saved_file_id}")
    else:
        # 기존 파일 업데이트
        existing_file = drive.CreateFile({'id': saved_file_id})
        existing_file.SetContentString(text)
        existing_file.Upload()
        print(f"File updated on Google Drive with ID: {saved_file_id}")

def openFile():
    global saved_file_id
    file = askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
    if file is not None:
        # 선택된 파일을 읽고 구글 드라이브에 업로드
        content = file.read()
        entry.delete(1.0, END)
        entry.insert(INSERT, content)

        # Google Drive에 저장
        new_file = drive.CreateFile({'title': file.name.split('/')[-1], 'mimeType': 'text/plain'})
        new_file.SetContentString(content)
        new_file.Upload()
        saved_file_id = new_file['id']  # 파일 ID 저장
        print(f"File uploaded to Google Drive with ID: {saved_file_id}")

def clearFile():
    entry.delete(1.0, END)

def auto_save():
    if saved_file_id is not None:
        # 자동 저장 시 Google Drive에 업데이트
        existing_file = drive.CreateFile({'id': saved_file_id})
        text = entry.get(1.0, END)
        existing_file.SetContentString(text)
        existing_file.Upload()
        print(f"Auto-saved to Google Drive with ID: {saved_file_id}")
    root.after(10000, auto_save)  # 10초마다 자동 저장 실행

# CustomTkinter settings
set_appearance_mode("dark")
set_default_color_theme("orange.json")

root = CTk()  # Create main window
root.geometry("400x600")
root.title("Notepad")

# Frame for buttons
top = CTkFrame(root)
top.pack(padx=10, pady=5, anchor='nw')

# Buttons for Open, Save
b1 = CTkButton(top, text="Open", command=openFile)
b1.pack(side=LEFT, padx=5)

b2 = CTkButton(top, text="Save", command=saveFile)
b2.pack(side=LEFT, padx=5)

# Textbox for content
entry = CTkTextbox(root, wrap=WORD, font=("Poppins", 15))
entry.pack(padx=10, pady=5, expand=True, fill=BOTH)

root.after(10000, auto_save)  # 10초마다 자동저장

root.mainloop()  # Run the application
