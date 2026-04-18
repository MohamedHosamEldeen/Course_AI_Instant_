import json
from abc import ABC, abstractmethod

# ================= ABSTRACT =================
class Person(ABC):
    def __init__(self, name, age, code):
        self.name = name
        self.age = age
        self.code = code

    @abstractmethod
    def display(self):
        pass

# ================= ENTITIES =================
class Student(Person):
    def __init__(self, name, age, code, gpa, hours, subjects, department):
        super().__init__(name, age, code)
        self.gpa = gpa
        self.hours = hours
        self.subjects = subjects
        self.department = department

    def display(self):
        return (self.code, self.name, self.gpa, self.department)


class Doctor(Person):
    def __init__(self, name, age, code, subject, department, salary):
        super().__init__(name, age, code)
        self.subject = subject
        self.department = department
        self.salary = salary

    def display(self):
        return (self.code, self.name, self.subject, self.department, self.salary)


class Subject:
    def __init__(self, name, code, hours):
        self.name = name
        self.code = code
        self.hours = hours

    def display(self):
        return (self.code, self.name, self.hours)


# ================= DATABASE =================
class Database:
    def __init__(self):
        self.people = []
        self.subjects = []
        self.trash = []
        self.load()

    # ---------- SAVE ----------
    def save(self):
        data = {
            "people": [self._serialize(p) for p in self.people],
            "subjects": [self._serialize(s) for s in self.subjects],
            "trash": [self._serialize(t) for t in self.trash],
        }
        with open("data.json", "w") as f:
            json.dump(data, f)

    # ---------- LOAD ----------
    def load(self):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)

            self.people = [self._deserialize(p) for p in data.get("people", []) if p]
            self.subjects = [self._deserialize(s) for s in data.get("subjects", []) if s]
            self.trash = [self._deserialize(t) for t in data.get("trash", []) if t]
        except:
            pass

    def _serialize(self, obj):
        data = obj.__dict__.copy()
        data["type"] = obj.__class__.__name__
        return data

    def _deserialize(self, data):
        if not data:
            return None

        t = data.get("type")
        data.pop("type", None)

        if t == "Student":
            return Student(**data)
        elif t == "Doctor":
            return Doctor(**data)
        elif t == "Subject":
            return Subject(**data)

    # ---------- CRUD ----------
    def add_person(self, p):
        if any(x.code == p.code for x in self.people):
            return False
        self.people.append(p)
        self.save()
        return True

    def add_subject(self, s):
        if any(x.code == s.code for x in self.subjects):
            return False
        self.subjects.append(s)
        self.save()
        return True

    def delete(self, code):
        for i in self.people:
            if i.code == code:
                self.people.remove(i)
                self.trash.append(i)
                self.save()
                return True

        for i in self.subjects:
            if i.code == code:
                self.subjects.remove(i)
                self.trash.append(i)
                self.save()
                return True
        return False

    def restore(self, code):
        for i in self.trash:
            if i.code == code:
                if isinstance(i, Subject):
                    self.subjects.append(i)
                else:
                    self.people.append(i)
                self.trash.remove(i)
                self.save()
                return True
        return False

    def delete_forever(self, code):
        self.trash = [x for x in self.trash if x.code != code]
        self.save()
        return True

    def update(self, code, **data):
        for i in self.people + self.subjects:
            if i.code == code:
                for k, v in data.items():
                    setattr(i, k.lower(), v)
                self.save()
                return True
        return False


# ================= SYSTEM =================
class SystemManager:
    def __init__(self):
        self.db = Database()

    def add_student(self, *a):
        return self.db.add_person(Student(*a))

    def add_doctor(self, *a):
        return self.db.add_person(Doctor(*a))

    def add_subject(self, *a):
        return self.db.add_subject(Subject(*a))

    def update(self, code, **data):
        return self.db.update(code, **data)