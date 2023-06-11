from PyQt5.QtWidgets import QTableWidgetItem


class TableSortingItem(QTableWidgetItem):
    def __init__(self, value):
        QTableWidgetItem.__init__(self)
        self.value = value

    def __lt__(self, other):
        if isinstance(other, TableSortingItem):
            return self.value > other.value

        return super(QTableWidgetItem, self).__lt__(other)
