#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
comando_piloto.

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

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# Python library
import logging

# model
import model.newton.defs_newton as ldefs

import model.stock.instruction as inst

# < module data >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# < class CComandoPil >----------------------------------------------------------------------------

class CComandoPil(inst.CInstruction):
    """
    DOCUMENT ME
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, fs_msg=""):

        # logger
        # M_LOG.info("__init__:>>")

        # verifica parâmetros de entrada
        # assert f_control

        # inicia a super classe
        super(CComandoPil, self).__init__()

        # herdados de CInstruction
        # self.en_cmd_ope    # comando
        # self.f_param_1     # parâmetro 1
        # self.f_param_2     # parâmetro 2
        # self.s_text        # texto do comando

        # recebeu uma mensagem ?
        if "" != fs_msg:

            # salva o texto da mensagem
            self.s_text = fs_msg

            # parse mensagem
            self.__parse_comando(fs_msg)

        # logger
        # M_LOG.info("__init__:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_altitude(self, flst_tok):

        # logger
        # M_LOG.info("__cmd_altitude:>>")

        # verifica parâmetros de entrada
        assert flst_tok

        M_LOG.debug("lista de tokens: " + str(flst_tok))

        # comando
        self.en_cmd_ope = ldefs.E_ALT

        # altitude em pés(ft)
        self.f_param_1 = float(flst_tok[0])

        # parâmetro razão ?
        if "RAZ" == flst_tok[1]:

            # parse command
            self.__cmd_razao(flst_tok[2:])

        # logger
        # M_LOG.info("__cmd_altitude:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_curva(self, flst_tok):

        # logger
        # M_LOG.info("__cmd_curva:>>")

        # verifica parâmetros de entrada
        assert flst_tok

        M_LOG.debug("lista de tokens: " + str(flst_tok))

        # parâmetro direita ?
        if "DIR" == flst_tok[0]:

            # comando curva direita
            self.en_cmd_ope = ldefs.E_CDIR

        # parâmetro esquerda ?
        elif "ESQ" == flst_tok[0]:

            # comando curva esquerda
            self.en_cmd_ope = ldefs.E_CESQ

        # parâmetro menor ?
        else:
            # comando curva menor
            self.en_cmd_ope = ldefs.E_CMNR

        # parâmetro proa ?
        if "PROA" == flst_tok[1]:

            # parse proa
            self.__cmd_proa(flst_tok[2:])
        
        # parâmetro graus ?
        elif "GRAUS" == flst_tok[2]:

            # parse graus
            self.__cmd_graus(flst_tok[1:])
        
        # parâmetro razão ?
        elif "RAZ" == flst_tok[1]:

            # parse razão
            self.__cmd_razao(flst_tok[2:])

        # logger
        # M_LOG.info("__cmd_curva:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_graus(self, flst_tok):

        # logger
        # M_LOG.info("__cmd_graus:>>")

        # verifica parâmetros de entrada
        assert flst_tok
        
        M_LOG.debug("lista de tokens: " + str(flst_tok))

        # graus
        self.f_param_1 = float(flst_tok[0])

        # parâmetro razão ?
        if "RAZ" == flst_tok[2]:

            # parse command razão
            self.__cmd_razao(flst_tok[3:])

        # logger
        # M_LOG.info("__cmd_graus:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_nivel(self, flst_tok):

        # logger
        # M_LOG.info("__cmd_nivel:>>")

        # verifica parâmetros de entrada
        assert flst_tok
        
        M_LOG.debug("lista de tokens: " + str(flst_tok))

        # comando nível
        self.en_cmd_ope = ldefs.E_NIV

        # nível
        self.f_param_1 = float(flst_tok[0])

        # parâmetro razão ?
        if "RAZ" == flst_tok[1]:

            # parse command
            self.__cmd_razao(flst_tok[2:])

        # logger
        # M_LOG.info("__cmd_nivel:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_proa(self, flst_tok):

        # logger
        # M_LOG.info("__cmd_proa:>>")

        # verifica parâmetros de entrada
        assert flst_tok
        
        M_LOG.debug("lista de tokens: " + str(flst_tok))

        # proa
        self.f_param_1 = float(flst_tok[0])

        # parâmetro razão ?
        if "RAZ" == flst_tok[1]:

            # parse command razão
            self.__cmd_razao(flst_tok[2:])

        # logger
        # M_LOG.info("__cmd_proa:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_razao(self, flst_tok):

        # logger
        # M_LOG.info("__cmd_razao:>>")

        # verifica parâmetros de entrada
        assert flst_tok
        
        M_LOG.debug("lista de tokens: " + str(flst_tok))

        # razão
        self.f_param_2 = float(flst_tok[0])

        # logger
        # M_LOG.info("__cmd_razao:<<")

    # ---------------------------------------------------------------------------------------------

    def __cmd_velocidade(self, flst_tok):

        # logger
        # M_LOG.info("__cmd_velocidade:>>")

        # verifica parâmetros de entrada
        assert flst_tok

        M_LOG.debug("lista de tokens: " + str(flst_tok))

        # comando
        self.en_cmd_ope = ldefs.E_IAS

        # velocidade
        self.f_param_1 = float(flst_tok[0])

        # logger
        # M_LOG.info("__cmd_velocidade:<<")

    # ---------------------------------------------------------------------------------------------

    def __parse_comando(self, fs_cmd=""):

        # logger
        # M_LOG.info("__parse_comando:>>")

        # verifica parâmetros de entrada
        # assert f_control

        # recebeu um comando ?
        if "" == fs_cmd:

            # logger
            # M_LOG.info("__parse_comando:<E01: comando vazio")

            # return
            return

        # faz o split do comando
        llst_tok = fs_cmd.split()

        # comando de altitude ?
        if "ALT" == llst_tok[0]:
            # parse command
            self.__cmd_altitude(llst_tok[1:])

        # comando de curva ?
        elif "CURVA" == llst_tok[0]:
            # parse command
            self.__cmd_curva(llst_tok[1:])

        # comando de nível ?
        elif "NIV" == llst_tok[0]:
            # parse command
            self.__cmd_nivel(llst_tok[1:])

        # comando de velocidade ?
        elif "VEL" == llst_tok[0]:
            # parse command
            self.__cmd_velocidade(llst_tok[1:])

        # logger
        # M_LOG.info("__parse_comando:<<")

    # =============================================================================================
    # data
    # =============================================================================================
            
    # ---------------------------------------------------------------------------------------------
    '''                
    @property
    def en_cmd_ope(self):
        """
        get comando operacional
        """
        return self.__en_cmd_ope
                                                        
    @en_cmd_ope.setter
    def en_cmd_ope(self, f_val):
        """
        set comando operacional
        """
        self.__en_cmd_ope = f_val
    '''                                                        
# < the end >--------------------------------------------------------------------------------------
