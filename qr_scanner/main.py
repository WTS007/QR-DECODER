import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import threading
from pyzbar.pyzbar import decode
import cv2
import pyperclip
from datetime import datetime
import json
import webbrowser
from tkinterdnd2 import TkinterDnD, DND_FILES

class QRScannerApp:
    def __init__(self):
        # Initialize the main window with modern styling
        self.window = TkinterDnD.Tk()
        self.window.title("QR Code Scanner")
        self.window.geometry("800x900")
        
        # Initialize settings
        self.load_settings()
        
        # Create main container
        self.create_main_interface()
        
        # Initialize camera variables
        self.camera = None
        self.camera_active = False
        self.camera_thread = None
        
        # Initialize history
        self.load_history()

    def load_settings(self):
        """Load application settings from file"""
        self.settings_file = "qr_scanner_settings.json"
        default_settings = {
            "theme": "light",
            "save_history": True,
            "camera_device": 0
        }
        
        try:
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = default_settings
            self.save_settings()

    def save_settings(self):
        """Save application settings to file"""
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

    def create_main_interface(self):
        """Create the main application interface"""
        # Create main container with padding
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Add title and theme toggle
        self.create_header()
        
        # Create tab view for different scanning methods
        self.create_tabs()
        
        # Create results area
        self.create_results_area()
        
        # Create history section
        self.create_history_section()

    def create_header(self):
        """Create header with title and theme toggle"""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="📷 QR Code Scanner",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Theme toggle
        self.theme_button = ctk.CTkButton(
            header_frame,
            text="🌙" if self.settings["theme"] == "light" else "☀️",
            width=40,
            command=self.toggle_theme
        )
        self.theme_button.pack(side="right", padx=10)

    def create_tabs(self):
        """Create tabs for file upload and camera capture"""
        self.tab_view = ctk.CTkTabview(self.main_frame)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # File Upload Tab
        file_tab = self.tab_view.add("File Upload")
        self.create_file_upload_area(file_tab)
        
        # Camera Tab
        camera_tab = self.tab_view.add("Camera")
        self.create_camera_area(camera_tab)

    def select_file(self):
        """Open file dialog to select an image"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.process_image(file_path)

    def create_file_upload_area(self, parent):
        """Create the file upload area with drag and drop support"""
        self.upload_frame = ctk.CTkFrame(
            parent,
            fg_color="#F8F9FA",
            corner_radius=8,
            border_width=2,
            border_color="#E9ECEF"
        )
        self.upload_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Add drag and drop binding
        self.upload_frame.drop_target_register(DND_FILES)
        self.upload_frame.dnd_bind('<<Drop>>', self.handle_drop)
        self.upload_frame.dnd_bind('<<DragEnter>>', lambda e: self.upload_frame.configure(border_color="#0D6EFD"))
        self.upload_frame.dnd_bind('<<DragLeave>>', lambda e: self.upload_frame.configure(border_color="#E9ECEF"))
        
        upload_label = ctk.CTkLabel(
            self.upload_frame,
            text="⬆️",
            font=ctk.CTkFont(size=32)
        )
        upload_label.pack(pady=(40, 10))
        
        upload_text = ctk.CTkLabel(
            self.upload_frame,
            text="Drop files here or click to upload",
            font=ctk.CTkFont(size=14)
        )
        upload_text.pack()
        
        self.upload_button = ctk.CTkButton(
            self.upload_frame,
            text="Choose File",
            command=self.select_file
        )
        self.upload_button.pack(pady=20)
        
        # Preview area
        self.preview_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.preview_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.preview_label = None

    def create_camera_area(self, parent):
        """Create the camera capture area"""
        self.camera_frame = ctk.CTkFrame(parent)
        self.camera_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Camera feed display
        self.camera_label = ctk.CTkLabel(self.camera_frame, text="Camera feed will appear here")
        self.camera_label.pack(pady=20)
        
        # Camera controls
        controls_frame = ctk.CTkFrame(self.camera_frame, fg_color="transparent")
        controls_frame.pack(fill="x", pady=10)
        
        self.camera_button = ctk.CTkButton(
            controls_frame,
            text="Start Camera",
            command=self.toggle_camera
        )
        self.camera_button.pack(side="left", padx=5)
        
        self.capture_button = ctk.CTkButton(
            controls_frame,
            text="Capture",
            command=self.capture_frame,
            state="disabled"
        )
        self.capture_button.pack(side="left", padx=5)

    def create_results_area(self):
        """Create the results display area"""
        self.results_frame = ctk.CTkFrame(self.main_frame)
        self.results_frame.pack(fill="x", padx=20, pady=10)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(self.results_frame)
        self.progress.set(0)
        
        # Results display
        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="",
            wraplength=600
        )
        self.results_label.pack(pady=10)
        
        # Copy button
        self.copy_button = ctk.CTkButton(
            self.results_frame,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
            state="disabled"
        )
        self.copy_button.pack(pady=5)

    def create_history_section(self):
        """Create the scan history section"""
        self.history_frame = ctk.CTkFrame(self.main_frame)
        self.history_frame.pack(fill="x", padx=20, pady=10)
        
        history_label = ctk.CTkLabel(
            self.history_frame,
            text="Recent Scans",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        history_label.pack(pady=5)
        
        self.history_list = ctk.CTkTextbox(
            self.history_frame,
            height=100
        )
        self.history_list.pack(fill="x", padx=10, pady=5)

    def handle_drop(self, event):
        """Handle file drop events"""
        file_path = event.data
        if file_path:
            file_path = file_path.strip('{}')
            self.process_image(file_path)
        self.upload_frame.configure(border_color="#E9ECEF")

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        new_theme = "dark" if self.settings["theme"] == "light" else "light"
        self.settings["theme"] = new_theme
        ctk.set_appearance_mode(new_theme)
        self.theme_button.configure(text="☀️" if new_theme == "dark" else "🌙")
        self.save_settings()

    def toggle_camera(self):
        """Toggle camera on/off"""
        if not self.camera_active:
            self.start_camera()
        else:
            self.stop_camera()

    def start_camera(self):
        """Start camera feed"""
        self.camera = cv2.VideoCapture(self.settings["camera_device"])
        if self.camera.isOpened():
            self.camera_active = True
            self.camera_button.configure(text="Stop Camera")
            self.capture_button.configure(state="normal")
            self.camera_thread = threading.Thread(target=self.update_camera_feed)
            self.camera_thread.daemon = True
            self.camera_thread.start()
        else:
            self.show_error("Could not open camera")

    def stop_camera(self):
        """Stop camera feed"""
        self.camera_active = False
        if self.camera:
            self.camera.release()
        self.camera_button.configure(text="Start Camera")
        self.capture_button.configure(state="disabled")
        self.camera_label.configure(image=None, text="Camera feed will appear here")

    def update_camera_feed(self):
        """Update camera feed display"""
        while self.camera_active:
            ret, frame = self.camera.read()
            if ret:
                # Convert frame to RGB and create PhotoImage
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                frame_pil.thumbnail((400, 300))
                photo = ImageTk.PhotoImage(frame_pil)
                
                # Update label in main thread
                self.window.after(0, self.camera_label.configure, {"image": photo})
                self.camera_label.image = photo

    def capture_frame(self):
        """Capture frame from camera and scan for QR code"""
        if self.camera_active:
            ret, frame = self.camera.read()
            if ret:
                # Save frame temporarily
                temp_path = "temp_capture.png"
                cv2.imwrite(temp_path, frame)
                
                # Process the captured frame
                self.process_image(temp_path)
                
                # Clean up temporary file
                try:
                    os.remove(temp_path)
                except:
                    pass

    def process_image(self, file_path):
        """Process image file for QR code scanning"""
        try:
            # Show progress bar
            self.progress.pack(pady=5)
            self.progress.set(0)
            
            # Load and create preview
            image = Image.open(file_path)
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)
            
            # Update preview
            if self.preview_label:
                self.preview_label.destroy()
            self.preview_label = ctk.CTkLabel(self.preview_frame, text="")
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo
            self.preview_label.pack(pady=10)
            
            # Start scanning in separate thread
            thread = threading.Thread(target=self.scan_qr, args=(file_path,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.show_error(f"Error processing image: {str(e)}")

    def scan_qr(self, file_path):
        """Scan QR code in separate thread"""
        try:
            # Update progress
            self.window.after(0, self.progress.set, 0.3)
            
            # Decode QR code
            img = Image.open(file_path)
            decoded_data = decode(img)
            
            # Update progress
            self.window.after(0, self.progress.set, 0.6)
            
            # Update UI in main thread
            self.window.after(0, self.update_results, decoded_data)
            
        except Exception as e:
            self.window.after(0, self.show_error, f"Error scanning QR code: {str(e)}")

    def update_results(self, decoded_data):
        """Update UI with scan results"""
        self.progress.set(1.0)
        self.window.after(1000, self.progress.pack_forget)
        
        if decoded_data:
            result = decoded_data[0].data.decode('utf-8')
            self.results_label.configure(
                text=f"Decoded QR content:\n{result}",
                text_color="#0D6EFD"
            )
            self.copy_button.configure(state="normal")
            self.add_to_history(result)
        else:
            self.results_label.configure(
                text="No QR code found in the image.",
                text_color="#DC3545"
            )
            self.copy_button.configure(state="disabled")

    def copy_to_clipboard(self):
        """Copy results to clipboard"""
        result_text = self.results_label.cget("text").replace("Decoded QR content:\n", "")
        pyperclip.copy(result_text)
        
        # Show temporary confirmation
        original_text = self.copy_button.cget("text")
        self.copy_button.configure(text="Copied!")
        self.window.after(1500, lambda: self.copy_button.configure(text=original_text))

    def add_to_history(self, result):
        """Add scan result to history"""
        if self.settings["save_history"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history_entry = f"{timestamp}: {result}\n"
            self.history_list.insert("1.0", history_entry)
            self.save_history()

    def load_history(self):
        """Load scan history from file"""
        try:
            with open("qr_scan_history.txt", "r") as f:
                history = f.read()
                if hasattr(self, 'history_list'):
                    self.history_list.delete("1.0", "end")
                    self.history_list.insert("1.0", history)
        except FileNotFoundError:
            pass

    def save_history(self):
        """Save scan history to file"""
        if self.settings["save_history"]:
            with open("qr_scan_history.txt", "w") as f:
                f.write(self.history_list.get("1.0", "end"))

    def show_error(self, message):
        """Show error message in results area"""
        self.progress.pack_forget()
        self.results_label.configure(text=message, text_color="#DC3545")
        self.copy_button.configure(state="disabled")

    def on_closing(self):
        """Handle application closing"""
        # Stop camera if active
        if self.camera_active:
            self.stop_camera()
        
        # Save settings and history
        self.save_settings()
        self.save_history()
        
        # Close the window
        self.window.destroy()

    def run(self):
        """Start the application"""
        # Set up closing handler
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Start the main loop
        self.window.mainloop()

if __name__ == "__main__":
    app = QRScannerApp()
    app.run()