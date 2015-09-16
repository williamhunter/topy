"""
# ==============================================================================
# Material constants and finite element dimensions.
#
# Author: William Hunter <willemjagter@gmail.com>
# Date: 01-06-2007
# Last change: 18-11-2008
# Copyright (C) 2008, William Hunter.
# ==============================================================================
"""

from __future__ import division

__all__ = ['_a', '_b', '_c', '_E', '_nu', '_G', '_g', '_k']

# ======================================
# === Element and material constants ===
# ======================================
# NOTE! Any changes you make here is only reflected in the elements once
# you've re-created them! There's a 'recreate_all.py' script that you can run.

_a, _b, _c = 0.5, 0.5, 0.5  # element dimensions (half-lengths) don't change!
_E  = 1  # modulus of elasticity
_nu = 1 / 3  # poisson's ratio
_G = _E / (2 * (1 + _nu))  # modulus of rigidity
_g = _E /  ((1 + _nu) * (1 - 2 * _nu))
_k = 1  # thermal conductivity of steel = 50 (ref. Mills)

# EOF matlcons.py
