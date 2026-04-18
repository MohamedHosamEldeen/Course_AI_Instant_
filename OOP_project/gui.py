import tkinter as tk
from tkinter import ttk, messagebox
from models import SystemManager, Student, Doctor, Subject


class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("University System Pro")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f4f6f9")

        self.m = SystemManager()
        self.mode = "student"
        self.selected_code = None
        self.edit_mode = False

        # ================= ICONS =================
        self.icons = {
            "student": tk.PhotoImage(width=20, height=20),
            "doctor": tk.PhotoImage(width=20, height=20),
            "subject": tk.PhotoImage(width=20, height=20),
        }

        self.icons["student"].put("#2ecc71", to=(0,0,20,20))
        self.icons["doctor"].put("#3498db", to=(0,0,20,20))
        self.icons["subject"].put("#f39c12", to=(0,0,20,20))

        # ================= LEFT MENU =================
        self.left = tk.Frame(root, bg="#2c3e50", width=220)
        self.left.pack(side="left", fill="y")

        self.right = tk.Frame(root, bg="#f4f6f9")
        self.right.pack(side="right", fill="both", expand=True)

        tk.Label(self.left, text="SYSTEM",
                 bg="#2c3e50", fg="white",
                 font=("Arial", 20, "bold")).pack(pady=20)

        btn = {"bg": "#34495e", "fg": "white", "bd": 0,
               "pady": 12, "font": ("Arial", 11)}

        tk.Button(self.left, text="👨‍🎓 Students",
                  command=lambda: self.switch("student"), **btn).pack(fill="x")

        tk.Button(self.left, text="👨‍🏫 Doctors",
                  command=lambda: self.switch("doctor"), **btn).pack(fill="x")

        tk.Button(self.left, text="📚 Subjects",
                  command=lambda: self.switch("subject"), **btn).pack(fill="x")

        tk.Button(self.left, text="🗑 Trash",
                  command=self.open_trash,
                  bg="#e74c3c", fg="white",
                  font=("Arial", 11)).pack(fill="x", pady=20)

        # ================= TITLE =================
        self.title = tk.Label(self.right, text="",
                              font=("Arial", 24, "bold"),
                              bg="#f4f6f9", fg="#2c3e50")
        self.title.pack(pady=10)

        # ================= FORM =================
        self.form = tk.Frame(self.right, bg="#f4f6f9")
        self.form.pack()

        self.btns = tk.Frame(self.right, bg="#f4f6f9")
        self.btns.pack(pady=10)

        self.tree = ttk.Treeview(self.right)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.select_row)

        self.entries = {}

        self.build_student()

    # ================= CLEAR =================
    def clear(self):
        for w in self.form.winfo_children():
            w.destroy()
        for w in self.btns.winfo_children():
            w.destroy()
        self.entries = {}
        self.selected_code = None
        self.edit_mode = False

    # ================= FIELD =================
    def field(self, name, i):
        tk.Label(self.form, text=name,
                 bg="#f4f6f9",
                 font=("Arial", 11)).grid(row=i, column=0, padx=5, pady=3)

        e = tk.Entry(self.form, font=("Arial", 11))
        e.grid(row=i, column=1, padx=5, pady=3)
        self.entries[name] = e

    # ================= VIEWS =================
    def build_student(self):
        self.clear()
        self.mode = "student"
        self.title.config(text="👨‍🎓 Students")

        for i, f in enumerate(["Name","Age","Code","GPA","Hours","Subjects","Department"]):
            self.field(f, i)

        self.buttons()
        self.table(["Icon","Code","Name","GPA","Department"])
        self.view()

    def build_doctor(self):
        self.clear()
        self.mode = "doctor"
        self.title.config(text="👨‍🏫 Doctors")

        for i, f in enumerate(["Name","Age","Code","Subject","Department","Salary"]):
            self.field(f, i)

        self.buttons()
        self.table(["Icon","Code","Name","Subject","Department","Salary"])
        self.view()

    def build_subject(self):
        self.clear()
        self.mode = "subject"
        self.title.config(text="📚 Subjects")

        for i, f in enumerate(["Name","Code","Hours"]):
            self.field(f, i)

        self.buttons()
        self.table(["Icon","Code","Name","Hours"])
        self.view()

    # ================= BUTTONS =================
    def buttons(self):
        tk.Button(self.btns, text="Add / Save",
                  bg="#2ecc71", fg="white",
                  command=self.add).grid(row=0, column=0, padx=5)

        tk.Button(self.btns, text="Delete",
                  bg="#e74c3c", fg="white",
                  command=self.delete_selected).grid(row=0, column=1, padx=5)

        tk.Button(self.btns, text="Edit",
                  bg="#f39c12", fg="white",
                  command=self.edit).grid(row=0, column=2, padx=5)

        tk.Button(self.btns, text="View",
                  bg="#3498db", fg="white",
                  command=self.view).grid(row=0, column=3, padx=5)

    # ================= TABLE =================
    def table(self, cols):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = cols
        self.tree["show"] = "headings"

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130)

    # ================= VIEW =================
    def view(self):
        self.tree.delete(*self.tree.get_children())

        if self.mode == "student":
            for p in self.m.db.people:
                if isinstance(p, Student):
                    self.tree.insert("", "end",
                                     values=(self.icons["student"],
                                             p.code, p.name, p.gpa, p.department))

        elif self.mode == "doctor":
            for p in self.m.db.people:
                if isinstance(p, Doctor):
                    self.tree.insert("", "end",
                                     values=(self.icons["doctor"],
                                             p.code, p.name, p.subject,
                                             p.department, p.salary))

        else:
            for s in self.m.db.subjects:
                self.tree.insert("", "end",
                                 values=(self.icons["subject"],
                                         s.code, s.name, s.hours))

    # ================= SELECT =================
    def select_row(self, event):
        row = self.tree.focus()
        val = self.tree.item(row, "values")
        if val:
            self.selected_code = val[1]

    # ================= ADD / EDIT =================
    def add(self):
        d = {k: v.get() for k, v in self.entries.items()}

        if "" in d.values():
            messagebox.showerror("Error", "Fill all fields")
            return

        if self.edit_mode:
            d.pop("Code", None)  
            self.m.update(self.selected_code, **d)

        else:
            if self.mode == "student":
                self.m.add_student(d["Name"], int(d["Age"]), d["Code"],
                                   float(d["GPA"]), int(d["Hours"]),
                                   d["Subjects"], d["Department"])

            elif self.mode == "doctor":
                self.m.add_doctor(d["Name"], int(d["Age"]), d["Code"],
                                  d["Subject"], d["Department"], float(d["Salary"]))

            else:
                self.m.add_subject(d["Name"], d["Code"], int(d["Hours"]))

        self.view()

    # ================= EDIT =================
    def edit(self):
        if not self.selected_code:
            messagebox.showerror("Error", "Select item first")
            return
        self.edit_mode = True

    # ================= DELETE =================
    def delete_selected(self):
        if self.selected_code:
            self.m.db.delete(self.selected_code)
            self.view()

    # ================= TRASH =================
    def open_trash(self):
        win = tk.Toplevel(self.root)
        win.title("Trash")
        win.geometry("650x420")

        tree = ttk.Treeview(win)
        tree.pack(fill="both", expand=True)

        tree["columns"] = ("Code","Name","Type")
        tree["show"] = "headings"

        for c in tree["columns"]:
            tree.heading(c, text=c)
            tree.column(c, width=180)

        def load():
            tree.delete(*tree.get_children())
            for i in self.m.db.trash:
                tree.insert("", "end",
                            values=(i.code, getattr(i, "name", ""), type(i).__name__))

        def restore():
            sel = tree.focus()
            val = tree.item(sel, "values")
            if val:
                self.m.db.restore(val[0])
                load()
                self.view()

        def delete_forever():
            sel = tree.focus()
            val = tree.item(sel, "values")
            if val:
                self.m.db.delete_forever(val[0])
                load()

        tk.Button(win, text="Restore", bg="green", fg="white",
                  command=restore).pack()

        tk.Button(win, text="Delete Forever", bg="red", fg="white",
                  command=delete_forever).pack()

        load()

    # ================= SWITCH =================
    def switch(self, mode):
        if mode == "student":
            self.build_student()
        elif mode == "doctor":
            self.build_doctor()
        else:
            self.build_subject()


# ================= RUN =================
root = tk.Tk()
app = AppGUI(root)

def on_close():
    app.m.db.save()   
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()