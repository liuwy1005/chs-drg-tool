from views.main_window import MainWindow

class MainController:
    def __init__(self):
        self.main_window = MainWindow()
    
    def show_main_window(self):
        self.main_window.show()