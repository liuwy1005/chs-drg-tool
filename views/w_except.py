import os
from PySide6.QtWidgets import QWidget, QMessageBox, QHeaderView,QTableView,QLineEdit,QVBoxLayout
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt,QSortFilterProxyModel
from PySide6.QtUiTools import QUiLoader
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.exceptdiag_model import ExceptDiag
from models.exceptoper_model import ExceptOper
from models.database import SessionLocal

class w_except(QWidget):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        # 动态加载 UI 文件
        ui_path = os.path.join(os.path.dirname(__file__), '../ui/except.ui')
        self.ui = loader.load(ui_path)
        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.ui)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        # 查找控件
        self.filterDiag = self.ui.findChild(QLineEdit,"filterDiag")
        self.filterOper = self.ui.findChild(QLineEdit,"filterOper")
        self.ExceptDiag = self.ui.findChild(QTableView,"ExceptDiag")
        self.ExceptOper = self.ui.findChild(QTableView,"ExceptOper")
        
        # TableView不让编辑单元格
        self.ExceptDiag.setEditTriggers(QTableView.NoEditTriggers)
        self.ExceptOper.setEditTriggers(QTableView.NoEditTriggers)

        self.setup_ui()        
        self.setup_table_models()
        self.setup_filter_connections()
        self.query_except()

    def setup_ui(self):
        """初始化 UI 设置"""
        self.setWindowTitle("不应编码诊断与手术查询")
        self.filterDiag.setPlaceholderText("输入诊断编码或名称进行过滤")
        self.filterOper.setPlaceholderText("输入手术编码或名称进行过滤")
    
    def setup_filter_connections(self):
        """设置过滤信号连接"""
        self.filterDiag.textChanged.connect(self.on_filter_diag_text_changed)
        self.filterOper.textChanged.connect(self.on_filter_oper_text_changed)

    def on_filter_diag_text_changed(self, text):
        """处理诊断过滤文本变化"""
        self.proxy_exceptdiag_model.setFilterKeyColumn(-1)  # 过滤所有列
        self.proxy_exceptdiag_model.setFilterFixedString(text)

    def on_filter_oper_text_changed(self, text):
        """处理手术过滤文本变化"""
        self.proxy_exceptoper_model.setFilterKeyColumn(-1)  # 过滤所有列
        self.proxy_exceptoper_model.setFilterFixedString(text)

    def setup_table_models(self):
        """设置表格模型"""
        # 不应编码诊断模型
        self.exceptdiag_model = QStandardItemModel()
        self.exceptdiag_model.setHorizontalHeaderLabels(['诊断编码', '诊断名称'])
        self.proxy_exceptdiag_model = QSortFilterProxyModel()
        self.proxy_exceptdiag_model.setSourceModel(self.exceptdiag_model)
        self.proxy_exceptdiag_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ExceptDiag.setModel(self.proxy_exceptdiag_model)

        # 不应编码手术模型
        self.exceptoper_model = QStandardItemModel()
        self.exceptoper_model.setHorizontalHeaderLabels(['手术编码', '手术名称'])
        self.proxy_exceptoper_model = QSortFilterProxyModel()
        self.proxy_exceptoper_model.setSourceModel(self.exceptoper_model)
        self.proxy_exceptoper_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ExceptOper.setModel(self.proxy_exceptoper_model)

        self.setup_table_properties()
    
    def setup_table_properties(self):
        """设置表格属性"""
        self.ExceptDiag.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)  # 第一列可交互
        self.ExceptDiag.setColumnWidth(0, 120) 
        self.ExceptDiag.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)  # 第二列可交互
        self.ExceptDiag.setColumnWidth(1, 350)  # 设置第二列宽度为280像素

        self.ExceptOper.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)  # 第一列可交互
        self.ExceptOper.setColumnWidth(0, 120) 
        self.ExceptOper.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)  # 第二列可交互
        self.ExceptOper.setColumnWidth(1, 350)  # 设置第二列宽度为280像素

        self.ExceptDiag.setAlternatingRowColors(True)
        self.ExceptOper.setAlternatingRowColors(True)

        self.ExceptDiag.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.ExceptOper.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

    def query_except(self):
        """查询不应编码诊断与手术数据"""
        try:
            session = SessionLocal()

            # 查询不应编码诊断数据
            self.exceptdiag_model.removeRows(0, self.exceptdiag_model.rowCount())
            except_diag_records = session.query(ExceptDiag).all()
            for record in except_diag_records:
                diag_code_item = QStandardItem(record.diagcode)
                diag_name_item = QStandardItem(record.diagname)
                self.exceptdiag_model.appendRow([diag_code_item, diag_name_item])

            # 查询不应编码手术数据
            self.exceptoper_model.removeRows(0, self.exceptoper_model.rowCount())
            except_oper_records = session.query(ExceptOper).all()
            for record in except_oper_records:
                oper_code_item = QStandardItem(record.opercode)
                oper_name_item = QStandardItem(record.opername)
                self.exceptoper_model.appendRow([oper_code_item, oper_name_item])

        except Exception as e:
            QMessageBox.critical(self, "查询错误", f"查询不应编码数据时出错: {str(e)}")
        finally:
            session.close()