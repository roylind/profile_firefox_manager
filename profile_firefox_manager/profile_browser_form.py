
from PySide2.QtCore import *
from PySide2.QtWidgets import *


class Ui_profileBrowser(object):
    def setupUi(self, profileBrowser):
        if not profileBrowser.objectName():
            profileBrowser.setObjectName(u"profileBrowser")
        profileBrowser.resize(494, 600)
        self.centralwidget = QWidget(profileBrowser)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.editSearch = QLineEdit(self.centralwidget)
        self.editSearch.setObjectName(u"editSearch")

        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.editSearch)

        self.tableProfile = QTableWidget(self.centralwidget)
        self.tableProfile.setObjectName(u"tableProfile")
        self.tableProfile.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.tableProfile.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.formLayout_2.setWidget(1, QFormLayout.SpanningRole, self.tableProfile)


        self.horizontalLayout.addLayout(self.formLayout_2)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")

        self.buttSave = QPushButton(self.centralwidget)
        self.buttSave.setObjectName(u"Save")

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.buttSave)

        self.buttUp = QPushButton(self.centralwidget)
        self.buttUp.setObjectName(u"Up")

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.buttUp)

        self.buttDown = QPushButton(self.centralwidget)
        self.buttDown.setObjectName(u"Down")

        self.formLayout.setWidget(4, QFormLayout.SpanningRole, self.buttDown)

        self.buttImport = QPushButton(self.centralwidget)
        self.buttImport.setObjectName(u"Import")

        self.formLayout.setWidget(6, QFormLayout.SpanningRole, self.buttImport)

        self.buttExport = QPushButton(self.centralwidget)
        self.buttExport.setObjectName(u"Export")

        self.formLayout.setWidget(7, QFormLayout.SpanningRole, self.buttExport)

        self.buttClearSelection = QPushButton(self.centralwidget)
        self.buttClearSelection.setObjectName(u"Clear Selection")

        self.formLayout.setWidget(9, QFormLayout.SpanningRole, self.buttClearSelection)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Ignored, QSizePolicy.Minimum)

        self.formLayout.setItem(2, QFormLayout.SpanningRole, self.horizontalSpacer)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Ignored, QSizePolicy.Minimum)

        self.formLayout.setItem(5, QFormLayout.SpanningRole, self.horizontalSpacer_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Ignored, QSizePolicy.Minimum)

        self.formLayout.setItem(8, QFormLayout.SpanningRole, self.horizontalSpacer_3)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Ignored, QSizePolicy.Minimum)

        self.formLayout.setItem(10, QFormLayout.SpanningRole, self.horizontalSpacer_4)

        self.buttEnableProxy = QPushButton(self.centralwidget)
        self.buttEnableProxy.setObjectName(u"Enable Proxy")

        self.formLayout.setWidget(11, QFormLayout.SpanningRole, self.buttEnableProxy)

        self.buttDisableProxy = QPushButton(self.centralwidget)
        self.buttDisableProxy.setObjectName(u"Disable Proxy")

        self.formLayout.setWidget(12, QFormLayout.SpanningRole, self.buttDisableProxy)


        self.horizontalLayout.addLayout(self.formLayout)

        profileBrowser.setCentralWidget(self.centralwidget)

        self.retranslateUi(profileBrowser)

        QMetaObject.connectSlotsByName(profileBrowser)

    def retranslateUi(self, profileBrowser):
        profileBrowser.setWindowTitle(QCoreApplication.translate("profileBrowser", u"Profile Browser", None))
        self.buttSave.setText(QCoreApplication.translate("profileBrowser", u"Save", None))
        self.buttUp.setText(QCoreApplication.translate("profileBrowser", u"Up", None))
        self.buttDown.setText(QCoreApplication.translate("profileBrowser", u"Down", None))
        self.buttImport.setText(QCoreApplication.translate("profileBrowser", u"Import", None))
        self.buttExport.setText(QCoreApplication.translate("profileBrowser", u"Export", None))
        self.buttClearSelection.setText(QCoreApplication.translate("profileBrowser", u"Clear Selection", None))
        self.buttEnableProxy.setText(QCoreApplication.translate("profileBrowser", u"Enable Proxy", None))
        self.buttDisableProxy.setText(QCoreApplication.translate("profileBrowser", u"Disable Proxy", None))

