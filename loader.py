import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

def parse_color(color_str):
    try:
        start_index = color_str.find("[") + 1
        end_index = color_str.find("]", start_index)
        rgb_values = [int(val.strip()) for val in color_str[start_index:end_index].split(',')]
        if len(rgb_values) == 3:
            return tuple(rgb_values)
        else:
            raise ValueError("Invalid RGB color format.")
    except ValueError as e:
        print(f"Error parsing color: {e}")
        return None

def rgb_to_hex(rgb_color):
    return f'#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}'

def create_text_with_color(text, rgb_color, padding):
    root = TkinterDnD.Tk()
    hex_color = rgb_to_hex(rgb_color)
    root.configure(bg=hex_color)
    
    # Remove extra quotation marks from the text
    text = text.replace('"', '')

    # Create a Label with padding
    label = tk.Label(root, text=text, bg=hex_color, fg='white', padx=padding, pady=padding)
    label.pack()
    
    root.mainloop()

def parse_padding(padding_str):
    try:
        padding_value = int(padding_str.strip())
        return padding_value
    except ValueError:
        print("Invalid padding value. Using default padding.")
        return 0  # Default padding value

def main():
    root = TkinterDnD.Tk()

    def on_drop(event):
        filename = event.data.strip()
        print(f"File dropped: {filename}")
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

            rgb_color = None
            text = None
            padding = 0
            for line in lines:
                if line.startswith("c: ["):
                    rgb_color = parse_color(line)
                elif line.startswith("text:"):
                    text = line.split("text:")[1].strip().strip('"')
                elif line.startswith("p:"):
                    padding = parse_padding(line.split("p:")[1])
            
            if rgb_color and text:
                create_text_with_color(text, rgb_color, padding)
        except Exception as e:
            print(f"Error loading or processing file: {e}")

    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)

    root.mainloop()

if __name__ == "__main__":
    main()
