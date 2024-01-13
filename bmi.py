import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BMICalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")

        # Variables
        self.weight_var = tk.DoubleVar()
        self.height_var = tk.DoubleVar()
        self.bmi_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.history = []

        # Widgets
        self.label_weight = tk.Label(master, text="Weight (kg):")
        self.label_weight.grid(row=0, column=0, padx=10, pady=10)

        self.entry_weight = tk.Entry(master, textvariable=self.weight_var)
        self.entry_weight.grid(row=0, column=1, padx=10, pady=10)

        self.label_height = tk.Label(master, text="Height (cm):")
        self.label_height.grid(row=1, column=0, padx=10, pady=10)

        self.entry_height = tk.Entry(master, textvariable=self.height_var)
        self.entry_height.grid(row=1, column=1, padx=10, pady=10)

        self.button_calculate = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi)
        self.button_calculate.grid(row=2, column=0, columnspan=2, pady=10)

        self.label_bmi = tk.Label(master, text="BMI:")
        self.label_bmi.grid(row=3, column=0, padx=10, pady=10)

        self.result_bmi = tk.Label(master, textvariable=self.bmi_var)
        self.result_bmi.grid(row=3, column=1, padx=10, pady=10)

        self.label_category = tk.Label(master, text="Category:")
        self.label_category.grid(row=4, column=0, padx=10, pady=10)

        self.result_category = tk.Label(master, textvariable=self.category_var)
        self.result_category.grid(row=4, column=1, padx=10, pady=10)

        self.button_save = tk.Button(master, text="Save Data", command=self.save_data)
        self.button_save.grid(row=5, column=0, columnspan=2, pady=10)

        self.button_show_history = tk.Button(master, text="Show History", command=self.show_history)
        self.button_show_history.grid(row=6, column=0, columnspan=2, pady=10)

    def calculate_bmi(self):
        try:
            weight = self.weight_var.get()
            height_cm = self.height_var.get()
            height_m = height_cm / 100  # Convert height to meters
            bmi = weight / (height_m ** 2)

            self.bmi_var.set(f"{bmi:.2f}")

            # Classify BMI into categories
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 24.9:
                category = "Normal"
            elif 25 <= bmi < 29.9:
                category = "Overweight"
            else:
                category = "Obese"

            self.category_var.set(category)

            # Add data to history
            self.history.append((weight, height_cm, bmi, category))

        except ZeroDivisionError:
            messagebox.showerror("Error", "Height cannot be zero.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_data(self):
        if self.history:
            with open("bmi_history.txt", "a") as file:
                for data in self.history:
                    file.write(f"{data[0]},{data[1]},{data[2]},{data[3]}\n")

            messagebox.showinfo("Success", "Data saved successfully.")
        else:
            messagebox.showwarning("Warning", "No data to save.")

    def show_history(self):
        if self.history:
            weights = [data[0] for data in self.history]
            heights = [data[1] for data in self.history]
            bmis = [data[2] for data in self.history]
            categories = [data[3] for data in self.history]

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

            ax1.plot(weights, label="Weight")
            ax1.plot(heights, label="Height")
            ax1.legend()
            ax1.set_title("Weight and Height Over Time")

            ax2.plot(bmis, color='red', label="BMI")
            ax2.legend()
            ax2.set_title("BMI Over Time")

            plt.tight_layout()

            # Display the plot
            history_window = tk.Toplevel(self.master)
            history_window.title("BMI History")

            canvas = FigureCanvasTkAgg(fig, master=history_window)
            canvas.get_tk_widget().pack()
            canvas.draw()

        else:
            messagebox.showwarning("Warning", "No history to show.")


def main():
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()