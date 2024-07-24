import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, ttk
from gtts import gTTS
from pydub import AudioSegment
import pygame
from ttkthemes import ThemedTk
from tkinter import font as tkfont

class TextToAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Audio Converter")
        self.root.geometry("600x500")  # Set a fixed window size

        # Initialize pygame mixer
        pygame.mixer.init()

        # Define font
        self.font = tkfont.Font(family="Helvetica", size=12)

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Define styles
        style = ttk.Style(self.root)
        style.configure("TButton", font=self.font, padding=10, relief='flat')
        style.configure("TLabel", font=self.font, padding=5)
        style.configure("TCombobox", font=self.font, padding=5)
        style.configure("TScale", background="#f0f0f0")

        # Text area
        self.text_area = tk.Text(self.root, wrap=tk.WORD, height=10, width=50, bg="#f0f0f0", fg="#333333", font=self.font, bd=0, highlightthickness=0)
        self.text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Format selection
        self.format_var = StringVar(value="mp3")
        self.format_menu = ttk.Combobox(self.root, textvariable=self.format_var, values=["mp3", "wav", "ogg"])
        self.format_menu.pack(pady=5, padx=10)

        # Rate, Volume, and Pitch controls
        self.rate_var = tk.IntVar(value=150)
        self.volume_var = tk.DoubleVar(value=1.0)
        self.pitch_var = tk.IntVar(value=50)

        ttk.Label(self.root, text="Speech Rate:").pack(pady=5, padx=10)
        self.rate_slider = tk.Scale(self.root, from_=50, to_=300, variable=self.rate_var, orient='horizontal', sliderlength=30, length=300)
        self.rate_slider.pack(pady=5, padx=10)

        ttk.Label(self.root, text="Volume:").pack(pady=5, padx=10)
        self.volume_slider = tk.Scale(self.root, from_=0, to_=1, variable=self.volume_var, orient='horizontal', sliderlength=30, length=300, resolution=0.1)
        self.volume_slider.pack(pady=5, padx=10)

        ttk.Label(self.root, text="Pitch (not directly supported in gTTS):").pack(pady=5, padx=10)
        self.pitch_slider = tk.Scale(self.root, from_=0, to_=100, variable=self.pitch_var, orient='horizontal', sliderlength=30, length=300)
        self.pitch_slider.pack(pady=5, padx=10)

        # Buttons
        self.convert_button = ttk.Button(self.root, text="Convert to Audio", command=self.convert_to_audio)
        self.convert_button.pack(pady=5, padx=10, fill=tk.X)

        self.play_button = ttk.Button(self.root, text="Play Audio", command=self.play_audio, state=tk.DISABLED)
        self.play_button.pack(pady=5, padx=10, fill=tk.X)

        self.save_button = ttk.Button(self.root, text="Save Audio", command=self.save_audio, state=tk.DISABLED)
        self.save_button.pack(pady=5, padx=10, fill=tk.X)

        self.clear_button = ttk.Button(self.root, text="Clear Text", command=self.clear_text)
        self.clear_button.pack(pady=5, padx=10, fill=tk.X)

        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack(pady=5, padx=10)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, length=300, mode='indeterminate')
        self.progress.pack(pady=10, padx=10)

        # Custom styling for rounded buttons
        self.style_button()

    def style_button(self):
        self.root.option_add('*TButton*borderWidth', 1)
        self.root.option_add('*TButton*relief', 'flat')
        self.root.option_add('*TButton*padding', [10, 5])
        self.root.option_add('*TButton*background', '#007BFF')
        self.root.option_add('*TButton*foreground', 'white')

    def convert_to_audio(self):
        # Get the text from the text area
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text to convert.")
            return

        # Show progress bar
        self.progress.start()

        # Convert text to speech using gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        self.output_file = "output.mp3"
        tts.save(self.output_file)

        # Update status and enable buttons
        self.status_label.config(text=f"Audio saved as {self.output_file}")
        self.play_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.progress.stop()

    def play_audio(self):
        try:
            # Load and play the audio file
            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play()
            
            # Wait for the music to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            messagebox.showerror("Playback Error", f"An error occurred while playing the file: {e}")

    def save_audio(self):
        # Ask the user where to save the file
        filetypes = [("Audio Files", "*.mp3 *.wav *.ogg")]
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=filetypes)
        if file_path:
            try:
                audio = AudioSegment.from_file(self.output_file)
                audio.export(file_path, format=self.format_var.get())
                messagebox.showinfo("Save Success", f"Audio saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred while saving the file: {e}")

    def clear_text(self):
        # Clear the text area
        self.text_area.delete("1.0", tk.END)

if __name__ == "__main__":
    root = ThemedTk(theme="breeze")  # Choose your preferred theme
    app = TextToAudioApp(root)
    root.mainloop()
