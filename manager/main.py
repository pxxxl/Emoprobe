import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QListWidget, QPushButton, QVBoxLayout, QWidget
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QUrl, QByteArray, QIODevice

ListRequestUrl = "http://116.204.9.108:12321/api/v1/videos/list"
DeleteRequestUrl = "http://116.204.9.108:12321/api/v1/videos"

class EmoprobeManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emoprobe Manager")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        self.refresh_button = QPushButton("刷新")
        button_layout.addWidget(self.refresh_button)
        self.refresh_button.clicked.connect(self.refresh_list)

        self.delete_button = QPushButton("删除")
        button_layout.addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.delete_selected_item)

        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.handle_response)

        self.refresh_list()

    def refresh_list(self):
        url = QUrl(ListRequestUrl)
        request = QNetworkRequest(url)
        self.network_manager.get(request)

    def handle_response(self, reply):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            video_data = self.parse_video_data(data)
            self.list_widget.clear()
            for video in video_data:
                video_bid = video.get("video_bid", "")
                video_title = video.get("video_title", "")
                video_item = f"{video_bid} - {video_title}"
                self.list_widget.addItem(video_item)
        else:
            print("请求失败:", reply.errorString())

        reply.deleteLater()

    def parse_video_data(self, data):
        data_str = str(data, encoding='utf-8')
        json_data = json.loads(data_str)
        video_data = json_data.get("data", {}).get("videos", [])
        return video_data

    def view_selected_item(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            item_text = selected_item.text()
            print("查看选中的项:", item_text)

    def delete_selected_item(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            bv_and_title = selected_item.text()
            bv = bv_and_title.split(" - ")[0]
            delete_request_url = DeleteRequestUrl + "?bv=" + bv
            url = QUrl(delete_request_url)
            request = QNetworkRequest(url)
            self.network_manager.deleteResource(request)
            self.refresh_list()
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmoprobeManager()
    window.show()
    sys.exit(app.exec())