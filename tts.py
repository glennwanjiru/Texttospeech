import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, ttk
from gtts import gTTS
from pydub import AudioSegment
import pygame
from ttkthemes import ThemedTk
from tkinter import font as tkfont
import os
import uuid

class TextToAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Audio Converter")
        self.root.geometry("700x600")  # Increased window size for better layout

        # Initialize pygame mixer
        pygame.mixer.init()

        # Define font
        self.font = tkfont.Font(family="Helvetica", size=12)

        # Define colors
        self.bg_color = "#F7F7F7"
        self.fg_color = "#333333"
        self.button_bg_color = "#007BFF"
        self.button_fg_color = "#FFFFFF"
        self.button_hover_bg_color = "#0056b3"
        self.button_hover_fg_color = "#FFFFFF"
        self.label_bg_color = "#E0E0E0"
        self.progress_color = "#007BFF"

        # Create GUI elements
        self.create_widgets()

        # Initialize state variables
        self.is_playing = False
        self.is_paused = False
        self.current_pos = 0

    def create_widgets(self):
        # Set background color for the root window
        self.root.configure(bg=self.bg_color)

        # Define styles
        style = ttk.Style(self.root)
        style.configure("TButton", font=self.font, padding=10, relief='flat')
        style.configure("TLabel", font=self.font, padding=5, background=self.label_bg_color)
        style.configure("TCombobox", font=self.font, padding=5)
        style.configure("TScale", background=self.bg_color)
        style.configure("TProgressbar", thickness=20, troughcolor=self.bg_color, background=self.progress_color)

        # Text area
        self.text_area = tk.Text(self.root, wrap=tk.WORD, height=10, width=60, bg="#FFFFFF", fg=self.fg_color, font=self.font, bd=0, highlightthickness=0)
        self.text_area.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Format selection
        self.format_var = StringVar(value="mp3")
        self.format_menu = ttk.Combobox(self.root, textvariable=self.format_var, values=["mp3", "wav", "ogg"], state='readonly')
        self.format_menu.pack(pady=5, padx=20)

        # Rate, Volume, and Pitch controls
        self.rate_var = tk.IntVar(value=200)  # Set default speech rate to 200
        self.volume_var = tk.DoubleVar(value=1.0)
        self.pitch_var = tk.IntVar(value=50)

        ttk.Label(self.root, text="Speech Rate:").pack(pady=5, padx=20)
        self.rate_slider = tk.Scale(self.root, from_=50, to_=300, variable=self.rate_var, orient='horizontal', sliderlength=30, length=300, bg=self.bg_color)
        self.rate_slider.pack(pady=5, padx=20)

        ttk.Label(self.root, text="Volume:").pack(pady=5, padx=20)
        self.volume_slider = tk.Scale(self.root, from_=0, to_=1, variable=self.volume_var, orient='horizontal', sliderlength=30, length=300, resolution=0.1, bg=self.bg_color)
        self.volume_slider.pack(pady=5, padx=20)

        ttk.Label(self.root, text="Pitch (not directly supported in gTTS):").pack(pady=5, padx=20)
        self.pitch_slider = tk.Scale(self.root, from_=0, to_=100, variable=self.pitch_var, orient='horizontal', sliderlength=30, length=300, bg=self.bg_color)
        self.pitch_slider.pack(pady=5, padx=20)

        # Buttons
        button_frame = ttk.Frame(self.root, style="TFrame")
        button_frame.pack(pady=10, padx=20, fill=tk.X)

        self.convert_button = ttk.Button(button_frame, text="Convert to Audio", command=self.convert_to_audio)
        self.convert_button.pack(side=tk.LEFT, padx=5, expand=True)
        self.apply_button_styles(self.convert_button)

        self.play_button = ttk.Button(button_frame, text="Play", command=self.play_audio, state=tk.DISABLED)
        self.play_button.pack(side=tk.LEFT, padx=5, expand=True)
        self.apply_button_styles(self.play_button)

        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_audio, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5, expand=True)
        self.apply_button_styles(self.pause_button)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_audio, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, expand=True)
        self.apply_button_styles(self.stop_button)

        self.save_button = ttk.Button(button_frame, text="Save Audio", command=self.save_audio, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5, expand=True)
        self.apply_button_styles(self.save_button)

        self.clear_button = ttk.Button(button_frame, text="Clear Text", command=self.clear_text)
        self.clear_button.pack(side=tk.LEFT, padx=5, expand=True)
        self.apply_button_styles(self.clear_button)

        self.status_label = ttk.Label(self.root, text="", background=self.bg_color)
        self.status_label.pack(pady=5, padx=20)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, length=300, mode='indeterminate')
        self.progress.pack(pady=10, padx=20)

    def apply_button_styles(self, button):
        button.configure(style="TButton")
        button.bind("<Enter>", lambda e: button.configure(background=self.button_hover_bg_color, foreground=self.button_hover_fg_color))
        button.bind("<Leave>", lambda e: button.configure(background=self.button_bg_color, foreground=self.button_fg_color))

    def convert_to_audio(self):
        # Get the text from the text area
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text to convert.")
            return

        # Show progress bar
        self.progress.start()

        # Generate a unique filename for each conversion
        unique_filename = f"output_{uuid.uuid4().hex}.mp3"
        
        try:
            # Convert text to speech using gTTS
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(unique_filename)
            
            # Update the output file and status
            self.output_file = unique_filename
            self.status_label.config(text=f"Audio saved as {self.output_file}")

            # Enable buttons
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Conversion Error", f"An error occurred while converting text to audio: {e}")
        finally:
            # Stop the progress bar
            self.progress.stop()

    def play_audio(self):
        try:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.is_playing = True
            else:
                pygame.mixer.music.load(self.output_file)
                pygame.mixer.music.play(start=self.current_pos)
                self.is_playing = True
        except Exception as e:
            messagebox.showerror("Playback Error", f"An error occurred while playing the file: {e}")

    def pause_audio(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.current_pos = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
            self.is_paused = True
            self.is_playing = False

    def stop_audio(self):
        pygame.mixer.music.stop()
        self.current_pos = 0
        self.is_playing = False
        self.is_paused = False

    def save_audio(self):
        # Ask the user where to save the file
        filetypes = [("Audio Files", "*.mp3 *.wav *.ogg")]
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=filetypes)
        if file_path:
            try:
                # Check if the output file exists before exporting
                if os.path.exists(self.output_file):
                    audio = AudioSegment.from_file(self.output_file)
                    audio.export(file_path, format=self.format_var.get())
                    messagebox.showinfo("Save Success", f"Audio saved to {file_path}")
                else:
                    messagebox.showerror("Save Error", "No audio file to save.")
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred while saving the file: {e}")

    def clear_text(self):
        # Clear the text area
        self.text_area.delete("1.0", tk.END)

if __name__ == "__main__":
    root = ThemedTk(theme="breeze")  # Choose your preferred theme
    app = TextToAudioApp(root)
    root.mainloop()
