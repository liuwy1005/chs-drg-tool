import os
from PySide6.QtWidgets import QWidget, QMessageBox, QHeaderView,QTableView,QHBoxLayout,QLineEdit,QToolButton
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt,QSortFilterProxyModel
from PySide6.QtUiTools  import QUiLoader
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.maindiagindex_model import MainDiagIndex
from models.mainsurgeryindex_model import MainSurgeryIndex
from models.database import SessionLocal

class w_group_query(QWidget):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        # 动态加载 UI 文件
        ui_path = os.path.join(os.path.dirname(__file__), '../ui/group_query.ui')
        self.ui = loader.load(ui_path)

        layout = QHBoxLayout()
        layout.addWidget(self.ui)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.DiagInput = self.ui.findChild(QLineEdit,"DiagInput")
        self.OperInput = self.ui.findChild(QLineEdit,"OperInput")
        self.ClearDiag = self.ui.findChild(QToolButton,"ClearDiag")
        self.ClearOper = self.ui.findChild(QToolButton,"ClearOper")
        self.DiagView = self.ui.findChild(QTableView,"DiagView")
        self.OperView = self.ui.findChild(QTableView,"OperView")

        self.DiagView.setEditTriggers(QTableView.NoEditTriggers)
        self.OperView.setEditTriggers(QTableView.NoEditTriggers)
        
        self.setup_ui()
        self.setup_table_models()
        self.setup_filter_connections()
        self.query_group()

    def setup_ui(self):
        """初始化 UI 设置"""
        self.setWindowTitle("DRG分组查询")
        self.DiagInput.setPlaceholderText("输入任意内容进行过滤")
        self.OperInput.setPlaceholderText("输入任意内容进行过滤")
    
    def setup_filter_connections(self):
        """设置过滤信号连接"""
        self.DiagInput.textChanged.connect(self.on_filter_diag_text_changed)
        self.OperInput.textChanged.connect(self.on_filter_oper_text_changed)

        self.ClearDiag.clicked.connect(self.on_clear_diag)
        self.ClearOper.clicked.connect(self.on_clear_oper)
    
    def on_clear_diag(self):
        """清除诊断过滤输入框"""
        self.DiagInput.clear()
    
    def on_clear_oper(self):
        """清除手术过滤输入框"""
        self.OperInput.clear()

    def on_filter_diag_text_changed(self, text):
        """处理诊断过滤文本变化"""
        self.proxy_maindiagindex_model.setFilterKeyColumn(-1)  # 过滤所有列
        self.proxy_maindiagindex_model.setFilterFixedString(text)

    def on_filter_oper_text_changed(self, text):
        """处理手术过滤文本变化"""
        self.proxy_mainoperindex_model.setFilterKeyColumn(-1)  # 过滤所有列
        self.proxy_mainoperindex_model.setFilterFixedString(text)
    
    def setup_table_models(self):
        """设置表格模型"""
        # 诊断索引模型
        self.maindiagindex_model = QStandardItemModel()
        self.maindiagindex_model.setHorizontalHeaderLabels(['诊断编码', '诊断名称', 'ADRG'])
        self.proxy_maindiagindex_model = QSortFilterProxyModel()
        self.proxy_maindiagindex_model.setSourceModel(self.maindiagindex_model)
        self.proxy_maindiagindex_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.DiagView.setModel(self.proxy_maindiagindex_model)

        # 手术索引模型
        self.mainoperindex_model = QStandardItemModel()
        self.mainoperindex_model.setHorizontalHeaderLabels(['手术编码', '手术名称', 'ADRG'])
        self.proxy_mainoperindex_model = QSortFilterProxyModel()
        self.proxy_mainoperindex_model.setSourceModel(self.mainoperindex_model)
        self.proxy_mainoperindex_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.OperView.setModel(self.proxy_mainoperindex_model)

        self.setup_table_properties()
    
    def setup_table_properties(self):
        """设置表格属性"""
        self.DiagView.setAlternatingRowColors(True)
        self.DiagView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.DiagView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)  # 第一列可交互
        self.DiagView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)  # 第二列可交互
        self.DiagView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)  # 第三列可交互
        self.DiagView.setColumnWidth(0, 120)
        self.DiagView.setColumnWidth(1, 280) 
        self.DiagView.setColumnWidth(2, 50)

        self.OperView.setAlternatingRowColors(True)
        self.OperView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.OperView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)  # 第一列可交互
        self.OperView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)  # 第二列可交互
        self.OperView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)  # 第三列可交互
        self.OperView.setColumnWidth(0, 120)
        self.OperView.setColumnWidth(1, 280) 
        self.OperView.setColumnWidth(2, 50)

    def query_group(self):
        """查询 DRG 分组数据"""
        session = SessionLocal()
        try:
            # 查询诊断索引数据
            diag_results = session.query(MainDiagIndex).all()
            self.maindiagindex_model.setRowCount(0)  # 清空现有数据
            for diag in diag_results:
                items = [
                    QStandardItem(diag.diagcode),
                    QStandardItem(diag.diagname),
                    QStandardItem(diag.acode)
                ]
                self.maindiagindex_model.appendRow(items)
            
            # 查询手术索引数据
            oper_results = session.query(MainSurgeryIndex).all()
            self.mainoperindex_model.setRowCount(0)  # 清空现有数据
            for oper in oper_results:
                items = [
                    QStandardItem(oper.opercode),
                    QStandardItem(oper.opername),
                    QStandardItem(oper.acode)
                ]
                self.mainoperindex_model.appendRow(items)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"查询 DRG 分组数据时出错: {e}")
        finally:
            session.close()