import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

class FileRenamer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Renamer")
        self.root.geometry("500x300")
        
        # Путь к выбранной папке
        self.folder_path = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Кнопка выбора папки
        select_btn = tk.Button(self.root, text="Выберите папку", command=self.select_folder)
        select_btn.pack(pady=10)
        
        # Отображение выбранного пути
        path_label = tk.Label(self.root, textvariable=self.folder_path, wraplength=450)
        path_label.pack(pady=5)
        
        # Рамка для ввода диапазона индексов
        range_frame = tk.LabelFrame(self.root, text="Диапазон индексов", padx=20, pady=10)
        range_frame.pack(pady=10)
        
        # Поля ввода для начального и конечного индексов
        tk.Label(range_frame, text="Начальный индекс:").grid(row=0, column=0, padx=5)
        self.start_index = tk.Entry(range_frame, width=10)
        self.start_index.grid(row=0, column=1, padx=5)
        self.start_index.insert(0, "1")
        
        tk.Label(range_frame, text="Конечный индекс:").grid(row=0, column=2, padx=5)
        self.end_index = tk.Entry(range_frame, width=10)
        self.end_index.grid(row=0, column=3, padx=5)
        self.end_index.insert(0, "999")
        
        # Кнопка переименования
        rename_btn = tk.Button(self.root, text="Переименовать файлы", command=self.rename_files)
        rename_btn.pack(pady=20)
        
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            
    def rename_files(self):
        if not self.folder_path.get():
            messagebox.showerror("Ошибка", "Пожалуйста, выберите папку")
            return
            
        try:
            start = int(self.start_index.get())
            end = int(self.end_index.get())
            
            if start < 1 or end < start:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные индексы")
            return
            
        # Получаем список файлов в папке
        try:
            files = [f for f in os.listdir(self.folder_path.get()) 
                    if os.path.isfile(os.path.join(self.folder_path.get(), f))]
            files.sort()
        except OSError as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать содержимое папки: {str(e)}")
            return
        
        # Проверяем, достаточно ли файлов для заданного диапазона
        if not files:
            messagebox.showerror("Ошибка", "В выбранной папке нет файлов")
            return
            
        # Определяем количество цифр для форматирования
        max_digits = len(str(max(end, len(files))))
        
        # Переименовываем файлы
        renamed_count = 0
        for i, file in enumerate(files, start=start):
            if i > end:
                break
                
            old_path = os.path.join(self.folder_path.get(), file)
            extension = os.path.splitext(file)[1]
            new_name = f"{str(i).zfill(max_digits)}{extension}"
            new_path = os.path.join(self.folder_path.get(), new_name)
            
            try:
                os.rename(old_path, new_path)
                renamed_count += 1
            except OSError as e:
                messagebox.showerror("Ошибка", f"Не удалось переименовать файл {file}: {str(e)}")
                return
        
        messagebox.showinfo("Успех", f"Успешно переименовано {renamed_count} файлов")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FileRenamer()
    app.run()