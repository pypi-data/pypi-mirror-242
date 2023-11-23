"""Functions used to convert between units and quantities."""
from typing import Union

import numpy as np


########################## Unit Conversions ##########################
def ab_mag_to_flux(AB_mag: Union[np.ndarray, float, int]) -> Union[np.ndarray, float, int]:
    """Convert AB magnitude to flux.
    Params:
        AB_mag: The AB magnitude.
    Returns:
        The fluxes values (Janskys).
    """
    return 10**((AB_mag - 8.9) / -2.5)


def flux_to_ab_mag(flux: Union[np.ndarray, float, int]) -> Union[np.ndarray, float, int]:
    """Convert flux to AB magnitude.
    Params:
        flux: Flux values (Janskys).
    Returns:
        AB mag values.
    """
    return -2.5 * np.log10(flux) + 8.9


########################## Error Propagation ########################## (source: https://en.wikipedia.org/wiki/Propagation_of_uncertainty)
def ab_magerr_to_ferr(sigma_m: Union[np.ndarray, float, int], fluxes: Union[np.ndarray, float, int]) -> Union[np.ndarray, float, int]:
    """Convert the error in magnitude to the error in flux.
    Params:
        sigma_m: The magnitude error.
        fluxes: The flux values.
    Returns
        The errors in flux error units.
    """
    return np.abs(fluxes * np.log(10) * (sigma_m / 2.5))


def err_to_logerr(Xerr: Union[np.ndarray, float, int], X: Union[np.ndarray, float, int]) -> Union[np.ndarray, float, int]:
    """Transformation on the error of a random variable transformed by f=ln(X)
    Params:
        Xerr: Errors in X.
        X: The X variable.
    Returns:
        The propagated error f=ln(X).
    """
    return np.abs(Xerr / (10**X * np.log(10)))
