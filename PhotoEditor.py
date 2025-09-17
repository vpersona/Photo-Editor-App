from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QComboBox, QLabel, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance
import os

class EditorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.editor=Editor(self)
        self.setWindowTitle("Photo Editor")
        self.resize(1000,800)
        self.working_dir = ""
        #Widgets

        self.select_btn = QPushButton("Select Folder")
        self.options_list = QListWidget()

        self.btn_left = QPushButton("Left")
        self.btn_right = QPushButton("Right")
        self.mirror = QPushButton("Mirror")
        self.sharp = QPushButton("Sharpness")
        self.bw = QPushButton("B/W")
        self.clr = QPushButton("Color")
        self.contrast = QPushButton("Contrast")
        self.blur = QPushButton("Blur")

        self.image_box = QLabel("?")

        #Dropdown box

        self.choice_cb = QComboBox()
        self.choice_cb.addItem("Original")
        self.choice_cb.addItem("Left")
        self.choice_cb.addItem("Right")
        self.choice_cb.addItem("Mirror")
        self.choice_cb.addItem("Sharpen")
        self.choice_cb.addItem("B/W")
        self.choice_cb.addItem("Color")
        self.choice_cb.addItem("Contrast")
        self.choice_cb.addItem("Blur")

        #Design

        master_layout = QHBoxLayout()
        col1 = QVBoxLayout()
        col2=QVBoxLayout()

        col1.addWidget(self.select_btn)
        col1.addWidget(self.options_list)
        col1.addWidget(self.choice_cb)
        col1.addWidget(self.btn_left)
        col1.addWidget(self.btn_right)
        col1.addWidget(self.mirror)
        col1.addWidget(self.sharp)
        col1.addWidget(self.bw)
        col1.addWidget(self.clr)
        col1.addWidget(self.contrast)

        col1.addWidget(self.blur)
        col2.addWidget(self.image_box)

        master_layout.addLayout(col1, 20)
        master_layout.addLayout(col2, 80)

        self.setLayout(master_layout)
        self.Events()

        

    

    def filter(self, files, extensions):
            results_list = []
            for file in files:
                for ext in extensions:
                    if file.endswith(ext):
                        results_list.append(file)
            return results_list


    def getWorkingDir(self):
        global working_dir
        self.working_dir = QFileDialog.getExistingDirectory()
        extensions = ['.jpg','.png','.jpeg','.svg']
        filenames= self.filter(os.listdir(self.working_dir), extensions)
        self.options_list.clear()
        for filename in filenames:
            self.options_list.addItem(filename)



    def Events(self):
         self.select_btn.clicked.connect(self.getWorkingDir)
         self.options_list.currentRowChanged.connect(self.displayImage)
         self.bw.clicked.connect(self.editor.gray)
         self.mirror.clicked.connect(self.editor.mirror)
         self.sharp.clicked.connect(self.editor.sharpness)
         self.clr.clicked.connect(self.editor.color)
         self.contrast.clicked.connect(self.editor.contrast)
         self.btn_left.clicked.connect(self.editor.left)
         self.btn_right.clicked.connect(self.editor.right)
         self.blur.clicked.connect(self.editor.blur)
         self.choice_cb.currentTextChanged.connect(self.editor.handle_filter)

    def displayImage(self):
         if self.options_list.currentRow()>=0:
              filename = self.options_list.currentItem().text()
              self.editor.load_image(filename)
              self.editor.show_image(os.path.join(self.working_dir, self.editor.filename))

        

class Editor():
    def __init__(self, ea: "EditorApp"):
          self.ea = ea
          self.image=None
          self.original = None 
          self.filename = None
          self.save_folder='edits/'

    def load_image(self, filename):
         self.filename = filename
         fullname = os.path.join(self.ea.working_dir , self.filename )
         self.image = Image.open(fullname)
         self.original = self.image.copy()

    def save_image(self):
         path = os.path.join(self.ea.working_dir, self.save_folder)
         if not(os.path.exists(path) or os.path.isdir(path)):
              os.mkdir(path)


         fullname = os.path.join(path, self.filename)
         self.image.save(fullname)
          
    def show_image(self, path):
         self.ea.image_box.hide()
         image = QPixmap(path)
         w, h = self.ea.image_box.width(), self.ea.image_box.height()
         image = image.scaled(w,h, Qt.KeepAspectRatio)
         self.ea.image_box.setPixmap(image)
         self.ea.image_box.show()


    #Filters - editing tools

    def gray(self):
         self.image = self.image.convert("L")
         self.save_image()
         image_path = os.path.join(self.ea.working_dir, self.save_folder, self.filename)
         self.show_image(image_path)

    def mirror(self):
         self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
         self.save_image()
         image_path = os.path.join(self.ea.working_dir, self.save_folder, self.filename)
         self.show_image(image_path)

    def sharpness(self):
         self.image = ImageEnhance.Sharpness(self.image).enhance(1.2)
         self.save_image()
         image_path = os.path.join(self.ea.working_dir, self.save_folder, self.filename)
         self.show_image(image_path)


    def color(self):
         self.image = ImageEnhance.Color(self.image).enhance(1.2)
         self.save_image()
         image_path = os.path.join(self.ea.working_dir, self.save_folder, self.filename)
         self.show_image(image_path)

         
    def contrast(self):
         self.image = ImageEnhance.Contrast(self.image).enhance(1.2)
         self.save_image()
         image_path = os.path.join(self.ea.working_dir, self.save_folder, self.filename)
         self.show_image(image_path)

    def left(self):
            self.image = self.image.transpose(Image.ROTATE_90)
            self.save_image()
            image_path = os.path.join(self.ea.working_dir, self.save_folder, self.filename)
            self.show_image(image_path)
            
    def right(self):
         self.image = self.image.transpose(Image.Transpose.ROTATE_270)
         self.save_image()
         image_path = os.path.join(self.ea.working_dir, self.save_folder, self.filename)
         self.show_image(image_path)

    def blur(self):
         self.image=ImageEnhance.Sharpness(self.image).enhance(0.0)
         self.save_image()
         image_path = os.path.join(self.ea.working_dir, self.save_folder, self.filename)
         self.show_image(image_path)


    def apply_filter(self, filter_name):
          if filter_name =="Original":
              self.image=self.original.copy()
          else:
               mapping = {
                    "Left": lambda image: image.transpose(Image.ROTATE_90),
                    "Right": lambda image: image.transpose(Image.ROTATE_270),
                    "Mirror":lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
                    "Sharpen": lambda image: ImageEnhance.Sharpness(image).enhance(1.2),
                    "B/W":lambda image: image.convert("L"),
                    "Color": lambda image: ImageEnhance.Color(image).enhance(1.2),
                    "Contrast": lambda image: ImageEnhance.Contrast(image).enhance(1.2),
                    "Blur": lambda image: ImageEnhance.Sharpness(image).enhance(0.0)
           
               }
               filter_func = mapping.get(filter_name)
               if filter_func:
                    self.image = filter_func(self.image)
                    self.save_image()
                    image_path = os.path.join(self.ea.working_dir, self.save_folder, self.filename)
                    self.show_image(image_path)
               pass

          self.save_image()
          image_path = os.path.join(self.ea.working_dir, self.save_folder, self.filename)
          self.show_image(image_path)

    def handle_filter(self):
         if self.ea.options_list.currentRow()>=0:
              select_filter = self.ea.choice_cb.currentText()
              self.apply_filter(select_filter)

     
         
         


#Run
if __name__ == '__main__':
    app = QApplication([])
    main_window=EditorApp()
    main_window.show()
    app.exec_()


