import os
from PySide6.QtWidgets import QWidget, QMessageBox, QHeaderView,QTableView,QPushButton,QLineEdit,QHBoxLayout
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt,QSortFilterProxyModel
from PySide6.QtUiTools import QUiLoader
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.cc_model import CC
from models.exclude_model import Exclude
from models.database import SessionLocal

class w_cc_query(QWidget):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        # 动态加载 UI 文件
        ui_path = os.path.join(os.path.dirname(__file__), '../ui/cc.ui')
        self.ui = loader.load(ui_path)

        # 设置布局
        layout = QHBoxLayout()
        layout.addWidget(self.ui)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        # 查找控件
        self.queryButton = self.ui.findChild(QPushButton,"queryButton")
        self.inputBox = self.ui.findChild(QLineEdit,"inputBox") 
        self.filterBox = self.ui.findChild(QLineEdit,"filterBox")
        self.ccView = self.ui.findChild(QTableView,"ccView")
        self.excludeView = self.ui.findChild(QTableView,"excludeView")

        self.ccView.setEditTriggers(QTableView.NoEditTriggers)
        self.excludeView.setEditTriggers(QTableView.NoEditTriggers)

        self.setup_ui()
        self.setup_table_models()  # 初始化表格模型
        self.setup_connections()
    
    def setup_ui(self):
        """初始化 UI 设置"""
        self.setWindowTitle("功能1 - 并发症查询")
        self.queryButton.setText("查询")
        self.inputBox.setPlaceholderText("请输入并发症编码查询...")
        self.filterBox.setPlaceholderText("输入主要诊断进行过滤...")
    
    def setup_connections(self):
        """连接信号和槽"""
        self.queryButton.clicked.connect(self.on_query_clicked)
        self.inputBox.returnPressed.connect(self.on_query_clicked)
        self.ccView.selectionModel().selectionChanged.connect(self.on_cc_selection_changed)
        self.filterBox.textChanged.connect(self.on_filter_text_changed)

    def setup_table_models(self):
        """初始化表格数据模型"""
        # 左侧表格模型 - 显示并发症信息
        self.cc_model = QStandardItemModel()
        self.cc_model.setHorizontalHeaderLabels(['诊断编码', '排除表', '并发症类型', 'CCL级别'])
        self.ccView.setModel(self.cc_model)
        
        # 右侧表格模型 - 显示排除条件或其他相关信息
        self.exclude_model = QStandardItemModel()
        
        # 新增：创建代理模型用于过滤
        self.exclude_proxy_model = QSortFilterProxyModel()
        self.exclude_proxy_model.setSourceModel(self.exclude_model)
        self.exclude_proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)  # 不区分大小写
        self.exclude_proxy_model.setFilterKeyColumn(1)  # 在第1列（主要诊断列）进行过滤
        
        self.exclude_model.setHorizontalHeaderLabels(['排除表', '主要诊断'])
        self.excludeView.setModel(self.exclude_proxy_model) 

        # 设置表格属性
        self.setup_table_properties()
    
    def setup_table_properties(self):
        """设置表格显示属性"""
        # 设置表格列宽自适应
        self.ccView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.excludeView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # 设置交替行颜色
        self.ccView.setAlternatingRowColors(True)
        self.excludeView.setAlternatingRowColors(True)
        
        # 设置选择模式
        self.ccView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.excludeView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
    
    def on_filter_text_changed(self, text):
        """处理filterBox文本变化，实现过滤功能"""
        print(f"🔍 过滤文本变化: '{text}'")
        
        # 设置过滤模式为正则表达式，支持更灵活的过滤
        self.exclude_proxy_model.setFilterRegularExpression(text)
        
        # 显示过滤结果信息（可选）
        filtered_count = self.exclude_proxy_model.rowCount()
        total_count = self.exclude_model.rowCount()
        print(f"📊 过滤结果: {filtered_count}/{total_count} 条记录")

    def on_query_clicked(self):
        """查询按钮点击事件"""
        code = self.inputBox.text().strip()
        if len(code) < 3:
            QMessageBox.warning(self, "输入错误", "请输入不小于三位数的并发症编码!")
            return
        print(f"查询并发症: {code}")
        self.perform_query(code)
    
    def perform_query(self, code):
        """执行数据库查询操作"""
        db: Session = SessionLocal()
        try:
            # 查询匹配的诊断编码
            cc_records = db.query(CC).filter(CC.diagcode == code).all()
            
            if cc_records:
                # 查询到记录，更新表格显示
                self.display_query_results(cc_records)
            else:
                # 未找到记录，尝试模糊查询
                self.try_fuzzy_query(db, code)
                
        except Exception as e:
            QMessageBox.critical(self, "查询错误", f"查询过程中发生错误: {str(e)}")
            print(f"Database error: {e}")
            
        finally:
            db.close()
    
    def try_fuzzy_query(self, db: Session, code: str):
        """尝试模糊查询"""
        try:
            # 使用like进行模糊查询
            cc_records = db.query(CC).filter(CC.diagcode.like(f'{code}%')).all()
            
            if cc_records:
                self.display_query_results(cc_records)
            else:
                self.clear_table_views()
                QMessageBox.information(self, "查询结果", "未找到相关记录")
                
        except Exception as e:
            QMessageBox.critical(self, "查询错误", f"模糊查询过程中发生错误: {str(e)}")
    
    def display_query_results(self, cc_records):
        """在表格中显示查询结果"""
        # 清空现有数据
        self.cc_model.removeRows(0, self.cc_model.rowCount())
        self.exclude_model.removeRows(0, self.exclude_model.rowCount())
        
        # 填充左侧表格 - 主要并发症信息
        for record in cc_records:
            self.add_cc_record_to_table(record)
        # 如果有数据，默认选择第一行
        # if cc_records:
        #     self.ccView.selectRow(0) 
    
    def add_cc_record_to_table(self, record: CC):
        """添加单个CC记录到左侧表格"""
        row = self.cc_model.rowCount()
        
        # 诊断编码
        diagcode_item = QStandardItem(record.diagcode or "")
        diagcode_item.setData(record.diagcode, Qt.ItemDataRole.UserRole)  # 保存原始数据
        
        # TB字段
        tb_item = QStandardItem(record.tb or "")
        
        # 并发症类型
        cctype_item = QStandardItem(record.cctype or "")
        
        # CCL等级
        ccl_item = QStandardItem(str(record.ccl) if record.ccl is not None else "")
        
        # 根据CCL等级设置不同的背景色
        if record.ccl is not None:
            if record.ccl == 2:
                ccl_item.setBackground(Qt.GlobalColor.red)
                ccl_item.setForeground(Qt.GlobalColor.white)
            elif record.ccl == 1:
                ccl_item.setBackground(Qt.GlobalColor.green)
                ccl_item.setForeground(Qt.GlobalColor.black)
        
        # 添加到模型
        self.cc_model.appendRow([diagcode_item, tb_item, cctype_item, ccl_item])
    
    def on_cc_selection_changed(self, selected, deselected):
        """左侧表格选择变化事件"""
        print(f"🔍 选择变化事件触发")
        print(f"   选中的索引: {selected.indexes()}")
        print(f"   取消选中的索引: {deselected.indexes()}")
        
        # 获取当前选中的行
        selected_indexes = self.ccView.selectionModel().selectedRows()
        print(f"   选中的行: {[index.row() for index in selected_indexes]}")
        
        if not selected_indexes:
            print("   ❌ 没有选中任何行")
            self.clear_exclude_table()
            return
        
        # 获取第一选中的行
        selected_row = selected_indexes[0].row()
        print(f"   处理第 {selected_row} 行")
        
        # 检查模型数据
        print(f"   模型行数: {self.cc_model.rowCount()}")
        print(f"   模型列数: {self.cc_model.columnCount()}")
        
        # 安全地获取列数据
        try:
            # 获取该行的所有列数据
            for col in range(self.cc_model.columnCount()):
                index = self.cc_model.index(selected_row, col)
                if index.isValid():
                    data = self.cc_model.data(index)
                    user_data = self.cc_model.data(index, Qt.ItemDataRole.UserRole)
                    print(f"   列 {col}: 显示数据='{data}', 用户数据='{user_data}'")
                else:
                    print(f"   列 {col}: 索引无效")
            
            # 获取该行的tb值（第1列）
            tb_index = self.cc_model.index(selected_row, 1)  # 第1列是tb字段
            if tb_index.isValid():
                tb_value = self.cc_model.data(tb_index, Qt.ItemDataRole.UserRole)
                print(f"   TB值 (UserRole): '{tb_value}'")
                
                # 如果UserRole没有值，尝试获取显示文本
                if not tb_value:
                    tb_value = self.cc_model.data(tb_index)  # 获取显示文本
                    print(f"   TB值 (显示文本): '{tb_value}'")
                
                if tb_value:
                    print(f"   📌 开始查询排除表，TB值: {tb_value}")
                    self.query_exclude_by_tb(tb_value)
                else:
                    print("   ❌ 没有获取到TB值")
                    self.clear_exclude_table()
            else:
                print("   ❌ TB索引无效")
                self.clear_exclude_table()
                
        except Exception as e:
            print(f"   ❌ 获取数据时出错: {e}")
            import traceback
            print(traceback.format_exc())
            self.clear_exclude_table()
    
    def query_exclude_by_tb(self, tb_value):
        """根据tb值查询Exclude表"""
        db: Session = SessionLocal()
        try:
            # 查询Exclude表中匹配的记录
            exclude_records = db.query(Exclude).filter(Exclude.tb == tb_value).all()
            
            # 更新右侧表格
            self.update_exclude_table(exclude_records)
            
            print(f"📊 找到 {len(exclude_records)} 条排除记录")
            
        except Exception as e:
            QMessageBox.critical(self, "查询错误", f"查询排除表时发生错误: {str(e)}")
            print(f"Exclude query error: {e}")
            
        finally:
            db.close()  
    
    def update_exclude_table(self, exclude_records):
        """更新右侧排除表格"""
        # 清空现有数据
        self.exclude_model.removeRows(0, self.exclude_model.rowCount())
        
        self.filterBox.clear()

        if exclude_records:
            # 填充排除数据
            for record in exclude_records:
                tb_item = QStandardItem(record.tb or "")
                maindiag_item = QStandardItem(record.maindiag or "")
                
                self.exclude_model.appendRow([tb_item, maindiag_item])
        else:
            # 没有排除记录
            no_data_item = QStandardItem("无排除数据")
            no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.exclude_model.appendRow([no_data_item, QStandardItem("")])    
    
    def clear_exclude_table(self):
        """清空右侧表格"""
        self.exclude_model.removeRows(0, self.exclude_model.rowCount())
        no_data_item = QStandardItem("请选择左侧行")
        no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.exclude_model.appendRow([no_data_item, QStandardItem("")])

        self.filterBox.clear()
    
    def clear_table_views(self):
        """清空表格显示"""
        self.cc_model.removeRows(0, self.cc_model.rowCount())
        self.exclude_model.removeRows(0, self.exclude_model.rowCount())
        
        self.filterBox.clear()

        # 添加提示信息
        no_data_item = QStandardItem("无数据")
        no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cc_model.appendRow([no_data_item, QStandardItem(""), QStandardItem(""), QStandardItem("")])
        
        self.exclude_model.appendRow([QStandardItem("无"), QStandardItem("未找到匹配记录")])
    
    def closeEvent(self, event):
        """窗口关闭事件，用于清理资源"""
        super().closeEvent(event)