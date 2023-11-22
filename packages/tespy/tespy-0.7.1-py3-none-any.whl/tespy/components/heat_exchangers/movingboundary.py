# -*- coding: utf-8

"""Module of class HeatExchanger.


This file is part of project TESPy (github.com/oemof/tespy). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location
tespy/components/heat_exchangers/base.py

SPDX-License-Identifier: MIT
"""
import numpy as np

from tespy.components.heat_exchangers.base import HeatExchanger
from tespy.tools.data_containers import ComponentCharacteristics as dc_cc
from tespy.tools.data_containers import ComponentProperties as dc_cp
from tespy.tools.data_containers import GroupedComponentCharacteristics as dc_gcc
from tespy.tools.document_models import generate_latex_eq
from tespy.tools.fluid_properties import h_mix_pQ
from tespy.tools.fluid_properties import T_mix_ph


class MovingBoundaryHeatExchanger(HeatExchanger):

    def kA_func(self, **kwargs):
        Q_total = self.inl[0].m.val_SI * (self.outl[0].h.val_SI - self.inl[0].h.val_SI)
        h_sat = h_mix_pQ(self.outl[0].p.val_SI, 1, self.outl[0].fluid_data)
        if self.outl[0].h.val_SI < h_sat:
            Q_desup = self.inl[0].m.val_SI * (h_sat - self.inl[0].h.val_SI)
            Q_cond = self.inl[0].m.val_SI * (self.outl[0].h.val_SI - h_sat)
            T_desup_i1 = self.inl[0].calc_T()
            T_desup_o1 =  self.outl[0].calc_T_sat()
            T_cond_i1 = T_desup_o1
            T_cond_o1 = T_desup_i1

            T_cond_i2 = self.inl[1].calc_T()
            h_cond_o2 = self.inl[1].h.val_SI + abs(Q_cond) / self.inl[1].m.val_SI
            T_cond_o2 = T_mix_ph(self.inl[1].p.val_SI, h_cond_o2, self.inl[1].fluid_data)
            T_desup_i2 = T_cond_o2
            T_desup_o2 = self.outl[1].calc_T()
            # print(T_cond_i2, T_cond_o2, T_desup_o2)

            ttd_desup_u = T_desup_i1 - T_desup_o2
            ttd_desup_l = T_desup_o1 - T_desup_i2

            ttd_cond_u = T_cond_i1 - T_cond_o2
            ttd_cond_l = T_cond_o1 - T_cond_i2

            td_log_desup = (ttd_desup_l - ttd_desup_u) / np.log(ttd_desup_l / ttd_desup_u)
            td_log_cond = (ttd_cond_l - ttd_cond_u) / np.log(ttd_cond_l / ttd_cond_u)

            u_desup = 4000
            u_cond = 16000
            residual = Q_total + self.A * (Q_desup / Q_total) * u_desup * td_log_desup + self.A * (Q_cond / Q_total) * u_cond * td_log_cond
            # print(Q_desup / Q_total)
            # print(Q_total)
            # print(self.A * (Q_desup / Q_total) * u_desup * td_log_desup)
            # print(self.A * (Q_cond / Q_total) * u_cond * td_log_cond)
            # print(self.outl[0].h.val_SI)
            print("two-phase-func")
        else:
            residual = Q_total + self.kA.val * self.calculate_td_log()
        return residual

    def kA_deriv(self, increment_filter, k):
        r"""
        Partial derivatives of heat transfer coefficient function.

        Parameters
        ----------
        increment_filter : ndarray
            Matrix for filtering non-changing variables.

        k : int
            Position of derivatives in Jacobian matrix (k-th equation).
        """
        f = self.kA_func
        for c in self.inl + self.outl:
            if self.is_variable(c.m):
                self.jacobian[k, c.m.J_col] = self.numeric_deriv(f, "m", c)
            if self.is_variable(c.p):
                self.jacobian[k, c.p.J_col] = self.numeric_deriv(f, 'p', c)
            if self.is_variable(c.h):
                self.jacobian[k, c.h.J_col] = self.numeric_deriv(f, 'h', c, d=1e-5)