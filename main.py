import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        # Data file
        self.data_file = "inventory_data.json"
        self.inventory = self.load_data()

        # Create interface
        self.create_widgets()
        self.refresh_table()

    def load_data(self):
        """Load data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_data(self):
        """Save data to file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.inventory, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        # Title frame
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(title_frame, text="Inventory Management System",
                               font=("Arial", 20, "bold"),
                               bg="#2c3e50", fg="white")
        title_label.pack(pady=15)

        # Input frame
        input_frame = tk.LabelFrame(self.root, text="Add/Edit Product",
                                    font=("Arial", 12, "bold"),
                                    bg="#ecf0f1", padx=20, pady=15)
        input_frame.pack(fill=tk.X, padx=20, pady=10)

        # Input fields
        fields_frame = tk.Frame(input_frame, bg="#ecf0f1")
        fields_frame.pack()

        # Product code
        tk.Label(fields_frame, text="Product Code:", font=("Arial", 10),
                 bg="#ecf0f1").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.code_entry = tk.Entry(fields_frame, font=("Arial", 10), width=20)
        self.code_entry.grid(row=0, column=1, padx=5, pady=5)

        # Product name
        tk.Label(fields_frame, text="Product Name:", font=("Arial", 10),
                 bg="#ecf0f1").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(fields_frame, font=("Arial", 10), width=25)
        self.name_entry.grid(row=0, column=3, padx=5, pady=5)

        # Quantity
        tk.Label(fields_frame, text="Quantity:", font=("Arial", 10),
                 bg="#ecf0f1").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.quantity_entry = tk.Entry(fields_frame, font=("Arial", 10), width=20)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        # Price
        tk.Label(fields_frame, text="Price:", font=("Arial", 10),
                 bg="#ecf0f1").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.price_entry = tk.Entry(fields_frame, font=("Arial", 10), width=25)
        self.price_entry.grid(row=1, column=3, padx=5, pady=5)

        # Buttons
        buttons_frame = tk.Frame(input_frame, bg="#ecf0f1")
        buttons_frame.pack(pady=10)

        tk.Button(buttons_frame, text="Add Product", font=("Arial", 10, "bold"),
                  bg="#27ae60", fg="white", padx=20, pady=5,
                  command=self.add_product).pack(side=tk.LEFT, padx=5)

        tk.Button(buttons_frame, text="Update Product", font=("Arial", 10, "bold"),
                  bg="#3498db", fg="white", padx=20, pady=5,
                  command=self.update_product).pack(side=tk.LEFT, padx=5)

        tk.Button(buttons_frame, text="Delete Product", font=("Arial", 10, "bold"),
                  bg="#e74c3c", fg="white", padx=20, pady=5,
                  command=self.delete_product).pack(side=tk.LEFT, padx=5)

        tk.Button(buttons_frame, text="Clear Fields", font=("Arial", 10, "bold"),
                  bg="#95a5a6", fg="white", padx=20, pady=5,
                  command=self.clear_fields).pack(side=tk.LEFT, padx=5)

        # Search frame
        search_frame = tk.Frame(self.root, bg="#f0f0f0")
        search_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(search_frame, text="Search:", font=("Arial", 10),
                 bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_products())

        tk.Button(search_frame, text="Refresh Table", font=("Arial", 10),
                  bg="#16a085", fg="white", padx=15, pady=3,
                  command=self.refresh_table).pack(side=tk.LEFT, padx=5)

        # Products table
        table_frame = tk.Frame(self.root, bg="#f0f0f0")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Scrollbars
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(table_frame,
                                 columns=("code", "name", "quantity", "price", "total"),
                                 show="headings",
                                 yscrollcommand=scroll_y.set,
                                 xscrollcommand=scroll_x.set)

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Define columns
        self.tree.heading("code", text="Product Code")
        self.tree.heading("name", text="Product Name")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("price", text="Price")
        self.tree.heading("total", text="Total Value")

        self.tree.column("code", width=100, anchor="center")
        self.tree.column("name", width=200, anchor="center")
        self.tree.column("quantity", width=100, anchor="center")
        self.tree.column("price", width=100, anchor="center")
        self.tree.column("total", width=150, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind click event to select row
        self.tree.bind('<ButtonRelease-1>', self.select_product)

        # Table styling
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

    def add_product(self):
        """Add new product"""
        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()

        if not all([code, name, quantity, price]):
            messagebox.showwarning("Warning", "Please fill in all fields!")
            return

        if code in self.inventory:
            messagebox.showwarning("Warning", "Product code already exists!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity and price must be numbers!")
            return

        self.inventory[code] = {
            "name": name,
            "quantity": quantity,
            "price": price
        }

        self.save_data()
        self.refresh_table()
        self.clear_fields()
        messagebox.showinfo("Success", "Product added successfully!")

    def update_product(self):
        """Update existing product"""
        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        price = self.price_entry.get().strip()

        if not code:
            messagebox.showwarning("Warning", "Please enter product code!")
            return

        if code not in self.inventory:
            messagebox.showwarning("Warning", "Product not found!")
            return

        if name:
            self.inventory[code]["name"] = name
        if quantity:
            try:
                self.inventory[code]["quantity"] = int(quantity)
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a number!")
                return
        if price:
            try:
                self.inventory[code]["price"] = float(price)
            except ValueError:
                messagebox.showerror("Error", "Price must be a number!")
                return

        self.save_data()
        self.refresh_table()
        self.clear_fields()
        messagebox.showinfo("Success", "Product updated successfully!")

    def delete_product(self):
        """Delete product"""
        code = self.code_entry.get().strip()

        if not code:
            messagebox.showwarning("Warning", "Please enter product code!")
            return

        if code not in self.inventory:
            messagebox.showwarning("Warning", "Product not found!")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this product?")
        if confirm:
            del self.inventory[code]
            self.save_data()
            self.refresh_table()
            self.clear_fields()
            messagebox.showinfo("Success", "Product deleted successfully!")

    def refresh_table(self):
        """Refresh table"""
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add data
        for code, data in self.inventory.items():
            total = data["quantity"] * data["price"]
            self.tree.insert("", tk.END, values=(
                code,
                data["name"],
                data["quantity"],
                f"{data['price']:.2f}",
                f"{total:.2f}"
            ))

    def search_products(self):
        """Search products"""
        search_term = self.search_entry.get().strip().lower()

        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add matching products
        for code, data in self.inventory.items():
            if (search_term in code.lower() or
                    search_term in data["name"].lower()):
                total = data["quantity"] * data["price"]
                self.tree.insert("", tk.END, values=(
                    code,
                    data["name"],
                    data["quantity"],
                    f"{data['price']:.2f}",
                    f"{total:.2f}"
                ))

    def select_product(self, event):
        """Select product from table"""
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected)['values']
            self.code_entry.delete(0, tk.END)
            self.code_entry.insert(0, values[0])
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, values[2])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, values[3])

    def clear_fields(self):
        """Clear input fields"""
        self.code_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)


# Run the program
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()