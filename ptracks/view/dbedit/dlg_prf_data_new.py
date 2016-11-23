#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
dlg_prf_data_new

mantém as informações sobre a dialog de edição da tabela de performances

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.1$"
__author__ = "mlabru, ICEA"
__date__ = "2014/11"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging
import os
import sys

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# model
import model.items.prf_data as dctPrf

# view
import view.dbedit.dlg_prf_edit_new as dlgPrfEditNEW
import view.dbedit.dlg_prf_data_new_ui as CDlgPrfDataNEW_ui

# control
import control.events.events_basic as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CDlgPrfDataNEW >---------------------------------------------------------------------------

class CDlgPrfDataNEW (QtGui.QDialog, CDlgPrfDataNEW_ui.Ui_CDlgPrfDataNEW):
    """
    mantém as informações sobre a dialog de edição da tabela de performances
    """
    # galileu dbus service server
    # cSRV_Path = "org.documentroot.Galileu"

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_parent=None):
        """
        constructor
        cria a dialog de edição da tabela de performances

        @param f_control: control manager do editor da base de dados
        @param f_parent: janela vinculada.
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert (f_control)

        # init super class
        super(CDlgPrfDataNEW, self).__init__(f_parent)

        # salva o control manager localmente
        self._control = f_control

        # obtém o event manager
        self._event = f_control.oEvent
        assert (self._event)

        # obtém o gerente de configuração
        self._config = f_control.oConfig
        assert (self._config)

        # obtém o dicionário de configuração
        self._dctConfig = self._config.dctConfig
        assert self._dctConfig

        # obtém o model manager
        self._model = f_control.oModel
        assert self._model

        # salva a parent window localmente
        self._parent = f_parent

        # existe uma parent window ?
        if self._parent is not None:
            # esconde a parent window
            self._parent.setVisible(False)

        # pointer para os itens correntes
        self._oPrf = None

        # pointer para o dicionário a editar
        self._dctPrf = None

        # monta a dialog
        self.setupUi(self)

        # configurações de conexões slot/signal
        self.configConnects()

        # configurações de títulos e mensagens da janela de edição
        self.configTexts()

        # restaura as configurações da janela de edição
        self.restoreSettings()

        # configura título da dialog
        self.setWindowTitle(u"TrackS [Edição de Performances]")

        # faz a carrga inicial do diretório de performances
        QtCore.QTimer.singleShot(0, self.loadInitial)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def accept(self):
        """
        callback de btnOk da dialog de edição
        faz o accept da dialog
        """
        # logger
        # M_LOG.info("__init__:>>")

        # ok para continuar ?
        if self.okToContinue():
            # faz o "accept"
            QtGui.QDialog.accept(self)

            # fecha a janela de edição
            self.close()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def closeEvent(self, event):
        """
        callback de tratamento do evento Close

        @param  event : ...
        """
        # logger
        # M_LOG.info("__init__:>>")

        # ok para continuar ?
        if self.okToContinue():
            # obtém os settings
            l_set = QtCore.QSettings()
            assert (l_set)

            # salva geometria da janela
            l_set.setValue("%s/Geometry" % (self._txtSettings),
                           QtCore.QVariant(self.saveGeometry()))

            # existe a parent window ?
            if self._parent is not None:
                # exibe a parent window
                self._parent.setVisible(True)

        # senão, ignora o request
        else:
            # ignora o evento
            event.ignore()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def configConnects(self):
        """
        configura as conexões slot/signal
        """
        # logger
        # M_LOG.info("__init__:>>")

        # performance

        # conecta click a remoção de performance
        self.connect(self.btnDel,
                     QtCore.SIGNAL("clicked()"),
                     self.prfDel)
        '''
        # conecta click a edição de performance
        self.connect ( self.btnEdit,
                       QtCore.SIGNAL ( "clicked()" ),
                       self.prfEdit )
        '''
        # conecta click a inclusão de performance
        self.connect(self.btnNew,
                     QtCore.SIGNAL("clicked()"),
                     self.prfNew)

        # conecta click a seleção da linha
        self.connect(self.qtwPrfTab,
                     QtCore.SIGNAL("itemSelectionChanged()"),
                     self.prfSelect)

        # conecta botão Ok
        self.connect(self.bbxPrfTab,
                     QtCore.SIGNAL("accepted()"),
                     self.accept)

        # conecta botão Cancela
        self.connect(self.bbxPrfTab,
                     QtCore.SIGNAL("rejected()"),
                     self.reject)

        # configura botões
        self.bbxPrfTab.button(QtGui.QDialogButtonBox.Cancel).setText("&Cancela")
        self.bbxPrfTab.button(QtGui.QDialogButtonBox.Ok).setFocus()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def configTexts(self):
        """
        configura títulos e mensagens
        """
        # logger
        # M_LOG.info("__init__:>>")

        self._txtSettings = "CDlgPrfDataNEW"
        '''
        self._txtContinueTit = u"TrackS - Alterações pendentes"
        self._txtContinueMsg = u"Salva alterações pendentes ?"
        '''
        self._txtDelPrfTit = u"TrackS - Apaga performance"
        self._txtDelPrfMsg = u"Apaga performance {0} ?"

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def prfDel(self):
        """
        callback de btnDel da dialog de edição
        deleta um performance da lista
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica condições de execução
        assert self.qtwPrfTab is not None
        assert self._dctPrf is not None

        # obtém a performance selecionado
        self._oPrf = self.getCurrentSel(self._dctPrf, self.qtwPrfTab)

        if self._oPrf is not None:
            # apaga a performance atual ?
            if (QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self, self._txtDelPrfTit,
                                             self._txtDelPrfMsg.format(self._oPrf._sPrfID),
                                             QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)):
                # apaga a performance
                self.prfRemove(self._oPrf)

        # logger
        # M_LOG.info("__init__:<<")
    '''
    # ---------------------------------------------------------------------------------------------
    def prfEdit ( self ):
        """
        callback de btnEdit da dialog de edição.
        edita um performance da QTableWidget.
        """
        # logger
        # M_LOG.debug ( ">>" )

        # verifica condições de execução
        assert self.qtwPrfTab is not None
        assert self._dctPrf is not None

        # obtém a performance selecionado
        self._oPrf = self.getCurrentSel ( self._dctPrf, self.qtwPrfTab )

        if ( self._oPrf is not None ):

            # cria a dialog de edição de performances
            l_Dlg = dlgPrfEditNEW.dlgPrfEditNEW ( self._control, self._oPrf, self )
            assert ( l_Dlg )

            # processa a dialog de edição de performances (modal)
            if ( l_Dlg.exec_ ()):

                # salva em disco as alterações na performance
                # self._oPrf.save2Disk ( self._oPrf._sPN )

                # se ok, atualiza a QTableWidget de performances
                self.prfUpdateWidget ()

        # logger
        # M_LOG.debug ( "<<" )
    '''
    # ---------------------------------------------------------------------------------------------
    def prfNew(self):
        """
        callback de btnNew da dialog de edição
        cria um nova performance na lista
        """
        # logger
        # M_LOG.info("__init__:>>")

        # cria a dialog de edição de performances
        l_Dlg = dlgPrfEditNEW.dlgPrfEditNEW(self._control, None, self)
        assert l_Dlg

        # processa a dialog de edição de performances (modal)
        if l_Dlg.exec_():
            # obtém os dados da edição
            self._oPrf = l_Dlg.getData()

            # performance existente ?
            if (self._oPrf is not None) and (self._dctPrf is not None):
                # insere a performance na lista
                self._dctPrf.append(self._oPrf)

                # salva o arquivo no disco
                # self._oPrf.save2Disk ( l_sPath )

                # se ok, atualiza a QTableWidget de performances
                self.prfUpdateWidget()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def prfRemove(self, f_oPrf):
        """
        remove a performance selecionado.

        @param  f_oPrf : pointer para a performance a remover.
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica condições de execução
        assert (f_oPrf is not None)

        # M_LOG.info("f_oPrf: " + str(f_oPrf))

        # remove a linha da widget
        self.qtwPrfTab.removeRow(self.qtwPrfTab.currentRow())

        # remove a performance da lista
        self._dctPrf.remove(f_oPrf)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def prfSelect(self):
        """
        seleciona um performance a editar
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica condições de execução
        assert (self._dctPrf is not None)
        assert (self.qtwPrfTab is not None)

        # obtém a performance selecionado
        self._oPrf = self.getCurrentSel(self._dctPrf, self.qtwPrfTab)
        assert (self._oPrf)

        # atualiza a área de dados da performance selecionado
        self.prfUpdateSel()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def prfUpdateList(self):
        """
        atualiza na tela os dados da lista de performances
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica condições de execução
        assert self._dctPrf is not None
        assert self.qtwPrfTab is not None

        # atualiza a QTableWidget de performances
        self.prfUpdateWidget()

        # obtém a performance selecionada
        self._oPrf = self.getCurrentSel(self._dctPrf, self.qtwPrfTab)
        # assert self._oPrf

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def prfUpdateSel(self):
        """
        atualiza na tela os dados da performance selecionado
        """
        # logger
        # M_LOG.info("__init__:>>")

        # performance selecionado existe ?
        if self._oPrf is not None:
            # indicativo da performance
            l_sPrfID = self._oPrf.sPrfID

            # atualiza a visualização da performance
            # self._oSrv.configPrf ( l_sPrfID, dbus_interface = self.cSRV_Path )

            # identificação
            self.txtPrfID.setText(self._oPrf.sPrfID)
            self.qlePrfDesc.setText(self._oPrf.sPrfDesc)
            '''
            # geografia

            # comprimento
            self.txtComp.setText ( str ( self._oPrf._uiPrfComp ))

            # largura
            self.txtLarg.setText ( str ( self._oPrf._uiPrfLarg ))

            # diferença de declinação magnética
            self.txtDecl.setText ( str ( self._oPrf._fPrfDeclMag ))

            # ARP
            l_iX, l_iY = self._oPrf._oCentro.getPto ()

            self.txtCntrX.setText ( str ( l_iX ))
            self.txtCntrY.setText ( str ( l_iY ))

            # altitude
            self.txtAlt.setText ( str ( self._oPrf._uiPrfAlt ))
            '''
        # senão, a performance não existe
        else:
            # posiciona cursor no início do formulário
            self.txtPrfID.setFocus()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def prfUpdateWidget(self):
        """
        atualiza na tela os dados da QTableWidget de performances
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica condições de execução
        assert self.qtwPrfTab is not None
        assert self._dctPrf is not None

        # limpa a QTableWidget
        self.qtwPrfTab.clear()

        # seta o número de linhas da QTableWidget para o tamanho da lista
        self.qtwPrfTab.setRowCount(len(self._dctPrf))

        # seta número de colunas e cabeçalho das colunas
        self.qtwPrfTab.setColumnCount(2)
        self.qtwPrfTab.setHorizontalHeaderLabels([u"Indicativo", u"Descrição"])

        # seta QTableWidget
        self.qtwPrfTab.setAlternatingRowColors(True)
        self.qtwPrfTab.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.qtwPrfTab.setSelectionBehavior(QtGui.QTableWidget.SelectRows)
        self.qtwPrfTab.setSelectionMode(QtGui.QTableWidget.SingleSelection)
        self.qtwPrfTab.setSortingEnabled(False)

        # linha 0 (objeta performance)
        l_oA0 = None

        # linha selecionada (objeta performance)
        l_oSItem = None

        # para cada performance no dicionário...
        for l_iNdx, l_sPrfID in enumerate(sorted(self._dctPrf.keys())):
            # indicativo da performance
            l_twiPrfID = QtGui.QTableWidgetItem(l_sPrfID)
            l_twiPrfID.setData(QtCore.Qt.UserRole, QtCore.QVariant(l_sPrfID))

            self.qtwPrfTab.setItem(l_iNdx, 0, l_twiPrfID)

            # é a performance selecionado ?
            if (self._oPrf is not None) and (self._oPrf._sPrfID == l_sPrfID):
                # salva pointer para o item selecionado
                l_oSItem = l_twiPrfID

            # obtém a performance
            l_oPrf = self._dctPrf[l_sPrfID]
            assert l_oPrf

            # descrição
            l_twiPrfDesc = QtGui.QTableWidgetItem(l_oPrf._sPrfDesc)

            self.qtwPrfTab.setItem(l_iNdx, 1, l_twiPrfDesc)

        # existe um performance selecionado ?
        if self._oPrf is not None:
            # seleciona o item
            self.qtwPrfTab.setCurrentItem(l_oSItem)

            # posiciona no item selecionado
            self.qtwPrfTab.scrollToItem(l_oSItem)

            # marca que existe seleção
            l_oSItem.setSelected(True)

        # senão, não existe um performance selecionado
        else:
            # seleciona a primeira linha
            self.qtwPrfTab.selectRow(0)

            # obtém a performance atual
            self._oPrf = self.getCurrentSel(self._dctPrf, self.qtwPrfTab)
            # assert self._oPrf

        # ajusta o tamanho das colunas pelo conteúdo
        self.qtwPrfTab.resizeColumnsToContents()

        # habilita a ordenação
        self.qtwPrfTab.setSortingEnabled(True)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def getCurrentData(self, f_qtwTab, f_iCol):
        """
        retorna os dados associados a linha selecionada
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica condições de execução
        assert (f_qtwTab is not None)

        # o dado da linha selecionada
        l_sData = ""

        # obtém o item da linha selecionada
        l_oItem = self.getCurrentItem(f_qtwTab, f_iCol)
        # M_LOG.info("l_oItem: " + str(l_oItem))

        # existe uma linha selecionada ?
        if l_oItem is not None:
            # obtém o dado associado a linha
            l_sData = l_oItem.data(QtCore.Qt.UserRole).toString()
            # M_LOG.info("l_sData: " + str(l_sData))

        # logger
        # M_LOG.info("__init__:<<")

        # retorna o dado associado a linha selecionada
        return l_sData

    # ---------------------------------------------------------------------------------------------
    def getCurrentItem(self, f_qtwTab, f_iCol):
        """
        retorna o item associado a linha selecionada
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica condições de execução
        assert (f_qtwTab is not None)

        # o item selecionado
        l_oItem = None

        # obtém o número da linha selecionada
        l_iRow = f_qtwTab.currentRow()
        # M_LOG.info("l_iRow: " + str(l_iRow))

        # existe uma linha selecionada ?
        if l_iRow > -1:
            # obtém o item associado
            l_oItem = f_qtwTab.item(l_iRow, f_iCol)
            # M_LOG.info("l_oItem: " + str(l_oItem))
            assert l_oItem

        # logger
        # M_LOG.info("__init__:<<")

        # retorna o item selecionado na lista
        return l_oItem

    # ---------------------------------------------------------------------------------------------
    def getCurrentSel(self, f_dct, f_qtw):
        """
        retorna o elemento associado a linha selecionada na lista.
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica condições de execução
        assert f_dct is not None
        assert f_qtw is not None

        # obtém o index da linha selecionada
        l_sID = self.getCurrentData(f_qtw, 0)
        # M_LOG.info("l_sID: " + str(l_sID))

        # indice válido ?
        if str(l_sID) in f_dct:
            # obtém o elemento selecionado se existir uma linha selecionada
            l_oSel = f_dct[str(l_sID)]
            assert (l_oSel)
            # M_LOG.info("l_oSel: " + str(l_oSel))

        # senão, índice inválido
        else:
            # não há elemento selecionado
            l_oSel = None

        # logger
        # M_LOG.info("__init__:<<")

        # retorna o elemento da linha selecionada na lista
        return l_oSel

    # ---------------------------------------------------------------------------------------------
    def loadInitial(self):
        """
        faz a carga inicial da tabela de performances
        """
        # logger
        # M_LOG.info("__init__:>>")

        # obtém o dicionário de performances
        self._dctPrf = self._model.dctPrf

        # o dicionário de performances não existe ?
        if self._dctPrf is None:
            # logger
            # M_LOG.critical(u"<E01: Tabela de performances não carregada !")

            # cria um evento de quit
            l_evtQuit = events.Quit()
            assert l_evtQuit

            # dissemina o evento
            self._event.post(l_evtQuit)

            # cai fora...
            sys.exit(1)

        # atualiza na tela os dados da tabela de performances
        self.prfUpdateList()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def okToContinue(self):
        """
        cria uma messageBox

        @return True se tratou a resposta, senão False
        """
        # logger
        # M_LOG.info("__init__:>>")

        # resposta
        l_bAns = True
        '''
        # M_LOG.info ( "self._bChanged: " + str ( self._bChanged ))

        # flag de alterações setado ?
        if self._bChanged:
            # questiona sobre alterações pendentes
            l_Resp = QtGui.QMessageBox.question ( self, self._txtContinueTit,
                                                        self._txtContinueMsg,
                                                        QtGui.QMessageBox.Yes |
                                                        QtGui.QMessageBox.No |
                                                        QtGui.QMessageBox.Cancel )

            # cancela ?
            if ( QtGui.QMessageBox.Cancel == l_Resp ):
                # não sai
                l_bAns = False

            # salva ?
            elif ( QtGui.QMessageBox.Yes == l_Resp ):
                # salva as pendências e sai
                l_bAns = True

            # não salva ?
            else:
                # reseta o flag de alterações...
                self._bChanged = False
                # M_LOG.info ( "self._bChanged: " + str ( self._bChanged ))

                # ...e sai
                l_bAns = True
        '''
        # logger
        # M_LOG.info("__init__:<<")

        # retorna a resposta
        return l_bAns

    # ---------------------------------------------------------------------------------------------
    def reject(self):
        """
        """
        # logger
        # M_LOG.info("__init__:>>")

        self._oPrf = None

        # faz o "reject"
        QtGui.QDialog.reject(self)

        self.close()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    def restoreSettings(self):
        """
        restaura as configurações salvas para esta janela
        """
        # logger
        # M_LOG.info("__init__:>>")

        # obtém os settings
        l_set = QtCore.QSettings()
        assert (l_set)

        # restaura geometria da janela
        self.restoreGeometry(l_set.value("%s/Geometry" % (self._txtSettings)).toByteArray())

        # logger
        # M_LOG.info("__init__:<<")

        return True

# < the end >--------------------------------------------------------------------------------------
