import sys
import datetime, time

from PyQt4 import QtGui, QtCore

from qt import Ui_Taskr
import model
from model import Task, Tag

class TaskrWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_Taskr()
        self.ui.setupUi(self)
        #Config Window
        self.icon = QtGui.QPixmap('./static/img/taskr-logo.png')
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.ui.lblIcon.setPixmap(self.icon)
        #Color Properties
        self.colors = {1:QtGui.QColor(170, 0, 0), 2:QtGui.QColor(226, 49, 5),
                        3:QtGui.QColor(167, 145, 36), 4:QtGui.QColor(206, 216, 90),
                        5:QtGui.QColor(107, 105, 170), 0:QtGui.QColor(QtCore.Qt.transparent)}
        #Config Calendar
        self.ui.dateEdit.setCalendarPopup(True)
        date = datetime.datetime.today()
        qdate = QtCore.QDate(date.year, date.month, date.day)
        self.ui.dateEdit.setDate(qdate)
        #Config Table Header Date Width
        self.ui.table.setColumnWidth(0, 70)
        self.ui.table.setColumnWidth(1, 170)
        #Load Elements content
        self._load_list_tags()
        self._load_table_tasks()
        self.create = True
        self._identifier = None
        
        #Signal -> Slot
        self.connect(self.ui.btnCreate, QtCore.SIGNAL("clicked()"), self._create_task)
        self.connect(self.ui.btn1, QtCore.SIGNAL("clicked()"), lambda: self._search_by_priority(self.ui.btn1.text()))
        self.connect(self.ui.btn2, QtCore.SIGNAL("clicked()"), lambda: self._search_by_priority(self.ui.btn2.text()))
        self.connect(self.ui.btn3, QtCore.SIGNAL("clicked()"), lambda: self._search_by_priority(self.ui.btn3.text()))
        self.connect(self.ui.btn4, QtCore.SIGNAL("clicked()"), lambda: self._search_by_priority(self.ui.btn4.text()))
        self.connect(self.ui.btn5, QtCore.SIGNAL("clicked()"), lambda: self._search_by_priority(self.ui.btn5.text()))
        self.connect(self.ui.btnAll, QtCore.SIGNAL("clicked()"), lambda: self._search_by_priority(self.ui.btnAll.text()))
        self.connect(self.ui.listTags, QtCore.SIGNAL("currentRowChanged(int)"), self._search_by_tags)
        self.connect(self.ui.table, QtCore.SIGNAL("cellClicked(int, int)"), self._cell_data)
        self.connect(self.ui.btnClean, QtCore.SIGNAL("clicked()"), self._clear_components)
        
    def _create_task(self):
        name = str(self.ui.textName.text())
        description = str(self.ui.textDesc.text())
        priority = int(str(self.ui.comboPrio.currentText()))
        #datetime
        qdate = self.ui.dateEdit.date()
        qtime = self.ui.timeEdit.time()
        end = time.mktime([qdate.year(), qdate.month(), qdate.day(), qtime.hour(), qtime.minute(), 0, 0, 0, 0])
        tags = str(self.ui.textTags.text()).split(',')
        tags = [model.Tag(t) for t in tags]
        
        t = Task(name, description, end, priority, False, None, tags)
        if self.create:
            model.manager.create(t)
        else:
            t.identifier = self._identifier
            model.manager.modify(t)
        self._add_tags(tags)
        self._clear_components()
        
    def _clear_components(self):
        self.ui.textName.setText('')
        self.ui.textDesc.setText('')
        self.ui.textTags.setText('')
        date = datetime.datetime.today()
        qdate = QtCore.QDate(date.year, date.month, date.day)
        self.ui.dateEdit.setDate(qdate)
        self.ui.timeEdit.setTime(QtCore.QTime(0,0))
        self.ui.textName.setFocus()
        self.ui.btnCreate.setText('Create!')
        self.create = True
        self._identifier = None
        self.ui.textTags.setReadOnly(False)
        self._load_table_tasks()
        
    def _search_by_priority(self, val):
        if val == 'all':
            self._load_table_tasks()
        else:
            priority = int(val)
            tasks = model.manager.get_by_priority(int(priority))
            self._load_table(tasks)
        
    def _search_by_tags(self, val):
        tag = str(self.ui.listTags.item(val).text())
        tasks = model.manager.get_by_tag(tag)
        self._load_table(tasks)
        
    def _load_list_tags(self):
        tags = model.manager.get_tags()
        self.ui.listTags.addItems([t.name for t in tags])
        
    def _load_table_tasks(self):
        tasks = model.manager.get_tasks()
        self._load_table(tasks)
        
    def _load_table(self, tasks):
        self._actives = [t.finished for t in tasks]
        while self.ui.table.rowCount() > 0:
            self.ui.table.removeRow(0)
        self.ui.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.table.setHorizontalHeaderLabels(['Finished', 'Date', 'Name', 'Description', 'Tags'])
        r = 0
        for task in tasks:
            if task.finished:
                color = self.colors[0]
            else:
                color = self.colors[task.priority]
            self.ui.table.insertRow(r)
            #Column 1
            date = datetime.datetime.fromtimestamp(task.end)
            item = QtGui.QTableWidgetItem(date.strftime("%d. %B %Y - %H:%M"))
            item.setBackgroundColor(color)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
            self.ui.table.setItem(r, 1, item)
            #Column 2
            item = QtGui.QTableWidgetItem(task.name)
            item.setBackgroundColor(color)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.ui.table.setItem(r, 2, item)
            #Column 3
            item = QtGui.QTableWidgetItem(task.description)
            item.setBackgroundColor(color)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.ui.table.setItem(r, 3, item)
            #Column 2
            item = QtGui.QTableWidgetItem(', '.join([tag.name for tag in task.tags]))
            item.setBackgroundColor(color)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.ui.table.setItem(r, 4, item)
            #Column 0
            item = QtGui.QTableWidgetItem('')
            item.setBackgroundColor(color)
            self.ui.table.setItem(r, 0, item)
            if task.finished:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            r += 1
        self.loadedTasks = tasks
            
    def _cell_data(self, row, col):
        if col == 0:
            self._actives[row] = not self._actives[row]
            task = self.loadedTasks[row]
            task.finished = self._actives[row]
            model.manager.modify(task)
            for i in range(5):
                if task.finished:
                    self.ui.table.item(row, i).setBackgroundColor(self.colors[0])
                else:
                    self.ui.table.item(row, i).setBackgroundColor(self.colors[task.priority])
        else:
            self._load_task_to_modify(self.loadedTasks[row])
        
    def _load_task_to_modify(self, task):
        self.ui.textName.setText(task.name)
        self.ui.textDesc.setText(task.description)
        #time
        date = datetime.datetime.fromtimestamp(task.end)
        qdate = QtCore.QDate(date.year, date.month, date.day)
        qtime = QtCore.QTime(date.hour, date.minute)
        self.ui.dateEdit.setDate(qdate)
        self.ui.timeEdit.setTime(qtime)
        self.ui.comboPrio.setCurrentIndex(task.priority-1)
        self.ui.textTags.setText(','.join([t.name for t in task.tags]))
        self.ui.btnCreate.setText('Modify!')
        self.ui.textTags.setReadOnly(True)
        self.create = False
        self._identifier = task.identifier
        
    def _add_tags(self, tags):
        actualTags = [str(self.ui.listTags.item(i).text()) for i in range(self.ui.listTags.count())]
        tags = [t.name for t in tags]
        tagsToAdd = [t for t in tags if t not in actualTags]
        self.ui.listTags.addItems(tagsToAdd)
        
    def resizeEvent(self, event):
        height = self.height()
        width = self.width()
        self.ui.line.setFixedWidth(width-16)
        self.ui.lblIcon.setFixedWidth(width-406)
        self.ui.listTags.setFixedHeight(height-349)
        self.ui.table.setFixedWidth(width-156)
        self.ui.table.setFixedHeight(height-259)
        

app = QtGui.QApplication(sys.argv)
taskrWin = TaskrWindow()
taskrWin.show()

sys.exit(app.exec_())
