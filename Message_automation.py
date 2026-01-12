import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import pywhatkit as kit
import threading
import time
import pandas as pd
import os
from datetime import datetime

class WhatsAppAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Message Automator")
        self.root.geometry("700x850")
        self.root.configure(bg="#f5f5f5")
        
        self.phone_numbers = []
        
        # --- UI LAYOUT ---
        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Label(self.root, text="WhatsApp Automation Tool", font=("Helvetica", 18, "bold"), bg="#075E54", fg="white", pady=10)
        header.pack(fill="x")

        # 1. File Upload Section
        file_frame = tk.LabelFrame(self.root, text=" 1. Contact List (Excel/CSV/TXT) ", font=("Arial", 10, "bold"), padx=15, pady=15, bg="#ffffff")
        file_frame.pack(fill="x", padx=20, pady=10)

        self.file_info = tk.Label(file_frame, text="No file loaded. Please select a file.", fg="red", bg="#ffffff")
        self.file_info.pack(side="left")

        btn_browse = tk.Button(file_frame, text="📁 Choose File", command=self.load_file, bg="#34b7f1", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=10)
        btn_browse.pack(side="right")

        # 2. Message Section
        msg_frame = tk.LabelFrame(self.root, text=" 2. Message Content ", font=("Arial", 10, "bold"), padx=15, pady=15, bg="#ffffff")
        msg_frame.pack(fill="x", padx=20, pady=10)

        self.msg_text = scrolledtext.ScrolledText(msg_frame, height=10, font=("Segoe UI", 10))
        self.msg_text.pack(fill="x")
        
        # Default Message from your code
        default_msg = ("Kindly join the group ASAP for updates on the SnapAR Workshop happening on 27th Oct 2025.\n"
                       "👉 https://chat.whatsapp.com/GiRACH58E9aJ3TG5O1tBv5\n\n"
                       "📚 Learn XR/AR concepts, SnapAR tools, and Lens building.\n"
                       "💻 Bring your laptop tomorrow — it’s mandatory.\n"
                       "🎟️ Entry only for registered GITM students.")
        self.msg_text.insert(tk.END, default_msg)

        # 3. Settings Section
        settings_frame = tk.Frame(self.root, bg="#f5f5f5")
        settings_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(settings_frame, text="Delay between messages (seconds):", bg="#f5f5f5").pack(side="left")
        self.delay_entry = tk.Entry(settings_frame, width=5)
        self.delay_entry.insert(0, "45")
        self.delay_entry.pack(side="left", padx=10)

        # 4. Progress and Controls
        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate", length=600)
        self.progress.pack(pady=15)

        self.start_btn = tk.Button(self.root, text="🚀 START SENDING MESSAGES", command=self.start_thread, 
                                   bg="#25D366", fg="white", font=("Arial", 12, "bold"), pady=10, cursor="hand2")
        self.start_btn.pack(fill="x", padx=20)

        # 5. Log Window
        log_frame = tk.LabelFrame(self.root, text=" Live Status Log ", font=("Arial", 10, "bold"), bg="#ffffff")
        log_frame.pack(fill="both", expand=True, padx=20, pady=15)

        self.log_area = scrolledtext.ScrolledText(log_frame, state='disabled', bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9))
        self.log_area.pack(fill="both", expand=True)

    # --- LOGIC ---

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Data Files", "*.xlsx *.csv *.txt")])
        if not path:
            return
        
        try:
            ext = os.path.splitext(path)[1].lower()
            if ext == '.csv':
                df = pd.read_csv(path)
                self.phone_numbers = self.clean_dataframe(df)
            elif ext == '.xlsx':
                df = pd.read_excel(path)
                self.phone_numbers = self.clean_dataframe(df)
            elif ext == '.txt':
                with open(path, 'r') as f:
                    self.phone_numbers = [line.strip() for line in f if line.strip()]
            
            self.file_info.config(text=f"Loaded: {os.path.basename(path)} ({len(self.phone_numbers)} contacts)", fg="green")
            self.log(f"File loaded: {len(self.phone_numbers)} contacts found.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")

    def clean_dataframe(self, df):
        # Look for common column names
        cols = [c for c in df.columns if any(x in c.lower() for x in ['phone', 'number', 'mobile', 'contact'])]
        target_col = cols[0] if cols else df.columns[0]
        
        # Convert to string and remove .0 if it's an excel float
        return [str(val).split('.')[0].strip() for val in df[target_col].dropna()]

    def start_thread(self):
        if not self.phone_numbers:
            messagebox.showwarning("Missing Data", "Please upload a contact list first.")
            return
        
        confirm = messagebox.askyesno("Confirm", f"Sending to {len(self.phone_numbers)} contacts. Start now?")
        if confirm:
            thread = threading.Thread(target=self.process_sending, daemon=True)
            thread.start()

    def process_sending(self):
        self.start_btn.config(state="disabled", text="RUNNING...")
        msg_body = self.msg_text.get("1.0", tk.END).strip()
        delay = int(self.delay_entry.get())
        
        self.progress['maximum'] = len(self.phone_numbers)
        logs = []

        for i, raw_num in enumerate(self.phone_numbers, start=1):
            # Format number (your logic)
            number = raw_num if raw_num.startswith('+') else '+91' + raw_num
            
            self.log(f"Sending {i}/{len(self.phone_numbers)} to {number}")
            
            try:
                # Execution (your logic)
                kit.sendwhatmsg_instantly(
                    phone_no=number,
                    message=msg_body,
                    wait_time=12,
                    tab_close=True,
                    close_time=4
                )
                self.log(f"✅ Success: {number}")
                logs.append({"Number": number, "Status": "Sent", "Time": datetime.now()})
            except Exception as e:
                self.log(f"❌ Failed: {number} | {e}")
                logs.append({"Number": number, "Status": f"Error: {e}", "Time": datetime.now()})

            self.progress['value'] = i
            
            if i < len(self.phone_numbers):
                self.log(f"Cooling down for {delay} seconds...")
                time.sleep(delay)

        # Wrap up
        pd.DataFrame(logs).to_csv("automation_report.csv", index=False)
        self.log("🏁 Batch Complete. Report saved to 'automation_report.csv'.")
        self.start_btn.config(state="normal", text="🚀 START SENDING MESSAGES")
        messagebox.showinfo("Success", "All messages have been processed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppAutomationApp(root)
    root.mainloop()