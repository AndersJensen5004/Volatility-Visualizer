import tkinter as tk
from tkinter import ttk
from ctypes import windll
from PIL import Image, ImageTk

from equity import Equity

# Initialize Instances
equity_instance = Equity(None)


def invalid_command(output, args):
    output_text = tk.Text(output, height=20, width=80, font=('Poppins', 14), wrap='word', highlightthickness=0, bd=0,
                          background="#b3b2af")
    output_text.pack(expand=True, fill='both', padx=8, pady=6)
    output_text.tag_configure("red_tag_center", foreground="#a82d3c", justify="center")
    output_text.insert(tk.END, "\n\nInvalid Command >>> " + ' '.join(args) + "\n", "red_tag_center")
    output_text.config(state="disabled")


def get_command() -> list:
    """
    Parses and returns the user-entered command as a list of lowercase words.
    """
    command = command_entry.get().lower().strip()
    return command.split() if command else [""]


def execute_command(event, output):
    args = get_command()

    # Clear the output before each command execution
    for widget in output.winfo_children():
        widget.destroy()

    commands = {
        "equity": lambda: equity_instance.execute_command(output, args),
        "close": lambda: exit(),
        "_default": lambda: invalid_command(output, args),
    }

    selected_command = commands.get(args[0], commands["_default"])
    selected_command()
    command_entry.delete(0, tk.END)
    return 'break'


def loading_screen(output) -> None:
    """
    Displays an image on the output widget.
    """
    output_text = tk.Text(output, height=1, width=80, font=('Poppins', 12), wrap='word', highlightthickness=0, bd=0,
                          background="#b3b2af")
    output_text.pack(expand=True, fill='both', padx=8, pady=6)

    image = Image.open("equity_cat.jpg")  # Replace "equity_cat.jpg" with your image file path
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(output, image=photo)
    label.image = photo
    label.pack()

    output_text.tag_configure("bold_center", foreground="#35a60c", justify="center", font=("Poppins", 30, "bold"))
    output_text.insert(tk.END, "\n>>> FurEver Finance Terminal\n", "bold_center")
    output_text.config(state='disabled')

def main():

    # Set the process to be DPI aware
    try:
        pass
        windll.shcore.SetProcessDpiAwareness(1)
    except AttributeError:
        pass

    root = tk.Tk()
    root.geometry("1400x800")
    root.title("FurEver Finance Terminal")

    y_spacing = 6

    # Set the overall background color to a dark shade
    root.configure(bg="#222222")

    # Configure the style to use a dark theme
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', foreground='white', background='#222222', font=('Poppins', 12))
    style.configure('TEntry', foreground='white', fieldbackground='#333333', background='#333333', borderwidth=0,
                    bordercolor='#333333', relief='flat', font=('Poppins', 12))
    style.configure('TFrame', background='#222222')
    style.configure('TText', foreground='#454441', background='#444444', font=('Poppins', 12))

    # Create a frame for the command line
    command_frame = ttk.Frame(root)
    command_frame.pack(pady=y_spacing)

    # Create a label and entry for the command line
    command_label = ttk.Label(command_frame, text=">>>", font=('Poppins', 12, 'bold'), foreground='#5ca9fa')
    command_label.pack(side=tk.LEFT)

    global command_entry
    command_entry = ttk.Entry(command_frame, width=90, font=('Poppins', 12), style='Custom.TEntry')
    command_entry.pack(side=tk.LEFT, padx=5)

    # Create a frame to act as the output area
    global output_frame
    output_frame = ttk.Frame(root, height=400, width=800, style='Output.TFrame')
    output_frame.pack(expand=True, fill='both', padx=8, pady=y_spacing)

    # Bind Enter to execute command
    command_entry.bind('<Return>', lambda event: execute_command(event, output_frame))

    # Run the loading screen
    loading_screen(output_frame)

    # Embed a button in the text widget
    # button_in_text = ttk.Button(output_text, text="Button in Text", command=lambda: print("Button clicked"))
    # output_text.window_create(tk.END, window=button_in_text)


    # Run the application
    root.mainloop()


if __name__ == "__main__":
    main()
