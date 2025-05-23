# More methods

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtWidgets import QGridLayout, QFormLayout
from PyQt5.QtWidgets import QStackedWidget, QScrollArea
from PyQt5.QtWidgets import QTextEdit, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt



class MethodWidget(QWidget):
    """
    Add some possible shortcut methods compared to QWidget
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = None
    
    def create_layout(self, layout_type = QVBoxLayout):
        """
        >>> a, w = QApplication([]), MethodWidget()
        >>> layout = w.create_layout(QVBoxLayout)
        >>> isinstance(layout, QVBoxLayout)
        True
        """
        self.layout = layout_type()
        self.setLayout(self.layout)
        return self.layout
    
    def more_widgets(self, *widgets, stretch = 0):
        """
        Multiple add method for widget
        Single stretch length
        如果你只传入了一个对象应该使用','解引
        Only for widget with QVBoxLayout or QHBoxLayout
        >>> a, w = QApplication([]), MethodWidget()
        >>> layout = w.create_layout(QVBoxLayout)
        >>> top, center, button = w.more_widgets(QGroupBox(), QGroupBox(), QPushButton())
        >>> isinstance(top, QGroupBox)
        True
        >>> bottom, = w.more_widgets(QLabel())
        >>> isinstance(bottom, QLabel)
        True
        """
        assert self.layout is not None, "Undefined layout"
        assert isinstance(self.layout, QVBoxLayout) or isinstance(self.layout, QHBoxLayout), "Incorrect layout type"

        for widget in widgets:
            self.layout.addWidget(widget)
            self.layout.addStretch(stretch)
        return widgets
    

class MGroupBox(QGroupBox):
    """
    Similar to MethodWidget
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = None
    
    def create_layout(self, layout_type = QVBoxLayout):
        """
        >>> a, g = QApplication([]), MGroupBox()
        >>> layout = g.create_layout(QVBoxLayout)
        >>> isinstance(layout, QVBoxLayout)
        True
        """
        self.layout = layout_type()
        self.setLayout(self.layout)
        return self.layout
    
    def more_widgets(self, *widgets, stretch = 0):
        """
        Multiple add method
        Only for widget with QVBoxLayout or QHBoxLayout
        >>> a, g = QApplication([]), MGroupBox()
        >>> layout = g.create_layout(QVBoxLayout)
        >>> top, center, button = g.more_widgets(QGroupBox(), QGroupBox(), QPushButton())
        >>> isinstance(top, QGroupBox)
        True

        """
        assert self.layout is not None, "Undefined layout"
        assert isinstance(self.layout, QVBoxLayout) or isinstance(self.layout, QHBoxLayout), "Incorrect layout type"

        for widget in widgets:
            self.layout.addWidget(widget)
            self.layout.addStretch(stretch)
        return widgets


    
if __name__ == "__main__":
    import doctest
    doctest.testmod()