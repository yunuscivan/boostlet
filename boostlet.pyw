import os
import sys
import ctypes

def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
        pythonw = sys.executable.replace("python.exe", "pythonw.exe")
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", pythonw, f'"{script}" {params}', None, 1)
        except Exception as e:
            print("Failed to relaunch as admin:", e)
        sys.exit()

run_as_admin()

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QLineEdit, QCheckBox, QMessageBox,
    QSystemTrayIcon, QMenu, QFrame
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QTimer, Qt
import psutil
import platform
import json
import time
import subprocess

class BoostletGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boostlet - Intelligent Resource Optimizer")
        self.setFixedSize(400, 600)
        self.setWindowIcon(QIcon("boostlet.ico"))

        self.icon_label = QLabel()
        pixmap = QPixmap("boostlet.ico").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(pixmap)

        self.title_label = QLabel("<h1>Boostlet</h1>")
        self.title_label.setAlignment(Qt.AlignCenter)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.icon_label)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        header_line = QFrame()
        header_line.setFrameShape(QFrame.HLine)
        header_line.setFrameShadow(QFrame.Sunken)

        self.cpu_label = QLabel("CPU Threshold (%):")
        self.cpu_input = QLineEdit()
        self.ram_label = QLabel("RAM Threshold (%):")
        self.ram_input = QLineEdit()

        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(self.cpu_label)
        threshold_layout.addWidget(self.cpu_input)
        threshold_layout.addWidget(self.ram_label)
        threshold_layout.addWidget(self.ram_input)

        self.alert_checkbox = QCheckBox("Alert me when thresholds are exceeded")
        self.apply_checkbox = QCheckBox("Auto-clean RAM when thresholds are exceeded")
        self.both_required_checkbox = QCheckBox("Only trigger if BOTH thresholds are exceeded (recommended)")
        self.both_required_checkbox.setChecked(True)
        self.deep_clean_checkbox = QCheckBox("Enable deep RAM cleaning (standby purge)")

        self.autostart_checkbox = QCheckBox("Start Boostlet on system startup")
        self.interval_checkbox = QCheckBox("Scheduled RAM Cleaning (Interval Mode)")
        self.interval_input = QLineEdit()
        self.interval_input.setPlaceholderText("Minutes (e.g., 30)")
        self.interval_input.setEnabled(False)

        info_line = QFrame()
        info_line.setFrameShape(QFrame.HLine)
        info_line.setFrameShadow(QFrame.Sunken)

        self.system_info_title = QLabel("\n🔎 System Info:")
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignLeft)

        uptime_line = QFrame()
        uptime_line.setFrameShape(QFrame.HLine)
        uptime_line.setFrameShadow(QFrame.Sunken)

        self.usage_label = QLabel("CPU: --%\nRAM: --%")
        self.usage_label.setAlignment(Qt.AlignLeft)

        self.threshold_exceeded_line = QFrame()
        self.threshold_exceeded_line.setFrameShape(QFrame.HLine)
        self.threshold_exceeded_line.setFrameShadow(QFrame.Sunken)
        self.threshold_exceeded_line.setVisible(False)

        self.clean_now_button = QPushButton("Clean RAM Now")
        self.clean_now_button.clicked.connect(self.clean_and_notify_gui)

        self.close_button = QPushButton("Close Window")
        self.close_button.clicked.connect(self.hide)

        layout = QVBoxLayout()
        layout.addLayout(header_layout)
        layout.addWidget(header_line)
        layout.addLayout(threshold_layout)
        layout.addWidget(self.alert_checkbox)
        layout.addWidget(self.apply_checkbox)
        layout.addWidget(self.both_required_checkbox)
        layout.addWidget(self.deep_clean_checkbox)
        layout.addWidget(self.autostart_checkbox)
        layout.addWidget(self.interval_checkbox)
        layout.addWidget(self.interval_input)
        layout.addWidget(info_line)
        layout.addWidget(self.system_info_title)
        layout.addWidget(self.info_label)
        layout.addWidget(uptime_line)
        layout.addWidget(self.usage_label)
        layout.addWidget(self.threshold_exceeded_line)
        layout.addStretch()
        layout.addWidget(self.clean_now_button)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

        self.load_settings()
        self.update_system_info()

        self.cpu_input.textChanged.connect(self.save_settings)
        self.ram_input.textChanged.connect(self.save_settings)
        self.alert_checkbox.stateChanged.connect(self.save_settings)
        self.apply_checkbox.stateChanged.connect(self.save_settings)
        self.both_required_checkbox.stateChanged.connect(self.save_settings)
        self.deep_clean_checkbox.stateChanged.connect(self.save_settings)
        self.autostart_checkbox.stateChanged.connect(self.toggle_autostart)
        self.interval_checkbox.stateChanged.connect(self.switch_modes)
        self.interval_input.textChanged.connect(self.update_interval_timer)
        self.alert_checkbox.stateChanged.connect(self.toggle_alert_auto_exclusivity)
        self.apply_checkbox.stateChanged.connect(self.toggle_alert_auto_exclusivity)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_usage)
        self.timer.start(3000)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Boostlet",
            "Uygulama arka planda çalışıyor.",
            QSystemTrayIcon.Information,
            3000
        )

    def show_about(self):
        QMessageBox.information(self, "About Boostlet", "2025 Yunus Civan · Switzerland")

    def clean_and_notify_gui(self):
        self.clean_ram()
        if hasattr(self, 'cleaning_result'):
            QMessageBox.information(self, "Boostlet - RAM Cleaner", self.cleaning_result)

    def clean_ram_and_notify_tray(self):
        self.clean_ram()
        if hasattr(self, 'cleaning_result'):
            self.tray_icon.hide()
            self.tray_icon.show()
            QApplication.processEvents()
            time.sleep(0.1)
            self.tray_icon.showMessage(
                "Boostlet",
                self.cleaning_result,
                QSystemTrayIcon.Information,
                5000
            )

    def clean_ram(self):
        os_type = platform.system()
        if os_type == "Windows":
            before_ram = psutil.virtual_memory().percent
            PROCESS_QUERY_INFORMATION = 0x0400
            PROCESS_SET_QUOTA = 0x0100
            empty_ws = ctypes.windll.psapi.EmptyWorkingSet

            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    handle = ctypes.windll.kernel32.OpenProcess(
                        PROCESS_QUERY_INFORMATION | PROCESS_SET_QUOTA, False, proc.info['pid']
                    )
                    if handle:
                        empty_ws(handle)
                        ctypes.windll.kernel32.CloseHandle(handle)
                except:
                    continue

            after_ram = psutil.virtual_memory().percent
            self.cleaning_result = f"RAM cleaned!\nBefore: {before_ram:.1f}% → After: {after_ram:.1f}%"

            if self.deep_clean_checkbox.isChecked():
                self.cleaning_result += "\nDeep RAM cleaning enabled."
                try:
                    subprocess.run(["EmptyStandbyList.exe", "standbylist"], shell=True)
                    subprocess.run(["EmptyStandbyList.exe", "workingsets"], shell=True)
                except Exception as e:
                    self.cleaning_result += f"\nDeep clean failed: {e}"
        else:
            self.cleaning_result = "RAM cleaning only supported on Windows."

    def update_usage(self):
        try:
            self.cpu_threshold = int(self.cpu_input.text())
            self.ram_threshold = int(self.ram_input.text())
        except ValueError:
            self.cpu_threshold = 80
            self.ram_threshold = 80

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        usage_text = f"CPU: {cpu}%\nRAM: {ram}%"

        both_required = self.both_required_checkbox.isChecked()
        threshold_condition = (
            (cpu >= self.cpu_threshold and ram >= self.ram_threshold)
            if both_required else (cpu >= self.cpu_threshold or ram >= self.ram_threshold)
        )

        if not self.interval_checkbox.isChecked() and threshold_condition:
            usage_text += "\n⚠️ Threshold exceeded!"
            self.threshold_exceeded_line.setVisible(True)
            if self.alert_checkbox.isChecked():
                self.ask_user(cpu, ram)
            elif self.apply_checkbox.isChecked():
                self.clean_ram()
        else:
            self.threshold_exceeded_line.setVisible(False)

        if hasattr(self, 'cleaning_result'):
            usage_text += f"\n\n{self.cleaning_result}"
            del self.cleaning_result

        self.usage_label.setText(usage_text)

    def ask_user(self, cpu, ram):
        msg = f"System thresholds exceeded:\nCPU: {cpu}% | RAM: {ram}%\nClean RAM now?"
        if QMessageBox.question(self, "Boostlet", msg) == QMessageBox.Yes:
            self.clean_ram()

    def toggle_autostart(self):
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "Boostlet"
        exe_path = os.path.abspath(sys.argv[0])
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            if self.autostart_checkbox.isChecked():
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
            else:
                winreg.DeleteValue(key, app_name)
            winreg.CloseKey(key)
        except:
            pass

    def toggle_alert_auto_exclusivity(self):
        self.apply_checkbox.setEnabled(not self.alert_checkbox.isChecked())
        self.alert_checkbox.setEnabled(not self.apply_checkbox.isChecked())

    def switch_modes(self):
        enabled = not self.interval_checkbox.isChecked()
        for widget in [self.cpu_input, self.ram_input, self.alert_checkbox,
                       self.apply_checkbox, self.both_required_checkbox]:
            widget.setEnabled(enabled)
        self.interval_input.setEnabled(not enabled)
        if enabled:
            self.stop_interval_timer()
        else:
            self.start_interval_timer()

    def start_interval_timer(self):
        try:
            minutes = int(self.interval_input.text())
            if minutes > 0:
                self.interval_timer = QTimer()
                self.interval_timer.timeout.connect(self.clean_ram)
                self.interval_timer.start(minutes * 60000)
        except:
            pass

    def stop_interval_timer(self):
        if hasattr(self, 'interval_timer'):
            self.interval_timer.stop()

    def update_interval_timer(self):
        if self.interval_checkbox.isChecked():
            self.stop_interval_timer()
            self.start_interval_timer()

    def save_settings(self):
        settings = {
            'cpu_threshold': self.cpu_input.text(),
            'ram_threshold': self.ram_input.text(),
            'alert_enabled': self.alert_checkbox.isChecked(),
            'apply_enabled': self.apply_checkbox.isChecked(),
            'autostart_enabled': True,
            'interval_enabled': self.interval_checkbox.isChecked(),
            'interval_minutes': self.interval_input.text(),
            'both_required': self.both_required_checkbox.isChecked()
        }
        with open('boostlet_settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

    def load_settings(self):
        if os.path.exists('boostlet_settings.json'):
            with open('boostlet_settings.json', 'r') as f:
                s = json.load(f)
                self.cpu_input.setText(s.get('cpu_threshold', '80'))
                self.ram_input.setText(s.get('ram_threshold', '80'))
                self.alert_checkbox.setChecked(s.get('alert_enabled', False))
                self.apply_checkbox.setChecked(s.get('apply_enabled', False))
                self.autostart_checkbox.setChecked(True)
                self.interval_checkbox.setChecked(s.get('interval_enabled', False))
                self.interval_input.setText(s.get('interval_minutes', ''))
                self.both_required_checkbox.setChecked(s.get('both_required', True))
        else:
            self.cpu_input.setText('80')
            self.ram_input.setText('80')
            self.autostart_checkbox.setChecked(True)

    def update_system_info(self):
        ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        cpu_name = platform.processor() or "Unknown CPU"
        uptime_sec = time.time() - psutil.boot_time()
        uptime_hr, uptime_min = int(uptime_sec // 3600), int((uptime_sec % 3600) // 60)
        sys_info = f"CPU: {cpu_name}\nOS: {platform.system()} {platform.release()}\nRAM: {ram_gb} GB\nUptime: {uptime_hr}h {uptime_min}m"
        self.info_label.setText(sys_info)

def create_tray_icon(app, gui):
    gui.tray_icon = QSystemTrayIcon(QIcon("boostlet.ico"), app)
    tray = gui.tray_icon
    menu = QMenu()

    action_about = menu.addAction("About")
    action_about.triggered.connect(gui.show_about)

    menu.addSeparator()
    menu.addAction("Show Boostlet", gui.show)
    menu.addAction("Clean RAM Now", lambda: gui.clean_and_notify_gui())
    menu.addSeparator()
    menu.addAction("Exit Boostlet", app.quit)

    tray.setContextMenu(menu)
    tray.setToolTip("Boostlet • Intelligent Resource Optimizer")
    tray.show()
    tray.activated.connect(lambda r: gui.show() if r == QSystemTrayIcon.Trigger else None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = BoostletGUI()
    create_tray_icon(app, gui)
    gui.show()
    sys.exit(app.exec())