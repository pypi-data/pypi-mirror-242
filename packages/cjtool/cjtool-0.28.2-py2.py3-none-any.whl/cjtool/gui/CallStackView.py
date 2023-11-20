from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QMenu, QTreeView
from PyQt5.Qt import QStandardItem
from common import FunctionData


class StandardItem(QStandardItem):
    def __init__(self, txt=''):
        super().__init__()
        self.setEditable(False)
        self.setText(txt)
        self.count = 1
        self.offset = 0
        self.functionData: FunctionData = None

    def increaseCount(self):
        self.count += 1
        txt = self.functionName()
        self.setText(f'{txt} * {self.count}')

    def functionName(self):
        arr = self.text().split('*')
        return arr[0].rstrip()


class CallStackView(QTreeView):
    def __init__(self) -> None:
        super().__init__()
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._rightClickMenu)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.bStyleSheetNone = False

    def _rightClickMenu(self, pos) -> None:
        try:
            self.contextMenu = QMenu()

            indexes = self.selectedIndexes()
            if len(indexes) > 0:
                self.actionCopy = self.contextMenu.addAction('复制')
                self.actionCopy.triggered.connect(self._copy)
                self.contextMenu.addSeparator()

            self.actionStyleSheet = self.contextMenu.addAction('样式切换')
            self.actionStyleSheet.triggered.connect(self._styleSheetChange)

            self.actionExpand = self.contextMenu.addAction('全部展开')
            self.actionExpand.triggered.connect(self.expandAll)

            arr = ['一级展开', '二级展开', '三级展开', '四级展开']
            self.actionExpandAction = [None]*4
            def foo(i): return lambda: self._expandLevel(i+1)
            for i, mi in enumerate(arr):
                self.actionExpandAction[i] = self.contextMenu.addAction(mi)
                self.actionExpandAction[i].triggered.connect(foo(i))

            self.actionLoopMatch = self.contextMenu.addAction('循环识别')
            self.actionLoopMatch.triggered.connect(self._loopMatch)

            self.contextMenu.exec_(self.mapToGlobal(pos))
        except Exception as e:
            print(e)

    def _copy(self) -> None:
        index = self.selectedIndexes()[0]
        item = index.model().itemFromIndex(index)
        clipboard = QApplication.clipboard()
        clipboard.setText(item.text())

    def _styleSheetChange(self) -> None:
        if self.bStyleSheetNone:
            self.setStyleSheet(
                "QTreeView::branch: {border-image: url(:/vline.png);}")
        else:
            self.setStyleSheet(
                "QTreeView::branch {border-image: url(none.png);}")

        self.bStyleSheetNone = not self.bStyleSheetNone

    def _expandLevel(self, nLevel: int):
        model = self.model()
        rootNode = model.invisibleRootItem()
        queue = []
        queue.append((rootNode, 0))
        while (queue):
            elem, level = queue.pop(0)
            if (level < nLevel):
                self.setExpanded(elem.index(), True)
                for row in range(elem.rowCount()):
                    child = elem.child(row, 0)
                    queue.append((child, level + 1))
            elif (level == nLevel):
                self.setExpanded(elem.index(), False)

    def _loopMatch(self):
        model = self.model()
        rootNode = model.invisibleRootItem()
        queue = []
        queue.append(rootNode)
        nCount = 0
        while (queue):
            elem = queue.pop(0)
            nCount += 1
            preChild = None
            row = 0
            while row < elem.rowCount():
                child = elem.child(row, 0)
                if row > 0 and preChild.functionName() == child.text():
                    elem.removeRow(row)
                    preChild.increaseCount()
                else:
                    row += 1
                    preChild = child
                    queue.append(child)
