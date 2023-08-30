import cv2
import pytesseract
import pyttsx3
import re
import pyautogui
import os
import time
from pynput import keyboard

# Константы
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
PAUSE_RATE = 200
PAUSE_DURATION_FACTOR = 0.2  # Пропорционально длине предложения

# Установка пути к исполняемому файлу Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def capture_screen():
    # Получение текущего рабочего каталога
    current_directory = os.getcwd()

    # Формирование пути к файлу скриншота
    screenshot_path = os.path.join(current_directory, "screenshot.png")

    # Координаты области для захвата скриншота
    x = 550  # Левая координата области
    y = 100  # Верхняя координата области
    width = 800  # Ширина области
    height = 800  # Высота области

    # Захват скриншота в указанной области
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(screenshot_path)

    # Загрузка скриншота
    image = cv2.imread(screenshot_path)
    return image

def preprocess_image(image):
    # Применение бинаризации изображения для улучшения контраста текста
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary_image

def extract_text(image):
    # Извлечение текста изображения с помощью PyTesseract
    text = pytesseract.image_to_string(image, lang='rus')  # Распознавание текста на русском языке с помощью PyTesseract
    return text

def clean_text(text):
    # Очистка текста от нежелательных символов
    cleaned_text = re.sub(r'[^а-яА-ЯёЁ0-9\s]', '', text)  # Фильтрация только русских символов и цифр с использованием регулярного выражения
    return cleaned_text

def speak(text):
    # Озвучивание текста с помощью pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)  # Установка скорости речи (200 слов в минуту)
    
    # Разделение текста на предложения с учетом знаков пунктуации
    sentences = re.split(r'[.!?]', text)
    
    # Проход по каждому предложению и озвучивание с паузами
    for sentence in sentences:
        sentence = sentence.strip()  # Удаление начальных и конечных пробелов
        if sentence:
            engine.say(sentence)
            engine.runAndWait()
            pause_duration = len(sentence.split()) / 5  # Пауза, пропорциональная длине предложения
            engine.setProperty('rate', 100)  # Уменьшение скорости для паузы
            engine.say('pause')
            engine.runAndWait()
            engine.setProperty('rate', 200)  # Возвращение к обычной скорости
            time.sleep(pause_duration)  # Пауза между предложениями

def on_press(key):
    if key == keyboard.Key.esc:
        # Выход из программы
        return False
    elif key == keyboard.Key.ctrl_r:
        # Захват скриншота и озвучивание текста
        screenshot = capture_screen()
        preprocessed_image = preprocess_image(screenshot)
        text = extract_text(preprocessed_image)
        cleaned_text = clean_text(text)
        
        # Удаление переносов строк из текста
        cleaned_text = cleaned_text.replace('\n', ' ')
        
        speak(cleaned_text)

def main():
    # Запуск цикла прослушивания горячей клавиши
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    main()
