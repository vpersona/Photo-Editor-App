from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QComboBox, QLabel, QHBoxLayout, QVBoxLayout

#Settings 

app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Photo Editor")
main_window.resize(1000,800)

#Widgets

select_btn = QPushButton("Select Folder")
options_list = QListWidget()

btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
mirror = QPushButton("Mirror")
sharp = QPushButton("Sharpness")
bw = QPushButton("B/W")
clr = QPushButton("Color")
contrast = QPushButton("Contrast")
blur = QPushButton("Blur")

image_box = QLabel("?")

#Dropdown box

choice_cb = QComboBox()
choice_cb.addItem("Original")
choice_cb.addItem("Left")
choice_cb.addItem("Right")
choice_cb.addItem("Mirror")
choice_cb.addItem("Sharpen")
choice_cb.addItem("B/W")
choice_cb.addItem("Color")
choice_cb.addItem("Contrast")
choice_cb.addItem("Blur")

#Design

master_layout = QHBoxLayout()
col1 = QVBoxLayout()
col2=QVBoxLayout()

col1.addWidget(select_btn)
col1.addWidget(options_list)
col1.addWidget(choice_cb)
col1.addWidget(btn_left)
col1.addWidget(btn_right)
col1.addWidget(mirror)
col1.addWidget(sharp)
col1.addWidget(bw)
col1.addWidget(clr)
col1.addWidget(contrast)

col2.addWidget(image_box)

master_layout.addLayout(col1)
master_layout.addLayout(col2)
#Run
main_window.setLayout(master_layout)
main_window.show()
app.exec_()


