import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# Имя файла для хранения истории
HISTORY_FILE = 'tasks.json'

# Предопределённые задачи
PREDEFINED_TASKS = [
    {"task": "Прочитать статью", "type": "учёба"},
    {"task": "Сделать зарядку", "type": "спорт"},
    {"task": "Ответить на почту", "type": "работа"},
    {"task": "Пойти погулять", "type": "спорт"},
    {"task": "Изучить новый язык", "type": "учёба"},
]

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        
        self.tasks = PREDEFINED_TASKS.copy()
        self.history = []
        self.load_history()

        self.filtered_tasks = self.tasks.copy()

        # Создаём интерфейс
        self.create_widgets()
        self.update_history_list()

    def create_widgets(self):
        # Кнопка генерации задачи
        self.generate_button = tk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_button.pack(pady=10)

        # Отображение текущей задачи
        self.current_task_label = tk.Label(self.root, text="Задача: None", font=('Arial', 14))
        self.current_task_label.pack(pady=5)

        # Фильтрация по типу
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)

        self.task_type_var = tk.StringVar(value="Все")
        filter_options = ["Все", "учёба", "спорт", "работа"]
        self.filter_combo = ttk.Combobox(filter_frame, textvariable=self.task_type_var, values=filter_options, state="readonly")
        self.filter_combo.pack(side=tk.LEFT)
        self.filter_combo.bind("<<ComboboxSelected>>", self.apply_filter)

        # История задач
        self.history_label = tk.Label(self.root, text="История задач:")
        self.history_label.pack()

        self.history_listbox = tk.Listbox(self.root, width=50, height=10)
        self.history_listbox.pack()

        # Добавление новой задачи
        add_frame = tk.Frame(self.root)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Новая задача:").pack(side=tk.LEFT)
        self.new_task_entry = tk.Entry(add_frame)
        self.new_task_entry.pack(side=tk.LEFT)

        tk.Label(add_frame, text="Тип:").pack(side=tk.LEFT)
        self.new_task_type_entry = tk.Entry(add_frame, width=10)
        self.new_task_type_entry.pack(side=tk.LEFT)

        self.add_task_button = tk.Button(add_frame, text="Добавить задачу", command=self.add_task)
        self.add_task_button.pack(side=tk.LEFT, padx=5)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []

    def save_history(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def generate_task(self):
        if not self.filtered_tasks:
            messagebox.showinfo("Информация", "Нет задач для выбранного фильтра.")
            return
        task = random.choice(self.filtered_tasks)
        self.current_task_label.config(text=f"Задача: {task['task']} ({task['type']})")
        # Добавляем в историю
        self.history.append(task)
        self.save_history()
        self.update_history_list()

    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.history, 1):
            self.history_listbox.insert(tk.END, f"{idx}. {task['task']} ({task['type']})")

    def apply_filter(self, event=None):
        selected_type = self.task_type_var.get()
        if selected_type == "Все":
            self.filtered_tasks = self.tasks
        else:
            self.filtered_tasks = [t for t in self.tasks if t['type'] == selected_type]

    def add_task(self):
        task_text = self.new_task_entry.get().strip()
        task_type = self.new_task_type_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Предупреждение", "Введите текст задачи.")
            return
        if not task_type:
            messagebox.showwarning("Предупреждение", "Введите тип задачи.")
            return
        new_task = {"task": task_text, "type": task_type}
        self.tasks.append(new_task)
        # Обновляем текущий фильтр
        self.apply_filter()
        # Очищаем поля
        self.new_task_entry.delete(0, tk.END)
        self.new_task_type_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Задача добавлена.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
