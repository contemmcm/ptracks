#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
emula_piloto

the actual flight control

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
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import json
import logging
import threading
import time

# model
import ptracks.model.glb_data as gdata
import ptracks.model.glb_defs as gdefs

import ptracks.model.emula.emula_model as model

import ptracks.model.piloto.data_piloto as ldata
import ptracks.model.piloto.aircraft_piloto as canv

# control
import ptracks.control.events.events_flight as events

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CEmulaPiloto >---------------------------------------------------------------------------

class CEmulaPiloto(model.CEmulaModel):
    """
    the flight model class generates new flights and handles their movement. It has a list of
    flight objects holding all flights that are currently active. The flights are generated when
    activation time comes, or quando ja foi ativado na confecção do exercicio. Once a flight has
    been generated it is handed by the flight engine
    """
    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __init__(self, f_model, f_control):
        """
        @param f_model: model manager
        @param f_control: control manager
        """
        # logger
        # M_LOG.info("__init__:>>")

        # verifica parametros de entrada
        assert f_control
        assert f_model

        # inicia a super classe
        super(CEmulaPiloto, self).__init__(f_model, f_control)

        # herdados de CFlightModel
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager
        # self.dct_flight    # dictionary for active flights
        # self.model         # model manager

        # obtém a queue de dados
        self.__q_rcv_trks = f_control.q_rcv_trks
        assert self.__q_rcv_trks

        # obtém o data listener
        self.__sck_rcv_trks = f_control.sck_rcv_trks
        assert self.__sck_rcv_trks

        # obtém o http server listener
        self.__sck_http = f_control.sck_http
        assert self.__sck_http

        # obtém o relógio da simulação
        self.__sim_time = f_control.sim_time
        assert self.__sim_time

        # obtém o dicionário de performances
        self.__dct_prf = f_model.dct_prf
        assert self.__dct_prf is not None

        # cria a trava da lista de vôos
        gdata.G_LCK_FLIGHT = threading.Lock()
        assert gdata.G_LCK_FLIGHT
                        
        # logger
        # M_LOG.info("__init__:<<")
                                        
    # ---------------------------------------------------------------------------------------------
    # void (?)
    def __msg_trk(self, flst_data):
        """
        checks whether it's time to created another flight

        @param flst_data: mensagem de status
        """
        # logger
        # M_LOG.info("__msg_trk:>>")

        # check for requirements
        assert self.__sck_http is not None
        assert self.dct_config is not None
        assert self.dct_flight is not None
        assert self.__dct_prf is not None
                
        # obtém o callsign da aeronave
        ls_callsign = flst_data[10]
        # M_LOG.debug("__msg_trk:callsign:[{}]".format(ls_callsign))
                            
        # trava a lista de vôos
        gdata.G_LCK_FLIGHT.acquire()

        try:
            # aeronave já está no dicionário ?
            if ls_callsign in self.dct_flight:

                # atualiza os dados da aeronave
                self.dct_flight[ls_callsign].update_data(flst_data[1:])

            # senão, aeronave nova...
            else:
                # create new aircraft
                self.dct_flight[ls_callsign] = canv.CAircraftPiloto(self, flst_data[1:])
                assert self.dct_flight[ls_callsign]
                                                                                                                                                                                                                                                            
        finally:
            # libera a lista de vôos
            gdata.G_LCK_FLIGHT.release()

        # obtém o indicativo da performance
        ls_prf_ind = flst_data[11]
        # M_LOG.debug("__msg_trk:ls_prf_ind:[{}]".format(ls_prf_ind))
                            
        # performance não está no dicionário ?
        if self.__dct_prf.get(ls_prf_ind, None) is None:

            # monta o request da performance
            ls_req = "data/prf.json?{}".format(ls_prf_ind)
            # M_LOG.debug("__msg_trk:ls_req:[{}]".format(ls_req))

            # get server address
            l_srv = self.dct_config.get("srv.addr", None)
            
            if l_srv is not None:
                # obtém os dados de performance do servidor
                l_prf = self.__sck_http.get_data(l_srv, ls_req)
                # M_LOG.debug("__msg_trk:l_prf:[{}]".format(l_prf))

                if (l_prf is not None) and (l_prf != ""):
                    # salva a performance no dicionário
                    self.__dct_prf[ls_prf_ind] = json.loads(l_prf)
                    # M_LOG.debug("__msg_trk:dct_prf:[{}]".format(self.__dct_prf))

                # senão, não achou no servidor...
                else:
                    # logger
                    l_log = logging.getLogger("CEmulaPiloto::__msg_trk")
                    l_log.setLevel(logging.WARNING)
                    l_log.error(u"<E01: performance({}) não existe no servidor.".format(ls_prf_ind))

            # senão, não achou endereço do servidor
            else:
                # logger
                l_log = logging.getLogger("CEmulaPiloto::__msg_trk")
                l_log.setLevel(logging.WARNING)
                l_log.warning(u"<E02: srv.addr não existe na configuração.")

        # cria um evento de atualização de aeronave
        l_evt = events.CFlightUpdate(ls_callsign)
        assert l_evt

        # dissemina o evento
        self.event.post(l_evt)

        # logger
        # M_LOG.info("__msg_trk:<<")

    # ---------------------------------------------------------------------------------------------
    # void (?)
    def run(self):
        """
        checks whether it's time to created another flight
        """
        # logger
        # M_LOG.info("run:>>")
                
        # check de colisão
        lf_tim_rrbn = float(self.dct_config["tim.rrbn"])

        # enquanto não inicia...
        while not gdata.G_KEEP_RUN:
            # aguarda 1 seg
            time.sleep(1)

        # inicia o recebimento de mensagens de pista
        self.__sck_rcv_trks.start()

        # obtém o tempo inicial em segundos
        lf_now = time.time()

        # loop
        while gdata.G_KEEP_RUN:
            # obtém um item da queue de entrada
            llst_data = self.__q_rcv_trks.get()
            # M_LOG.debug("llst_data: (%s)" % str(llst_data))

            # queue tem dados ?
            if llst_data:
                # mensagem de status de aeronave ?
                if gdefs.D_MSG_NEW == int(llst_data[0]):
                    # trata mensagem de status de aeronave
                    self.__msg_trk(llst_data)
                    
                # mensagem de eliminação de aeronave ?
                elif gdefs.D_MSG_Kll == int(llst_data[0]):
                    # coloca a mensagem na queue
                    # M_LOG.debug("Elimina: (%s)" % str(ls_callsign))

                    # trava a lista de vôos
                    ldata.G_LCK_FLIGHT.acquire()

                    try:
                        # aeronave está no dicionário ?
                        if ls_callsign in self.dct_flight:
                            # retira a aeronave do dicionário
                            del self.dct_flight[ls_callsign]

                    finally:
                        # libera a lista de vôos
                        ldata.G_LCK_FLIGHT.release()

                    # cria um evento de eliminação de aeronave
                    l_evt = events.FlightKill(ls_callsign)
                    assert l_evt

                    # dissemina o evento
                    self._event.post(l_evt)

                # senão, mensagem não reconhecida ou não tratada
                else:
                    # logger
                    l_log = logging.getLogger("CEmulaPiloto::run")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E01: mensagem não reconhecida ou não tratada.")

            # salva o tempo anterior
            lf_ant = lf_now

            # obtém o tempo atual em segundos
            lf_now = time.time()
                                    
            # obtém o tempo final em segundos e calcula o tempo decorrido
            lf_dif = lf_now - lf_ant
                                                                            
            # está adiantado ?
            if lf_tim_rrbn > lf_dif:
                # permite o scheduler
                time.sleep(lf_tim_rrbn - lf_dif)

    # ---------------------------------------------------------------------------------------------
    @property
    def sck_rcv_trks(self):
        """
        data listener
        """
        return self.__sck_rcv_trks

# < the end >--------------------------------------------------------------------------------------
