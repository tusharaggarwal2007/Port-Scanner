import socket
import threading
import flet as ft
from concurrent.futures import ThreadPoolExecutor

# Helper to get local device IP
def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except: return "127.0.0.1"

def main(page: ft.Page):
    page.title = "Port Scanner"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    page.window.icon = "cc.ico"
    stop_event = threading.Event()
    
    # UI Elements
    ip_field = ft.TextField(label="Target IP", value=get_local_ip(), width=300)
    port_start = ft.TextField(label="Start", value="1", width=120)
    port_end = ft.TextField(label="End", value="1024", width=120)
    filter_switch = ft.Switch(label="Show Open Only", value=True)
    status_text = ft.Text("Ready", color="#00FF00")
    log_area = ft.ListView(expand=True, spacing=2)

    # Thread-safe storage for scan data
    scan_results = []
    results_lock = threading.Lock()

    def update_display():
        new_controls = []
        show_only_open = filter_switch.value
        
        with results_lock:
            for port, is_open, desc in scan_results:
                if is_open:
                    new_controls.append(
                        ft.Text(f"[+] OPEN: {port} | {desc}", color="#00FF00", weight="bold")
                    )
                elif not show_only_open:
                    new_controls.append(
                        ft.Text(f"[-] CLOSED: {port} | {desc}", color="#333333")
                    )
        
        # Safely replace controls array and refresh UI
        log_area.controls = new_controls
        page.update()

    def on_filter_change(e):
        update_display()

    filter_switch.on_change = on_filter_change

    def scan_single(target, port):
        if stop_event.is_set():
            return
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                desc = socket.getservbyport(port, "tcp")
            except:
                desc = "Unknown"
            s.settimeout(0.2)
            is_open = s.connect_ex((target, port)) == 0
            
            with results_lock:
                scan_results.append((port, is_open, desc))
            
            # Throttle UI updates or update safely
            update_display()

    def start_scan(e):
        stop_event.clear()
        with results_lock:
            scan_results.clear()
        log_area.controls.clear()
        status_text.value = "Scanning..."
        page.update()
        
        def run_threads():
            with ThreadPoolExecutor(max_workers=200) as executor:
                for p in range(int(port_start.value), int(port_end.value) + 1):
                    if stop_event.is_set(): 
                        break
                    executor.submit(scan_single, ip_field.value, p)
            
            if not stop_event.is_set():
                status_text.value = "Scan Complete"
            else:
                status_text.value = "Stopped"
            update_display()
            
        threading.Thread(target=run_threads, daemon=True).start()

    def stop_scan(e):
        stop_event.set()
        status_text.value = "Stopped"
        page.update()

    page.add(
        ft.Stack([
            ft.Column([
                ft.Text("PORT SCANNER", size=24, color="#00FF00"),
                ip_field,
                ft.Row([port_start, port_end]),
                filter_switch,
                status_text,
                ft.Row([
                    ft.Button("START", on_click=start_scan, bgcolor="#004400"),
                    ft.Button("STOP", on_click=stop_scan, bgcolor="#440000")
                ]),
                ft.Container(
                    log_area, 
                    height=300, 
                    border=ft.Border(
                        left=ft.BorderSide(1, "#00FF00"),
                        top=ft.BorderSide(1, "#00FF00"),
                        right=ft.BorderSide(1, "#00FF00"),
                        bottom=ft.BorderSide(1, "#00FF00")
                    )
                )
            ])
        ]),
    )

if __name__ == "__main__":
    ft.run(main)