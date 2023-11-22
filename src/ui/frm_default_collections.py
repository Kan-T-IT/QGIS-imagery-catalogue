# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/fernando/proyectos_kan/plugins-qgis/kan-imagery-catalog/github/QGIS-KICa/src/ui/frm_default_collections.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frm_default_collections(object):
    def setupUi(self, frm_default_collections):
        frm_default_collections.setObjectName('frm_default_collections')
        frm_default_collections.resize(700, 600)
        frm_default_collections.setMinimumSize(QtCore.QSize(700, 220))
        frm_default_collections.setMaximumSize(QtCore.QSize(999999, 999999))
        self.verticalLayout = QtWidgets.QVBoxLayout(frm_default_collections)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName('verticalLayout')
        self.frame_content = QtWidgets.QFrame(frm_default_collections)
        self.frame_content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_content.setObjectName('frame_content')
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_content)
        self.gridLayout_6.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName('gridLayout_6')
        self.frame_5 = QtWidgets.QFrame(self.frame_content)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName('frame_5')
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_2.setContentsMargins(0, 20, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(15)
        self.gridLayout_2.setObjectName('gridLayout_2')
        self.label_2 = QtWidgets.QLabel(self.frame_5)
        self.label_2.setMinimumSize(QtCore.QSize(210, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_2.setObjectName('label_2')
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.frame_7 = QtWidgets.QFrame(self.frame_5)
        self.frame_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName('frame_7')
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 6)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_filter_results = QtWidgets.QPushButton(self.frame_7)
        self.btn_filter_results.setMinimumSize(QtCore.QSize(200, 30))
        self.btn_filter_results.setMaximumSize(QtCore.QSize(200, 30))
        self.btn_filter_results.setObjectName('btn_filter_results')
        self.horizontalLayout_2.addWidget(self.btn_filter_results)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout_2.addWidget(self.frame_7, 1, 0, 1, 3)
        self.txt_search = QtWidgets.QLineEdit(self.frame_5)
        self.txt_search.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txt_search.setObjectName('txt_search')
        self.gridLayout_2.addWidget(self.txt_search, 0, 1, 1, 1)
        self.gridLayout_6.addWidget(self.frame_5, 0, 0, 1, 2)
        self.frame = QtWidgets.QFrame(self.frame_content)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName('frame')
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setVerticalSpacing(6)
        self.gridLayout_3.setObjectName('gridLayout_3')
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_3.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName('label_3')
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 1, 1, 1)
        self.btn_remove_selected = QtWidgets.QPushButton(self.frame)
        self.btn_remove_selected.setMinimumSize(QtCore.QSize(200, 30))
        self.btn_remove_selected.setMaximumSize(QtCore.QSize(200, 30))
        self.btn_remove_selected.setObjectName('btn_remove_selected')
        self.gridLayout_3.addWidget(self.btn_remove_selected, 0, 2, 1, 1)
        self.tbl_selected_collections = QtWidgets.QTableWidget(self.frame)
        self.tbl_selected_collections.setObjectName('tbl_selected_collections')
        self.tbl_selected_collections.setColumnCount(0)
        self.tbl_selected_collections.setRowCount(0)
        self.gridLayout_3.addWidget(self.tbl_selected_collections, 1, 0, 1, 3)
        self.gridLayout_6.addWidget(self.frame, 2, 0, 1, 2)
        self.frame_2 = QtWidgets.QFrame(self.frame_content)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName('frame_2')
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 15)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName('gridLayout')
        self.tbl_provider_collections = QtWidgets.QTableWidget(self.frame_2)
        self.tbl_provider_collections.setObjectName('tbl_provider_collections')
        self.tbl_provider_collections.setColumnCount(0)
        self.tbl_provider_collections.setRowCount(0)
        self.gridLayout.addWidget(self.tbl_provider_collections, 0, 0, 1, 3)
        spacerItem3 = QtWidgets.QSpacerItem(270, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 0, 1, 1)
        self.btn_add_selected = QtWidgets.QPushButton(self.frame_2)
        self.btn_add_selected.setMinimumSize(QtCore.QSize(200, 30))
        self.btn_add_selected.setMaximumSize(QtCore.QSize(200, 30))
        self.btn_add_selected.setObjectName('btn_add_selected')
        self.gridLayout.addWidget(self.btn_add_selected, 1, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(269, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 1, 2, 1, 1)
        self.gridLayout_6.addWidget(self.frame_2, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_content)

        self.retranslateUi(frm_default_collections)
        QtCore.QMetaObject.connectSlotsByName(frm_default_collections)

    def retranslateUi(self, frm_default_collections):
        _translate = QtCore.QCoreApplication.translate
        frm_default_collections.setWindowTitle(_translate('frm_default_collections', 'Catalog selection'))
        self.label_2.setText(_translate('frm_default_collections', 'Search by name/description:'))
        self.btn_filter_results.setText(_translate('frm_default_collections', 'Filter'))
        self.label_3.setText(_translate('frm_default_collections', 'Selected collections'))
        self.btn_remove_selected.setText(_translate('frm_default_collections', 'Delete selected'))
        self.btn_add_selected.setText(_translate('frm_default_collections', 'Add selected'))


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    frm_default_collections = QtWidgets.QWidget()
    ui = Ui_frm_default_collections()
    ui.setupUi(frm_default_collections)
    frm_default_collections.show()
    sys.exit(app.exec_())
