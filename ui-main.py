from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QFileDialog,
)
from PyQt5.QtGui import QDragEnterEvent, QPixmap
from PyQt5.QtCore import Qt
import sys


WIDTH = 1000
HEIGHT = 600


class ImageLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(WIDTH, HEIGHT)

        self.layout = QVBoxLayout()

        self.label = QLabel("Drag and Drop an Image Here")

        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.button_layout = QHBoxLayout()

        self.button = QPushButton("Open Image")
        self.button.setFixedSize(200, 75)
        self.button.clicked.connect(self.open_image)
        self.button_layout.addWidget(self.button)

        self.process_button = QPushButton("Start Processing")
        self.process_button.setFixedSize(200, 75)
        self.process_button.clicked.connect(self.process_image)
        self.button_layout.addWidget(self.process_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.setWindowTitle("Image Loader")
        self.setAcceptDrops(True)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File")
        if file_path:
            self.file_path = file_path
            self.display_image(file_path)

    def process_image(self):
        from zoedepth.models.builder import build_model
        from zoedepth.utils.config import get_config
        from PIL import Image
        import torch

        print("test1")

        # Load the ZoeDepth model
        conf = get_config("zoedepth", "infer")
        model = build_model(conf)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)

        # Load and process the image
        image = Image.open(self.file_path).convert("RGB")
        depth = model.infer_pil(image)

        # Display the depth map (optional)
        depth_image = Image.fromarray((depth * 255).astype("uint8"))
        depth_image.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.file_path = file_path
            self.display_image(file_path)

            event.accept()
        else:
            event.ignore()

    def display_image(self, file_path):
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(
            self.label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.label.setPixmap(pixmap)


app = QApplication(sys.argv)
loader = ImageLoader()
loader.show()
sys.exit(app.exec_())
