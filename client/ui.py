import sys
import traceback
import main
from loguru import logger
from PySide6.QtWidgets import (QWidget, QApplication, QMessageBox)
from PySide6.QtUiTools import QUiLoader
import res


# 加载配置文件类
class Main(QWidget):
    def __init__(self):
        # 读取配置文件
        config_file = main.check_config_file()
        if config_file[0] == "true":
            logger.info("找到配置文件")
            logger.info("正在读取配置文件")
            max_memory = config_file[1]
            user_name = config_file[2]
            java_version = config_file[3]
            logger.info("最大内存:" + str(max_memory) + "M")
            logger.info("玩家ID:" + str(user_name))
            logger.info("Java版本：" + java_version)
            # 加载窗口类
            start_game = StartGame(java_version=java_version, username=user_name, max_memory=max_memory)
            start_game.ui.show()
            sys.exit(app.exec())
        elif config_file[0] == "false":
            logger.error("找不到配置文件")
            logger.info("新建配置文件中")
            # 新建配置文件
            main.create_config_file("Java8", 0, "输入游戏ID")
            start_game = StartGame(java_version="Java8", username="输入游戏ID", max_memory=0)
            start_game.ui.show()
            sys.exit(app.exec())


# 主窗口类
class StartGame(QWidget):

    def __init__(self, java_version, username, max_memory):
        try:
            super().__init__()
            # 加载参数
            self.username = username
            self.max_memory = max_memory
            self.java_version = java_version
            self.ui = None
            self.init_ui()
        except:
            self.exception(traceback.format_exc())

    # 加载主ui方法
    def init_ui(self):
        try:
            self.ui = QUiLoader().load("main.ui")
            self.ui.inputGameID.setText(self.username)
            self.ui.start_game.clicked.connect(self.start_game)
            self.ui.settings.clicked.connect(self.settings)
            self.ui.show()
        except:
            self.exception(traceback.format_exc())

    # 启动游戏
    def start_game(self):
        username = self.ui.inputGameID.text()
        # 判断玩家ID是否合法
        reply = main.username_validation(username)
        if reply == "only_num_letter":
            QMessageBox.information(self, '错误', '用户名只能包含数字、字母和下划线')
        elif reply == "first_letter":
            QMessageBox.information(self, '错误', '首字母只能是英文或数字')
        elif reply == "ok":
            self.username = username
            # 写入配置文件
            main.change_username(username)
            self.ui.close()
            # 正式启动游戏
            launch_exception = main.start(java_version=self.java_version, username=self.username,
                                          maxMemory=self.max_memory)
            self.exception(e=launch_exception)

    # 加载设置窗口
    def settings(self):
        try:
            self.ui = QUiLoader().load("settings.ui")
            self.ui.max_memory.setText(str(self.max_memory))
            self.ui.show()
            self.ui.save.clicked.connect(self.save_settings)
        except:
            self.exception(traceback.format_exc())

    def save_settings(self):
        try:
            self.max_memory = self.ui.max_memory.text()
            self.java_version = self.ui.java_version.currentText()
            # 覆盖配置文件
            main.create_config_file(java_version=self.java_version, max_memory=self.max_memory, username=self.username)
            QMessageBox.information(self, '提示', '保存成功')
            # 关闭设置ui
            self.ui.close()
            # 加载主ui
            self.init_ui()
        except:
            self.exception(traceback.format_exc())

    # 关闭提示（没卵用）
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出', '确定退出吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 错误窗口
    def exception(self, e):
        self.ui = QUiLoader().load("exception.ui")
        self.ui.exception.setText(str(e))
        self.ui.show()


if __name__ == '__main__':
    app = QApplication([])
    main_ui = Main()
    sys.exit(app.exec())
