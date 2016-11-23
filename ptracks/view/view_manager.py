#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
view_manager

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

revision 0.3  2016/ago  mlabru
pequenas correções e otimizações

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/08"

# < imports >--------------------------------------------------------------------------------------

# python library
# import logging

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CViewManager >---------------------------------------------------------------------------

class CViewManager(object):
    """
    handles all interaction with user. This class is the interface
    It draws the scope on the screen and handles all mouse input
    """
    # ---------------------------------------------------------------------------------------------
    # void (???)
    def __init__(self, f_control):
        """
        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")
                
        # check input
        assert f_control

        # save control manager
        self.__control = f_control

        # register as listener
        f_control.event.register_listener(self)
                                                                                                
        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------
    # @abstractmethod
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        # logger
        # M_LOG.info("notify:><")
        pass

    # ---------------------------------------------------------------------------------------------
    # @abstractmethod
    def run(self):
        """
        DOCUMENT ME!
        """
        # logger
        # M_LOG.info("run:><")
                
        # return
        return False

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def app(self):
        """
        get app manager
        """
        return self.__control.app

    @app.setter
    def app(self, f_val):
        """
        set app manager
        """
        # check input
        assert f_val

        # save app manager
        self.__control.app = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def config(self):
        """
        get config manager
        """
        return self.__control.config

    @config.setter
    def config(self, f_val):
        """
        set config manager
        """
        # check input
        assert f_val

        # save config manager
        self.__control.config = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_config(self):
        """
        get configuration dictionary
        """
        return self.__control.config.dct_config

    @dct_config.setter
    def dct_config(self, f_val):
        """
        set configuration dictionary
        """
        # check input
        assert f_val

        # save configuration dictionary
        self.__control.config.dct_config = f_val

    # ---------------------------------------------------------------------------------------------

    @property
    def control(self):
        """
        get control manager
        """
        return self.__control

    @control.setter
    def control(self, f_val):
        """
        set control manager
        """
        # check input
        assert f_val

        # save control manager
        self.__control = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def event(self):
        """
        get event manager
        """
        return self.__control.event

    @event.setter
    def event(self, f_val):
        """
        set event manager
        """
        # check input
        assert f_val

        # save event manager
        self.__control.event = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        """
        get model manager
        """
        return self.__control.model

    @model.setter
    def model(self, f_val):
        """
        set model manager
        """
        # check input
        assert f_val

        # save model manager
        self.__control.model = f_val

# < the end >--------------------------------------------------------------------------------------
