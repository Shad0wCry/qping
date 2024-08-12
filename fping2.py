import tkinter as tk
from tkinter import scrolledtext
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.ip_label = tk.Label(self)
        self.ip_label["text"] = "Enter IP addresses (one per line):"
        self.ip_label.grid(row=0, column=0, columnspan=2, sticky="nw")

        self.ip_entry = scrolledtext.ScrolledText(self, width=50, height=10)
        self.ip_entry.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.ping_button = tk.Button(self)
        self.ping_button["text"] = "Ping"
        self.ping_button["command"] = self.ping_ips
        self.ping_button.grid(row=2, column=0, sticky="ew")

        self.nslookup_button = tk.Button(self)
        self.nslookup_button["text"] = "Nslookup"
        self.nslookup_button["command"] = self.nslookup_ips
        self.nslookup_button.grid(row=2, column=1, sticky="ew")

        self.output_label = tk.Label(self)
        self.output_label["text"] = "Output:"
        self.output_label.grid(row=3, column=0, columnspan=2, sticky="nw")

        self.output_text = scrolledtext.ScrolledText(self, width=50, height=10)
        self.output_text.grid(row=4, column=0, columnspan=2, sticky="nsew")

        self.failed_ping_label = tk.Label(self)
        self.failed_ping_label["text"] = "Failed pings:"
        self.failed_ping_label.grid(row=5, column=0, columnspan=2, sticky="nw")

        self.failed_ping_text = scrolledtext.ScrolledText(self, width=50, height=5)
        self.failed_ping_text.grid(row=6, column=0, columnspan=2, sticky="nsew")

        self.failed_nslookup_label = tk.Label(self)
        self.failed_nslookup_label["text"] = "Failed nslookups:"
        self.failed_nslookup_label.grid(row=7, column=0, columnspan=2, sticky="nw")

        self.failed_nslookup_text = scrolledtext.ScrolledText(self, width=50, height=5)
        self.failed_nslookup_text.grid(row=8, column=0, columnspan=2, sticky="nsew")

        self.rowconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(8, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def ping_ips(self):
        ips = self.ip_entry.get("1.0", tk.END).splitlines()
        output = ""
        failed_output = ""
        for ip in ips:
            command = f"ping -n 1 {ip}"
            ping_output = os.popen(command).read()
            if "unreachable" in ping_output or "timed out" in ping_output:
                failed_output += f"Failed to ping {ip}\n"
            else:
                output += ping_output
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", output)
        self.failed_ping_text.delete("1.0", tk.END)
        self.failed_ping_text.insert("1.0", failed_output)

    def nslookup_ips(self):
     ips = self.ip_entry.get("1.0", tk.END).splitlines()
     output = ""
     failed_output = ""
     for ip in ips:
        command = f"nslookup {ip}"
        nslookup_output = os.popen(command).read()
        if "can't find" in nslookup_output or "connection timed out" in nslookup_output or "Non-existent domain" in nslookup_output:
            failed_output += f"Failed to nslookup {ip}\n"
        else:
            output += nslookup_output
     self.output_text.delete("1.0", tk.END)
     self.output_text.insert("1.0", output)
     self.failed_nslookup_text.delete("1.0", tk.END)
     self.failed_nslookup_text.insert("1.0", failed_output)

root = tk.Tk()
app = Application(master=root)
app.mainloop()