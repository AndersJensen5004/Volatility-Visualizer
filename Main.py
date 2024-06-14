import tkinter as tk
from tkinter import ttk
from ctypes import windll
from PIL import Image, ImageTk
import math

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


class LoadingSpinner(tk.Canvas):
    def __init__(self, parent, dot_count=10, radius=40, dot_size=12, *args, **kwargs):
        super().__init__(parent, width=2 * radius + dot_size * 2, height=2 * radius + dot_size * 2, bg="#15061c", bd=0,
                         highlightthickness=0, *args, **kwargs)
        self.dot_count = dot_count
        self.radius = radius
        self.dot_size = dot_size
        self.angle_step = 360 / dot_count
        self.dots = []

        for i in range(dot_count):
            angle = math.radians(i * self.angle_step)
            x = radius + radius * math.cos(angle)
            y = radius + radius * math.sin(angle)
            dot = self.create_oval(x, y, x + dot_size, y + dot_size, fill="#dea404", outline="")
            self.dots.append(dot)

        self.current_dot = 0
        self.animate()

    def animate(self):
        for i, dot in enumerate(self.dots):
            if i == self.current_dot:
                self.itemconfig(dot, fill="#dea404")
            else:
                self.itemconfig(dot, fill="#444444")

        self.current_dot = (self.current_dot + 1) % self.dot_count
        self.after(100, self.animate)

def loading_screen(output) -> None:
    """
    Displays a modern loading screen with an image and stylized text on the output widget.
    """
    # Clear the output widget before displaying the loading screen
    for widget in output.winfo_children():
        widget.destroy()

    # Load the image
    image = Image.open("equity_cat.jpg")  # Replace with your image file path
    image = image.resize((400, 400))  # Resize the image to fit better
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(output, image=photo, bg="#15061c")
    image_label.image = photo  # Store a reference to the image to prevent it from being garbage collected
    image_label.pack(pady=(50, 20))

    # Create a label to display the main title
    title_label = tk.Label(output, text=">>> FurEver Finance Terminal", fg="#dea404", bg="#15061c",
                           font=("Poppins", 30, "bold"))
    title_label.pack()

    # Create a label to display the subtitle
    subtitle_label = tk.Label(output, text="@EquityCats", fg="#5ca9fa", bg="#15061c",
                              font=("Poppins", 15, "italic"))
    subtitle_label.pack(pady=(10, 30))

    # Add the loading spinner
    spinner = LoadingSpinner(output)
    spinner.pack(pady=(0, 30))

def main():

    # Set the process to be DPI aware
    try:
        pass
        windll.shcore.SetProcessDpiAwareness(1)
    except AttributeError:
        pass

    root = tk.Tk()
    root.geometry("1400x900")
    root.title("FurEver Finance Terminal")

    y_spacing = 5

    # Set the overall background color to a dark shade
    root.configure(bg="#15061c")

    # Configure the style to use a dark theme
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', foreground='white', background='#15061c', font=('Poppins', 12))
    style.configure('TEntry', foreground='white', fieldbackground='#15061c', background='#15061c', borderwidth=0,
                    bordercolor='#333333', relief='flat', font=('Poppins', 12))
    style.configure('TFrame', background='#15061c')
    style.configure('TText', foreground='#454441', background='#15061c', font=('Poppins', 12))

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
