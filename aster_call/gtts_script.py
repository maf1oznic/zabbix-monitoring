import sys
from gtts import gTTS
import os

# Получаем текст и имя файла из аргументов
if len(sys.argv) < 3:
    print("Usage: gtts_script.py <text> <filename>")
    sys.exit(1)

text = sys.argv[1]  # Текст для синтеза
output_file = sys.argv[2]  # Имя выходного файла

try:
    # Генерация речи
    tts = gTTS(text, lang='en')
    temp_mp3 = "/tmp/temp.mp3"  # Временный файл
    tts.save(temp_mp3)

    # Конвертация MP3 в WAV с частотой 8kHz
    os.system(f"sox {temp_mp3} -r 8000 -c 1 {output_file}")
    os.remove(temp_mp3)  # Удаляем временный файл

except Exception as e:
    print(f"Error: {str(e)}")
    sys.exit(1)
