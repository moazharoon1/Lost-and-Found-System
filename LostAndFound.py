# Import necessary libraries
import tkinter as tk
import tkinter.messagebox as messagebox
import pyodbc
import webbrowser

# Define the LostAndFoundSystem class
class LostAndFoundSystem:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Lost and Found Management System")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.student_button = tk.Button(root, text="Student", command=self.open_student_dashboard)
        self.student_button.pack(pady=10)
        self.prefect_button = tk.Button(root, text="Prefect", command=self.open_admin_login)
        self.prefect_button.pack(pady=10)

    def open_student_dashboard(self):
        self.root.destroy()
        root_student = tk.Tk()
        dashboard_student = StudentDashboard(root_student)
        root_student.mainloop()

    def open_admin_login(self):
        self.root.destroy()
        root_admin_login = tk.Tk()
        admin_login = AdminLogin(root_admin_login)
        root_admin_login.mainloop()

# Define the AdminLogin class
class AdminLogin:
    def __init__(self, root):
        # Initialize the admin login window
        self.root = root
        self.root.title("Admin Login")
        conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=LOCALHOST\\SQLEXPRESS;DATABASE=LostAndFound;Trusted_Connection=yes;'
        self.conn = pyodbc.connect(conn_str)
        self.create_tables()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.email_label = tk.Label(root, text="Email:")
        self.email_entry = tk.Entry(root)
        self.password_label = tk.Label(root, text="Password:")
        self.password_entry = tk.Entry(root, show="*")
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.student_button = tk.Button(root, text="I'm a student", command=self.show_student_dashboard)
        self.email_label.pack(pady=5)
        self.email_entry.pack(pady=5)
        self.password_label.pack(pady=5)
        self.password_entry.pack(pady=5)
        self.login_button.pack(pady=10)
        self.student_button.pack(pady=10)

    def show_student_dashboard(self):
        self.root.destroy()
        root_student = tk.Tk()
        dashboard_student = StudentDashboard(root_student)
        root_student.mainloop()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        self.show_prefect_dashboard() if self.validate_user(email, password) else messagebox.showinfo("Login Failed", "Invalid email or password")

    def show_prefect_dashboard(self):
        self.root.destroy()
        root_prefect = tk.Tk()
        dashboard_prefect = PrefectDashboard(root_prefect, self.conn)
        root_prefect.mainloop()

    def validate_user(self, email, password):
        with self.conn:
            return self.conn.execute('SELECT * FROM UserCredentials WHERE email = ? AND password = ?', (email, password)).fetchone() is not None

    def create_tables(self):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                SELECT * FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'UserCredentials' AND TABLE_SCHEMA = 'dbo'
            ''')
            if not cursor.fetchone():
                cursor.execute('''
                    CREATE TABLE UserCredentials (
                        id INT PRIMARY KEY IDENTITY(1,1),
                        email NVARCHAR(255) UNIQUE NOT NULL,
                        password NVARCHAR(255) NOT NULL,
                        userRole NVARCHAR(255) NOT NULL
                    );
                ''')
                cursor.execute('''
                    INSERT INTO UserCredentials (email, password, userRole)
                    VALUES (?, ?, ?)
                ''', ('123', '123', 'prefect'))

# Define the TechItems, Clothings, and SchoolStuffs classes
class TechItems:
    category_name = "techItems"
class Clothings:
    category_name = "clothings"
class SchoolStuffs:
    category_name = "schoolStuffs"

# Define the ItemCategory class
class ItemCategory:
    def __init__(self, root, conn, category_name):
        # Initialize the item category dashboard
        self.root = root
        self.conn = conn
        self.category_name = category_name
        self.items = []
        self.register_item_window = None  # Define register_item_window here
        with self.conn.cursor() as cursor:
            cursor.execute(f'''
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES 
                                WHERE TABLE_NAME = '{category_name}' AND TABLE_SCHEMA = 'dbo')
                BEGIN
                    CREATE TABLE {category_name} (
                        id INT PRIMARY KEY IDENTITY(1,1),
                        owner NVARCHAR(255) NOT NULL,
                        status NVARCHAR(50) NOT NULL,
                        type NVARCHAR(50) NOT NULL,
                        date_lost DATE
                    );
                END
            ''')
        screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
        window_width, window_height = screen_width // 2, screen_height // 2
        x_position, y_position = (screen_width - window_width) // 2, (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.title(f"{category_name} Dashboard")
        self.register_item_button = tk.Button(root, text=f"Register {category_name} Item", command=self.show_register_item_window)
        self.view_items_button = tk.Button(root, text=f"View {category_name} Items", command=self.view_items)
        self.register_item_button.pack(pady=10)
        self.view_items_button.pack(pady=10)

    def show_register_item_window(self):
        self.register_item_window = tk.Toplevel(self.root)  
        self.register_item_window.title(f"Register {self.category_name} Item")
        window_width, window_height = self.root.winfo_screenwidth() // 2, self.root.winfo_screenheight() // 2
        x_position, y_position = (self.root.winfo_screenwidth() - window_width) // 2, (self.root.winfo_screenheight() - window_height) // 2
        self.register_item_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        labels_and_entries = [(tk.Label(self.register_item_window, text="Owner:"), tk.Entry(self.register_item_window)),
            (tk.Label(self.register_item_window, text="Status (Missing/Found):"), tk.Entry(self.register_item_window)),
            (tk.Label(self.register_item_window, text="Type (Subcategory):"), tk.Entry(self.register_item_window)),
            (tk.Label(self.register_item_window, text="Date Lost (YYYY-MM-DD):"), tk.Entry(self.register_item_window))]
        [label.grid(row=i, column=0, pady=5, padx=5, sticky="e") for i, (label, entry) in enumerate(labels_and_entries)], [entry.grid(row=i, column=1, pady=5, padx=5, sticky="w") for i, (label, entry) in enumerate(labels_and_entries)]
        register_button = tk.Button(self.register_item_window, text=f"Register {self.category_name} Item", command=self.register_item)
        register_button.grid(row=len(labels_and_entries), columnspan=2, pady=10)

    def register_item(self):
        values = [entry.get() for entry in self.register_item_window.winfo_children() if isinstance(entry, tk.Entry)]
        with self.conn.cursor() as cursor:
            cursor.execute(f'''
                INSERT INTO {self.category_name} (owner, status, type, date_lost)
                VALUES (?, ?, ?, ?)
            ''', values)
        self.conn.commit()
        messagebox.showinfo("Item Registered", f"{self.category_name} item registered successfully.")
        self.register_item_window.destroy()  # Use self.register_item_window here

    def view_items(self):
        view_items_window = tk.Toplevel(self.root)
        view_items_window.title(f"View {self.category_name} Items")
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {self.category_name}')
            items = cursor.fetchall()
        listbox = tk.Listbox(view_items_window, width=50, height=10)
        [listbox.insert(tk.END, f"ID: {item[0]}, Owner: {item[1]}, Status: {item[2]}, Type: {item[3]}, Date Lost: {item[4]}") for item in items]

        def delete_item():
            selected_index = listbox.curselection()
            if selected_index:
                item_id = items[selected_index[0]][0]
                confirmation = messagebox.askyesno("Delete Item", "Are you sure you want to delete this item?")
                if confirmation:
                    with self.conn.cursor() as cursor:
                        cursor.execute(f'DELETE FROM {self.category_name} WHERE id = ?', (item_id,))
                    self.conn.commit()
                    messagebox.showinfo("Item Deleted", f"{self.category_name} item has been deleted successfully.")
                    view_items_window.destroy()
                    self.view_items()
        
        def on_item_select(event):
            selected_index = listbox.curselection()
            if selected_index:
                item_id, current_status = items[selected_index[0]][0], items[selected_index[0]][2]
                [button.config(state="normal", command=lambda: self.change_subcategory(item_id)) for button in (change_subcategory_button, change_status_button)]
                change_status_button.config(command=lambda: self.change_status(item_id, current_status))
        listbox.bind("<<ListboxSelect>>", on_item_select)
        listbox.pack(pady=10)
        change_subcategory_button = tk.Button(view_items_window, text="Change Subcategory", state="disabled")
        change_subcategory_button.pack(pady=5)
        change_status_button = tk.Button(view_items_window, text="Change Status", state="disabled")
        change_status_button.pack(pady=5)
        delete_button = tk.Button(view_items_window, text="Delete Item", command=delete_item)
        delete_button.pack(pady=10)
        close_button = tk.Button(view_items_window, text="Close", command=view_items_window.destroy)
        close_button.pack(pady=10)

    def change_subcategory(self, item_id):
        change_subcategory_window = tk.Toplevel(self.root)
        change_subcategory_window.title(f"Change Subcategory")
        subcategory_label, subcategory_entry = tk.Label(change_subcategory_window, text="New Subcategory:"), tk.Entry(change_subcategory_window)
        subcategory_label.pack(pady=5)
        subcategory_entry.pack(pady=5)

        def save_changes():
            new_subcategory = subcategory_entry.get()
            with self.conn.cursor() as cursor:
                cursor.execute(f'UPDATE {self.category_name} SET type = ? WHERE id = ?', (new_subcategory, item_id))
            self.conn.commit()
            messagebox.showinfo("Subcategory Changed", f"Subcategory of item {item_id} changed successfully.")
            change_subcategory_window.destroy()
        save_button = tk.Button(change_subcategory_window, text="Save", command=save_changes)
        save_button.pack(pady=10)

    def change_status(self, item_id, current_status):
        new_status = "Missing" if current_status == "Found" else "Found"
        with self.conn.cursor() as cursor:
            cursor.execute(f'UPDATE {self.category_name} SET status = ? WHERE id = ?', (new_status, item_id))
        self.conn.commit()
        messagebox.showinfo("Status Updated", f"Status of item {item_id} changed to {new_status}.")

# Define the PrefectDashboard class
class PrefectDashboard:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.categories = ["TechItems", "Clothings", "SchoolStuffs"]
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.title("Prefect Dashboard")
        self.category_buttons = []
        for category in self.categories:
            button = tk.Button(root, text=f"Manage {category}", command=lambda cat=category: self.show_category_dashboard(cat))
            self.category_buttons.append(button)
            button.pack(pady=10)

    def show_category_dashboard(self, category):
        root_category = tk.Tk()
        category_dashboard = ItemCategory(root_category, self.conn, category)
        root_category.mainloop()

class StudentDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Dashboard")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.lost_tech_button = tk.Button(root, text="Lost Technology", command=lambda: self.send_email("Lost Technology"))
        self.lost_clothing_button = tk.Button(root, text="Lost Clothing", command=lambda: self.send_email("Lost Clothing"))
        self.lost_school_stuff_button = tk.Button(root, text="Lost School Stuff", command=lambda: self.send_email("Lost School Stuff"))
        self.found_item_button = tk.Button(root, text="Found Item", command=lambda: self.send_email("Found Item"))
        self.view_items_button = tk.Button(root, text="View Lost Items", command=self.view_items)
        self.lost_tech_button.pack(pady=10)
        self.lost_clothing_button.pack(pady=10)
        self.lost_school_stuff_button.pack(pady=10)
        self.found_item_button.pack(pady=10)
        self.view_items_button.pack(pady=10)

    def send_email(self, category):
        receiver_email = ""  # Outlook account of recipient 
        subject = f"Lost Item Report - Category: {category}"
        body = ""
        body = "Username: [Username]\nStatus: FOUND\nSubcategory: [Subcategory]" if category == "Found Item" else "Username: [Username]\nStatus: MISSING\nSubcategory: [Subcategory]\nDate Lost: [Date Lost]"
        body = body.replace("\n", "%0D%0A")
        mailto_url = f"mailto:{receiver_email}?subject={subject}&body={body}"
        webbrowser.open(mailto_url)

    def view_items(self):
        view_items_window = tk.Toplevel(self.root)
        view_items_window.title("View Lost Items")
        listbox = tk.Listbox(view_items_window, width=50, height=10)
        listbox.pack(pady=10)
        def close_window():
            view_items_window.destroy()
        close_button = tk.Button(view_items_window, text="Close", command=close_window)
        close_button.pack(pady=10)

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = LostAndFoundSystem(root)
    root.mainloop()