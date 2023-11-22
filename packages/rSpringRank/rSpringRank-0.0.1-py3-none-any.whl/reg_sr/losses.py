#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Regularized-SpringRank -- regularized methods for efficient ranking in networks
#
# Copyright (C) 2023 Tzu-Chi Yen <tzuchi.yen@colorado.edu>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from numpy.linalg import norm
import cvxpy as cp
from numba import njit
from reg_sr.utils import (
    compute_cache_from_data,
    cast2sum_squares_form,
    compute_cache_from_data_t,
)


class Loss:
    """ """

    def __init__(self):
        pass

    def evaluate(self, theta):
        raise NotImplementedError(
            "This method is not implemented for the parent class."
        )

    def setup(self, data, K):
        """This function has any important setup required for the problem."""
        raise NotImplementedError(
            "This method is not implemented for the parent class."
        )

    def prox(self, t, nu, data, warm_start, pool):
        raise NotImplementedError(
            "This method is not implemented for the parent class."
        )

    def anll(self, data, G):
        return -np.mean(self.logprob(data, G))


class huber_loss(Loss):
    """
    TODO
    """

    def __init__(self):
        self.B = None
        self.b = None
        self.M = 0

    def evaluate_cvx(self, theta):
        return 0.5 * cp.sum(cp.huber(self.B @ theta - self.b, self.M))

    def setup(self, data, alpha, M, incl_reg):
        self.M = M
        self.B, self.b = cast2sum_squares_form(
            data, alpha=alpha, regularization=incl_reg
        )


class sum_squared_loss(Loss):
    """
    f(s) = || B @ s - b ||_2^2
    """

    def __init__(self):
        super().__init__()
        self.B = None
        self.b = None
        self.ell = None
        self.Bt_B_inv = None

    def evaluate(self, theta):
        return 0.5 * norm(self.B @ theta - self.b) ** 2

    def evaluate_cvx(self, theta):
        return 0.5 * cp.norm(self.B @ theta - self.b) ** 2

    def setup(self, data, alpha):
        # data is graph_tool.Graph()
        cache = compute_cache_from_data(data, alpha=alpha)
        self.B = cache["B"]
        self.b = cache["b"]
        self.ell = cache["ell"]
        self.Bt_B_inv = cache["Bt_B_inv"]

    def prox(self, theta):
        raise NotImplementedError(
            "This class is for the primal problem, and is only intended for CVXPY to solve."
        )

    def dual2primal(self, v):
        raise NotImplementedError(
            "This class is for the primal problem, and is only intended for CVXPY to solve."
        )

    def predict(self):
        pass

    def scores(self):
        pass

    def logprob(self):
        pass


class sum_squared_loss_conj(Loss):
    """
    Conjugate of ...
    f(s) = || B @ s - b ||_2^2
    """

    def __init__(self):
        super().__init__()
        self.B = None
        self.b = None
        self.ell = None
        self.Bt_B_inv = None
        self.Bt_B_invSqrt = None

        # derived ones
        self.Bt_B_invSqrt_Btb = None
        self.Bt_B_invSqrt_ellt = None
        self.ell_BtB_inv_Bt_b = None
        self.ell_BtB_inb_ellt = None
        self.term_2 = None

    def find_Lipschitz_constant(self):
        # TODO: do power method
        # f = lambda x: self.Bt_B_invSqrt @ (self.ell.T @ x)
        
        L = norm(self.Bt_B_invSqrt_ellt, ord=2) ** 2
        return L

    def evaluate(self, theta):
        f = lambda x: -self.Bt_B_invSqrt @ (self.ell.T @ x)
        term_1 = (
            0.5
            * norm(f(theta) + self.Bt_B_invSqrt_Btb) ** 2
        )
        return term_1 + self.term_2

    def evaluate_cvx(self, theta):
        term_1 = (
            0.5
            * cp.norm(self.Bt_B_invSqrt @ (-self.ell.T @ theta + self.B.T @ self.b))
            ** 2
        )
        term_2 = -0.5 * cp.norm(self.b.todense()) ** 2
        return term_1 + term_2

    def setup(self, data, alpha, **kwargs):
        method = kwargs.get("method", "annotated")
        if method == "annotated":
            cache = compute_cache_from_data(data, alpha=alpha)
        elif method == "time::l1":
            lambd = kwargs.get("lambd", 1)
            from_year = kwargs.get("from_year", 1960)
            to_year = kwargs.get("to_year", 2001)
            top_n = kwargs.get("top_n", 70)
            cache = compute_cache_from_data_t(
                data,
                alpha=1,
                lambd=lambd,
                from_year=from_year,
                to_year=to_year,
                top_n=top_n,
            )
        elif method == "time::l2":
            raise NotImplementedError("We do not use first-order solver for this case.")
        else:
            raise NotImplementedError("Method not implemented.")
    
        self.B = cache["B"]  # sparse
        self.b = cache["b"]  # sparse
        self.ell = cache["ell"]  # sparse
        self.Bt_B_inv = cache["Bt_B_inv"]  # dense
        self.Bt_B_invSqrt = cache["Bt_B_invSqrt"]  # dense

        # derived ones
        self.Bt_B_invSqrt_Btb = self.Bt_B_invSqrt @ self.B.T @ self.b
        self.Bt_B_invSqrt_ellt = self.Bt_B_invSqrt @ self.ell.T
        self.ell_BtB_inv_Bt_b = self.ell @ self.Bt_B_inv @ self.B.T @ self.b  # sparse
        self.ell_BtB_inb_ellt = self.ell @ self.Bt_B_inv @ -self.ell.T  # sparse
        self.ell_BtB_inv_Bt_b = np.array(self.ell_BtB_inv_Bt_b.todense(), dtype=np.float64)
        self.ell_BtB_inb_ellt = np.array(self.ell_BtB_inb_ellt.todense(), dtype=np.float64)


        self.term_2 = -0.5 * norm(self.b.todense()) ** 2
    
    def prox(self, theta):
        return - self.ell_BtB_inb_ellt @ theta - self.ell_BtB_inv_Bt_b

    def dual2primal(self, v):
        d = self.Bt_B_inv @ (-self.ell.T @ v + self.B.T @ self.b)
        return np.array(np.squeeze(d)).reshape(-1, 1)
    
    def predict(self):
        pass

    def scores(self):
        pass

    def logprob(self):
        pass
