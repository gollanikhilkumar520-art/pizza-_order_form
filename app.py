# pizza_order.py
import tkinter as tk











from tkinter import ttk, messagebox

class PizzaOrderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pizza Order Form")
        self.geometry("520x720")
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        heading = ttk.Label(self, text="🍕 Pizza Order Form", font=("Segoe UI", 18, "bold"))
        heading.pack(pady=12)

        # --- Size (radio buttons) ---
        size_frame = ttk.LabelFrame(self, text="Choose Size")
        size_frame.pack(fill="x", padx=16, pady=8)

        # size name -> base price
        self.sizes = {"Small": 150, "Medium": 250, "Large": 350}
        self.size_var = tk.StringVar(value="Medium")

        for size_name, price in self.sizes.items():
            text = f"{size_name} — ₹{price}"
            rb = ttk.Radiobutton(size_frame, text=text, value=size_name, variable=self.size_var)
            rb.pack(anchor="w", padx=10, pady=4)

        # --- Toppings (checkboxes) ---
        toppings_frame = ttk.LabelFrame(self, text="Toppings (select any)")
        toppings_frame.pack(fill="x", padx=16, pady=8)

        # topping -> price
        self.toppings = {
            "Extra Cheese": 40,
            "Pepperoni": 60,
            "Mushrooms": 35,
            "Onions": 20,
            "Olives": 30,
            "Capsicum": 25,
            "Tomatoes": 20,
            "Jalapeños": 30
        }

        self.topping_vars = {}
        for name, price in self.toppings.items():
            var = tk.IntVar(value=0)
            cb = ttk.Checkbutton(toppings_frame, text=f"{name} — ₹{price}", variable=var)
            cb.pack(anchor="w", padx=10, pady=3)
            self.topping_vars[name] = var

        # --- Quantity ---
        qty_frame = ttk.Frame(self)
        qty_frame.pack(fill="x", padx=16, pady=8)
        ttk.Label(qty_frame, text="Quantity:").pack(side="left", padx=(0,8))
        self.qty_var = tk.IntVar(value=1)
        qty_spin = ttk.Spinbox(qty_frame, from_=1, to=20, textvariable=self.qty_var, width=5)
        qty_spin.pack(side="left")

        # --- Special instructions ---
        instr_frame = ttk.LabelFrame(self, text="Special Instructions (optional)")
        instr_frame.pack(fill="both", expand=False, padx=16, pady=8)
        self.instr_text = tk.Text(instr_frame, height=4, wrap="word")
        self.instr_text.pack(fill="both", padx=8, pady=6)

        # --- Buttons ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=12)
        order_btn = ttk.Button(btn_frame, text="Place Order", command=self.place_order)
        order_btn.grid(row=0, column=0, padx=8)
        clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_form)
        clear_btn.grid(row=0, column=1, padx=8)
        quit_btn = ttk.Button(btn_frame, text="Quit", command=self.quit)
        quit_btn.grid(row=0, column=2, padx=8)

        # --- Order summary display ---
        summary_frame = ttk.LabelFrame(self, text="Order Summary")
        summary_frame.pack(fill="both", expand=True, padx=16, pady=(0,16))
        self.summary_label = tk.Label(summary_frame, justify="left", anchor="nw", padx=8, pady=8, font=("Segoe UI", 10))
        self.summary_label.pack(fill="both", expand=True)

        # Initialize summary
        self._update_summary_display("Select options and click 'Place Order' to see summary here.")

    def _calc_total(self):
        # base price by size
        size = self.size_var.get()
        base_price = self.sizes.get(size, 0)

        # toppings total
        toppings_selected = [name for name, var in self.topping_vars.items() if var.get()]
        toppings_total = sum(self.toppings[name] for name in toppings_selected)

        # quantity
        qty = max(1, int(self.qty_var.get()))

        # total
        single_pizza_price = base_price + toppings_total
        total_price = single_pizza_price * qty

        # return detailed breakdown
        return {
            "size": size,
            "base_price": base_price,
            "toppings_selected": toppings_selected,
            "toppings_total": toppings_total,
            "qty": qty,
            "single_price": single_pizza_price,
            "total_price": total_price
        }

    def place_order(self):
        details = self._calc_total()
        instructions = self.instr_text.get("1.0", "end").strip()

        summary_lines = [
            f"Size: {details['size']} (₹{details['base_price']})",
            f"Toppings ({len(details['toppings_selected'])}): " + (", ".join(details['toppings_selected']) if details['toppings_selected'] else "None"),
            f"Toppings total: ₹{details['toppings_total']}",
            f"Quantity: {details['qty']}",
            f"Price per pizza: ₹{details['single_price']}",
            f"Total: ₹{details['total_price']}"
        ]
        if instructions:
            summary_lines.append(f"Special instructions: {instructions}")

        summary_text = "\n".join(summary_lines)

        # Update right-hand summary label
        self._update_summary_display(summary_text)

        # Confirm with user via popup
        if messagebox.askyesno("Confirm Order", f"Confirm order?\n\n{summary_text}"):
            # In a real app you'd send the order to server or save it.
            messagebox.showinfo("Order Placed", f"Thank you! Your order for ₹{details['total_price']} has been placed.")
            # Optionally save to a simple text file
            self._save_order_to_file(details, instructions)
            self.clear_form(keep_message=True)

    def _save_order_to_file(self, details, instructions):
        try:
            with open("pizza_orders.txt", "a", encoding="utf-8") as f:
                f.write("---- New Order ----\n")
                f.write(f"Size: {details['size']} (₹{details['base_price']})\n")
                f.write("Toppings: " + (", ".join(details['toppings_selected']) if details['toppings_selected'] else "None") + "\n")
                f.write(f"Quantity: {details['qty']}\n")
                f.write(f"Total: ₹{details['total_price']}\n")
                if instructions:
                    f.write(f"Instructions: {instructions}\n")
                f.write("\n")
        except Exception as e:
            # fail silently for file save (but you could notify)
            print("Failed to save order:", e)

    def clear_form(self, keep_message=False):
        # reset size to default
        self.size_var.set("Medium")
        # clear toppings
        for var in self.topping_vars.values():
            var.set(0)
        # reset qty
        self.qty_var.set(1)
        # clear instructions
        self.instr_text.delete("1.0", "end")
        if not keep_message:
            self._update_summary_display("Form cleared. Select options and click 'Place Order' to see summary here.")

    def _update_summary_display(self, text):
        self.summary_label.config(text=text)

if __name__ == "__main__":
    app = PizzaOrderApp()
    app.mainloop()

