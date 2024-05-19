import tkinter as tk
from tkinter import messagebox
from database import ToDoDatabase

class ToDoApp:
    def __init__(self, root):
        self.db = ToDoDatabase()
        self.root = root
        self.root.title("To-Do List Application")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.task_label = tk.Label(self.frame, text="Task")
        self.task_label.grid(row=0, column=0)
        self.task_entry = tk.Entry(self.frame, width=50)
        self.task_entry.grid(row=0, column=1, columnspan=4)

        self.deadline_label = tk.Label(self.frame, text="Deadline (YYYY-MM-DD)")
        self.deadline_label.grid(row=1, column=0)
        self.deadline_entry = tk.Entry(self.frame)
        self.deadline_entry.grid(row=1, column=1)

        self.priority_label = tk.Label(self.frame, text="Priority")
        self.priority_label.grid(row=1, column=2)
        self.priority_entry = tk.Entry(self.frame)
        self.priority_entry.grid(row=1, column=3)

        self.category_label = tk.Label(self.frame, text="Category")
        self.category_label.grid(row=1, column=4)
        self.category_entry = tk.Entry(self.frame)
        self.category_entry.grid(row=1, column=5)

        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=2, column=1, pady=10)

        self.list_button = tk.Button(self.frame, text="List Tasks", command=self.list_tasks)
        self.list_button.grid(row=2, column=2, pady=10)

        self.delete_button = tk.Button(self.frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=3, pady=10)

        self.task_listbox = tk.Listbox(root, width=100, height=15)
        self.task_listbox.pack(pady=20)

        self.task_listbox.bind('<Double-1>', self.edit_task)

    def add_task(self):
        task = self.task_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()
        category = self.category_entry.get()

        if not task:
            messagebox.showwarning("Warning", "Task cannot be empty")
            return

        self.db.add_task(task, deadline, priority, category)
        self.task_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.list_tasks()

    def list_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.db.list_tasks()
        for task in tasks:
            task_str = f"{task[0]}. {task[1]} (Deadline: {task[2]}, Priority: {task[3]}, Category: {task[4]})"
            self.task_listbox.insert(tk.END, task_str)

    def edit_task(self, event):
        selected_task = self.task_listbox.get(self.task_listbox.curselection())
        task_id = int(selected_task.split('.')[0])

        task = self.db.get_task(task_id)
        if task:
            self.edit_window = tk.Toplevel(self.root)
            self.edit_window.title("Edit Task")

            tk.Label(self.edit_window, text="Task").grid(row=0, column=0)
            task_entry = tk.Entry(self.edit_window, width=50)
            task_entry.grid(row=0, column=1)
            task_entry.insert(0, task[1])

            tk.Label(self.edit_window, text="Deadline (YYYY-MM-DD)").grid(row=1, column=0)
            deadline_entry = tk.Entry(self.edit_window)
            deadline_entry.grid(row=1, column=1)
            deadline_entry.insert(0, task[2])

            tk.Label(self.edit_window, text="Priority").grid(row=2, column=0)
            priority_entry = tk.Entry(self.edit_window)
            priority_entry.grid(row=2, column=1)
            priority_entry.insert(0, task[3])

            tk.Label(self.edit_window, text="Category").grid(row=3, column=0)
            category_entry = tk.Entry(self.edit_window)
            category_entry.grid(row=3, column=1)
            category_entry.insert(0, task[4])

            tk.Button(self.edit_window, text="Save", command=lambda: self.update_task(task_id, task_entry.get(), deadline_entry.get(), priority_entry.get(), category_entry.get())).grid(row=4, column=1, pady=10)

    def update_task(self, task_id, task, deadline, priority, category):
        self.db.update_task(task_id, task, deadline, priority, category)
        self.edit_window.destroy()
        self.list_tasks()

    def delete_task(self):
        selected_task = self.task_listbox.curselection()
        if not selected_task:
            messagebox.showwarning("Warning", "No task selected")
            return

        task_id = int(self.task_listbox.get(selected_task).split('.')[0])
        self.db.remove_task(task_id)
        self.list_tasks()
