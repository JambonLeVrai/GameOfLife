from PyQt6.QtWidgets import QApplication
import numpy as np
import sys

from gui import MainWindow


app = QApplication(sys.argv)

window = MainWindow()
window.show()

my_data = np.astype(np.trunc(np.random.rand(255, 255) * 255), np.uint8)
window.grid_image.set_image_data(my_data)

app.exec()
