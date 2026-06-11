import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datetime

# =========================
# CONFIG LOGIN
# =========================

VALID_USERNAME = "admin8"
VALID_PASSWORD = "1234"


# =========================
# LOG SYSTEM
# =========================

class Logger:
    def __init__(self, filename="parking_log.txt"):
        self.filename = filename

    def write(self, text):
        with open(self.filename, "a") as f:
            f.write(text + "\n")

    def clear(self):
        open(self.filename, "w").close()


logger = Logger()


# =========================
# PARKING SYSTEM CLASS
# =========================

class ParkingSystem:
    def __init__(self, levels=2):
        self.levels = levels
        self.parking = {}
        self.history = []

        for i in range(1, levels + 1):
            self.parking[f"Level {i}"] = {
                "VVIP1": None,
                "VVIP2": None,
                "OKU1": None,
                "OKU2": None,
                "P1": None,
                "P2": None,
                "P3": None,
                "P4": None,
                "P5": None,
                "P6": None
            }

    # =========================
    # ASSIGN SLOT
    # =========================

    def assign(self, vehicle, category):
        if category == "VVIP":
            slots = ["VVIP1", "VVIP2"]
        elif category == "OKU":
            slots = ["OKU1", "OKU2"]
        else:
            slots = ["P1", "P2", "P3", "P4", "P5", "P6"]

        for level in self.parking:
            for slot in slots:
                if self.parking[level][slot] is None:
                    self.parking[level][slot] = vehicle

                    time_in = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    record = {
                        "vehicle": vehicle,
                        "level": level,
                        "slot": slot,
                        "in": time_in,
                        "out": None
                    }

                    self.history.append(record)

                    logger.write(f"[IN] {vehicle} {level} {slot} {time_in}")

                    return level, slot

        return None, None

    # =========================
    # EXIT VEHICLE
    # =========================

    def exit_vehicle(self, vehicle):
        for record in self.history:
            if record["vehicle"] == vehicle and record["out"] is None:
                record["out"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for level in self.parking:
            for slot in self.parking[level]:
                if self.parking[level][slot] == vehicle:
                    self.parking[level][slot] = None

                    logger.write(f"[OUT] {vehicle} {level} {slot}")

                    return True, level, slot

        return False, None, None

    # =========================
    # SEARCH
    # =========================

    def search(self, vehicle):
        for record in self.history:
            if record["vehicle"] == vehicle and record["out"] is None:
                return record
        return None

    # =========================
    # STATS
    # =========================

    def stats(self):
        total = self.levels * 10
        occupied = 0

        for level in self.parking:
            for slot in self.parking[level]:
                if self.parking[level][slot] is not None:
                    occupied += 1

        available = total - occupied
        return available, occupied


# =========================
# MAIN APP
# =========================

class App:
    def __init__(self, root):
        self.root = root
        self.system = ParkingSystem(2)

        self.root.title("SMART PARKING MANAGEMENT SYSTEM")
        self.root.geometry("1000x700")

        self.build_ui()
        self.update_dashboard()

    # =========================
    # UI DESIGN
    # =========================

    def build_ui(self):

        title = tk.Label(self.root, text="SMART PARKING MANAGEMENT SYSTEM",
                         font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # DASHBOARD
        self.dash = tk.Frame(self.root)
        self.dash.pack()

        self.total_label = tk.Label(self.dash, text="Total: 20")
        self.total_label.grid(row=0, column=0, padx=20)

        self.available_label = tk.Label(self.dash, text="Available: 20")
        self.available_label.grid(row=0, column=1)

        self.occupied_label = tk.Label(self.dash, text="Occupied: 0")
        self.occupied_label.grid(row=0, column=2)

        # INPUT
        box = tk.LabelFrame(self.root, text="Vehicle Control")
        box.pack(fill="x", padx=20, pady=10)

        tk.Label(box, text="Plate").grid(row=0, column=0)
        self.plate = tk.Entry(box)
        self.plate.grid(row=0, column=1)

        tk.Label(box, text="Type").grid(row=0, column=2)
        self.type = ttk.Combobox(box, values=["STANDARD", "VVIP", "OKU"])
        self.type.current(0)
        self.type.grid(row=0, column=3)

        tk.Button(box, text="ENTRY", command=self.entry).grid(row=0, column=4)
        tk.Button(box, text="EXIT", command=self.exit).grid(row=0, column=5)
        tk.Button(box, text="SEARCH", command=self.search).grid(row=0, column=6)
        tk.Button(box, text="RESET", command=self.reset).grid(row=0, column=7)

        # LEVEL INFO
        self.level_frame = tk.LabelFrame(self.root, text="Level Status")
        self.level_frame.pack(fill="x", padx=20, pady=10)

        self.level_labels = {}

        for i in range(1, 3):
            lbl = tk.Label(self.level_frame, text=f"Level {i}: 10/10")
            lbl.pack(anchor="w")
            self.level_labels[i] = lbl

        # MAP
        mapf = tk.LabelFrame(self.root, text="Map")
        mapf.pack(fill="x", padx=20, pady=10)

        for i in range(1, 3):
            tk.Button(mapf, text=f"View Level {i}",
                      command=lambda x=f"Level {i}": self.view(x)).pack(side="left")

        # HISTORY
        self.history_box = tk.Text(self.root, height=10)
        self.history_box.pack(fill="x", padx=20, pady=10)

    # =========================
    # FUNCTIONS
    # =========================

    def entry(self):
        v = self.plate.get().upper()
        t = self.type.get()

        if v == "":
            messagebox.showerror("Error", "Enter Plate")
            return

        level, slot = self.system.assign(v, t)

        if level:
            messagebox.showinfo("Success", f"{v}\n{level}\n{slot}")
            self.update_dashboard()
            self.refresh_history()
        else:
            messagebox.showerror("Full", "No slot")

    def exit(self):
        v = self.plate.get().upper()

        ok, level, slot = self.system.exit_vehicle(v)

        if ok:
            messagebox.showinfo("Exit", f"{v} removed")
            self.update_dashboard()
            self.refresh_history()
        else:
            messagebox.showerror("Not Found", "Vehicle not found")

    def search(self):
        v = self.plate.get().upper()

        r = self.system.search(v)

        if r:
            messagebox.showinfo("Found",
                                f"{r['vehicle']}\n{r['level']}\n{r['slot']}")
        else:
            messagebox.showerror("Not Found", "No record")

    def reset(self):
        self.system = ParkingSystem(2)
        logger.clear()
        self.update_dashboard()
        self.refresh_history()
        messagebox.showinfo("Reset", "System Reset Done")

    def update_dashboard(self):
        a, o = self.system.stats()

        self.available_label.config(text=f"Available: {a}")
        self.occupied_label.config(text=f"Occupied: {o}")

    def refresh_history(self):
        self.history_box.delete("1.0", tk.END)

        for r in self.system.history[-20:]:
            self.history_box.insert(
                tk.END,
                f"{r['vehicle']} | {r['level']} | {r['slot']} | IN:{r['in']} | OUT:{r['out']}\n"
            )

    def view(self, level):
        win = tk.Toplevel(self.root)
        win.title(level)

        data = self.system.parking[level]

        r = 0
        c = 0

        for slot, v in data.items():

            color = "lightgreen"

            if slot.startswith("VVIP"):
                color = "khaki"
            elif slot.startswith("OKU"):
                color = "lightblue"

            if v:
                color = "tomato"

            tk.Label(win, text=f"{slot}\n{v or 'EMPTY'}",
                     bg=color, width=12, height=4).grid(row=r, column=c)

            c += 1
            if c == 5:
                c = 0
                r += 1


# =========================
# LOGIN SYSTEM
# =========================
def login():
    u = user.get()
    p = pwd.get()

    if u == VALID_USERNAME and p == VALID_PASSWORD:
        messagebox.showinfo("Login", "Success")
        login_root.destroy()

        root = tk.Tk()
        App(root)
        root.mainloop()
    else:
        messagebox.showerror("Login", "Wrong credentials")

login_root = tk.Tk()
login_root.title("SMART PARKING MANAGEMENT SYSTEM - LOGIN")
login_root.geometry("1000x600") #adjust saiz login skrin

# ===== LOAD IMAGE =====
img = Image.open("parking.jpg")  # adjust letakkan gambar dalam folder yang sama
img = img.resize((250, 150))
photo = ImageTk.PhotoImage(img)

# ===== PROJECT TITLE =====
tk.Label(
    login_root,
    text="SMART PARKING MANAGEMENT SYSTEM",
    font=("Arial", 14, "bold")
).pack(pady=10)

# ===== IMAGE =====
img_label = tk.Label(login_root, image=photo)
img_label.image = photo
img_label.pack(pady=10)

# ===== LOGIN FORM =====
tk.Label(login_root, text="Username").pack()
user = tk.Entry(login_root)
user.pack(pady=5)

tk.Label(login_root, text="Password").pack()
pwd = tk.Entry(login_root, show="*")
pwd.pack(pady=5)

tk.Button(
    login_root,
    text="Login",
    command=login,
    width=15
).pack(pady=20)

login_root.mainloop()