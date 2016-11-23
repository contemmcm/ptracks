#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
statusbar_visil

DOCUMENT ME!

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

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/12"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging

# PyQt library
from PyQt4 import QtCore
from PyQt4 import QtGui

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CStatusBarVisil >------------------------------------------------------------------------

class CStatusBarVisil(QtGui.QStatusBar):
    """
    used to display the Current Working Position, the Independant/Dependant mode, radar and weather
    services used, filters and coordinates of the mouse pointer on the status bar of a radar window
    """
    # ---------------------------------------------------------------------------------------------
    # void (???)
    def __init__(self, f_parent=None):
        """
        constructor
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        assert f_parent

        # init super class
        super(CStatusBarVisil, self).__init__(f_parent)

        # salva a QMainWindow localmente
        self._parent = f_parent

        # local variables
        self._lblInd = None
        self._lblCwp = None
        self._lblRadarService = None
        self._lblQNH = None
        self._lblTL = None
        self._lblWind = None
        self._lblCoords = None
        self._lblRange = None
        '''
        # int
        self.m_LowFilter = 0
        # bool
        self.m_LowFilterIsOn = False
        # int
        self.m_HighFilter = 0
        # bool
        self.m_HighFilterIsOn = False
        # int
        self.m_DepFilter = 0
        # bool
        self.m_DepFilterIsOn = False

        # bool
        self.m_IsInd = False
        # QString
        self.m_RadarService = ""
        # bool
        self.m_RadarIsNotAvail = False
        # bool
        self.m_RadarIsDiff = False
        # bool
        self.m_PrimFilter = False
        # bool
        self.m_VfrFilter = False
        # bool
        self.m_MilFilter = False
        # bool
        self.m_DataFilter = False
        # bool
        self.m_WeatherIsOn = False
        # bool
        self.m_WeatherNotAvail = False
        # QString
        self.m_Coordinates = 0
        '''
        # pointer QPixmap *
        self._pHBitmap = None

        # obtém a área da statusBar
        l_rect = f_parent.rect()

        # define o tamanho da status bar
        # self.setGeometry(0, l_rect.bottom() - 30, l_rect.width(), 30)

        # config status bar
        # self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setBackgroundMode(QtCore.Qt.NoBackground)
        # self.setStyleSheet("color: black;\nbackground-color: transparent;")

        # create permanent widgets
        self.createStatusBarLabels()

        # add widgets in status bar
        self.addWidget(self._lblInd)
        self.addWidget(self._lblCwp)
        self.addWidget(self._lblRadarService)

        # add permanent widgets in status bar
        self.addPermanentWidget(self._lblCoords)
        self.addPermanentWidget(self._lblRange)
        self.addPermanentWidget(self._lblQNH)
        self.addPermanentWidget(self._lblTL)
        self.addPermanentWidget(self._lblWind)

        # show message in status bar
        self.showMessage(QtGui.QApplication.translate("CStatusBarVisil", "Ready", None, QtGui.QApplication.UnicodeUTF8))

        # exibe a status bar
        self.show()

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def createStatusBarLabels(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("createStatusBarLabels:>>")

        # dependant/independant label
        self._lblInd = QtGui.QLabel(" WWW ")
        assert self._lblInd

        self._lblInd.setAlignment(QtCore.Qt.AlignHCenter)
        self._lblInd.setMinimumSize(self._lblInd.sizeHint())

        # CWP label
        self._lblCwp = QtGui.QLabel(" TWR ")
        assert self._lblCwp

        self._lblCwp.setAlignment(QtCore.Qt.AlignHCenter)
        self._lblCwp.setMinimumSize(self._lblCwp.sizeHint())

        # radar services label
        self._lblRadarService = QtGui.QLabel("WWWWWWWWWWWWWWWWWWW")
        assert self._lblRadarService

        self._lblRadarService.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self._lblRadarService.setMinimumSize(self._lblRadarService.sizeHint())
        # self._lblRadarService.setIndent(3)

        # coordinates label
        self._lblCoords = QtGui.QLabel(self)
        assert self._lblCoords

        self._lblCoords.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self._lblCoords.setMinimumSize(self._lblCoords.sizeHint())

        # range label
        self._lblRange = QtGui.QLabel(self)
        assert self._lblRange

        self._lblRange.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self._lblRange.setMinimumSize(self._lblRange.sizeHint())
        self._lblRange.setAutoFillBackground(True)

        l_pal = self._lblRange.palette()
        l_col = QtGui.QColor(255, 255, 150)
        assert l_col

        l_pal.setColor(QtGui.QPalette.Window, l_col)
        self._lblRange.setPalette(l_pal)

        # QNH label
        self._lblQNH = QtGui.QLabel(self)
        assert self._lblQNH

        self._lblQNH.setAutoFillBackground(True)

        l_pal = self._lblQNH.palette()
        l_col = QtGui.QColor(150, 255, 255)
        assert l_col

        l_pal.setColor(QtGui.QPalette.Window, l_col)
        self._lblQNH.setPalette(l_pal)

        # TL label
        self._lblTL = QtGui.QLabel(self)
        assert self._lblTL

        self._lblTL.setAutoFillBackground(True)

        l_pal = self._lblTL.palette()
        l_col = QtGui.QColor(255, 180, 255)
        assert l_col

        l_pal.setColor(QtGui.QPalette.Window, l_col)
        self._lblTL.setPalette(l_pal)

        # wind label
        self._lblWind = QtGui.QLabel(self)
        assert self._lblWind

        self._lblWind.setAutoFillBackground(True)

        l_pal = self._lblWind.palette()
        l_col = QtGui.QColor(255, 255, 150)
        assert l_col

        l_pal.setColor(QtGui.QPalette.Window, l_col)
        self._lblWind.setPalette(l_pal)

        # logger
        # M_LOG.info("createStatusBarLabels:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def draw3DRect(self, f_painter, f_rect, f_clr1, f_clr2):
        """
        draws the rectangle in the status bar to set the text in it
        """
        # logger
        # M_LOG.info("draw3DRect:>>")

        l_penAnt = f_painter.pen()

        f_painter.setPen(f_clr1)
        f_painter.drawLine(f_rect.bottomLeft(), f_rect.topLeft())
        f_painter.drawLine(f_rect.topLeft(), f_rect.topRight())

        f_painter.setPen(f_clr2)
        f_painter.drawLine(f_rect.topRight(), f_rect.bottomRight())
        f_painter.drawLine(f_rect.bottomRight(), f_rect.bottomLeft())

        f_painter.setPen(l_penAnt)

        # logger
        # M_LOG.info("draw3DRect:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def drawHeightFilters(self, f_painter):
        """
        resizes the status of a radar after a resizeEvent
        """
        # logger
        # M_LOG.info("drawHeightFilters:>>")
        '''
        QString str1,str2,str3,str4,str5
        QSize sizesep,sizeservice,sizeheight,size1,size2,size3,size4,size5

        f_painter.setPen(CColorMngr::GetColor(DefWindowTextClr))
        sizeheight=f_painter.boundingRect(0,0,0,0,QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop,"H(000/000/999)").size()
        sizeservice=f_painter.boundingRect(0,0,0,0,QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop,"WWWWWWWWWWWWWWWWWWW").size()
        QRect rect=QRect(41+sizeservice.width(),1,sizeheight.width()+23,28)
        int posy=(20+sizeheight.height())/2
        sizesep=f_painter.boundingRect(0,0,0,0,QtCore.Qt.AlignLeft,"/").size()
        str1="H("
        size1=f_painter.boundingRect(0,0,0,0,QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop,str1).size()
        str2.sprintf("%.3d",self.m_LowFilter)
        size2=f_painter.boundingRect(0,0,0,0,QtCore.Qt.AlignLeft,str2).size()
        str3.sprintf("%.3d",self.m_HighFilter)
        size3=f_painter.boundingRect(0,0,0,0,QtCore.Qt.AlignLeft,str3).size()
        str4.sprintf(" %.3d",self.m_DepFilter)
        size4=f_painter.boundingRect(0,0,0,0,QtCore.Qt.AlignLeft,str4).size()
        str5=")"
        size5=f_painter.boundingRect(0,0,0,0,QtCore.Qt.AlignLeft,str5).size()
        f_painter.drawText(rect.left()+5,posy,str1)

        if(!self.m_DepFilterIsOn)
        {
            f_painter.setPen(CColorMngr::GetColor(DefMenuDisTextClr))
            f_painter.drawText(rect.left()+4+size1.width(),posy-1,str4)
            f_painter.setPen(CColorMngr::GetColor(DefMenuLeftTopClr))
        }
        else
            f_painter.setPen(CColorMngr::GetColor(DefWindowTextClr))
        f_painter.drawText(rect.left()+5+size1.width(),posy,str4)

        if(!self.m_DepFilterIsOn)
        {
            f_painter.setPen(CColorMngr::GetColor(DefMenuDisTextClr))
            f_painter.drawText(rect.left()+4+size1.width()+size4.width(),posy-1,"/")
            f_painter.setPen(CColorMngr::GetColor(DefMenuLeftTopClr))
        }
        else
            f_painter.setPen(CColorMngr::GetColor(DefWindowTextClr))
        f_painter.drawText(rect.left()+5+size1.width()+size4.width(),posy,"/")

        if(!self.m_LowFilterIsOn)
        {
            f_painter.setPen(CColorMngr::GetColor(DefMenuDisTextClr))
            f_painter.drawText(rect.left()+4+size1.width()+size4.width()+sizesep.width(),posy-1,str2)
            f_painter.setPen(CColorMngr::GetColor(DefMenuLeftTopClr))
        }
        else
            f_painter.setPen(CColorMngr::GetColor(DefWindowTextClr))
        f_painter.drawText(rect.left()+5+size1.width()+size4.width()+sizesep.width(),posy,str2)

        if((!self.m_LowFilterIsOn) &&(!self.m_HighFilterIsOn))
        {
            f_painter.setPen(CColorMngr::GetColor(DefMenuDisTextClr))
            f_painter.drawText(rect.left()+4+size1.width()+size4.width()+sizesep.width()+size2.width(),posy-1,"/")
            f_painter.setPen(CColorMngr::GetColor(DefMenuLeftTopClr))
        }
        else
            f_painter.setPen(CColorMngr::GetColor(DefWindowTextClr))
        f_painter.drawText(rect.left()+5+size1.width()+size4.width()+sizesep.width()+size2.width(),posy,"/")

        if(!self.m_HighFilterIsOn)
        {
            f_painter.setPen(CColorMngr::GetColor(DefMenuDisTextClr))
            f_painter.drawText(rect.left()+4+size1.width()+size4.width()+sizesep.width()+size2.width()+sizesep.width(),posy-1,str3)
            f_painter.setPen(CColorMngr::GetColor(DefMenuLeftTopClr))
        }
        else
            f_painter.setPen(CColorMngr::GetColor(DefWindowTextClr))
        f_painter.drawText(rect.left()+5+size1.width()+size4.width()+sizesep.width()+size2.width()+sizesep.width(),posy,str3)

        f_painter.setPen(CColorMngr::GetColor(DefWindowTextClr))
        f_painter.drawText(rect.left()+5+size1.width()+size2.width()+sizesep.width()+size3.width()+sizesep.width()+size4.width(),posy,str5)

        Draw3dRect(dc,rect,CColorMngr::GetColor(DefWindowRightBottomClr),CColorMngr::GetColor(DefWindowLeftTopClr))
        rect.addCoords(1,1,-1,-1)
        Draw3dRect(dc,rect,CColorMngr::GetColor(DefWindowRightBottomClr),CColorMngr::GetColor(DefWindowLeftTopClr))
        '''
        # logger
        # M_LOG.info("drawHeightFilters:<<")
    '''
    # ---------------------------------------------------------------------------------------------
    # void (???)
    def paintEvent(self, f_event):
        """
        draws and positions in the status of a radar the radar and weather services, the filters,
        the coordinates of the mouse pointer
        """
        # logger
        l_log.debug(">>")

        self.setAttribute(QtCore.Qt.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #super(CStatusBarVisil, self).paintEvent(f_event)

        if(self._pHBitmap is None):
            return

        # logger
        l_log.debug("<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def resizeEvent(self, f_event):
        """
        resizes the status of a radar after a resizeEvent
        """
        # logger
        l_log.debug(">>")

        size = f_event.size()

        if(self._pHBitmap is not None):
            del self._pHBitmap

        self._pHBitmap = QtCore.QPixmap(size)

        # logger
        l_log.debug("<<")
    '''
    # ---------------------------------------------------------------------------------------------
    # void (???)
    def updateCoordinates(self, f_sCoordinates, f_vUpdate=True):
        """
        updates the latitude and longitude on the status bar of radar screen
        """
        # logger
        # M_LOG.info("updateCoordinates:>>")

        # flag update ?
        if f_vUpdate:
            # save coordinates
            # self._sCoordinates = f_sCoordinates

            # set latitude/longitude coordinates label
            self._lblCoords.setText(f_sCoordinates)

            # update status bar
            self.update()

        # logger
        # M_LOG.info("updateCoordinates:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def updateCWP(self, f_vCWP, f_vUpdate=True):
        """
        updates the CWP on the status bar of radar windows
        """
        # logger
        # M_LOG.info("updateCWP:>>")

        # save CWP position
        m_IsAppPos = f_vCwp

        # set CWP position label
        self._lblCwp.setText(" APP " if m_IsAppPos else " TWR ")

        # flag update ?
        if f_vUpdate:
            # update status bar
            self.update()

        # logger
        # M_LOG.info("updateCWP:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def updateFilters(self, f_vPrim, f_vVfr, f_vMil, f_vDataBlock, f_vWeather, f_vWeatherNotAvail, f_vUpdate=True):
        """
        updates, on the status bar of radar windows, the Primary, Vfr, Military, Datablock filters anf the Weather service and his status
        """
        # logger
        # M_LOG.info("updateFilters:>>")
        '''
        self.m_PrimFilter = f_vPrim
        self.m_VfrFilter = f_vVfr
        self.m_MilFilter = f_vMil
        self.m_DataFilter = f_vDataBlock
        self.m_WeatherIsOn = f_vWeather
        self.m_WeatherNotAvail = f_vWeatherNotAvail
        '''
        # flag update ?
        if f_vUpdate:
            # update status bar
            self.update()

        # logger
        # M_LOG.info("updateFilters:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def updateHeightFilter(self, f_iLowFilter, f_vLowFilterOn, f_iHighFilter, f_vHighFilterOn, f_iDepFilter, f_vDepFilterOn, f_vUpdate=True):
        """
        updates the height filters on the status bar of radar windows
        """
        # logger
        # M_LOG.info("updateHeightFilter:>>")
        '''
        self.m_LowFilter = LowFilter
        self.m_LowFilterIsOn = f_vLowFilterOn

        self.m_HighFilter = HighFilter
        self.m_HighFilterIsOn = f_vHighFilterOn

        self.m_DepFilter = DepFilter
        self.m_DepFilterIsOn = f_vDepFilterOn
        '''
        # flag update ?
        if f_vUpdate:
            # update status bar
            self.update()

        # logger
        # M_LOG.info("updateHeightFilter:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def updateInd(self, f_vInd, f_vUpdate=True):
        """
        updates the Independant/Dependant mode on the status bar of radar windows
        """
        # logger
        # M_LOG.info("updateInd:>>")
        '''
        # save mode
        m_IsInd = f_vInd
        '''
        # flag update ?
        if f_vUpdate:
            # independant mode ?
            self._lblInd.setText("")

            # update status bar
            self.update()

        # logger
        # M_LOG.info("updateInd:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def updateRadarService(self, f_sService, f_vUnavail, f_vDifferent, f_vUpdate=True):
        """
        updates the radar services used on the status bar of radar windows
        """
        # logger
        # M_LOG.info("updateRadarService:>>")
        '''
        self.m_RadarService=Service
        self.m_RadarIsNotAvail=Unavail
        self.m_RadarIsDiff=Different
        '''
        # flag update ?
        if f_vUpdate:
            # set radar services label
            self._lblRadarService.setText(" " + self._RadarService)

            # update status bar
            self.update()

        # logger
        # M_LOG.info("updateRadarService:<<")

    # ---------------------------------------------------------------------------------------------
    # void (???)
    def updateRange(self, f_nRange, f_vUpdate=True):
        """
        updates the range on the status bar of radar windows
        """
        # logger
        # M_LOG.info("updateRange:>>")

        # flag update ?
        if f_vUpdate:
            # set range label
            self._lblRange.setText("R%d" % f_nRange)

            # update status bar
            self.update()

        # logger
        # M_LOG.info("updateRange:<<")

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def lblCoords(self):
        # retorna as coordenadas
        return self._lblCoords

    @lblCoords.setter
    def lblCoords(self, f_sVal):
        # seta as coordenadas
        self._lblCoords = f_sVal

    # ---------------------------------------------------------------------------------------------
    @property
    def lblRange(self):
        # retorna o range
        return self._lblRange

    @lblRange.setter
    def lblRange(self, f_sVal):
        # seta o range
        self._lblRange = f_sVal

    # ---------------------------------------------------------------------------------------------
    @property
    def lblQNH(self):
        # retorna o QNH
        return self._lblQNH

    @lblQNH.setter
    def lblQNH(self, f_sVal):
        # seta o QNH
        self._lblQNH = f_sVal

    # ---------------------------------------------------------------------------------------------
    @property
    def lblTL(self):
        # retorna o TL
        return self._lblTL

    @lblTL.setter
    def lblTL(self, f_sVal):
        # seta o TL
        self._lblTL = f_sVal

    # ---------------------------------------------------------------------------------------------
    @property
    def lblWind(self):
        # retorna o Wind
        return self._lblWind

    @lblWind.setter
    def lblWind(self, f_sVal):
        # seta o wind
        self._lblWind = f_sVal

# < the end >--------------------------------------------------------------------------------------
