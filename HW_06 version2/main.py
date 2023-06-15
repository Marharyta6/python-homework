import shutil
import sys
from pathlib import Path

IMAGE_EXTENSIONS = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO_EXTENSIONS = ('AVI', 'MP4', 'MOV', 'MKV')
DOCUMENT_EXTENSIONS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
AUDIO_EXTENSIONS = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVE_EXTENSIONS = ('ZIP', 'GZ', 'TAR')


# Функція для транслітерації та нормалізації імен файлів
def normalize(filename):
    transliteration = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '',
        'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'iu', 'я': 'ia',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'IE', 'Ж': 'ZH', 'З': 'Z', 'И': 'I',
        'І': 'I', 'Ї': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ь': '',
        'Ы': 'Y', 'Ъ': '', 'Э': 'E', 'Ю': 'IU', 'Я': 'IA'
    }
    normalized = ''
    for char in filename:
        if char.isalnum():
            normalized += char
        elif char in transliteration:
            normalized += transliteration[char]
        else:
            normalized += '_'
    return normalized


# Функція для сортування папок та файлів
def sort_folder(path):
    for file_path in path.iterdir():
        if file_path.is_file():
            file_extension = file_path.suffix.lstrip('.')
            if file_extension in IMAGE_EXTENSIONS:
                move_file(file_path, 'images')
            elif file_extension in VIDEO_EXTENSIONS:
                move_file(file_path, 'video')
            elif file_extension in DOCUMENT_EXTENSIONS:
                move_file(file_path, 'documents')
            elif file_extension in AUDIO_EXTENSIONS:
                move_file(file_path, 'audio')
            elif file_extension in ARCHIVE_EXTENSIONS:
                extract_archive(file_path, 'archives')
        elif file_path.is_dir() and file_path.name not in ('archives', 'video', 'audio', 'documents', 'images'):
            sort_folder(file_path)


# Функція для перенесення файлів в нову папку
def move_file(file_path, folder_name):
    new_file_name = normalize(file_path.name)
    destination_folder = file_path.parent / folder_name
    destination_folder.mkdir(exist_ok=True)
    destination_path = destination_folder / new_file_name
    file_path.rename(destination_path)


# Функція для розпакування архіву та перенесення вмісту до папки
def extract_archive(file_path, folder_name):
    new_folder_name = normalize(file_path.stem)
    destination_folder = file_path.parent / folder_name
    destination_folder.mkdir(exist_ok=True)
    destination_path = destination_folder / new_folder_name

    if file_path.suffix == '.zip':
        shutil.unpack_archive(file_path, destination_path)
    elif file_path.suffix == '.tar.gz':
        shutil.unpack_archive(file_path, destination_path, 'gztar')
    elif file_path.suffix == '.tar':
        shutil.unpack_archive(file_path, destination_path)


# Основний код програми
if __name__ == '__main__':
    folder_path = Path("C:\Testfolder")
    if folder_path.is_dir():
        sort_folder(folder_path)
        print("Сортування завершено.")
    else:
        print("Невірний шлях до папки.")
