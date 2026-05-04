import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

DATA_FILE = "trainings.json"

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("600x550")
        
        self.trainings = self.load_data()

        # --- Блок ввода данных ---
        input_frame = tk.LabelFrame(root, text="Новая тренировка", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky="w")
        self.entry_date = tk.Entry(input_frame)
        self.entry_date.grid(row=0, column=1, pady=2)

        tk.Label(input_frame, text="Тип тренировки:").grid(row=1, column=0, sticky="w")
        self.entry_type = tk.Entry(input_frame)
        self.entry_type.grid(row=1, column=1, pady=2)

        tk.Label(input_frame, text="Длительность (мин):").grid(row=2, column=0, sticky="w")
        self.entry_duration = tk.Entry(input_frame)
        self.entry_duration.grid(row=2, column=1, pady=2)

        btn_add = tk.Button(input_frame, text="Добавить тренировку", command=self.add_training, bg="#e1e1e1")
        btn_add.grid(row=3, column=0, columnspan=2, pady=10, sticky="we")

        # --- Блок фильтрации ---
        filter_frame = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="По типу:").grid(row=0, column=0)
        self.filter_type = tk.Entry(filter_frame)
        self.filter_type.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="По дате:").grid(row=0, column=2)
        self.filter_date = tk.Entry(filter_frame)
        self.filter_date.grid(row=0, column=3, padx=5)

        btn_filter = tk.Button(filter_frame, text="Применить", command=self.refresh_table)
        btn_filter.grid(row=0, column=4, padx=5)

        btn_reset = tk.Button(filter_frame, text="Сброс", command=self.reset_filter)
        btn_reset.grid(row=0, column=5, padx=5)

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("Date", "Type", "Duration"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Type", text="Тип тренировки")
        self.tree.heading("Duration", text="Длительность (мин)")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_table()

    def add_training(self):
        date_val = self.entry_date.get().strip()
        type_val = self.entry_type.get().strip()
        dur_val = self.entry_duration.get().strip()

        # Валидация (Пункт 5)
        try:
            datetime.strptime(date_val, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Формат даты должен быть ДД.ММ.ГГГГ")
            return

        if not type_val:
            messagebox.showerror("Ошибка", "Введите тип тренировки")
            return

        try:
            if int(dur_val) <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        # Сохранение (Пункт 4)
        new_entry = {"date": date_val, "type": type_val, "duration": dur_val}
        self.trainings.append(new_entry)
        self.save_data()
        self.refresh_table()
        
        # Очистка полей
        self.entry_date.delete(0, tk.END)
        self.entry_type.delete(0, tk.END)
        self.entry_duration.delete(0, tk.END)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return []
        return []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def reset_filter(self):
        self.filter_type.delete(0, tk.END)
        self.filter_date.delete(0, tk.END)
        self.refresh_table()

    def refresh_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        f_type = self.filter_type.get().lower()
        f_date = self.filter_date.get()

        # Реализация фильтрации (Пункт 3)
        for t in self.trainings:
            match_type = f_type in t["type"].lower()
            match_date = f_date in t["date"]
            
            if match_type and match_date:
                self.tree.insert("", "end", values=(t["date"], t["type"], t["duration"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()
