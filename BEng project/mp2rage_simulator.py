"""
MP2RAGE signal simulator for quantitative MRI at 7T.

This class implements the MP2RAGE signal equations to simulate INV1, INV2.
"""

import numpy as np


class MP2RAGESimulator:
    """Simulates MP2RAGE signals and generates quantitative maps."""

    def __init__(self, protocol):
        """Initialize MP2RAGE simulator with sequence parameters.

        Args:
            protocol: a dictionary containing MP2RAGE sequence parameters
        """
        # Sequence parameters
        self.TR_MP2RAGE = protocol['TR_MP2RAGE']
        self.TI1 = protocol['TI1']
        self.TI2 = protocol['TI2']
        self.alpha1 = protocol['alpha1']
        self.alpha2 = protocol['alpha2']
        self.TR_GRE = protocol['TR_GRE']
        self.n = protocol['n']
        self.TE = protocol['TE']

        # Assumed eff as in paper
        self.eff = 1

        # Derived timing
        # TA and TB are from their respective inversions to the start of the
        # GRE block while TI1 and TI2 are till the center of GRE blocks.
        self.TA = self.TI1 - (self.n * self.TR_GRE) / 2
        self.TB = self.TI2 - self.TI1 - (self.n * self.TR_GRE)
        self.TC = self.TR_MP2RAGE - (self.TI2 + (self.n * self.TR_GRE) / 2)

        print(f"MP2RAGE Simulator initialized:")
        print(
            f"  GRE blocks: {self.n} excitations × {self.TR_GRE}ms = "
            f"{self.n * self.TR_GRE}ms each")
        print(
            f"  Timing: TA={self.TA:.0f}ms, TB={self.TB:.0f}ms, "
            f"TC={self.TC:.0f}ms")

    def deg2rad(self, angle_deg):
        """Convert degrees to radians as numpy expects radians"""
        return np.deg2rad(angle_deg)

    def longitudinal_mag(self, T1, PD):
        """Calculate steady-state longitudinal magnetization (Equation 1)."""
        # Convert flip angles to radians
        alpha1_rad = self.deg2rad(self.alpha1)
        alpha2_rad = self.deg2rad(self.alpha2)

        # Exponential terms
        EA = np.exp(-self.TA / T1)
        EB = np.exp(-self.TB / T1)
        EC = np.exp(-self.TC / T1)
        E1 = np.exp(-self.TR_GRE / T1)

        # Magnetization evolution through first GRE block
        cos_alpha1_E1 = np.cos(alpha1_rad) * E1
        cos_alpha2_E1 = np.cos(alpha2_rad) * E1
        # numerator
        numerator = (((((((1 - EA) * (cos_alpha1_E1) ** self.n) + (1 - E1)
                         * ((1 - (cos_alpha1_E1) ** self.n) / (
                        1 - cos_alpha1_E1))) * EB + (
                                    1 - EB)) * cos_alpha2_E1 **
                       self.n + (1 - E1)
                       * ((1 - (cos_alpha2_E1) ** self.n) / (
                        1 - cos_alpha2_E1))))) * PD * EC + ((1 - EC) * PD)

        # Denominator
        denominator = 1 + self.eff * (np.cos(alpha1_rad) * np.cos(
            alpha2_rad)) ** self.n * np.exp(-self.TR_MP2RAGE / T1)

        m_zss = numerator / denominator
        return m_zss, EA, EB, EC, E1, cos_alpha1_E1, cos_alpha2_E1

    def calculate_signals(self, T1, PD, T2star=30, B1minus=1):
        """Calculate INV1 and INV2 signals for given tissue parameters.
        Default T2star=30 (typical for WM/GM at 7T).
        B1minus=1 assumes ideal receiver field.
        """
        m_zss, EA, EB, EC, E1, cos_alpha1_E1, cos_alpha2_E1 = self.longitudinal_mag(
            T1, PD)
        alpha1_rad = self.deg2rad(self.alpha1)
        alpha2_rad = self.deg2rad(self.alpha2)
        decay = np.exp(-self.TE / T2star)

        # Equation 2 from paper
        INV1 = PD * B1minus * decay * np.sin(alpha1_rad) * (
                (-self.eff * (m_zss / PD) * EA + (1 - EA)) * (
            cos_alpha1_E1) ** (self.n / 3)
                + (1 - E1)
                * (1 - (cos_alpha1_E1) ** (self.n / 3))
                / (1 - np.cos(alpha1_rad) * E1)
        )
        # Equation 3 from paper
        INV2 = PD * B1minus * decay * np.sin(alpha2_rad) * (
                ((m_zss / PD) - (1 - EC)) / EC * (cos_alpha2_E1) ** (
                2 * self.n / 3)
                - (1 - E1)
                * ((cos_alpha2_E1) ** (-2 * self.n / 3 - 1))
                / (1 - np.cos(alpha2_rad) * E1)
        )

        return INV1, INV2
