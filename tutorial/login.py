import sys  # 系统参数操作
from PyQt5.QtWidgets import *  # 模块包含创造经典桌面风格的用户界面提供了一套UI元素的类
from PyQt5.QtCore import *  # 此模块用于处理时间、文件和目录、各种数据类型、流、URL、MIME类型、线程或进程
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setWindowTitle('购物清单')
        self.setFixedWidth(600)
        self.setFixedHeight(600)

class LoginDialog(QDialog):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setWindowTitle('欢迎登录')  # 设置标题
        self.resize(200, 200)  # 设置宽、高
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)  # 设置隐藏关闭X的按钮

        '''
        定义界面控件设置
        '''
        self.frame = QFrame(self)  # 初始化 Frame对象
        self.verticalLayout = QVBoxLayout(self.frame)  # 设置横向布局
        self.verticalLayout

        self.login_id = QLineEdit()  # 定义用户名输入框
        self.login_id.setPlaceholderText("请输入登录账号")  # 设置默认显示的提示语
        self.verticalLayout.addWidget(self.login_id)  # 将该登录账户设置添加到页面控件

        self.passwd = QLineEdit()  # 定义密码输入框
        self.passwd.setPlaceholderText("请输入登录密码")  # 设置默认显示的提示语
        self.verticalLayout.addWidget(self.passwd)  # 将该登录密码设置添加到页面控件

        self.button_enter = QPushButton()  # 定义登录按钮
        self.button_enter.setText("登录")  # 按钮显示值为登录
        self.verticalLayout.addWidget(self.button_enter)  # 将按钮添加到页面控件

        self.button_quit = QPushButton()  # 定义返回按钮
        self.button_quit.setText("返回")  # 按钮显示值为返回
        self.verticalLayout.addWidget(self.button_quit)  # 将按钮添加到页面控件

        # 绑定按钮事件
        self.button_enter.clicked.connect(self.button_enter_verify)
        self.button_quit.clicked.connect(
            QCoreApplication.instance().quit)  # 返回按钮绑定到退出

    def button_enter_verify(self):
        if self.login_id.text() == "yhm" and self.passwd.text() == "1234":
            print("登录成功")
            self.accept()
        # 验证通过，设置QDialog对象状态为允许
        else:
            QLineEdit.clear(self.login_id)
            QLineEdit.clear(self.passwd)
            print("登录失败，请重新输入")



if __name__ == "__main__":
    # 创建应用
    window_application = QApplication(sys.argv)
    # 设置登录窗口

    login_ui = LoginDialog()

    # 校验是否验证通过
    if login_ui.exec_() == QDialog.Accepted:
        # 初始化主功能窗口
        main_window = MainWindow()
        # 展示窗口
        main_window.show()
        # 设置应用退出
        sys.exit(window_application.exec_())