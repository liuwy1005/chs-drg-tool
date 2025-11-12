import os
from PySide6.QtWidgets import QWidget, QMessageBox, QHeaderView,QTableView,QLineEdit,QHBoxLayout
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt,QSortFilterProxyModel
from PySide6.QtUiTools import QUiLoader
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.adrg_model import ADRG
from models.database import SessionLocal
from models.mdcdiagpool_model import mdcdiagpool
from models.drgsgroup_model import DrgsGroup
from models.maindiagindex_model import MainDiagIndex
from models.mainsurgeryindex_model import MainSurgeryIndex
from models.otherdiagindex_model import OtherDiagIndex

class w_adrg(QWidget):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        ui_path = os.path.join(os.path.dirname(__file__), '../ui/adrg.ui')
        self.ui = loader.load(ui_path)

        layout = QHBoxLayout()
        layout.addWidget(self.ui)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.filterAdrg = self.ui.findChild(QLineEdit,"filterAdrg")
        self.filterMdcDiag = self.ui.findChild(QLineEdit,"filterMdcDiag")
        self.filterAdrgDiag = self.ui.findChild(QLineEdit,"filterAdrgDiag")
        self.filterAdrgOper = self.ui.findChild(QLineEdit,"filterAdrgOper")
        self.filterOtherDiag = self.ui.findChild(QLineEdit,"filterOtherDiag")
        self.AdrgTable = self.ui.findChild(QTableView,"AdrgTable")
        self.DrgTable = self.ui.findChild(QTableView,"DrgTable")
        self.AdrgDiagPool = self.ui.findChild(QTableView,"AdrgDiagPool")
        self.OtherDiagPool = self.ui.findChild(QTableView,"OtherDiagPool")
        self.AdrgOperPool = self.ui.findChild(QTableView,"AdrgOperPool")
        self.MdcDiagPool = self.ui.findChild(QTableView,"MdcDiagPool")

        self.AdrgTable.setEditTriggers(QTableView.NoEditTriggers)
        self.DrgTable.setEditTriggers(QTableView.NoEditTriggers)
        self.AdrgDiagPool.setEditTriggers(QTableView.NoEditTriggers)
        self.OtherDiagPool.setEditTriggers(QTableView.NoEditTriggers)
        self.AdrgOperPool.setEditTriggers(QTableView.NoEditTriggers)
        self.MdcDiagPool.setEditTriggers(QTableView.NoEditTriggers)

        self.setup_ui()
        self.setup_table_models()
        self.setup_filter_connections()
        self.setup_selection_connections()
        self.query_adrg()

    def setup_ui(self):
        """初始化 UI 设置"""
        self.setWindowTitle("功能1 - ADRG查询")
        self.filterAdrg.setPlaceholderText("输入关键字过滤表格中所有列...")
        self.filterMdcDiag.setPlaceholderText("输入关键字过滤MDC诊断池中所有列...")
        self.filterAdrgDiag.setPlaceholderText("输入关键字过滤ADRG主池中所有列...")
        self.filterAdrgOper.setPlaceholderText("输入关键字过滤ADRG主手池中所有列...")
        self.filterOtherDiag.setPlaceholderText("输入关键字过滤ADRG次池中所有列...")

    def setup_table_models(self):
        self.adrg_model = QStandardItemModel()
        self.adrg_model.setHorizontalHeaderLabels(['ADRG代码', 'ADRG名称', '内外科'])

        # 新增：创建代理模型用于过滤
        self.adrg_proxy_model = QSortFilterProxyModel()
        self.adrg_proxy_model.setSourceModel(self.adrg_model)
        self.adrg_proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.AdrgTable.setModel(self.adrg_proxy_model)

        # 其他表格模型
        self.setup_drg_table_model()
        self.setup_mdc_diag_pool_model()
        self.setup_adrg_diag_pool_model()
        self.setup_adrg_oper_pool_model()
        self.setup_adrg_other_diag_pool_model()

        self.setup_table_properties()

    def setup_drg_table_model(self):
        """设置DRG表格模型"""
        self.drgsgroup_model = QStandardItemModel()
        self.drgsgroup_model.setHorizontalHeaderLabels(['DRG组', '名称','判定主诊','判定主手','判定次诊','特殊判定','特殊规则','权重'])
        self.DrgTable.setModel(self.drgsgroup_model)

    def setup_mdc_diag_pool_model(self):
        """设置MDC诊断池表格模型"""
        self.mdcdiagpool_model = QStandardItemModel()
        self.mdcdiagpool_model.setHorizontalHeaderLabels(['MDC','诊断编码', '诊断名称', '损伤部位'])
        self.proxy_mdcdiagpool_model = QSortFilterProxyModel()
        self.proxy_mdcdiagpool_model.setSourceModel(self.mdcdiagpool_model)
        self.proxy_mdcdiagpool_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.MdcDiagPool.setModel(self.proxy_mdcdiagpool_model)

    def setup_adrg_diag_pool_model(self):
        """设置ADRG诊断池表格模型"""
        self.maindiagindex_model = QStandardItemModel()
        self.maindiagindex_model.setHorizontalHeaderLabels(['ADRG','诊断编码', '诊断名称','组别序号'])
        self.proxy_maindiagindex_model = QSortFilterProxyModel()
        self.proxy_maindiagindex_model.setSourceModel(self.maindiagindex_model)
        self.proxy_maindiagindex_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.AdrgDiagPool.setModel(self.proxy_maindiagindex_model)

    def setup_adrg_oper_pool_model(self):
        """设置ADRG手术池表格模型"""
        self.mainsurgeryindex_model = QStandardItemModel()
        self.mainsurgeryindex_model.setHorizontalHeaderLabels(['ADRG','手术编码', '手术名称','组别序号'])
        self.proxy_mainsurgeryindex_model = QSortFilterProxyModel()
        self.proxy_mainsurgeryindex_model.setSourceModel(self.mainsurgeryindex_model)
        self.proxy_mainsurgeryindex_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.AdrgOperPool.setModel(self.proxy_mainsurgeryindex_model)

    def setup_adrg_other_diag_pool_model(self):
        """设置ADRG其他诊断池表格模型"""
        self.otherdiagindex_model = QStandardItemModel()
        self.otherdiagindex_model.setHorizontalHeaderLabels(['ADRG','诊断编码', '诊断名称','组别序号'])
        self.proxy_otherdiagindex_model = QSortFilterProxyModel()
        self.proxy_otherdiagindex_model.setSourceModel(self.otherdiagindex_model)
        self.proxy_otherdiagindex_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.OtherDiagPool.setModel(self.proxy_otherdiagindex_model)

    def setup_filter_connections(self):
        """设置过滤信号连接"""
        # ADRG过滤
        self.filterAdrg.textChanged.connect(self.filter_adrg_table)
        self.filterMdcDiag.textChanged.connect(self.filter_mdc_diag_table)
        self.filterAdrgDiag.textChanged.connect(self.filter_adrg_diag_pool_table)
        self.filterAdrgOper.textChanged.connect(self.filter_adrg_oper_pool_table)
        self.filterOtherDiag.textChanged.connect(self.filter_other_diag_pool_table)
    
    def filter_other_diag_pool_table(self, text):
        """过滤ADRG其他诊断池表格"""
        try:
            # 设置过滤模式 - 在所有列中搜索
            self.proxy_otherdiagindex_model.setFilterKeyColumn(-1)  # -1 表示搜索所有列
            self.proxy_otherdiagindex_model.setFilterFixedString(text)
        except Exception as e:
            print(f"过滤ADRG其他诊断池表格时出错: {str(e)}")

    def filter_adrg_diag_pool_table(self, text):
        """过滤ADRG诊断池表格"""
        try:
            # 设置过滤模式 - 在所有列中搜索
            self.proxy_maindiagindex_model.setFilterKeyColumn(-1)  # -1 表示搜索所有列
            self.proxy_maindiagindex_model.setFilterFixedString(text)
        except Exception as e:
            print(f"过滤ADRG诊断池表格时出错: {str(e)}")

    def filter_adrg_oper_pool_table(self, text):
        """过滤ADRG手术池表格"""
        try:
            # 设置过滤模式 - 在所有列中搜索
            self.proxy_mainsurgeryindex_model.setFilterKeyColumn(-1)  # -1 表示搜索所有列
            self.proxy_mainsurgeryindex_model.setFilterFixedString(text)
        except Exception as e:
            print(f"过滤ADRG手术池表格时出错: {str(e)}")

    def filter_adrg_table(self, text):
        """过滤ADRG表格"""
        try:
            # 设置过滤模式 - 在所有列中搜索
            self.adrg_proxy_model.setFilterKeyColumn(-1)  # -1 表示搜索所有列
            self.adrg_proxy_model.setFilterFixedString(text)
        except Exception as e:
            print(f"过滤ADRG表格时出错: {str(e)}")
    
    def filter_mdc_diag_table(self, text):
        """过滤MDC诊断池表格"""
        try:
            # 设置过滤模式 - 在所有列中搜索
            self.proxy_mdcdiagpool_model.setFilterKeyColumn(-1)  # -1 表示搜索所有列
            self.proxy_mdcdiagpool_model.setFilterFixedString(text)
        except Exception as e:
            print(f"过滤MDC诊断池表格时出错: {str(e)}")

    def setup_table_properties(self):
        """设置表格显示属性"""
        # 设置表格列宽
        self.AdrgTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)  # 第一列可交互
        self.AdrgTable.setColumnWidth(0, 80) 
        self.AdrgTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)  # 第二列可交互
        self.AdrgTable.setColumnWidth(1, 200)  # 设置第二列宽度为200像素
        self.AdrgTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # 第三列自适应

        self.DrgTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)  # 第二列可交互
        self.DrgTable.setColumnWidth(1, 300)

        self.MdcDiagPool.setColumnWidth(0, 50) 
        self.AdrgDiagPool.setColumnWidth(0, 50)
        self.AdrgOperPool.setColumnWidth(0, 50)
        self.OtherDiagPool.setColumnWidth(0, 50)

        # 设置交替行颜色
        self.AdrgTable.setAlternatingRowColors(True)
        self.DrgTable.setAlternatingRowColors(True)
        self.MdcDiagPool.setAlternatingRowColors(True)
        self.AdrgDiagPool.setAlternatingRowColors(True)
        self.AdrgOperPool.setAlternatingRowColors(True)
        self.OtherDiagPool.setAlternatingRowColors(True)

        # 设置选择模式
        self.AdrgTable.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.DrgTable.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.MdcDiagPool.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.AdrgDiagPool.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.AdrgOperPool.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.OtherDiagPool.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

    def query_adrg(self):
        """执行ADRG查询并显示结果"""
        try:
            # 清空现有数据
            self.adrg_model.removeRows(0, self.adrg_model.rowCount())
            
            # 从数据库查询ADRG数据
            session = SessionLocal()
            try:
                adrg_list = session.query(ADRG).all()
                
                # 填充数据到表格
                for adrg in adrg_list:
                    row = [
                        QStandardItem(adrg.AdrgCode or ""),
                        QStandardItem(adrg.AdrgName or ""),
                        QStandardItem(adrg.Dept or "")
                    ]
                    # 设置文本对齐方式
                    for item in row:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    self.adrg_model.appendRow(row)
            except Exception as e:
                QMessageBox.critical(self, "查询错误", f"查询ADRG数据时出错: {str(e)}")
            finally:
                session.close()
                
        except Exception as e:
            QMessageBox.critical(self, "系统错误", f"系统错误: {str(e)}")
    
    def setup_selection_connections(self):
        """设置选择变化信号连接"""
        self.AdrgTable.selectionModel().selectionChanged.connect(self.on_adrg_selection_changed)

    def on_adrg_selection_changed(self, selected, deselected):
        """ADRG表格选择变化事件"""
        try:
            # 获取当前选中的行（在代理模型中的索引）
            selected_indexes = self.AdrgTable.selectionModel().selectedRows()
            
            if selected_indexes:
                # 获取第一个选中的行（在代理模型中的索引）
                proxy_index = selected_indexes[0]
                
                # 转换为源模型索引
                source_index = self.adrg_proxy_model.mapToSource(proxy_index)
                
                # 获取ADRG代码（第一列）
                adrg_code_item = self.adrg_model.item(source_index.row(), 0)
                
                if adrg_code_item:
                    adrg_code = adrg_code_item.text().strip()
                    self.query_related_data(adrg_code)
            else:
                # 没有选中行时清空其他表格
                self.clear_related_tables()
                
        except Exception as e:
            print(f"处理选择变化时出错: {str(e)}")
    
    def query_related_data(self, adrg_code):
        """根据ADRG代码查询相关数据"""
        try:
            session = SessionLocal()
            try:
                # 查询DRG细分组数据
                self.query_drg_data(session, adrg_code)
                
                # 查询MDC诊断池数据
                self.query_mdc_diag_data(session, adrg_code)
                
                # 查询ADRG诊断池数据
                self.query_adrg_diag_data(session, adrg_code)
                
                # 查询ADRG手术池数据
                self.query_adrg_oper_data(session, adrg_code)

                # 查询ADRG其他诊断池数据
                self.query_adrg_other_diag_data(session, adrg_code)
                
            except Exception as e:
                QMessageBox.critical(self, "查询错误", f"查询相关数据时出错: {str(e)}")
            finally:
                session.close()
                
        except Exception as e:
            QMessageBox.critical(self, "系统错误", f"系统错误: {str(e)}")

    def query_adrg_other_diag_data(self, session, adrg_code):
        """查询ADRG其他诊断池数据"""
        try:
            self.otherdiagindex_model.removeRows(0, self.otherdiagindex_model.rowCount())
            try:
                other_diag_list = session.query(OtherDiagIndex).filter(OtherDiagIndex.acode == adrg_code).all()
                
                # 填充数据到表格
                for diag in other_diag_list:
                    row = [
                        QStandardItem(diag.acode or ""), 
                        QStandardItem(diag.diagcode or ""), 
                        QStandardItem(diag.diagname or ""),   
                        QStandardItem(str(diag.grpno) if diag.grpno is not None else "")
                    ]
                    # 设置文本对齐方式
                    for item in row:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    self.otherdiagindex_model.appendRow(row)
                    
            except Exception as e:
                QMessageBox.critical(self, "查询错误", f"查询ADRG其他诊断池数据时出错: {str(e)}")
                # 注意：这里不要关闭session，因为session是在外部统一管理的
        except Exception as e:
            QMessageBox.critical(self, "系统错误", f"系统错误: {str(e)}")

    def query_adrg_oper_data(self, session, adrg_code):
        """查询ADRG手术池数据"""
        try:
            self.mainsurgeryindex_model.removeRows(0, self.mainsurgeryindex_model.rowCount())
            try:
                oper_list = session.query(MainSurgeryIndex).filter(MainSurgeryIndex.acode == adrg_code).all()
                
                # 填充数据到表格
                for oper in oper_list:
                    row = [
                        QStandardItem(oper.acode or ""), 
                        QStandardItem(oper.opercode or ""), 
                        QStandardItem(oper.opername or ""),   
                        QStandardItem(str(oper.grpno) if oper.grpno is not None else "")
                    ]
                    # 设置文本对齐方式
                    for item in row:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    self.mainsurgeryindex_model.appendRow(row)
                    
            except Exception as e:
                QMessageBox.critical(self, "查询错误", f"查询ADRG手术池数据时出错: {str(e)}")
                # 注意：这里不要关闭session，因为session是在外部统一管理的
        except Exception as e:
            QMessageBox.critical(self, "系统错误", f"系统错误: {str(e)}")

    def query_adrg_diag_data(self, session, adrg_code):
        """查询ADRG诊断池数据"""
        try:
            self.maindiagindex_model.removeRows(0, self.maindiagindex_model.rowCount())
            try:
                diag_list = session.query(MainDiagIndex).filter(MainDiagIndex.acode == adrg_code).all()
                
                # 填充数据到表格
                for diag in diag_list:
                    row = [
                        QStandardItem(diag.acode or ""), 
                        QStandardItem(diag.diagcode or ""), 
                        QStandardItem(diag.diagname or ""),
                        QStandardItem(str(diag.grpno) if diag.grpno is not None else "")
                    ]
                    # 设置文本对齐方式
                    for item in row:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    self.maindiagindex_model.appendRow(row)
                    
            except Exception as e:
                QMessageBox.critical(self, "查询错误", f"查询ADRG诊断池数据时出错: {str(e)}")
                # 注意：这里不要关闭session，因为session是在外部统一管理的
        except Exception as e:
            QMessageBox.critical(self, "系统错误", f"系统错误: {str(e)}")

    def query_mdc_diag_data(self,session, adrg_code):
        """查询MDC诊断池数据"""
        try:
            self.mdcdiagpool_model.removeRows(0, self.mdcdiagpool_model.rowCount())
            try:
                MDC = "MDC"+adrg_code[0:1]
                mdc_diag_list = session.query(mdcdiagpool).filter(mdcdiagpool.mdccode == MDC).all()
                
                # 填充数据到表格
                for diag in mdc_diag_list:
                    row = [
                        QStandardItem(diag.mdccode or ""), 
                        QStandardItem(diag.diagcode or ""), 
                        QStandardItem(diag.diagname or ""),   
                        QStandardItem(diag.submdc or "")
                    ]
                    # 设置文本对齐方式
                    for item in row:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    self.mdcdiagpool_model.appendRow(row)
                    
            except Exception as e:
                QMessageBox.critical(self, "查询错误", f"查询MDC诊断池数据时出错: {str(e)}")
                # 注意：这里不要关闭session，因为session是在外部统一管理的
        except Exception as e:
            QMessageBox.critical(self, "系统错误", f"系统错误: {str(e)}")

    def query_drg_data(self, session, adrg_code):
        """查询DRG细分组数据"""
        try:
            self.drgsgroup_model.removeRows(0, self.drgsgroup_model.rowCount())
          
            try:
                drg_list = session.query(DrgsGroup).filter(DrgsGroup.acode == adrg_code).all()
                
                # 填充数据到表格
                for drg in drg_list:  # 这里应该是drg，不是drg_list
                    if drg.iszz and drg.iszz == 1:
                        iszz_text = "是"
                    else:
                        iszz_text = "否"    

                    if drg.isop and drg.isop.strip() == "1":
                        isop_text = "是"    
                    else:
                        isop_text = "否"
                    
                    if drg.rule != None and drg.rule.strip() != "":
                        needmop_text = "是" 
                    else:
                        needmop_text = "否"
                    
                    if drg.iscz and drg.iscz == 1:
                        iscz_text = "是"
                    else:
                        iscz_text = "否"

                    row = [
                        QStandardItem(drg.grpcode or ""), 
                        QStandardItem(drg.grpname or ""), 
                        QStandardItem(iszz_text or ""),   
                        QStandardItem(isop_text or ""),
                        QStandardItem(iscz_text or ""),
                        QStandardItem(needmop_text or ""),
                        QStandardItem(drg.rule or ""),
                        QStandardItem(str(drg.paycw) if drg.paycw is not None else "")
                    ]
                    # 设置文本对齐方式
                    for item in row:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    self.drgsgroup_model.appendRow(row)
                    
            except Exception as e:
                QMessageBox.critical(self, "查询错误", f"查询细分组数据时出错: {str(e)}")
            # 注意：这里不要关闭session，因为session是在外部统一管理的
        except Exception as e:
            QMessageBox.critical(self, "系统错误", f"系统错误: {str(e)}")

    def clear_related_tables(self):
        """清空所有相关表格的数据"""
        try:
            # 清空DRG表格
            if hasattr(self, 'drgsgroup_model'):
                self.drgsgroup_model.removeRows(0, self.drgsgroup_model.rowCount())
            
            # 清空MDC诊断池表格
            if hasattr(self, 'mdcdiagpool_model'):
                self.mdcdiagpool_model.removeRows(0, self.mdcdiagpool_model.rowCount())
            
            # 清空ADRG诊断池表格
            if hasattr(self, 'maindiagindex_model'):
                self.maindiagindex_model.removeRows(0, self.maindiagindex_model.rowCount())
            
            # 清空ADRG手术池表格
            if hasattr(self, 'mainsurgeryindex_model'):
                self.mainsurgeryindex_model.removeRows(0, self.mainsurgeryindex_model.rowCount())
            
            # 清空ADRG其他诊断池表格
            if hasattr(self, 'otherdiagindex_model'):
                self.otherdiagindex_model.removeRows(0, self.otherdiagindex_model.rowCount())
                
        except Exception as e:
            print(f"清空相关表格时出错: {str(e)}")