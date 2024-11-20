import tkinter as tk
from tkinter import ttk, messagebox
import random

# Package class
class Package:
    def __init__(self, package_code, location, weight, distance):
        self.package_code = package_code
        self.location = location
        self.weight = weight
        self.distance = distance
        self.payment_status = "Unpaid"  # Default status


# Knapsack algorithm
def allocate_trucks(packages, max_weight):
    trucks = []
    while packages:
        truck, packages = ks_algorithm(packages, max_weight)
        # Sort the truck packages by distance in descending order
        truck.sort(key=lambda package: package.distance, reverse=True)
        trucks.append(truck)
    return trucks
def ks_algorithm(packages, max_weight):
    n = len(packages)
    dp = [[0 for _ in range(max_weight + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(max_weight + 1):
            dp[i][w] = dp[i - 1][w]
            if packages[i - 1].weight <= w:
                package_value = dp[i - 1][w - packages[i - 1].weight] + packages[i - 1].weight
                if package_value > dp[i][w]:
                    dp[i][w] = package_value

    truck = []
    w = max_weight
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            truck.append(packages[i - 1])
            w -= packages[i - 1].weight

    remaining_packages = [p for p in packages if p not in truck]
    return truck, remaining_packages

# Main Interface Class
class TruckInterface:
    def __init__(self, root, max_weight):
        self.root = root
        self.max_weight = max_weight
        self.packages = self.generate_initial_packages()
        self.trucks = allocate_trucks(self.packages, self.max_weight)

        self.root.title("Truck and Package Management")
        self.root.geometry("1000x1200")

        # Main Frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Package Table
        self.package_table_label = tk.Label(self.main_frame, text="Package List", font=("Arial", 14))
        self.package_table_label.pack(pady=10)

        self.package_table = ttk.Treeview(self.main_frame, columns=("Code", "Location", "Weight", "Distance"), show="headings")
        self.package_table.heading("Code", text="Package Code")
        self.package_table.heading("Location", text="Location")
        self.package_table.heading("Weight", text="Weight (kg)")
        self.package_table.heading("Distance", text="Distance (km)")
        self.package_table.pack(pady=10, fill=tk.BOTH, expand=True)

        # Buttons and Input Frame
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(pady=5)

        # Cancel Delivery Button
        self.cancel_button = tk.Button(self.input_frame, text="Cancel Delivery", command=self.cancel_delivery)
        self.cancel_button.grid(row=0, column=0, padx=5)

        # Cancel All Deliveries Button
        self.cancel_all_button = tk.Button(self.input_frame, text="Cancel All Deliveries", command=self.cancel_all_deliveries)
        self.cancel_all_button.grid(row=0, column=1, padx=5)

        # Add Delivery Form
        self.destination_label = tk.Label(self.input_frame, text="Destination:")
        self.destination_label.grid(row=0, column=2, padx=5)
        self.destination_entry = ttk.Combobox(self.input_frame, values=["Da Nang", "HCMC", "Nha Trang", "Dalat", "Hai Phong"], state="readonly")
        self.destination_entry.grid(row=0, column=3, padx=5)

        self.weight_label = tk.Label(self.input_frame, text="Weight (kg):")
        self.weight_label.grid(row=0, column=4, padx=5)
        self.weight_entry = tk.Entry(self.input_frame)
        self.weight_entry.grid(row=0, column=5, padx=5)

        self.add_button = tk.Button(self.input_frame, text="Add Delivery", command=self.add_delivery)
        self.add_button.grid(row=0, column=6, padx=5)

        # Truck Dropdown
        self.truck_dropdown_label = tk.Label(self.main_frame, text="Select Truck:", font=("Arial", 14))
        self.truck_dropdown_label.pack(pady=10)

        self.truck_dropdown = ttk.Combobox(self.main_frame, state="readonly", font=("Arial", 12))
        self.truck_dropdown.bind("<<ComboboxSelected>>", self.display_truck_data)
        self.truck_dropdown.pack(pady=5)

        # Truck Table
        self.truck_table_label = tk.Label(self.main_frame, text="Truck Packages", font=("Arial", 14))
        self.truck_table_label.pack(pady=10)

        self.truck_table = ttk.Treeview(self.main_frame, columns=("Code", "Location", "Weight", "Distance", "Payment Status"), show="headings")
        self.truck_table.heading("Code", text="Package Code")
        self.truck_table.heading("Location", text="Location")
        self.truck_table.heading("Weight", text="Weight (kg)")
        self.truck_table.heading("Distance", text="Distance (km)")
        self.truck_table.heading("Payment Status", text="Payment Status")
        self.truck_table.pack(pady=10, fill=tk.BOTH, expand=True)
        # Check Out Button
        self.check_out_button = tk.Button(self.input_frame, text="Check Out", command=self.check_out)
        self.check_out_button.grid(row=0, column=10, padx=5)
        self.payment_button = tk.Button(self.main_frame, text="Mark as Paid", command=self.mark_as_paid)
        self.payment_button.pack(pady=5)

        self.status_button = tk.Button(self.main_frame, text="Set Truck In Transit", command=self.set_truck_in_transit)
        self.status_button.pack(pady=5)
        self.log_label = tk.Label(self.main_frame, text="Activity Log", font=("Arial", 14))
        self.log_label.pack(pady=10)

        self.log_text = tk.Text(self.main_frame, height=10, state="disabled", wrap="word")
        self.log_text.pack(pady=5, fill=tk.BOTH, expand=True)



        # Initialize UI
        self.update_package_table()
        self.update_truck_dropdown()

    def generate_initial_packages(self):
        locations = [
            {"city": "Da Nang", "distance": 750},
            {"city": "HCMC", "distance": 1600},
            {"city": "Nha Trang", "distance": 1000},
            {"city": "Dalat", "distance": 1350},
            {"city": "Hai Phong", "distance": 120},
        ]
        packages = []
        for i in range(1, 11):
            location = random.choice(locations)
            package_code = f"PTD{i:03}"
            weight = random.randint(1, 15)
            packages.append(Package(package_code, location["city"], weight, location["distance"]))
        return packages

    def update_package_table(self):
        for row in self.package_table.get_children():
            self.package_table.delete(row)
        for package in self.packages:
            self.package_table.insert("", "end", values=(package.package_code, package.location, package.weight, package.distance))

    def update_truck_dropdown(self):
        self.truck_dropdown["values"] = [f"Truck {i + 1}" for i in range(len(self.trucks))]

        # Clear the truck table initially
        for row in self.truck_table.get_children():
            self.truck_table.delete(row)

        # Optionally set a blank value as default in the dropdown
        if self.trucks:
            self.truck_dropdown.set("")  # Set blank initially

    def display_truck_data(self, event):
        # Clear the truck table
        for row in self.truck_table.get_children():
            self.truck_table.delete(row)

        # Get the selected truck index
        selected_truck_index = self.truck_dropdown.current()

        # Only display data if a truck is selected
        if selected_truck_index != -1:
            truck = self.trucks[selected_truck_index]
            for package in truck:
                self.truck_table.insert("", "end", values=(package.package_code, package.location, package.weight, package.distance))
        else:
            self.truck_table.insert("", "end", values=("No truck selected", "", "", ""))
            
    def add_delivery(self):
        location = self.destination_entry.get()
        try:
            weight = int(self.weight_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Weight must be a valid number.")
            return
        if weight > self.max_weight:
            messagebox.showerror("Input Error", "We do not accept packages weight more than {} kilograms.".format(self.max_weight))
            return
        if not location:
            messagebox.showerror("Input Error", "Please select a destination.")
            return

        location_distance = {"Da Nang": 750, "HCMC": 1600, "Nha Trang": 1000, "Dalat": 1350, "Hai Phong": 120}
        distance = location_distance.get(location, 0)
        package_code = f"PTD{len(self.packages) + 1:03}"
        new_package = Package(package_code, location, weight, distance)
        self.packages.append(new_package)
        self.trucks = allocate_trucks(self.packages, self.max_weight)
        self.update_package_table()
        self.update_truck_dropdown()
        messagebox.showinfo("Success", f"Package {package_code} added successfully!")

    def cancel_delivery(self):
        selected = self.package_table.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a package to cancel.")
            return
        package_code = self.package_table.item(selected[0])["values"][0]
        self.packages = [p for p in self.packages if p.package_code != package_code]
        self.trucks = allocate_trucks(self.packages, self.max_weight)
        self.update_package_table()
        self.update_truck_dropdown()
        messagebox.showinfo("Success", f"Package {package_code} canceled successfully!")

    def cancel_all_deliveries(self):
        self.packages = []
        self.trucks = []
        self.update_package_table()
        self.update_truck_dropdown()
        messagebox.showinfo("Success", "All deliveries have been canceled!")

    def check_out(self):
        # Create a new window for package selection
        checkout_window = tk.Toplevel(self.root)
        checkout_window.title("Check Out")
        checkout_window.geometry("600x500")

        tk.Label(checkout_window, text="Select Packages to Check Out", font=("Arial", 14)).pack(pady=10)

        # Listbox to show packages
        package_listbox = tk.Listbox(checkout_window, selectmode=tk.MULTIPLE, width=80, height=15)
        package_listbox.pack(pady=10)

        # Populate the listbox with packages
        package_data = []
        for truck_number, truck in enumerate(self.trucks, start=1):
            for package in truck:
                package_data.append((truck_number, package))
                package_listbox.insert(
                    tk.END,
                    f"Truck {truck_number}: {package.package_code} - {package.location}, {package.weight}kg, {package.distance}km"
                )

        
        self.update_package_table()
        self.update_truck_dropdown()

        # Calculate and display receipt
        def generate_receipt():
            selected_indices = package_listbox.curselection()
            if not selected_indices:
                messagebox.showerror("Selection Error", "Please select at least one package.")
                return

            # Generate receipt content
            receipt_text = "Receipt\n" + "=" * 39 + "\n"
            total_cost = 0
            distance_rate = 0.10
            weight_rate = 0.05
            delivery_schedule = {}

            for index in selected_indices:
                truck_number, package = package_data[index]
                cost = (distance_rate * package.distance) + (weight_rate * package.weight)
                total_cost += cost
                delivery_day = delivery_schedule.get(truck_number, 1)
                delivery_schedule[truck_number] = delivery_day

                receipt_text += (
                    f"Truck {truck_number} - Day {delivery_day}\n"
                    f"Package: {package.package_code}\n"
                    f"Destination: {package.location}\n"
                    f"Weight: {package.weight} kg, Distance: {package.distance} km\n"
                    f"Cost: ${cost:.2f}\n\n"
                )

            receipt_text += "=" * 39 + f"\nTotal Cost: ${total_cost:.2f}"

            # Show receipt in a popup
            messagebox.showinfo("Receipt", receipt_text)

            # Remove selected packages from trucks
            for index in sorted(selected_indices, reverse=True):
                truck_number, package = package_data[index]
                self.trucks[truck_number - 1].remove(package)
                
            # Refresh UI
            self.update_package_table()
            self.update_truck_dropdown()

            checkout_window.destroy()

        # Buttons
        tk.Button(checkout_window, text="Generate Receipt", command=generate_receipt).pack(pady=10)
        tk.Button(checkout_window, text="Cancel", command=checkout_window.destroy).pack(pady=5)

    def mark_as_paid(self):
        selected_item = self.truck_table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a package to mark as Paid.")
            return

        for item in selected_item:
            package_code = self.truck_table.item(item, "values")[0]
            for truck in self.trucks:
                for package in truck:
                    if package.package_code == package_code and package.payment_status == "Unpaid":
                        package.payment_status = "Paid"
                        self.log_activity(f"Package {package_code} marked as Paid.")
                        break
        self.display_truck_data(None)  # Refresh truck table
    
    def set_truck_in_transit(self):
        selected_truck_index = self.truck_dropdown.current()
        if selected_truck_index == -1:
            messagebox.showerror("Selection Error", "Please select a truck.")
            return

        truck = self.trucks[selected_truck_index]
        if all(package.payment_status == "Paid" for package in truck):
            self.log_activity(f"Truck {selected_truck_index + 1} set to In Transit.")
            messagebox.showinfo("Truck Status", f"Truck {selected_truck_index + 1} is now In Transit.")
        else:
            messagebox.showerror("Payment Error", "All packages in the truck must be Paid before setting it to In Transit.")

    def log_activity(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.configure(state="disabled")
        self.log_text.see(tk.END)  # Auto-scroll

if __name__ == "__main__":
    root = tk.Tk()
    app = TruckInterface(root, max_weight=25)
    root.mainloop()
