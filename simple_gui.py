import tkinter as tk
from tkinter import ttk, messagebox
from micronix_controller.connect import MicronixSerialConnection
from micronix_controller.commands import Commands
import time
import threading
import serial.tools.list_ports

class SerialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Micronix Serial Command Interface")
        self.root.geometry("600x300")

        self.port_var = tk.StringVar()
        self.axis_var = tk.StringVar()
        self.command_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self.polling = False
        self.polling_thread = None

        self.create_widgets()
        self.serial_conn = None
        self.update_ports()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Port:").grid(row=0, column=0, sticky=tk.W)
        self.port_combobox = ttk.Combobox(frame, textvariable=self.port_var)
        self.port_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Button(frame, text="Refresh Ports", command=self.update_ports).grid(row=0, column=2, sticky=tk.W)
        
        ttk.Label(frame, text="Axis:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.axis_var).grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(frame, text="Command:").grid(row=2, column=0, sticky=tk.W)
        self.command_combobox = ttk.Combobox(frame, textvariable=self.command_var)
        self.command_combobox['values'] = [f"{cmd.command} - {cmd.description}" for cmd in Commands]
        self.command_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E))
        
        ttk.Button(frame, text="Send Command", command=self.send_command).grid(row=3, column=1, sticky=tk.E)
        
        ttk.Label(frame, text="Result:").grid(row=4, column=0, sticky=tk.W)
        self.result_label = ttk.Label(frame, textvariable=self.result_var)
        self.result_label.grid(row=4, column=1, sticky=(tk.W, tk.E))
        
        self.history_text = tk.Text(frame, height=10, wrap=tk.WORD)
        self.history_text.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.clear_button = ttk.Button(frame, text="Clear", command=self.clear_result)
        self.clear_button.grid(row=6, column=0, sticky=tk.W)
        
        self.poll_var = tk.BooleanVar()
        self.poll_checkbox = ttk.Checkbutton(frame, text="Enable Continuous Polling", variable=self.poll_var)
        self.poll_checkbox.grid(row=6, column=1, sticky=tk.W)
        
        self.poll_button = ttk.Button(frame, text="Start Polling", command=self.toggle_polling)
        self.poll_button.grid(row=6, column=2, sticky=tk.E)

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(5, weight=1)
        
    def update_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports if port.manufacturer is not None and "FTDI" in port.manufacturer]
            
        self.port_combobox['values'] = port_list

    def send_command(self):
        port = self.port_var.get()
        axis = self.axis_var.get()
        command_str = self.command_var.get().split(" - ")[0]

        if not port or not axis or not command_str:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        command = None
        for cmd in Commands:
            if cmd.command == command_str:
                command = cmd
                break
        
        if command is None:
            messagebox.showerror("Error", "Invalid command")
            return

        try:
            with MicronixSerialConnection(port) as conn:
                result = conn.poll_values(axis, command)
                if result:
                    self.result_var.set(result)
                    self.history_text.insert(tk.END, f"Sent: {axis}{command.command}?\nReceived: {result}\n\n")
                else:
                    self.result_var.set("No response or invalid")
                    self.history_text.insert(tk.END, f"Sent: {axis}{command.command}?\nReceived: No response or invalid\n\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.history_text.insert(tk.END, f"Error: {str(e)}\n\n")

    def clear_result(self):
        self.result_var.set("")
        self.history_text.delete(1.0, tk.END)

    def toggle_polling(self):
        if self.polling:
            self.polling = False
            self.poll_button.config(text="Start Polling")
            if self.polling_thread and self.polling_thread.is_alive():
                self.polling_thread.join()
        else:
            self.polling = True
            self.poll_button.config(text="Stop Polling")
            self.polling_thread = threading.Thread(target=self.poll_loop)
            self.polling_thread.start()

    def poll_loop(self):
        port = self.port_var.get()
        axis = self.axis_var.get()
        command_str = self.command_var.get().split(" - ")[0]

        if not port or not axis or not command_str:
            messagebox.showerror("Error", "Please fill in all fields")
            self.polling = False
            self.poll_button.config(text="Start Polling")
            return

        command = None
        for cmd in Commands:
            if cmd.command == command_str:
                command = cmd
                break
        
        if command is None:
            messagebox.showerror("Error", "Invalid command")
            self.polling = False
            self.poll_button.config(text="Start Polling")
            return

        try:
            with MicronixSerialConnection(port) as conn:
                while self.polling:
                    result = conn.poll_values(axis, command)
                    if result:
                        self.result_var.set(result)
                        self.history_text.insert(tk.END, f"Sent: {axis}{command.command}?\nReceived: {result}\n\n")
                    else:
                        self.result_var.set("No response or invalid")
                        self.history_text.insert(tk.END, f"Sent: {axis}{command.command}?\nReceived: No response or invalid\n\n")
                    time.sleep(1)  # Poll every second
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.history_text.insert(tk.END, f"Error: {str(e)}\n\n")
            self.polling = False
            self.poll_button.config(text="Start Polling")

def main():
    root = tk.Tk()
    app = SerialGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
