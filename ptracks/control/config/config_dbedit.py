#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
config_dbedit

mantém as informações de configuração do editor da base de dados

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
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import os

# from ...model 
import ptracks.model.data as data

# from ...control.config 
import ptracks.control.config.config_manager as config

# < class CConfigDBEdit >--------------------------------------------------------------------------

class CConfigDBEdit(config.CConfigManager):
    """
    mantém as informações de configuração do editor da base de dados
    """
    # informações comuns de configuração
    __CFG_DBEDIT = {"glb.exe": None,    # exercício

                    "tab.aer": "tabAer",    # tabela de aeródromos
                    "tab.apx": "tabApx",    # tabela de aproximações
                    "tab.esp": "tabEsp",    # tabela de procedimentos de espera
                    "tab.fix": "tabFix",    # tabela de fixos
                    "tab.prf": "tabPrf",    # tabela de performances
                    "tab.sub": "tabSub",    # tabela de procedimentos de subida
                    "tab.trj": "tabTrj",    # tabela de procedimentos de trajetória
                   }  # __CFG_DBEDIT

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_path):
        """
        inicia o gerente de configuração do editor da base de dados

        @param fs_path: full path do arquivo de configuração
        """
        # init super class
        super(CConfigDBEdit, self).__init__(fs_path)

        # herdados de CConfigManager
        # self.dct_config    # config manager data dictionary

        # carrega os atributos locais no dicionário de configuração
        for l_key in self.__CFG_DBEDIT.keys():
            if l_key not in self.dct_config:
                self.dct_config[l_key] = self.__CFG_DBEDIT[l_key]

        # load dirs section
        self.__load_dirs()

    # ---------------------------------------------------------------------------------------------
    def __load_dirs(self):
        """
        carrega as configurações de diretórios
        """
        # monta o diretório de exercícios
        self.dct_config["dir.exe"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.exe"]))

        # monta o diretório de procedimentos
        self.dct_config["dir.prc"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.prc"]))

        # monta o diretório de tabelas
        self.dct_config["dir.tab"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.tab"]))

        # monta o diretório de tráfegos
        self.dct_config["dir.trf"] = data.filepath(os.path.join(self.dct_config["dir.dat"],
                                                                self.dct_config["dir.trf"]))

# < the end >--------------------------------------------------------------------------------------
