import tkinter as tk
from tkinter import messagebox, ttk
import re

class Name:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

class Person:
    def __init__(self, name_obj, nin):
        self.name = name_obj
        self.nin = nin

    def get_name(self):
        return self.name

    def get_nin(self):
        return self.nin

class Registration:
    MAX_COURSES = 5
    AVAILABLE_COURSES = [
        "Automation & Robotics", "MEMS & VLSI", "System Modelling & Simulation", 
        "Power Electronics & Drives", "Full Automation LAB", "Engineering Law",
        "Project"
    ]

    def __init__(self, person_obj, courses):
        self.person = person_obj
        self.courses = courses

    def has_too_many_courses(self):
        return len(self.courses) > self.MAX_COURSES

    def get_registration_details(self):
        details = []
        details.append(f"📌 Student: {self.person.get_name().get_full_name()}")
        details.append(f"🆔 NIN: {self.person.get_nin()}")
        details.append(f"📚 Registered Courses ({len(self.courses)}/{self.MAX_COURSES}):")
        for course in self.courses:
            details.append(f" - {course}")
        if self.has_too_many_courses():
            details.append("⚠️ Too many courses! Limit is 5.")
        else:
            details.append("✅ Registration is valid.")
        return "\n".join(details)

class RegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Student Registration System")
        self.root.geometry("600x500")
        self.root.configure(bg="#4a6fa5")
        
        self.registration = None
        self.selected_courses = []
        
        self.create_welcome_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_welcome_screen(self):
        self.clear_window()
        
        # Header
        header = tk.Label(self.root, text="🎓 Student Registration System", 
                         font=("Arial", 20, "bold"), bg="#4a6fa5", fg="white")
        header.pack(pady=20)
        
        # Start Button
        start_btn = tk.Button(self.root, text="Start Registration", 
                             command=self.create_personal_info_screen,
                             bg="#28a745", fg="white", font=("Arial", 14),
                             padx=20, pady=10, bd=0)
        start_btn.pack(pady=50)

    def create_personal_info_screen(self):
        self.clear_window()
        
        # Header
        header = tk.Label(self.root, text="Personal Information", 
                         font=("Arial", 18, "bold"), bg="#4a6fa5", fg="white")
        header.pack(pady=20)
        
        # Form Frame
        form_frame = tk.Frame(self.root, bg="#4a6fa5")
        form_frame.pack(pady=20)
        
        # First Name
        tk.Label(form_frame, text="First Name:", bg="#4a6fa5", fg="white",
                font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.first_name_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Last Name
        tk.Label(form_frame, text="Last Name:", bg="#4a6fa5", fg="white",
                font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.last_name_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # NIN
        tk.Label(form_frame, text="NIN (10 digits):", bg="#4a6fa5", fg="white",
                font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.nin_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.nin_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Next Button
        next_btn = tk.Button(self.root, text="Next →", 
                            command=self.validate_personal_info,
                            bg="#ffc107", fg="black", font=("Arial", 12),
                            padx=15, pady=5)
        next_btn.pack(pady=20)

    def validate_personal_info(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        nin = self.nin_entry.get().strip()
        
        if not first_name or not last_name:
            messagebox.showerror("Error", "Please enter both first and last name")
            return
            
        if not re.match(r'^\d{10}$', nin):
            messagebox.showerror("Error", "NIN must be exactly 10 digits")
            return
            
        name_obj = Name(first_name, last_name)
        person_obj = Person(name_obj, nin)
        self.registration = Registration(person_obj, [])
        
        self.create_course_selection_screen()

    def create_course_selection_screen(self):
        self.clear_window()
        
        # Header
        header = tk.Label(self.root, text="Course Selection", 
                         font=("Arial", 18, "bold"), bg="#4a6fa5", fg="white")
        header.pack(pady=20)
        
        # Instructions
        tk.Label(self.root, 
                text=f"Select up to {Registration.MAX_COURSES} courses\n(Click to select/deselect)",
                bg="#4a6fa5", fg="white", font=("Arial", 12)).pack()
        
        # Course List Frame
        list_frame = tk.Frame(self.root, bg="#4a6fa5")
        list_frame.pack(pady=20)
        
        # Create listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self.course_listbox = tk.Listbox(list_frame, 
                                       selectmode=tk.MULTIPLE,
                                       yscrollcommand=scrollbar.set,
                                       font=("Arial", 12),
                                       width=30, height=8)
        scrollbar.config(command=self.course_listbox.yview)
        
        # Populate courses
        for course in Registration.AVAILABLE_COURSES:
            self.course_listbox.insert(tk.END, course)
        
        self.course_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action Buttons
        btn_frame = tk.Frame(self.root, bg="#4a6fa5")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Submit Registration", 
                 command=self.submit_registration,
                 bg="#28a745", fg="white", font=("Arial", 12),
                 padx=10, pady=5).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="← Back", 
                 command=self.create_personal_info_screen,
                 bg="#6c757d", fg="white", font=("Arial", 12),
                 padx=10, pady=5).pack(side=tk.LEFT, padx=10)

    def submit_registration(self):
        selected_indices = self.course_listbox.curselection()
        selected_courses = [Registration.AVAILABLE_COURSES[i] for i in selected_indices]
        
        if len(selected_courses) > Registration.MAX_COURSES:
            messagebox.showerror("Error", 
                               f"You can only select up to {Registration.MAX_COURSES} courses")
            return
            
        self.registration.courses = selected_courses
        self.create_registration_summary()

    def create_registration_summary(self):
        self.clear_window()
        
        # Header
        header = tk.Label(self.root, text="Registration Summary", 
                         font=("Arial", 18, "bold"), bg="#4a6fa5", fg="white")
        header.pack(pady=20)
        
        # Details Frame
        details_frame = tk.Frame(self.root, bg="#4a6fa5")
        details_frame.pack(pady=20)
        
        # Display registration details
        details = self.registration.get_registration_details().split("\n")
        for detail in details:
            tk.Label(details_frame, text=detail, bg="#4a6fa5", fg="white",
                    font=("Arial", 12), justify=tk.LEFT).pack(anchor="w", padx=20, pady=5)
        
        # Action Buttons
        btn_frame = tk.Frame(self.root, bg="#4a6fa5")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Edit Courses", 
                 command=self.create_course_selection_screen,
                 bg="#ffc107", fg="black", font=("Arial", 12),
                 padx=10, pady=5).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="New Registration", 
                 command=self.create_welcome_screen,
                 bg="#17a2b8", fg="white", font=("Arial", 12),
                 padx=10, pady=5).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="Exit", 
                 command=self.root.quit,
                 bg="#dc3545", fg="white", font=("Arial", 12),
                 padx=10, pady=5).pack(side=tk.LEFT, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()