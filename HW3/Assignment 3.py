# Program Name: Assignment3.py
# Course: IT3883/Section W01
# Student Name: Ayomide Laosun
# Assignment Number: 3
# Due Date: 10/3/2025
# Purpose: Build a GUI converter that turns Miles per Gallon into Kilometers per Liter.
#          The result updates as the user types and the app must not crash on letters or blanks.
# List Specific resources used to complete the assignment:
# Resources: Python official documentation (docs.python.org) - GUI Applications, String Formatting and Widgets using tkinter


import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

MPG_TO_KM_PER_L = 0.425143707  # Conversion rate

def make_app():
    """Create and return the main application window."""
    root = tk.Tk()
    root.title("MPG to KM per L Converter")
    root.resizable(False, False)

    # Make Times New Roman the default across the app
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(family="Times New Roman", size=12)

    text_font = tkfont.nametofont("TkTextFont")
    text_font.configure(family="Times New Roman", size=12)

    fixed_font = tkfont.nametofont("TkFixedFont")
    fixed_font.configure(family="Times New Roman", size=12)

    # Style ttk widgets so they inherit the same font
    style = ttk.Style(root)
    style.configure("TLabel", font=("Times New Roman", 12))
    style.configure("TEntry", font=("Times New Roman", 12))
    style.configure("TButton", font=("Times New Roman", 12, "bold"))
    style.configure("Title.TLabel", font=("Times New Roman", 14, "bold"))

    # Main frame
    frame = ttk.Frame(root, padding=16)
    frame.grid(row=0, column=0, sticky="nsew")

    # Variables backed by tkinter
    mpg_var = tk.StringVar()
    kmpl_var = tk.StringVar()
    status_var = tk.StringVar()  # small status message for gentle feedback

    def compute_kmpl(*_):
        """
        Convert mpg to km per liter.
        Runs on every text change.
        Does not raise exceptions on bad input.
        """
        text = mpg_var.get().strip()
        if text == "":
            kmpl_var.set("")
            status_var.set("Type a number for mpg")
            return

        # Remove commas so users can type numbers like 1,234.5
        cleaned = text.replace(",", "")
        try:
            mpg_value = float(cleaned)
            # Negative mpg does not make physical sense, treat as invalid
            if mpg_value < 0:
                kmpl_var.set("")
                status_var.set("Enter a nonnegative value")
                return

            kmpl_value = mpg_value * MPG_TO_KM_PER_L
            # Show six decimals to be precise but readable
            kmpl_var.set("{:.6f}".format(kmpl_value))
            status_var.set("OK")
        except ValueError:
            # If user types letters or symbols, just clear result
            kmpl_var.set("")
            status_var.set("Numbers only")

    # Wire the live update
    mpg_var.trace_add("write", compute_kmpl)

    # Row 0: Title
    title = ttk.Label(
        frame,
        text="Miles per Gallon to Kilometers per Liter",
        style="Title.TLabel"
    )
    title.grid(row=0, column=0, columnspan=2, pady=(0, 12))

    # Row 1: MPG input
    ttk.Label(frame, text="MPG").grid(row=1, column=0, sticky="e", padx=(0, 8))
    mpg_entry = ttk.Entry(frame, textvariable=mpg_var, width=24)
    mpg_entry.grid(row=1, column=1, sticky="w")
    mpg_entry.insert(0, "")  # placeholder left blank by design
    mpg_entry.focus()

    # Row 2: KM per L output
    ttk.Label(frame, text="KM per L").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=(8, 0))
    kmpl_display = ttk.Label(frame, textvariable=kmpl_var, width=24, relief="sunken", anchor="w")
    kmpl_display.grid(row=2, column=1, sticky="w", pady=(8, 0))

    # Row 3: Status text and formula reminder
    status = ttk.Label(frame, textvariable=status_var, foreground="gray")
    status.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))
    status_var.set("Type a number for mpg")

    formula = ttk.Label(frame, text="Formula: km per L = mpg × 0.425143707", foreground="gray")
    formula.grid(row=4, column=0, columnspan=2, sticky="w", pady=(4, 0))

    # Optional clear button. Compute happens automatically, no click needed for math.
    def clear_fields():
        mpg_var.set("")
        kmpl_var.set("")
        status_var.set("Cleared")

    clear_btn = ttk.Button(frame, text="Clear", command=clear_fields)
    clear_btn.grid(row=5, column=1, sticky="e", pady=(12, 0))

    return root

if __name__ == "__main__":
    app = make_app()
    app.mainloop()