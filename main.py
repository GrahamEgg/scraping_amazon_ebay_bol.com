import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import subprocess

global selected_file_path
global selected_option
global label_selected_file


def select_excel_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if selected_file_path:
        label_selected_file.config(text=f"Selected file: {selected_file_path}")


def start_scraping():
    global selected_file_path
    global selected_option
    selected_option_value = selected_option.get()

    if selected_option_value == 'Ebay':
        scraper = 'ebay_scrap'
        if selected_file_path:
            subprocess.Popen(["python", f"{scraper}.py", selected_file_path])
        else:
            print("No file selected.")
    elif selected_option_value == 'Bol':
        scraper = 'bol_scrap'
        if selected_file_path:
            subprocess.Popen(["python", f"{scraper}.py", selected_file_path])
        else:
            print("No file selected.")

    elif selected_option_value == 'Bol':
        scraper = 'bol_scrap'
        if selected_file_path:
            subprocess.Popen(["python", f"{scraper}.py", selected_file_path])
        else:
            print("No file selected.")


def interface():
    global selected_file_path
    global selected_option
    global label_selected_file

    root = tk.Tk()
    root.title("Scraper interface")
    # Calculate the position to center the window
    window_width = 800
    window_height = 500

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    welkom_label = tk.Label(root, text="Welcome to the BTMarkt Scraper.", font=("Arial", 16))
    welkom_label.pack(pady=20)
    try:
        logo_path = "./btpic.jpg"
        logo = Image.open(logo_path)
        logo = logo.resize((200, 100))  # Resize the image
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(root, image=logo)
        logo_label.image = logo  # Keep a reference to avoid garbage collection
        logo_label.pack()

    except tk.TclError as e:
        print("Error:", e)

    what_to_scrap = tk.Label(root, text="Select what website you want to scrape", font=("Arial", 10))
    what_to_scrap.pack()

    options = ["Ebay", "Bol", "Amazon"]
    selected_option = tk.StringVar(root)
    selected_option.set(options[0])

    select_menu = tk.OptionMenu(root, selected_option, *options)
    select_menu.pack(pady=20)

    selected_file_path = None
    open_button = tk.Button(root, text="Open Excel File", command=select_excel_file)
    open_button.pack(pady=20)

    label_selected_file = tk.Label(root, text="Selected file: ", wraplength=350)
    label_selected_file.pack()

    start_button = tk.Button(root, text="Start Scraping", command=start_scraping)
    start_button.pack(pady=20)

    root.mainloop()


if __name__ == '__main__':
    interface()
