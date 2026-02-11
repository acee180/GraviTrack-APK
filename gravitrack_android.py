"""
GraviTrack - Android/Desktop Cross-Platform App

This version uses Kivy and can be compiled to:
- Android APK (using Buildozer)
- Windows/Mac/Linux desktop app
- iOS app (using Kivy iOS)

Installation:
    pip install kivy requests

To build Android APK:
    pip install buildozer
    buildozer init
    buildozer -v android debug
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from kivy.core.window import Window
import requests
import threading
import time
from datetime import datetime

Window.clearcolor = (0.4, 0.5, 0.92, 1)  # Purple background

class GraviTrackApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_running = False
        self.monitor_thread = None
        self.last_notification_time = 0
        
    def build(self):
        self.title = 'GraviTrack'
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='[b]GraviTrack[/b]\nSensor Monitor',
            markup=True,
            size_hint=(1, 0.1),
            font_size='24sp',
            color=(1, 1, 1, 1)
        )
        layout.add_widget(title)
        
        # Status
        self.status_label = Label(
            text='● Stopped',
            size_hint=(1, 0.05),
            color=(1, 0.3, 0.3, 1),
            font_size='18sp'
        )
        layout.add_widget(self.status_label)
        
        # Sensor Display
        sensor_box = BoxLayout(size_hint=(1, 0.15), spacing=10)
        
        acc_box = BoxLayout(orientation='vertical')
        acc_box.add_widget(Label(text='Acceleration', size_hint=(1, 0.3), font_size='14sp'))
        self.acc_value = Label(text='0.00', font_size='32sp', bold=True)
        acc_box.add_widget(self.acc_value)
        acc_box.add_widget(Label(text='m/s²', size_hint=(1, 0.3), font_size='12sp'))
        
        gyr_box = BoxLayout(orientation='vertical')
        gyr_box.add_widget(Label(text='Gyroscope', size_hint=(1, 0.3), font_size='14sp'))
        self.gyr_value = Label(text='0.00', font_size='32sp', bold=True)
        gyr_box.add_widget(self.gyr_value)
        gyr_box.add_widget(Label(text='rad/s', size_hint=(1, 0.3), font_size='12sp'))
        
        sensor_box.add_widget(acc_box)
        sensor_box.add_widget(gyr_box)
        layout.add_widget(sensor_box)
        
        # Configuration (Scrollable)
        config_scroll = ScrollView(size_hint=(1, 0.4))
        config_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, padding=10)
        config_layout.bind(minimum_height=config_layout.setter('height'))
        
        # Phyphox IP
        config_layout.add_widget(Label(text='Phyphox IP:', size_hint_y=None, height=40))
        self.ip_input = TextInput(text='172.16.1.91', size_hint_y=None, height=40, multiline=False)
        config_layout.add_widget(self.ip_input)
        
        # Port
        config_layout.add_widget(Label(text='Port:', size_hint_y=None, height=40))
        self.port_input = TextInput(text='8080', size_hint_y=None, height=40, multiline=False)
        config_layout.add_widget(self.port_input)
        
        # Pushover User
        config_layout.add_widget(Label(text='Pushover User:', size_hint_y=None, height=40))
        self.pushover_user = TextInput(text='your_user_key', size_hint_y=None, height=40, multiline=False)
        config_layout.add_widget(self.pushover_user)
        
        # Pushover Token
        config_layout.add_widget(Label(text='Pushover Token:', size_hint_y=None, height=40))
        self.pushover_token = TextInput(text='your_api_token', size_hint_y=None, height=40, multiline=False)
        config_layout.add_widget(self.pushover_token)
        
        # Acc Threshold
        config_layout.add_widget(Label(text='Acc Threshold:', size_hint_y=None, height=40))
        self.acc_threshold = TextInput(text='59.75', size_hint_y=None, height=40, multiline=False)
        config_layout.add_widget(self.acc_threshold)
        
        # Gyr Threshold
        config_layout.add_widget(Label(text='Gyr Threshold:', size_hint_y=None, height=40))
        self.gyr_threshold = TextInput(text='25.00', size_hint_y=None, height=40, multiline=False)
        config_layout.add_widget(self.gyr_threshold)
        
        config_scroll.add_widget(config_layout)
        layout.add_widget(config_scroll)
        
        # Buttons
        button_box = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        self.start_btn = Button(
            text='START',
            background_color=(0.15, 0.68, 0.38, 1),
            font_size='18sp',
            bold=True
        )
        self.start_btn.bind(on_press=self.start_monitoring)
        
        self.stop_btn = Button(
            text='STOP',
            background_color=(0.91, 0.30, 0.24, 1),
            font_size='18sp',
            bold=True,
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_monitoring)
        
        button_box.add_widget(self.start_btn)
        button_box.add_widget(self.stop_btn)
        layout.add_widget(button_box)
        
        # Output
        output_label = Label(text='Output:', size_hint=(1, 0.03), font_size='14sp')
        layout.add_widget(output_label)
        
        output_scroll = ScrollView(size_hint=(1, 0.17))
        self.output = Label(
            text='GraviTrack ready!\n',
            size_hint_y=None,
            font_size='12sp',
            color=(0, 1, 0, 1),
            markup=True,
            halign='left',
            valign='top'
        )
        self.output.bind(texture_size=self.output.setter('size'))
        output_scroll.add_widget(self.output)
        layout.add_widget(output_scroll)
        
        return layout
    
    def log(self, message, color='00ff00'):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.output.text += f'[color={color}][{timestamp}] {message}[/color]\n'
    
    def start_monitoring(self, instance):
        self.is_running = True
        self.status_label.text = '● Running'
        self.status_label.color = (0.15, 0.68, 0.38, 1)
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        
        self.log('Starting monitoring...', '00ff00')
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self, instance):
        self.is_running = False
        self.status_label.text = '● Stopped'
        self.status_label.color = (1, 0.3, 0.3, 1)
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        
        self.log('Monitoring stopped', 'ffaa00')
    
    def monitor_loop(self):
        """Main monitoring loop."""
        ip = self.ip_input.text
        port = self.port_input.text
        
        while self.is_running:
            try:
                # Fetch data from phyphox
                url = f"http://{ip}:{port}/get"
                response = requests.get(url, timeout=2)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract sensor values
                    acc_x = acc_y = acc_z = 0.0
                    gyr_x = gyr_y = gyr_z = 0.0
                    
                    if 'buffer' in data:
                        for name, info in data['buffer'].items():
                            if 'buffer' not in info or not info['buffer']:
                                continue
                            
                            value = float(info['buffer'][-1])
                            name_lower = name.lower()
                            
                            if 'acc' in name_lower:
                                if 'x' in name_lower:
                                    acc_x = value
                                elif 'y' in name_lower:
                                    acc_y = value
                                elif 'z' in name_lower:
                                    acc_z = value
                            
                            if 'gyr' in name_lower or 'gyro' in name_lower:
                                if 'x' in name_lower:
                                    gyr_x = value
                                elif 'y' in name_lower:
                                    gyr_y = value
                                elif 'z' in name_lower:
                                    gyr_z = value
                    
                    # Calculate magnitudes
                    acc_mag = (acc_x**2 + acc_y**2 + acc_z**2)**0.5
                    gyr_mag = (gyr_x**2 + gyr_y**2 + gyr_z**2)**0.5
                    
                    # Update UI (must use Clock for thread safety)
                    Clock.schedule_once(lambda dt: self.update_display(acc_mag, gyr_mag))
                    
                    # Check thresholds
                    acc_thresh = float(self.acc_threshold.text)
                    gyr_thresh = float(self.gyr_threshold.text)
                    
                    if (acc_mag > acc_thresh or gyr_mag > gyr_thresh) and \
                       (time.time() - self.last_notification_time) > 10:
                        
                        alerts = []
                        if acc_mag > acc_thresh:
                            alerts.append(f'Acceleration: {acc_mag:.2f} m/s²')
                        if gyr_mag > gyr_thresh:
                            alerts.append(f'Gyroscope: {gyr_mag:.2f} rad/s')
                        
                        self.send_notification(alerts)
                        self.last_notification_time = time.time()
                
                else:
                    Clock.schedule_once(lambda dt: self.log(f'HTTP {response.status_code}', 'ff5555'))
            
            except Exception as e:
                Clock.schedule_once(lambda dt: self.log(f'Error: {str(e)}', 'ff5555'))
            
            time.sleep(0.5)
    
    def update_display(self, acc_mag, gyr_mag):
        """Update sensor display (called from main thread)."""
        self.acc_value.text = f'{acc_mag:.2f}'
        self.gyr_value.text = f'{gyr_mag:.2f}'
        self.log(f'Acc: {acc_mag:.2f} | Gyr: {gyr_mag:.2f}', '00ff00')
    
    def send_notification(self, alerts):
        """Send Pushover notification."""
        try:
            data = {
                'token': self.pushover_token.text,
                'user': self.pushover_user.text,
                'title': '[GraviTrack] Sensor Alert',
                'message': '\n'.join(alerts),
                'priority': 2,
                'retry': 30,
                'expire': 3600
            }
            
            response = requests.post('https://api.pushover.net/1/messages.json', data=data, timeout=5)
            
            if response.status_code == 200:
                Clock.schedule_once(lambda dt: self.log('Notification sent!', '00ff00'))
            else:
                Clock.schedule_once(lambda dt: self.log('Notification failed', 'ff5555'))
        
        except Exception as e:
            Clock.schedule_once(lambda dt: self.log(f'Notification error: {e}', 'ff5555'))


if __name__ == '__main__':
    GraviTrackApp().run()
