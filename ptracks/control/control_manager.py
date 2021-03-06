#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
control_manager

coordinates communications between the model, views and controllers through the use of events

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

revision 0.4  2016/ago  mlabru
pequenas correções e otimizações

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do event manager e alteração do config manager

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.4$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/08"

# < imports >--------------------------------------------------------------------------------------

# python library
import sys
import threading
import time

# model
import ptracks.model.glb_data as gdata

# control
import ptracks.control.events.events_manager as evtmgr
import ptracks.control.events.events_basic as events

# < class CControlManager >------------------------------------------------------------------------

class CControlManager(threading.Thread):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_path=None):
        """
        constructor

        @param fs_path: path do arquivo de configuração
        """
        # inicia a super classe
        super(CControlManager, self).__init__()

        # the application itself
        self.__app = None

        # instancia o event manager
        self.__event = evtmgr.CEventsManager()
        assert self.__event

        # registra a sí próprio como recebedor de eventos
        self.__event.register_listener(self)

        # carrega as opções de configuração
        self.__config = None

        # model manager
        self.__model = None

        # splash screen
        self.__splash = None

        # view manager
        self.__view = None

        # voip library
        self.__voip = None

    # ---------------------------------------------------------------------------------------------
    def cbk_termina(self):
        """
        termina a aplicação
        """
        # verifica condições de execução
        assert self.__event

        # cria um evento de quit
        l_evt = events.CQuit()
        assert l_evt

        # dissemina o evento
        self.__event.post(l_evt)

    # ---------------------------------------------------------------------------------------------
    @staticmethod
    def notify(f_event):
        """
        callback de tratamento de eventos recebidos.

        @param f_event: event.
        """
        # check input
        assert f_event

        # recebeu um aviso de término da aplicação ?
        if isinstance(f_event, events.CQuit):
            # para todos os processos
            gdata.G_KEEP_RUN = False

            # aguarda o término das tasks
            time.sleep(1)

            # termina a aplicação
            sys.exit()

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        executa a aplicação
        """
        # return
        return gdata.G_KEEP_RUN

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def app(self):
        """
        get application
        """
        return self.__app

    @app.setter
    def app(self, f_val):
        """
        set application
        """
        self.__app = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def config(self):
        """
        get config manager
        """
        return self.__config

    @config.setter
    def config(self, f_val):
        """
        set config manager
        """
        self.__config = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def event(self):
        """
        get event manager
        """
        return self.__event

    @event.setter
    def event(self, f_val):
        """
        set event manager
        """
        self.__event = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        """
        get model manager
        """
        return self.__model

    @model.setter
    def model(self, f_val):
        """
        set model manager
        """
        self.__model = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def splash(self):
        """
        get splash screen
        """
        return self.__splash

    @splash.setter
    def splash(self, f_val):
        """
        set splash screen
        """
        self.__splash = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def view(self):
        """
        get view manager
        """
        return self.__view

    @view.setter
    def view(self, f_val):
        """
        set view manager
        """
        self.__view = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def voip(self):
        """
        get voip library
        """
        return self.__voip

# < the end >--------------------------------------------------------------------------------------
