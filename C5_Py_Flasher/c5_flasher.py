# === ESP32-C5 Auto Flasher Script By: AWOK ===

import sys
import subprocess
import os
import platform
import glob
import time
import shutil
import argparse
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def ensure_package(pkg):
    try:
        __import__(pkg if pkg != 'gitpython' else 'git')
    except ImportError:
        print(f"Installing missing package: {pkg}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', pkg])

try:
    import serial.tools.list_ports
except ImportError:
    ensure_package('pyserial')
try:
    import esptool
except ImportError:
    ensure_package('esptool')
try:
    from colorama import Fore, Style
except ImportError:
    ensure_package('colorama')

# Dependency check and install if needed
REQUIRED_PACKAGES = [
    'pyserial',
    'esptool',
    'colorama'
]

def ensure_requirements():
    for pkg in REQUIRED_PACKAGES:
        ensure_package(pkg)
ensure_requirements()

# Finds the first file from a list of possible names in the bins folder
def find_file(name_options, bins_dir):
    for name in name_options:
        files = glob.glob(os.path.join(bins_dir, name))
        if files:
            return files[0]
    return None

CHIP_CONFIGS = {
    "esp32c5": {
        "display_name": "ESP32-C5",
        "bootloader_offset": "0x2000",
        "partition_offset": "0x8000",
        "ota_offset": "0xd000",
        "app_offset": "0x10000",
        "esptool_chip": "esp32c5",
    },
    "esp32": {
        "display_name": "ESP32",
        "bootloader_offset": "0x1000",
        "partition_offset": "0x8000",
        "ota_offset": "0xd000",
        "app_offset": "0x10000",
        "esptool_chip": "esp32",
    },
    "esp32-a1s": {
        "display_name": "ESP32-A1S",
        "bootloader_offset": "0x1000",
        "partition_offset": "0x8000",
        "ota_offset": "0xd000",
        "app_offset": "0x10000",
        "esptool_chip": "esp32",
    },
}

def list_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

COLOR_ANSI = {
    "yellow": Fore.YELLOW,
    "green": Fore.GREEN,
    "red": Fore.RED,
    "cyan": Fore.CYAN,
}

def choose_port(available_ports, preferred=None):
    if preferred and preferred in available_ports:
        return preferred
    if len(available_ports) == 1:
        return available_ports[0]
    print(Fore.YELLOW + "Multiple serial ports detected:" + Style.RESET_ALL)
    for idx, port in enumerate(available_ports, start=1):
        print(f"{idx}) {port}")
    while True:
        selection = input(Fore.YELLOW + "Select the port number to use: " + Style.RESET_ALL).strip()
        if selection.isdigit():
            choice = int(selection)
            if 1 <= choice <= len(available_ports):
                return available_ports[choice - 1]
        print(Fore.RED + "Invalid selection. Please try again." + Style.RESET_ALL)

def find_serial_port(args, log_fn=None):
    def log(message, color=None):
        if log_fn:
            log_fn(message, color)
        else:
            if color:
                ansi = COLOR_ANSI.get(color, "")
                print(ansi + message + Style.RESET_ALL)
            else:
                print(message)

    serial_port = None
    if args.port:
        available_ports = list_serial_ports()
        serial_port = choose_port(available_ports, preferred=args.port)
    elif not args.no_wait:
        existing_ports = set(list_serial_ports())
        log(f"Waiting for {args.chip_label} device to be connected...", "yellow")
        wait_start = time.time()
        while time.time() - wait_start < 30:
            current_ports = set(list_serial_ports())
            new_ports = current_ports - existing_ports
            if new_ports:
                if platform.system() == "Darwin":
                    macos_ports = [p for p in new_ports if p.startswith("/dev/cu.")]
                    serial_port = macos_ports[0] if macos_ports else new_ports.pop()
                else:
                    serial_port = new_ports.pop()
                break
            time.sleep(0.5)
    if serial_port is None:
        available_ports = list_serial_ports()
        if not available_ports:
            raise RuntimeError("No serial ports detected. Please connect your device and try again.")
        serial_port = choose_port(available_ports)
    return serial_port

def collect_bins(bins_dir):
    bootloader = find_file(['bootloader.bin'], bins_dir)
    partitions = find_file(['partition-table.bin', 'partitions.bin'], bins_dir)
    ota_data = find_file(['ota_data_initial.bin'], bins_dir)
    all_bins = glob.glob(os.path.join(bins_dir, "*.bin"))
    exclude = {bootloader, partitions, ota_data}
    firmware_bins = [f for f in all_bins if f not in exclude and os.path.isfile(f)]
    if not firmware_bins:
        raise RuntimeError("No application firmware .bin file found in the bins folder.")
    app_bin = max(firmware_bins, key=lambda f: os.path.getsize(f))
    return bootloader, partitions, ota_data, app_bin

def build_esptool_args(chip_config, serial_port, baud, bootloader, partitions, ota_data, app_bin):
    esptool_args = [
        '--chip', chip_config["esptool_chip"],
        '--port', serial_port,
        '--baud', str(baud),
        '--before', 'default_reset',
        '--after', 'hard_reset',
        'write_flash', '-z',
        chip_config["bootloader_offset"], bootloader,
        chip_config["partition_offset"], partitions,
    ]
    if ota_data:
        esptool_args += [chip_config["ota_offset"], ota_data]
    esptool_args += [chip_config["app_offset"], app_bin]
    return esptool_args

def run_flash(args, log_fn=None):
    def log(message, color=None):
        if log_fn:
            log_fn(message, color)
        else:
            if color:
                ansi = COLOR_ANSI.get(color, "")
                print(ansi + message + Style.RESET_ALL)
            else:
                print(message)

    if not os.path.isdir(args.bins_dir):
        raise RuntimeError(f"Bins directory not found: {args.bins_dir}")

    chip_config = CHIP_CONFIGS[args.chip]
    args.chip_label = chip_config["display_name"]

    serial_port = find_serial_port(args, log_fn=log_fn)
    log(f"Using serial port: {serial_port}", "green")

    bootloader, partitions, ota_data, app_bin = collect_bins(args.bins_dir)

    log(f"\nTarget chip:  {args.chip_label}", "cyan")
    log(f"Bootloader:   {bootloader or 'NOT FOUND'}")
    log(f"Partitions:   {partitions or 'NOT FOUND'}")
    log(f"OTA Data:     {ota_data or 'NOT FOUND'}")
    log(f"App (main):   {app_bin}\n")
    if not (bootloader and partitions):
        raise RuntimeError("Missing bootloader or partition table. Both are required for a complete flash!")

    if not args.auto_confirm:
        confirm = input(Fore.YELLOW + f"Ready to flash these files to {args.chip_label}? (y/N): " + Style.RESET_ALL)
        if confirm.strip().lower() != 'y':
            log("Aborting.")
            return

    esptool_args = build_esptool_args(
        chip_config,
        serial_port,
        args.baud,
        bootloader,
        partitions,
        ota_data,
        app_bin,
    )

    log(f"Flashing {args.chip_label} with bootloader, partition table, and application...", "yellow")
    try:
        esptool.main(esptool_args)
        log("Flashing complete!", "green")
    except Exception as exc:
        raise RuntimeError(f"Flashing failed: {exc}") from exc

def build_gui():
    root = tk.Tk()
    root.title("ESP32 Marauder Flasher")
    root.geometry("720x520")

    main_frame = ttk.Frame(root, padding=12)
    main_frame.pack(fill=tk.BOTH, expand=True)

    config_frame = ttk.LabelFrame(main_frame, text="Flash Settings", padding=10)
    config_frame.pack(fill=tk.X)

    chip_var = tk.StringVar(value="esp32c5")
    port_var = tk.StringVar()
    baud_var = tk.StringVar(value="921600")
    bins_var = tk.StringVar(value=os.path.join(os.path.dirname(__file__), "bins"))
    auto_detect_var = tk.BooleanVar(value=True)

    ttk.Label(config_frame, text="Chip:").grid(row=0, column=0, sticky=tk.W, pady=4)
    chip_menu = ttk.Combobox(config_frame, textvariable=chip_var, values=sorted(CHIP_CONFIGS.keys()), state="readonly")
    chip_menu.grid(row=0, column=1, sticky=tk.EW, pady=4)

    ttk.Label(config_frame, text="Port:").grid(row=1, column=0, sticky=tk.W, pady=4)
    port_menu = ttk.Combobox(config_frame, textvariable=port_var, state="readonly")
    port_menu.grid(row=1, column=1, sticky=tk.EW, pady=4)

    def refresh_ports():
        ports = list_serial_ports()
        port_menu["values"] = ports
        if ports:
            port_var.set(ports[0])

    ttk.Button(config_frame, text="Refresh Ports", command=refresh_ports).grid(row=1, column=2, padx=6, pady=4)

    ttk.Label(config_frame, text="Baud:").grid(row=2, column=0, sticky=tk.W, pady=4)
    ttk.Entry(config_frame, textvariable=baud_var).grid(row=2, column=1, sticky=tk.EW, pady=4)

    ttk.Label(config_frame, text="Bins Folder:").grid(row=3, column=0, sticky=tk.W, pady=4)
    bins_entry = ttk.Entry(config_frame, textvariable=bins_var)
    bins_entry.grid(row=3, column=1, sticky=tk.EW, pady=4)

    def browse_bins():
        selection = filedialog.askdirectory(initialdir=bins_var.get() or os.getcwd())
        if selection:
            bins_var.set(selection)

    ttk.Button(config_frame, text="Browse", command=browse_bins).grid(row=3, column=2, padx=6, pady=4)

    ttk.Checkbutton(
        config_frame,
        text="Auto-detect new device (wait up to 30s)",
        variable=auto_detect_var,
    ).grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=4)

    config_frame.columnconfigure(1, weight=1)

    log_frame = ttk.LabelFrame(main_frame, text="Status", padding=10)
    log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    log_text = tk.Text(log_frame, height=12, wrap=tk.WORD, state=tk.DISABLED)
    log_text.pack(fill=tk.BOTH, expand=True)

    def append_log(message, color=None):
        log_text.configure(state=tk.NORMAL)
        if color:
            tag = color
            log_text.tag_configure(tag, foreground=color)
            log_text.insert(tk.END, message + "\n", tag)
        else:
            log_text.insert(tk.END, message + "\n")
        log_text.configure(state=tk.DISABLED)
        log_text.see(tk.END)

    def run_flash_thread():
        try:
            baud_value = int(baud_var.get())
        except ValueError:
            messagebox.showerror("Invalid Baud", "Baud rate must be a number.")
            return

        if not bins_var.get():
            messagebox.showerror("Missing Bins Folder", "Please select a bins folder.")
            return

        args = argparse.Namespace(
            chip=chip_var.get(),
            port=port_var.get() if port_var.get() else None,
            baud=baud_value,
            bins_dir=bins_var.get(),
            no_wait=not auto_detect_var.get(),
            auto_confirm=True,
        )
        args.chip_label = CHIP_CONFIGS[args.chip]["display_name"]

        append_log(f"Starting flash for {args.chip_label}...")

        def worker():
            try:
                run_flash(args, log_fn=append_log)
            except Exception as exc:
                append_log(str(exc), "red")
                messagebox.showerror("Flash Failed", str(exc))

        threading.Thread(target=worker, daemon=True).start()

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X)
    ttk.Button(button_frame, text="Flash", command=run_flash_thread).pack(side=tk.RIGHT, padx=4)
    ttk.Button(button_frame, text="Exit", command=root.destroy).pack(side=tk.RIGHT)

    refresh_ports()
    return root

def main():
    parser = argparse.ArgumentParser(description="ESP32 Auto Flasher (bins subdir)")
    parser.add_argument(
        "--chip",
        default="esp32c5",
        choices=sorted(CHIP_CONFIGS.keys()),
        help="Target chip type (default: esp32c5). Use esp32-a1s for ESP32-A1S.",
    )
    parser.add_argument(
        "--port",
        default=None,
        help="Serial port to use (optional). If not provided, auto-detects.",
    )
    parser.add_argument(
        "--baud",
        default="921600",
        help="Baud rate for flashing (default: 921600).",
    )
    parser.add_argument(
        "--bins-dir",
        default=os.path.join(os.path.dirname(__file__), "bins"),
        help="Directory containing the .bin files (default: bins folder).",
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Skip waiting for a new device and instead select from available ports.",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the graphical interface instead of the CLI flow.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompt and flash immediately.",
    )
    args = parser.parse_args()

    if args.gui:
        root = build_gui()
        root.mainloop()
        return

    args.auto_confirm = args.yes

    run_flash(args)

if __name__ == "__main__":
    main()
