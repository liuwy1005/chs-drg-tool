import sys
from PySide6.QtWidgets import QApplication
from controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    # 创建主控制器
    controller = MainController()
    controller.show_main_window()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()