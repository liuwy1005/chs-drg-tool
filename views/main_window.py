import os
from PySide6.QtWidgets import QMainWindow,QListWidget,QTabWidget,QStatusBar
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt
from views.w_cc_query import w_cc_query
from views.w_adrg import w_adrg
from views.w_except import w_except
from views.w_group_query import w_group_query

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 动态加载 UI 文件
        ui_path = os.path.join(os.path.dirname(__file__), '../ui/main_window.ui')
        
        loader = QUiLoader()
        self.ui = loader.load(ui_path)
        self.setCentralWidget(self.ui)
        self.listWidgetMenu = self.ui.findChild(QListWidget, "listWidgetMenu")
        self.tabWidget = self.ui.findChild(QTabWidget,"tabWidget")
        self.statusbar = self.ui.findChild(QStatusBar,"statusbar")
        self.resize(1366, 768)
        self.setMinimumSize(1366, 768)
        
        # 居中显示
        self.center_window()

        self.setup_connections()

        self.setup_ui()

        # 存储标签页引用
        self.function_tabs = {
            "并发症查询": None,
            "ADRG查询": None,
            "不应编码诊断与手术": None,
            "入组查询": None
        }
    
    def setup_connections(self):
        """连接信号和槽"""
        self.listWidgetMenu.itemClicked.connect(self.on_menu_item_clicked)
        self.tabWidget.tabCloseRequested.connect(self.on_tab_close_requested)
    
    def setup_ui(self):
        """初始化 UI 设置"""
        self.setWindowTitle("chs-drg 2.0")
        self.statusbar.showMessage("就绪")
        
        # 设置标签页样式
        self.setup_tab_style()
    
    def setup_tab_style(self):
        """设置标签页样式"""
        # 设置标签页较小
        self.tabWidget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #C4C4C3;
                top: -1px;
            }
            QTabBar::tab {
                background: #f0f0f0;
                border: 1px solid #C4C4C3;
                padding: 4px 8px;
                margin-right: 1px;
                font-size: 11px;
                min-width: 80px;
                max-width: 120px;
                height: 20px;
            }
            QTabBar::tab:selected {
                background: #2b5b84;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background: #e0e0e0;
            }
        """)
    
    def on_menu_item_clicked(self, item):
        """菜单项点击事件"""
        function_name = item.text()
        
        if function_name == "并发症查询":
            self.open_function1()
        elif function_name == "ADRG查询":
            self.open_function2()
        elif function_name == "不应编码诊断与手术":
            self.open_function3()
        elif function_name == "入组查询":
            self.open_function4()
    
    def open_function1(self):
        """打开功能1标签页"""
        # 如果标签页已经存在，则激活它
        if self.function_tabs["并发症查询"] is not None:
            index = self.tabWidget.indexOf(self.function_tabs["并发症查询"])
            if index >= 0:
                self.tabWidget.setCurrentIndex(index)
                return
            else:
                # 标签页不存在了，清理引用
                self.function_tabs["并发症查询"] = None
        
        # 创建新的功能窗口
        function_widget = w_cc_query()
        
        # 添加到标签页
        index = self.tabWidget.addTab(function_widget, "并发症查询")
        self.tabWidget.setCurrentIndex(index)
        
        # 保存引用
        self.function_tabs["并发症查询"] = function_widget
        self.statusbar.showMessage("并发症查询")
    
    def open_function2(self):
        """打开ADRG查询2标签页"""
        # 如果标签页已经存在，则激活它
        if self.function_tabs["ADRG查询"] is not None:
            index = self.tabWidget.indexOf(self.function_tabs["ADRG查询"])
            if index >= 0:
                self.tabWidget.setCurrentIndex(index)
                return
            else:
                # 标签页不存在了，清理引用
                self.function_tabs["ADRG查询"] = None
        
        # 创建新的功能窗口
        function_widget = w_adrg()
        
        # 添加到标签页
        index = self.tabWidget.addTab(function_widget, "ADRG查询")
        self.tabWidget.setCurrentIndex(index)
        
        # 保存引用
        self.function_tabs["ADRG查询"] = function_widget
        self.statusbar.showMessage("已打开ADRG查询")
    
    def open_function3(self):
        """打开功能3标签页"""
        # 如果标签页已经存在，则激活它
        if self.function_tabs["不应编码诊断与手术"] is not None:
            index = self.tabWidget.indexOf(self.function_tabs["不应编码诊断与手术"])
            if index >= 0:
                self.tabWidget.setCurrentIndex(index)
                return
            else:
                # 标签页不存在了，清理引用
                self.function_tabs["不应编码诊断与手术"] = None
        
        # 创建新的功能窗口
        function_widget = w_except()  # 替换为实际的功能窗口类
        
        # 添加到标签页
        index = self.tabWidget.addTab(function_widget, "不应编码诊断与手术")
        self.tabWidget.setCurrentIndex(index)
        
        # 保存引用
        self.function_tabs["不应编码诊断与手术"] = function_widget
        self.statusbar.showMessage("已打开不应编码诊断与手术")

    def open_function4(self):
        """打开功能4标签页"""
        if self.function_tabs["入组查询"] is not None:
            index = self.tabWidget.indexOf(self.function_tabs["入组查询"])
            if index >= 0:
                self.tabWidget.setCurrentIndex(index)
                return
            else:
                # 标签页不存在了，清理引用
                self.function_tabs["不应编码诊断与手术"] = None

        function_widget = w_group_query()  # 替换为实际的功能窗口类

        index = self.tabWidget.addTab(function_widget, "入组查询")
        self.tabWidget.setCurrentIndex(index)
        self.function_tabs["入组查询"] = function_widget
        self.statusbar.showMessage("已打开入组查询")

    def on_tab_close_requested(self, index):
        """标签页关闭请求事件"""
        widget = self.tabWidget.widget(index)
        tab_title = self.tabWidget.tabText(index)
        
        # 从存储的引用中移除
        for function_name, tab_widget in list(self.function_tabs.items()):
            if tab_widget == widget:
                self.function_tabs[function_name] = None
                break
        
        # 移除标签页
        self.tabWidget.removeTab(index)
        self.statusbar.showMessage(f"已关闭{tab_title}")
        
        # 如果 widget 需要特殊清理，可以在这里处理
        if hasattr(widget, 'close'):
            widget.close()
    
    def center_window(self):
        """将窗口居中显示"""
        screen = self.screen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)