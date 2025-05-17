import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import tempfile
import logging


class ImagifyApp(ctk.CTk):
    """Imagify Image Converter - Because who doesn't want to convert images?"""

    def __init__(self):
        """Initialize the Imagify app window, theme, colors, logging, and widgets. 
        Because we all need another app to convert images, right?"""
        super().__init__()

        self.setup_window()

        # Default path setup
        self.default_store_path = os.path.join(
            os.path.expanduser("~"), "Pictures", "Imagify"
        )
        os.makedirs(self.default_store_path, exist_ok=True)

        # Logging setup
        self.setup_logging()

        # UI Elements
        self.create_widgets()

    def setup_logging(self):
        """Set up logging because we need to keep track of all our mistakes."""
        log_dir = os.path.join(tempfile.gettempdir(), "Imagify")
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_dir, "logs.txt"),
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        logging.info("Imagify App Initialized")

    def setup_window(self):
        """Set up the window. Because aesthetics matter, even for image converters."""
        self.title("Imagify")
        self.geometry("520x400")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Dark modern color palette
        self.colors = {
            "background": "#121921",
            "card_bg": "#1e2738",
            "accent": "#4a90e2",
            "button_bg": "#3269b0",
            "button_hover": "#3e7ad9",
            "label_text": "#cfd6e4",
            "entry_bg": "#2b3749",
            "entry_text": "#e6ebf1"
        }

        self.configure(fg_color=self.colors["background"])

    def create_widgets(self):
        """Create the UI widgets. Because buttons and labels are essential for any app."""
        self.title_label = ctk.CTkLabel(
            self,
            text="Imagify",
            font=ctk.CTkFont(family="Segoe UI", size=38, weight="bold"),
            text_color=self.colors["accent"]
        )
        self.title_label.pack(pady=(30, 20))

        self.card_frame = ctk.CTkFrame(
            master=self,
            fg_color=self.colors["card_bg"],
            corner_radius=18,
            border_width=0
        )
        self.card_frame.pack(padx=30, pady=10, fill="both", expand=False)
        self.card_frame.grid_columnconfigure(0, weight=1, uniform="a")
        self.card_frame.grid_columnconfigure(1, weight=1, uniform="a")

        self.dest_label = ctk.CTkLabel(
            self.card_frame,
            text="Destination",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=self.colors["label_text"]
        )
        self.dest_label.grid(row=0, column=0, sticky="w", padx=20, pady=(30, 10), columnspan=2)

        self.format_var = ctk.StringVar(value="PNG")
        self.format_dropdown = ctk.CTkComboBox(
            master=self.card_frame,
            values=["PNG", "JPEG", "WEBP", "ICO", "TGA", "BMP", "GIF", "TIFF"],
            variable=self.format_var,
            width=150,
            fg_color=self.colors["entry_bg"],
            text_color=self.colors["entry_text"],
            button_color=self.colors["button_bg"],
            button_hover_color=self.colors["button_hover"],
            border_width=0,
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.format_dropdown.grid(row=1, column=0, padx=20, pady=(0, 30), sticky="w")

        self.select_image_button = ctk.CTkButton(
            master=self.card_frame,
            text="Select Images",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=self.colors["button_bg"],
            hover_color=self.colors["button_hover"],
            corner_radius=15,
            width=180,
            height=40,
            command=self.select_images
        )
        self.select_image_button.grid(row=1, column=1, padx=20, pady=(0, 30), sticky="e")

        self.submit_button = ctk.CTkButton(
            master=self.card_frame,
            text="Convert",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            fg_color=self.colors["accent"],
            hover_color="#3678f5",
            corner_radius=18,
            width=360,
            height=50,
            command=self.submit
        )
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=(0, 30), padx=20, sticky="ew")

        self.selected_image_paths = []

    def select_images(self):
        """Let the user pick some images. Because we like making choices for you."""
        filetypes = (
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
            ("All files", "*.*")
        )
        try:
            filenames = filedialog.askopenfilenames(
                title="Select images",
                filetypes=filetypes
            )
        except Exception as e:
            logging.error(f"File dialog failed: {e}")
            messagebox.showerror("Oops!", f"Failed to open file dialog. Here's why: {e}")
            return

        if filenames:
            self.selected_image_paths = list(filenames)
            self.select_image_button.configure(text="Images Selected")
            logging.info(f"Selected images: {self.selected_image_paths}")
        else:
            logging.info("No images selected, as usual.")

    def submit(self):
        """Convert your precious images because who doesn't want more file formats?"""
        self.submit_button.configure(text="Converting...", state="disabled")

        if not self.selected_image_paths:
            messagebox.showwarning(
                "No images selected", 
                "No images? Sure, let's just stare at an empty conversion."
            )
            logging.warning("Submit pressed without selecting images.")
            self.submit_button.configure(text="Convert", state="normal")
            return

        selected_format = self.format_var.get().lower()
        logging.info(f"Starting conversion to {selected_format.upper()}")

        try:
            success = self.convert_images(selected_format)
            if success:
                messagebox.showinfo("Conversion Success", f"Images have been converted to {selected_format.upper()} format.")
            else:
                messagebox.showerror("Conversion Failed", "Something went terribly wrong. Check the logs for details.")
        except Exception as e:
            logging.error(f"Unexpected error during conversion: {e}")
            messagebox.showerror("Error", f"Unexpected error: {e}")

        self.select_image_button.configure(text="Select Images")
        self.submit_button.configure(text="Convert", state="normal")

    def convert_images(self, selected_format: str) -> bool:
        """Convert images to your chosen format, handling transparency because JPEG hates it."""
        # Flag to detect if at least one image converted successfully
        any_success = False
        for image_path in self.selected_image_paths:
            try:
                filename = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(self.default_store_path, f"{filename}.{selected_format}")
                image = Image.open(image_path)

                # Convert to RGB if format doesn't support alpha channel; because transparency is overrated
                if selected_format in ["jpg", "jpeg", "bmp"] and image.mode in ("RGBA", "LA"):
                    logging.info(f"Converting {filename} from {image.mode} to RGB for {selected_format.upper()}")
                    # Create a white background and composite the image on it to avoid black backgrounds
                    background = Image.new("RGB", image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1])  # Paste using alpha channel as mask
                    image = background
                elif image.mode == 'P':
                    # Convert palette images to RGBA to reduce surprises
                    image = image.convert('RGBA')

                # Attempt saving with fallback encodings for tricky formats
                save_format = "JPEG" if selected_format == "jpg" else selected_format.upper()
                try:
                    image.save(output_path, save_format)
                except OSError as e:
                    # Some formats may fail with certain parameters, try saving as PNG fallback
                    logging.warning(f"Failed saving {filename} as {save_format}, trying PNG fallback: {e}")
                    fallback_path = os.path.join(self.default_store_path, f"{filename}_fallback.png")
                    image.save(fallback_path, "PNG")
                    logging.info(f"Saved fallback image as {fallback_path}")
                    continue  # Continue converting other images

                logging.info(f"Saved: {output_path}")
                any_success = True

            except Exception as e:
                logging.error(f"Failed to convert {image_path} - {e}")
                messagebox.showerror("Error Occurred", f"Failed to convert {image_path}: {e}")
                # Continue trying to convert remaining images instead of stopping abruptly
                continue

        return any_success


if __name__ == "__main__":
    app = ImagifyApp()
    app.mainloop()

