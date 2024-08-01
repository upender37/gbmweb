from PySide2 import QtWidgets

from functools import partial
from gbm import utils


class MainWindow(QtWidgets.QMainWindow):
    pass

    def extract(self, status):
        if status == 'start':
            keyword_list = []
            for line in self.keyword_list_textedit.toPlainText().split('\n'):
                line = line.strip()
                if line and line not in keyword_list:
                    keyword_list.append(line)
            if not keyword_list:
                QtWidgets.QMessageBox.warning(self, 'Please fill keyword list!', 'Please fill keyword list!')
                return
            print("keyword_list================", keyword_list)
            #self.working_thread = GMapsExtractor(keyword_list=keyword_list)
            self.working_thread.error.connect(self.ui_on_error)
            self.working_thread.task_finished.connect(partial(self.extract, 'finished'))
            self.working_thread.start()

            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)

        elif status == 'stop':
            self.working_thread.stop = True
            self.stop_btn.setEnabled(False)
        # elif status == 'pause':
        #     pass
        elif status == 'finished':
            QtWidgets.QMessageBox.information(self, 'Finished!', 'Finished!')

            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

    def ui_on_error(self, msg):
        QtWidgets.QMessageBox.warning(self, 'Error!', msg)

    def closeEvent(self, event):
        if self.working_thread and self.working_thread.isRunning():
            self.working_thread.terminate()
        event.accept()
