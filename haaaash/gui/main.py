import sys
import os
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QComboBox, QFileDialog, QSpinBox,
                             QCheckBox, QProgressBar, QTableWidget, QTableWidgetItem,
                             QTabWidget, QAbstractItemView)
from PySide6.QtCore import Qt, QThread, Signal
from .. import hashs
from .. import outs
from ..enumerate import get_file_or_folder_contents_list

class HashCalculator(QThread):
    finished = Signal(list)  # 计算完成信号，发送原始结果列表
    error = Signal(str)     # 错误信号
    progress = Signal(str)  # 进度信号
    
    def __init__(self, files, method, length, parent=None):
        super().__init__(parent)
        self.files = files
        self.method = method
        self.length = length
        
    def run(self):
        try:
            self.progress.emit("正在计算哈希值...")
            results = hashs.hash(self.files, self.method, self.length, self.update_progress)
            
            if not results:
                self.error.emit("计算失败：未返回结果")
                return
                
            self.progress.emit("计算完成")
            self.finished.emit(results)
            
        except Exception as e:
            self.error.emit(f"计算出错: {str(e)}")
            
    def update_progress(self, msg):
        self.progress.emit(msg)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Haaaash - 文件哈希计算器")
        self.setMinimumSize(1000, 700)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 文件选择区域
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("选择文件或目录...")
        browse_file_button = QPushButton("选择文件...")
        browse_dir_button = QPushButton("选择目录...")
        browse_file_button.clicked.connect(self.browse_file)
        browse_dir_button.clicked.connect(self.browse_dir)
        file_layout.addWidget(QLabel("路径:"))
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(browse_file_button)
        file_layout.addWidget(browse_dir_button)
        layout.addLayout(file_layout)
        
        # 哈希设置区域
        hash_layout = QHBoxLayout()
        self.hash_method = QComboBox()
        self.hash_method.addItems(["md5", "sha1", "sha224", "sha256", "sha384", 
                                 "sha512", "sha3_224", "sha3_256", "sha3_384", 
                                 "sha3_512", "shake_128", "shake_256"])
        self.hash_method.setCurrentText("sha256")
        self.hash_length = QSpinBox()
        self.hash_length.setRange(1, 1000)
        self.hash_length.setValue(20)
        self.hash_length.setEnabled(False)
        self.hash_method.currentTextChanged.connect(self.on_hash_method_changed)
        
        hash_layout.addWidget(QLabel("哈希算法:"))
        hash_layout.addWidget(self.hash_method)
        hash_layout.addWidget(QLabel("哈希长度:"))
        hash_layout.addWidget(self.hash_length)
        hash_layout.addStretch()
        layout.addLayout(hash_layout)
        
        # 输出设置区域
        output_layout = QHBoxLayout()
        self.output_mode = QComboBox()
        self.output_mode.addItems(["default", "md", "csv", "json"])
        self.output_mode.currentTextChanged.connect(self.on_output_mode_changed)
        self.reverse_order = QCheckBox("反向输出")
        output_layout.addWidget(QLabel("输出格式:"))
        output_layout.addWidget(self.output_mode)
        output_layout.addWidget(self.reverse_order)
        output_layout.addStretch()
        layout.addLayout(output_layout)
        
        # 计算和保存按钮
        button_layout = QHBoxLayout()
        self.calc_button = QPushButton("计算哈希")
        self.save_button = QPushButton("保存结果...")
        self.calc_button.clicked.connect(self.calculate_hash)
        self.save_button.clicked.connect(self.save_result)
        button_layout.addWidget(self.calc_button)
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)
        
        # 进度显示
        self.progress_text = QLabel()
        layout.addWidget(self.progress_text)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 表格视图
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["文件", "哈希值"])
        self.table.horizontalHeader().setStretchLastSection(True)
        # 设置表格为只读模式
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置选择模式为整行选择
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 允许多选
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        # 文本视图
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        
        # 添加标签页
        self.tab_widget.addTab(self.table, "表格视图")
        self.tab_widget.addTab(self.result_text, "文本视图")
        
        layout.addWidget(self.tab_widget)
        
        # 存储最后的计算结果
        self.last_result = None
        self.last_raw_result = None
        
        # 初始化计算线程为None
        self.calculator = None
        
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "", "所有文件 (*.*)")
        if file_path:
            self.file_path.setText(file_path)
            
    def browse_dir(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择目录", "")
        if dir_path:
            self.file_path.setText(dir_path)
            
    def on_hash_method_changed(self, method):
        self.hash_length.setEnabled(method in ["shake_128", "shake_256"])
        
    def on_output_mode_changed(self, mode):
        if self.last_raw_result:
            self.update_display(self.last_raw_result)
            
    def update_display(self, results):
        # 更新表格
        self.table.setRowCount(len(results))
        for i, result in enumerate(results):
            file_item = QTableWidgetItem(result["file"])
            hash_item = QTableWidgetItem(result["hash"])
            # 设置单元格文本对齐方式
            file_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            hash_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(i, 0, file_item)
            self.table.setItem(i, 1, hash_item)
        self.table.resizeColumnsToContents()
        
        # 更新文本视图
        formatted_output = outs.chmod(results, self.output_mode.currentText())
        self.result_text.setText(formatted_output)
        self.last_result = formatted_output
            
    def calculate_hash(self):
        # 如果正在计算，则停止
        if self.calculator and self.calculator.isRunning():
            self.calculator.terminate()
            self.calculator.wait()
            self.calc_button.setText("计算哈希")
            self.progress_text.setText("")
            return
            
        file_path = self.file_path.text()
        if not file_path:
            self.result_text.setText("请选择文件或目录！")
            return
            
        if not os.path.exists(file_path):
            self.result_text.setText("路径不存在！")
            return
            
        try:
            # 获取文件列表
            files = get_file_or_folder_contents_list(
                [file_path], 
                self.reverse_order.isChecked()
            )
            
            if not files:
                self.result_text.setText("未找到任何文件！")
                return
                
            # 更改按钮文本
            self.calc_button.setText("停止计算")
            
            # 准备参数
            method = self.hash_method.currentText()
            length = self.hash_length.value() if method in ["shake_128", "shake_256"] else None
            
            # 创建并启动计算线程
            self.calculator = HashCalculator(
                files, 
                method, 
                length
            )
            self.calculator.finished.connect(self.on_calculation_finished)
            self.calculator.error.connect(self.on_calculation_error)
            self.calculator.progress.connect(self.on_progress_update)
            self.calculator.start()
            
        except Exception as e:
            self.result_text.setText(f"计算出错: {str(e)}")
            self.calc_button.setText("计算哈希")
            
    def on_calculation_finished(self, results):
        self.last_raw_result = results
        self.update_display(results)
        self.calc_button.setText("计算哈希")
        self.progress_text.setText("")
        
    def on_calculation_error(self, error_msg):
        self.result_text.setText(error_msg)
        self.calc_button.setText("计算哈希")
        self.progress_text.setText("")
        
    def on_progress_update(self, msg):
        self.progress_text.setText(msg)
            
    def save_result(self):
        if not self.last_result:
            self.result_text.setText("没有可保存的结果！")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "保存结果", 
            "", 
            "文本文件 (*.txt);;Markdown文件 (*.md);;CSV文件 (*.csv);;JSON文件 (*.json);;所有文件 (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.last_result)
                self.result_text.setText(f"结果已保存到：{file_path}")
            except Exception as e:
                self.result_text.setText(f"保存失败: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
