rom PyQt4.QtCore import *
from PyQt4.QtGui import *


class Form(QDialog):
    """ Just a simple dialog with a couple of widgets
    """
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.setWindowTitle('Just a dialog')
        self.lineedit = QLineEdit("Write something and press Enter")
        self.lineedit.selectAll()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.setFocus()
        self.connect(self.lineedit, SIGNAL("returnPressed()"),
                     self.update_ui)

    def update_ui(self):
        self.browser.append(self.lineedit.text())


if __name__ == "__main__":
    import sys, time

    app = QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = QPixmap('splash_loading.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Simulate something that takes time
    time.sleep(2)

    form = Form()
    form.show()
    splash.finish(form)
    app.exec_()
    
    #---------------------------------------------------------------------
    self.status_txt = QtGui.QLabel()
    movie = QtGui.QMovie("etc/loading.gif")
    self.status_txt.setMovie(movie)
    movie.start()
    self.status_txt.setLayout(QtGui.QHBoxLayout())
    self.status_txt.layout().addWidget(QLabel('Loading...'))

edit:

it's possible if you use your own version of a QLabel and a QPainter to paint the text yourself:

    from PyQt4.QtCore import QSize
    from PyQt4.QtGui import QApplication, QLabel, QMovie, QPainter, QFontMetrics
    
    class QTextMovieLabel(QLabel):
        def __init__(self, text, fileName):
            QLabel.__init__(self)
            self._text = text
            m = QMovie(fileName)
            m.start()
            self.setMovie(m)
    
        def setMovie(self, movie):
            QLabel.setMovie(self, movie)
            s=movie.currentImage().size()
            self._movieWidth = s.width()
            self._movieHeight = s.height()
    
        def paintEvent(self, evt):
            QLabel.paintEvent(self, evt)
            p = QPainter(self)
            p.setFont(self.font())
            x = self._movieWidth + 6
            y = (self.height() + p.fontMetrics().xHeight()) / 2
            p.drawText(x, y, self._text)
            p.end()
    
        def sizeHint(self):
            fm = QFontMetrics(self.font())
            return QSize(self._movieWidth + 6 + fm.width(self._text),
                    self._movieHeight)
    
        def setText(self, text):
            self._text = text

if __name__ == '__main__':
    import sys
