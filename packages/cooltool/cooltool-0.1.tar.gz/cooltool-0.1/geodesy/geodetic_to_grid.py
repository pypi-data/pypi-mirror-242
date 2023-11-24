import numpy as np
from .utils import (
    degr_min_sec_to_decimal_degr,
    degr_to_radians,
    get_ellipsoidal_parameters,
    get_transverse_mercator_parameters,
    from_ellipsoidal_parameters,
    check_float,
)


def geodetic_to_grid(phi, lam, ellipsoid: str, projection: str) -> tuple[float, float]:
    """Perform Gauss-Kruger transformation from geodetic latitude and longitude
    into grid coordiantes x and y.

    Args:
        phi (tuple): geodetic latitude in degrees, minutes and seconds, positive north
        lam (tuple): geodetic longitude in degrees, minutes and seconds, positive east
        ellips (str): ellipsiod, e.g. 'GRS1980'
        projection (str): projection, e.g. 'SWEREF99TM'

    Returns:
        tuple[float, float]: grid x, grid y
    """

    if len(phi) == 3 and len(lam) == 3:
        phi = degr_min_sec_to_decimal_degr(phi)
        lam = degr_min_sec_to_decimal_degr(lam)

    phi = check_float(phi)
    lam = check_float(lam)

    # Angles need to be expressed as radians
    phi = degr_to_radians(phi)
    lam = degr_to_radians(lam)

    a, f = get_ellipsoidal_parameters(ellipsoid)
    e, n, a_hat = from_ellipsoidal_parameters(a, f)
    lam0, k0, FN, FE = get_transverse_mercator_parameters(projection)

    A = e**2
    B = (1 / 6) * (5 * e**4 - e**6)
    C = (1 / 120) * (104 * e**6 - 45 * e**8)
    D = (1 / 1260) * (1237 * e**8)

    sin_2 = np.power(np.sin(phi), 2)
    sin_4 = np.power(np.sin(phi), 4)
    sin_6 = np.power(np.sin(phi), 6)
    phi_star = phi - np.sin(phi) * np.cos(phi) * (A + B * sin_2 + C * sin_4 + D * sin_6)

    delta_lambda = lam - lam0
    epislon = np.arctan(np.tan(phi_star) / np.cos(delta_lambda))
    new = np.arctanh(np.cos(phi_star) * np.sin(delta_lambda))

    b1 = (1 / 2) * n - (2 / 3) * n**2 + (5 / 16) * n**3 + (41 / 180) * n**4
    b2 = (13 / 48) * n**2 - (3 / 5) * n**3 + (557 / 1440) * n**4
    b3 = (61 / 240) * n**3 - (103 / 140) * n**4
    b4 = (49561 / 161280) * n**4

    x = (
        k0
        * a_hat
        * (
            epislon
            + b1 * np.sin(2 * epislon) * np.cosh(2 * new)
            + b2 * np.sin(4 * epislon) * np.cosh(4 * new)
            + b3 * np.sin(6 * epislon) * np.cosh(6 * new)
            + b4 * np.sin(8 * epislon) * np.cosh(8 * new)
        )
        + FN
    )

    y = (
        k0
        * a_hat
        * (
            new
            + b1 * np.cos(2 * epislon) * np.sinh(2 * new)
            + b2 * np.cos(4 * epislon) * np.sinh(4 * new)
            + b3 * np.cos(6 * epislon) * np.sinh(6 * new)
            + b4 * np.cos(8 * epislon) * np.sinh(8 * new)
        )
        + FE
    )

    x = np.round(x, 3)
    y = np.round(y, 3)

    return x, y
