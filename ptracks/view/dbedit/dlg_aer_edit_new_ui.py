# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dlg_aer_edit_new.ui'
#
# Created: Tue Jan 26 11:33:05 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DlgAerEditNEW(object):
    def setupUi(self, DlgAerEditNEW):
        DlgAerEditNEW.setObjectName(_fromUtf8("DlgAerEditNEW"))
        DlgAerEditNEW.setWindowModality(QtCore.Qt.WindowModal)
        DlgAerEditNEW.resize(369, 450)
        DlgAerEditNEW.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        DlgAerEditNEW.setSizeGripEnabled(True)
        DlgAerEditNEW.setModal(True)
        self.verticalLayout_7 = QtGui.QVBoxLayout(DlgAerEditNEW)
        self.verticalLayout_7.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.frm_id = QtGui.QFrame(DlgAerEditNEW)
        self.frm_id.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frm_id.setFrameShadow(QtGui.QFrame.Raised)
        self.frm_id.setLineWidth(1)
        self.frm_id.setObjectName(_fromUtf8("frm_id"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frm_id)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.wid_ind = QtGui.QWidget(self.frm_id)
        self.wid_ind.setObjectName(_fromUtf8("wid_ind"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.wid_ind)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lbl_ind = QtGui.QLabel(self.wid_ind)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_ind.sizePolicy().hasHeightForWidth())
        self.lbl_ind.setSizePolicy(sizePolicy)
        self.lbl_ind.setObjectName(_fromUtf8("lbl_ind"))
        self.horizontalLayout.addWidget(self.lbl_ind)
        self.qle_ind = QtGui.QLineEdit(self.wid_ind)
        self.qle_ind.setObjectName(_fromUtf8("qle_ind"))
        self.horizontalLayout.addWidget(self.qle_ind)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.wid_ind)
        self.wid_desc = QtGui.QWidget(self.frm_id)
        self.wid_desc.setObjectName(_fromUtf8("wid_desc"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.wid_desc)
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lbl_desc = QtGui.QLabel(self.wid_desc)
        self.lbl_desc.setObjectName(_fromUtf8("lbl_desc"))
        self.horizontalLayout_2.addWidget(self.lbl_desc)
        self.qle_desc = QtGui.QLineEdit(self.wid_desc)
        self.qle_desc.setObjectName(_fromUtf8("qle_desc"))
        self.horizontalLayout_2.addWidget(self.qle_desc)
        self.verticalLayout_2.addWidget(self.wid_desc)
        self.verticalLayout_7.addWidget(self.frm_id)
        self.gbx_dim = QtGui.QGroupBox(DlgAerEditNEW)
        self.gbx_dim.setObjectName(_fromUtf8("gbx_dim"))
        self.gridLayout = QtGui.QGridLayout(self.gbx_dim)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lbl_comp = QtGui.QLabel(self.gbx_dim)
        self.lbl_comp.setObjectName(_fromUtf8("lbl_comp"))
        self.gridLayout.addWidget(self.lbl_comp, 1, 0, 1, 1)
        self.lbl_larg = QtGui.QLabel(self.gbx_dim)
        self.lbl_larg.setObjectName(_fromUtf8("lbl_larg"))
        self.gridLayout.addWidget(self.lbl_larg, 3, 0, 1, 1)
        self.qsb_comp = QtGui.QSpinBox(self.gbx_dim)
        self.qsb_comp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qsb_comp.setMinimum(1000)
        self.qsb_comp.setMaximum(10000)
        self.qsb_comp.setSingleStep(100)
        self.qsb_comp.setProperty("value", 5000)
        self.qsb_comp.setObjectName(_fromUtf8("qsb_comp"))
        self.gridLayout.addWidget(self.qsb_comp, 1, 1, 1, 1)
        self.qsb_larg = QtGui.QSpinBox(self.gbx_dim)
        self.qsb_larg.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qsb_larg.setMinimum(1000)
        self.qsb_larg.setMaximum(10000)
        self.qsb_larg.setSingleStep(100)
        self.qsb_larg.setProperty("value", 5000)
        self.qsb_larg.setObjectName(_fromUtf8("qsb_larg"))
        self.gridLayout.addWidget(self.qsb_larg, 3, 1, 1, 1)
        self.verticalLayout_7.addWidget(self.gbx_dim)
        self.gbx_cntr = QtGui.QGroupBox(DlgAerEditNEW)
        self.gbx_cntr.setObjectName(_fromUtf8("gbx_cntr"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.gbx_cntr)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.qsb_centro_x = QtGui.QSpinBox(self.gbx_cntr)
        self.qsb_centro_x.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qsb_centro_x.setMaximum(7500)
        self.qsb_centro_x.setSingleStep(100)
        self.qsb_centro_x.setProperty("value", 2500)
        self.qsb_centro_x.setObjectName(_fromUtf8("qsb_centro_x"))
        self.horizontalLayout_3.addWidget(self.qsb_centro_x)
        self.qsb_centro_y = QtGui.QSpinBox(self.gbx_cntr)
        self.qsb_centro_y.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qsb_centro_y.setMaximum(7500)
        self.qsb_centro_y.setSingleStep(100)
        self.qsb_centro_y.setProperty("value", 2500)
        self.qsb_centro_y.setObjectName(_fromUtf8("qsb_centro_y"))
        self.horizontalLayout_3.addWidget(self.qsb_centro_y)
        self.qsb_centro_z = QtGui.QSpinBox(self.gbx_cntr)
        self.qsb_centro_z.setEnabled(False)
        self.qsb_centro_z.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qsb_centro_z.setMaximum(7500)
        self.qsb_centro_z.setSingleStep(100)
        self.qsb_centro_z.setObjectName(_fromUtf8("qsb_centro_z"))
        self.horizontalLayout_3.addWidget(self.qsb_centro_z)
        self.verticalLayout_7.addWidget(self.gbx_cntr)
        self.gbx_geo = QtGui.QGroupBox(DlgAerEditNEW)
        self.gbx_geo.setObjectName(_fromUtf8("gbx_geo"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gbx_geo)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lbl_alt = QtGui.QLabel(self.gbx_geo)
        self.lbl_alt.setObjectName(_fromUtf8("lbl_alt"))
        self.gridLayout_2.addWidget(self.lbl_alt, 0, 0, 1, 1)
        self.qsb_alt = QtGui.QSpinBox(self.gbx_geo)
        self.qsb_alt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qsb_alt.setMinimum(-100)
        self.qsb_alt.setMaximum(10000)
        self.qsb_alt.setSingleStep(100)
        self.qsb_alt.setObjectName(_fromUtf8("qsb_alt"))
        self.gridLayout_2.addWidget(self.qsb_alt, 0, 1, 1, 1)
        self.lbl_dif_decl = QtGui.QLabel(self.gbx_geo)
        self.lbl_dif_decl.setObjectName(_fromUtf8("lbl_dif_decl"))
        self.gridLayout_2.addWidget(self.lbl_dif_decl, 1, 0, 1, 1)
        self.qsb_dif_decl = QtGui.QSpinBox(self.gbx_geo)
        self.qsb_dif_decl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qsb_dif_decl.setMinimum(-179)
        self.qsb_dif_decl.setMaximum(180)
        self.qsb_dif_decl.setSingleStep(5)
        self.qsb_dif_decl.setObjectName(_fromUtf8("qsb_dif_decl"))
        self.gridLayout_2.addWidget(self.qsb_dif_decl, 1, 1, 1, 1)
        self.verticalLayout_7.addWidget(self.gbx_geo)
        self.bbx_aer_edit = QtGui.QDialogButtonBox(DlgAerEditNEW)
        self.bbx_aer_edit.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbx_aer_edit.setObjectName(_fromUtf8("bbx_aer_edit"))
        self.verticalLayout_7.addWidget(self.bbx_aer_edit)

        self.retranslateUi(DlgAerEditNEW)
        QtCore.QMetaObject.connectSlotsByName(DlgAerEditNEW)

    def retranslateUi(self, DlgAerEditNEW):
        DlgAerEditNEW.setWindowTitle(_translate("DlgAerEditNEW", "Edição de Aeródromos", None))
        self.lbl_ind.setText(_translate("DlgAerEditNEW", "Indicativo:", None))
        self.lbl_desc.setText(_translate("DlgAerEditNEW", "Descrição:", None))
        self.gbx_dim.setTitle(_translate("DlgAerEditNEW", "Dimensão", None))
        self.lbl_comp.setText(_translate("DlgAerEditNEW", "Comprimento:", None))
        self.lbl_larg.setText(_translate("DlgAerEditNEW", "Largura:", None))
        self.qsb_comp.setSuffix(_translate("DlgAerEditNEW", " m", None))
        self.qsb_larg.setSuffix(_translate("DlgAerEditNEW", " m", None))
        self.gbx_cntr.setTitle(_translate("DlgAerEditNEW", "Centro", None))
        self.qsb_centro_x.setSuffix(_translate("DlgAerEditNEW", " m", None))
        self.qsb_centro_y.setSuffix(_translate("DlgAerEditNEW", " m", None))
        self.qsb_centro_z.setSuffix(_translate("DlgAerEditNEW", " ft", None))
        self.gbx_geo.setTitle(_translate("DlgAerEditNEW", "Geografia", None))
        self.lbl_alt.setText(_translate("DlgAerEditNEW", "Altitude:", None))
        self.qsb_alt.setSuffix(_translate("DlgAerEditNEW", " ft", None))
        self.lbl_dif_decl.setText(_translate("DlgAerEditNEW", "Dif. Declinação:", None))
        self.qsb_dif_decl.setSuffix(_translate("DlgAerEditNEW", " gr", None))

import qrc_resources_rc
