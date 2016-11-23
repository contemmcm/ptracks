#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
prc_espera

realiza o procedimento de espera

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
import logging
import math

# libs
import libs.coords.coord_defs as cdefs

# model
import model.newton.defs_newton as ldefs

import model.emula.cine.abort_prc as abnd
import model.emula.cine.calc_proa_demanda as cpd
import model.emula.cine.prc_dir_ponto as dp
import model.emula.cine.sentido_curva as scrv

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# nível 140 = 14000FT
M_14000FT = 14000 * cdefs.D_CNV_FT2M

# velocidade máxima de 230KT quando o nível <= 14000FT
M_VEL_MAX = 230. * cdefs.D_CNV_KT2MS

# razão máxima de subida/descida = 1000ft/min
M_RAZ_SUB = (1000. * cdefs.D_CNV_FT2M) / 60.

# -------------------------------------------------------------------------------------------------
def __check_cancel_espera(f_atv, f_esp):
    """
    checa condições de abandonar a espera. A condição é executada pelo comando de pilotagem

    @param f_atv: pointer para aeronave
    @param f_esp: pointer para espera

    @return True se condição de abandonar a espera, senão False (condição de permanecer em espera)
    """
    # logger
    # M_LOG.info("__check_cancel_espera:>>")
        
    # check input
    assert f_atv

    # verifica condições para execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # logger
        # M_LOG.info("__check_cancel_espera:<E01: aeronave não ativa.")

        # cai fora...
        return True

    # verifica condições para execução
    if (f_esp is None) or (not f_esp.v_prc_ok):
        # logger
        # M_LOG.info("__check_cancel_espera:<E02: procedimento de espera não existe.")
                        
        # cai fora...
        return True

    # condição de cancelamento ?
    if f_atv.v_atv_cnl_esp:
        # coloca a aeronave na condição de abandonar a espera
        abnd.abort_prc(f_atv)
                
        # logger
        # M_LOG.info("__check_cancel_espera:<E03: em condição de abandonar.")

        # return
        return True

    # logger
    # M_LOG.info("__check_cancel_espera:<<")
        
    # return
    return False

# -------------------------------------------------------------------------------------------------
def __setor_entrada(f_atv, f_esp):
    """
    determina o setor de entrada na espera

    @param f_atv: pointer para aeronave
    @param f_esp: pointer para espera

    @return ldefs.E_FASE_SETOR1, ldefs.E_FASE_SETOR2 ou ldefs.E_FASE_SETOR3
    """
    # logger
    # M_LOG.info("__setor_entrada:>>")
        
    # check input
    assert f_atv

    # verifica condições para execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # logger
        # M_LOG.info("__setor_entrada:<E01: aeronave não ativa.")

        # cai fora...
        return -1

    # verifica condições para execução
    if (f_esp is None) or (not f_esp.v_prc_ok):
        # logger
        # M_LOG.info("__setor_entrada:<E02: procedimento de espera não existe.")
                        
        # cai fora...
        return -1

    # calcula o ângulo de entrada
    lf_ang_entrada = f_atv.f_trf_pro_atu - 180.

    # normaliza o ângulo de entrada
    if lf_ang_entrada < 0.:
        lf_ang_entrada += 360.

    # verifica o sentido da espera (direita/esquerda)

    # espera pela direita ?
    if ldefs.E_DIREITA == f_esp.en_esp_sentido_curva:
        # calcula o limite pelo setor 2
        lf_limite_2 = f_esp.f_esp_rumo - 70.

        # normaliza o limite
        if lf_limite_2 < 0.:
            lf_limite_2 += 360.

        # cálculo da diferença entre os ângulos
        lf_dif_ang = lf_ang_entrada - lf_limite_2

        # normaliza da diferença entre os ângulos
        if lf_dif_ang < 0.:
            lf_dif_ang += 360.

        # determina o setor de entrada da aeronave
        if lf_dif_ang <= 70.:
            # logger
            # M_LOG.info("__setor_entrada:<E03: FASE_SETOR2.")

            # realiza fase entrada no setor 2
            return ldefs.E_FASE_SETOR2

        elif lf_dif_ang <= 180.:
            # logger
            # M_LOG.info("__setor_entrada:<E04: FASE_SETOR1.")

            # realiza fase entrada no setor 1
            return ldefs.E_FASE_SETOR1

        else:
            # logger
            # M_LOG.info("__setor_entrada:<E05: FASE_SETOR3.")

            # realiza fase entrada no setor 3
            return ldefs.E_FASE_SETOR3

    # espera pela esquerda
    else:
        # cálculo da diferença entre os ângulos
        lf_dif_ang = f_esp.f_esp_rumo - lf_ang_entrada

        # normaliza a diferença entre os ângulos
        if lf_dif_ang < 0.:
            lf_dif_ang += 360.

        # determina o setor de entrada da aeronave
        if lf_dif_ang <= 110.:
            # logger
            # M_LOG.info("__setor_entrada:<E06: FASE_SETOR1.")

            # realiza fase entrada no setor 1
            return ldefs.E_FASE_SETOR1

        elif lf_dif_ang <= 290.:
            # logger
            # M_LOG.info("__setor_entrada:<E07: FASE_SETOR3.")

            # realiza fase entrada no setor 3
            return ldefs.E_FASE_SETOR3

        else:
            # logger
            # M_LOG.info("__setor_entrada:<E08: FASE_SETOR2.")

            # realiza fase entrada no setor 2
            return ldefs.E_FASE_SETOR2

    # logger
    # M_LOG.info("__setor_entrada:<<")
        
    # return
    return -1

# -------------------------------------------------------------------------------------------------
def prc_espera(f_atv, f_cine_data, f_stk_context, ff_delta_t):
    """
    DOCUMENT ME!
    
    @param f_atv: pointer para struct aeronaves
    @param f_cine_data: dados da cinemática
    @param f_stk_context: pointer para pilha
    @param ff_delta_t: tempo decorrido desde a última atualização
    """
    # logger
    # M_LOG.info("prc_espera:>>")
        
    # check input
    assert f_atv
    assert f_cine_data
    assert f_stk_context is not None

    # verifica condições para execução
    if (not f_atv.v_atv_ok) or (ldefs.E_ATIVA != f_atv.en_trf_est_atv):
        # logger
        # M_LOG.info(u"prc_espera:<E01: aeronave não ativa.")

        # cai fora...
        return

    # verifica condições para execução
    if (f_atv.ptr_trf_prf is None) or (not f_atv.ptr_trf_prf.v_prf_ok):
        # logger
        # M_LOG.info(u"prc_espera:<E02: performance não existe.")
                        
        # cai fora...
        return

    # aponta para a espera planejada e valida pointer
    l_esp = f_atv.ptr_trf_prc

    if (l_esp is None) or (not l_esp.v_prc_ok):
        # logger
        l_log = logging.getLogger("prc_espera::prc_espera")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E03: espera inexistente. aeronave:[%d/%s]", f_atv.i_trf_id, f_atv.s_trf_ind)

        # não encontrou a espera, força a aeronave abandonar o procedimento
        abnd.abort_prc(f_atv)
                
        # logger
        # M_LOG.info("prc_espera:<E03: espera inexistente.")

        # return
        return

    # aeronave abaixo de 14000ft ?
    if (f_atv.f_trf_alt_atu <= M_14000FT) and (f_atv.f_trf_vel_atu > M_VEL_MAX):
        # velocidade máxima é de 230KT
        f_atv.f_atv_vel_dem = M_VEL_MAX

    # M_LOG.debug("prc_espera:fase [{}/{}] da espera.".format(f_atv.en_atv_fase, ldefs.DCT_FASE[f_atv.en_atv_fase]))

    # preparação de dados ?
    if ldefs.E_FASE_ZERO == f_atv.en_atv_fase:
        # obtém dados do fixo de espera e valida pointer
        l_fix = l_esp.ptr_esp_fix
        # M_LOG.debug("prc_espera:ptr_atv_fix_prc:[{}/{}]".format(l_fix.i_fix_id, l_fix.s_fix_desc))

        if (l_fix is None) or (not l_fix.v_fix_ok):
            # logger
            l_log = logging.getLogger("prc_espera::prc_espera")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E04: fixo da espera inexistente. aeronave:[%d/%s]", f_atv.i_trf_id, f_atv.s_trf_ind)

            # não encontrou o fixo, força a aeronave abandonar o procedimento
            abnd.abort_prc(f_atv)

            # logger
            # M_LOG.info("prc_espera:<E04: fixo da espera inexistente.")

            # return
            return

        # checa condição de cancelamento, caso tenha sido comandado pelo piloto
        if __check_cancel_espera(f_atv, l_esp):
            # break
            return

        # direciona ao fixo de espera                                                   !!!REVER!!!
        if dp.prc_dir_ponto(f_atv, l_fix.f_fix_x, l_fix.f_fix_y, f_cine_data):
            # determina qual o setor de entrada na espera
            f_atv.en_atv_fase = __setor_entrada(f_atv, l_esp)

            # valida proa para perna de afastamento
            f_cine_data.f_afasta = l_esp.f_esp_rumo - 180.

            # normaliza proa para perna de afastamento
            if f_cine_data.f_afasta < 0.:
                f_cine_data.f_afasta += 360.

            # limita a razão de subida/descida na espera em no máximo 1000FT/MIN        !!!REVER!!!
            if f_atv.f_atv_raz_sub > M_RAZ_SUB:
                # salva a razão atual
                f_cine_data.f_raz_sub_des = f_atv.f_atv_raz_sub

                # limita a razão
                f_atv.f_atv_raz_sub = M_RAZ_SUB

    # seguir na perna de aproximação em direção oposta (perna de afastamento)
    elif ldefs.E_FASE_SETOR1 == f_atv.en_atv_fase:
        # ajusta a razão de curva em relação ao sentido da espera
        if ldefs.E_DIREITA == l_esp.en_esp_sentido_curva:
            # curva pela direita (positivo)
            f_atv.f_atv_raz_crv = -abs(f_atv.f_atv_raz_crv)

        # senão,...
        else:
            # curva pela esquerda (negativo)
            f_atv.f_atv_raz_crv = abs(f_atv.f_atv_raz_crv)

        # inicia dados da espera na pilha
        f_cine_data.i_setor_ent     = 1
        f_cine_data.i_bloqueio_fixo = 1

        # seguir numa paralela no sentido "oposto" da perna de aproximação
        f_atv.f_atv_pro_dem = f_cine_data.f_afasta

        # obtém o tempo limite na perna de aproximação considerando o limite de 14000FT
        f_cine_data.h_tempo = 90. if (f_atv.f_trf_alt_atu > M_14000FT) else 50.

        # sinaliza nova fase
        f_atv.en_atv_fase = ldefs.E_FASE_TEMPO

        # M_LOG.debug("prc_espera:E_FASE_SETOR1:[{}/{}]".format(f_atv.f_atv_raz_crv, f_cine_data.h_tempo))

    # seguir no rumo perna de afastamento defasado de 30 graus
    elif ldefs.E_FASE_SETOR2 == f_atv.en_atv_fase:
        # curva pela direita ?
        if ldefs.E_DIREITA == l_esp.en_esp_sentido_curva:
            # calcula a nova proa de demanda
            f_atv.f_atv_pro_dem = f_cine_data.f_afasta - 30.

            # normaliza
            if f_atv.f_atv_pro_dem < 0.:
                f_atv.f_atv_pro_dem += 360.

        # senão, curva pela esquerda
        else:
            # calcula a nova proa de demanda
            f_atv.f_atv_pro_dem = f_cine_data.f_afasta + 30.

            # normaliza
            if f_atv.f_atv_pro_dem > 360.:
                f_atv.f_atv_pro_dem -= 360.

        # razão de curva pelo menor lado
        scrv.sentido_curva(f_atv)

        # verifica o tempo na defasagem (1 minuto e meio no limite de 14000FT)
        f_cine_data.h_tempo = 90. if (f_atv.f_trf_alt_atu > M_14000FT) else 60.

        # sinaliza nova fase
        f_atv.en_atv_fase = ldefs.E_FASE_TEMPOSETOR

        # M_LOG.debug("prc_espera:E_FASE_SETOR2:[{}/{}]".format(f_atv.f_atv_raz_crv, f_cine_data.h_tempo))

    # entrada pelo setor 3
    elif ldefs.E_FASE_SETOR3 == f_atv.en_atv_fase:
        # entrada pelo setor 3
        f_atv.f_atv_pro_dem = f_cine_data.f_afasta

        # entra na órbita
        f_atv.en_atv_fase = ldefs.E_FASE_CRVAFASTA

        # curva pela esquerda ?
        if ldefs.E_ESQUERDA == l_esp.en_esp_sentido_curva:
            # curva pela esquerda (negativa)
            f_atv.f_atv_raz_crv = -abs(f_atv.f_atv_raz_crv)

        # senão, curva pela direita
        else:
            # curva pela direita (positiva)
            f_atv.f_atv_raz_crv = abs(f_atv.f_atv_raz_crv)

        # M_LOG.debug("prc_espera:E_FASE_SETOR2:[{}/{}]".format(f_atv.f_atv_raz_crv, f_cine_data.h_tempo))

    # permanência na perna de aproximação
    elif ldefs.E_FASE_TEMPO == f_atv.en_atv_fase:
        # permanece na perna de aproximação ?
        if f_cine_data.h_tempo > 0.:
            # decrementa o tempo na perna
            f_cine_data.h_tempo -= ff_delta_t

        # senão, estorou o tempo
        else:
            # nova fase
            f_atv.en_atv_fase = ldefs.E_FASE_VOLTA

        # M_LOG.debug("prc_espera:E_FASE_TEMPO:[{}]".format(f_cine_data.h_tempo))

    # permanência nos 30 graus do rumo para o setor 2
    elif ldefs.E_FASE_TEMPOSETOR == f_atv.en_atv_fase:
        # permanece nos 30 graus ?
        if f_cine_data.h_tempo > 0.:
            # decrementa o tempo na perna
            f_cine_data.h_tempo -= ff_delta_t

        # senão, estorou o tempo
        else:
            # nova fase
            f_atv.en_atv_fase = ldefs.E_FASE_VOLTA

        # M_LOG.debug("prc_espera:E_FASE_TEMPOSETOR:[{}]".format(f_cine_data.h_tempo))

    # fase volta ?
    elif ldefs.E_FASE_VOLTA == f_atv.en_atv_fase:

        # acessa dados do fixo de espera e valida parâmetro
        l_fix = l_esp.ptr_esp_fix

        if (l_fix is None) or not l_fix.v_fix_ok:
            # logger
            l_log = logging.getLogger("prc_espera::prc_espera")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E05: fixo da espera inexistente. aeronave:[%d/%s]", f_atv.i_trf_id, f_atv.s_trf_ind)

            # não encontrou o fixo, força a aeronave abandonar o procedimento
            abnd.abort_prc(f_atv)

            # logger
            # M_LOG.info("prc_espera:<E05: fixo da espera inexistente.")

            # return
            return

        # calcula distância da aeronave ao ponto (x, y)
        lf_coord_x = l_fix.f_fix_x - f_atv.f_trf_x
        lf_coord_y = l_fix.f_fix_y - f_atv.f_trf_y

        # calcula distância linear da aeronave ao ponto
        lf_dst_anv_pto = math.sqrt((lf_coord_x ** 2) + (lf_coord_y ** 2))

        # calcula nova proa de demanda
        f_atv.f_atv_pro_dem = cpd.calc_proa_demanda(lf_coord_x, lf_coord_y)

        # calcula novo sentido de curva
        scrv.sentido_curva(f_atv)

        # aeronave atingiu o fixo de espera ? (distância ao ponto <= passo da aeronave)
        if lf_dst_anv_pto <= math.sqrt((f_cine_data.f_delta_x ** 2) + (f_cine_data.f_delta_y ** 2)):
            # checa condição de cancelamento e ajusta a razão
            if __check_cancel_espera(f_atv, l_esp):
                # ajusta a razão de subida/descida
                f_atv.f_atv_raz_sub = f_atv.f_prf_raz_des_crz

                # break
                return

            # verifica se a função operacional anterior era aproximação
            # if ldefs.E_APROXIMACAO == f_atv.en_trf_fnc_opeAnt:
                # verifica se aeronave chegou na altitude do fixo de espera
                # if f_atv.f_trf_alt_atu == f_atv.f_atv_alt_dem:
                    # verifica se existe algo na pilha
                    # if 0 != f_cine_data.iCinPtr:
                        # f_cine_data.iCinPtr -= 1

                        # se existe, desempilha o contexto
                        # f_atv.f_atv_vel_dem = f_pAtr.fAtrPrfVelApx
                        # f_atv.f_atv_pro_dem = l_esp.f_esp_rumo

                        # calcula novo sentido de curva
                        # scrv.sentidoCurva(f_atv)

                        # f_atv.en_trf_fnc_ope = f_stk_context [ f_cine_data.iCinPtr ].eItmFncOpe
                        # f_atv.en_atv_fase    = f_stk_context [ f_cine_data.iCinPtr ].iItmFase
                        # f_atv.pAnvPtrBkp     = f_stk_context [ f_cine_data.iCinPtr ].pItmPtrBkp
                        # f_atv.ptr_trf_prc    = f_stk_context [ f_cine_data.iCinPtr ].pItmPtrPrc

                        # f_atv.f_atv_raz_sub = f_cine_data.f_raz_sub_des

                        # return  # break

            # aprumar no rumo da espera (sentido afastamento)
            f_atv.f_atv_pro_dem = f_cine_data.f_afasta

            # entrar na órbita
            f_atv.en_atv_fase = ldefs.E_FASE_CRVAFASTA

            f_cine_data.i_setor_ent = 0
            f_cine_data.i_bloqueio_fixo = 0

        # espera a direita ?
        if ldefs.E_DIREITA == l_esp.en_esp_sentido_curva:
            if (1 == f_cine_data.i_setor_ent) and (1 == f_cine_data.i_bloqueio_fixo):
                # ajusta a razão de curva
                f_atv.f_atv_raz_crv = -abs(f_atv.f_atv_raz_crv)

            else:
                # ajusta a razão de curva
                f_atv.f_atv_raz_crv = abs(f_atv.f_atv_raz_crv)

        # senão, espera a esquerda
        else:
            if (1 == f_cine_data.i_setor_ent) and (1 == f_cine_data.i_bloqueio_fixo):
                # ajusta a razão de curva
                f_atv.f_atv_raz_crv = abs(f_atv.f_atv_raz_crv)

            else:
                # ajusta a razão de curva
                f_atv.f_atv_raz_crv = -abs(f_atv.f_atv_raz_crv)

    # fase curva de afastamento ?
    elif ldefs.E_FASE_CRVAFASTA == f_atv.en_atv_fase:
        # já aprumou ?
        if f_atv.f_trf_pro_atu == f_atv.f_atv_pro_dem:
            # obtém o tempo (limite de 14000FT)
            f_cine_data.h_tempo = 90. if (f_atv.f_trf_alt_atu > M_14000FT) else 50.

            # sinaliza nova fase
            f_atv.en_atv_fase = ldefs.E_FASE_TEMPO

    # senão,...
    else:
        # logger
        l_log = logging.getLogger("prc_espera::prc_espera")
        l_log.setLevel(logging.ERROR)
        l_log.error("<E06: fase [{}/{}] da espera não identificada.".format(f_atv.en_atv_fase, ldefs.DCT_FASE[f_atv.en_atv_fase]))

    # logger
    # M_LOG.info("prc_espera:<<")
        
# < the end >--------------------------------------------------------------------------------------
