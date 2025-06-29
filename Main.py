import flet as ft
import subprocess

class ManagerWindows:
    def __init__(self):
        super().__init__()
        self.services = self.get_services()
        self.checkboxes = [
            ft.Checkbox(
                label=service["display"],
                value=False,
                on_change=self.check_box_event,
                data=service["name"]
            )
            for service in self.services
        ]

        self.start_button = ft.ElevatedButton(
            content=ft.Text("Запустить"),
            on_click=self.start_services
        )

        self.stop_button = ft.ElevatedButton(
            content=ft.Text("Остановить"),
            on_click=self.stop_services
        )

        self.output_text = ft.Text()

    def get_services(self):
        return [
            {"name": "YandexBrowserService", "display": "Служба обновления Яндекс"},
            {"name": "Fax", "display": "Факс"},
            {"name": "AJRouter", "display": "Служба маршрутизатора AllJoyn"},
            {"name": "BDESVC", "display": "Служба шифрования дисков BitLocker"},
            {"name": "bthserv", "display": "Служба поддержки Bluetooth"},
            {"name": "MapsBroker", "display": "Обновление офлайн-карт"},
            {"name": "NetTcpPortSharing", "display": "Совместное использование портов Net.Tcp"},
            {"name": "PhoneSvc", "display": "Синхронизация с телефонами (только для Windows 10 Mobile)"},
            {"name": "SSDPSRV", "display": "Обнаружение UPnP-устройств в сети"},
            {"name": "WbioSrvc", "display": "Биометрическая аутентификация (Windows Hello)"},
            {"name": "XblAuthManager", "display": "Авторизация Xbox Live"},
            {"name": "XblGameSave", "display": "Синхронизация сохранений Xbox"},
            {"name": "DiagTrack", "display": "Телеметрия и диагностика (Connected User Experiences)"},
            {"name": "dmwappushservice", "display": "Push-уведомления (WAP)"},
            {"name": "FrameServer", "display": "Камера Windows (требуется для приложения 'Камера')"},
            {"name": "icssvc", "display": "Мобильный хот-спот (Windows 10+)"},
            {"name": "lfsvc", "display": "Геолокация"},
            {"name": "NaturalAuthentication", "display": "Распознавание лиц/голоса"},
            {"name": "PNRPsvc", "display": "P2P-имена (Peer Name Resolution Protocol)"},
        ]

    def stop_services(self, e):
        log = []
        for checkbox in self.checkboxes:
            if checkbox.value:
                service_name = checkbox.data
                try:
                    subprocess.run(["sc", "stop", service_name], check=True, capture_output=True)
                    log.append(f"{checkbox.label} остановлена.")
                except subprocess.CalledProcessError as err:
                    log.append(f"Ошибка при остановке: {checkbox.label}: {err}")
        self.output_text.value = "\n".join(log)
        self.output_text.update()

    def start_services(self, e):
        log = []
        for checkbox in self.checkboxes:
            if checkbox.value:
                service_name = checkbox.data
                try:
                    subprocess.run(["sc", "start", service_name], check=True, capture_output=True)
                    log.append(f"{checkbox.label} запущена")
                except subprocess.CalledProcessError as err:
                    log.append(f"Ошибка при запуске: {checkbox.label}: {err}")
        self.output_text.value = "\n".join(log)
        self.output_text.update()

    def setup_ui(self):
        for col in range(3):
            self.window_columnconfigure(col, weight=1)
        for row in range(len(self.services) + 1):
            self.grid_rowconfigure(row, weight=1)

    def check_box_event(self, e):
        service_name = e.control.label
        status = "включена" if e.control.value else "выключена"
        message = f"{service_name}: {status}"
        self.output_text.value = message
        self.output_text.update()

    def build(self):
        half = len(self.checkboxes) // 2
        left_column = self.checkboxes[:half]
        right_column = self.checkboxes[half:]

        return ft.Column([
            ft.Text("Выберите службы для отключения:"),

            ft.Row([
                ft.Column(left_column, scroll="auto"),
                ft.Column(right_column, scroll="auto")
            ], alignment=ft.MainAxisAlignment.START),

            self.output_text,
            ft.Row([self.start_button, self.stop_button], alignment=ft.MainAxisAlignment.CENTER)
        ])

def main(page: ft.Page):
    page.title = "Менеджер Windows"
    page.window_width = 1920
    page.window_height = 1080

    manager = ManagerWindows()
    page.add(manager.build())

if __name__ == "__main__":
    ft.run(main)