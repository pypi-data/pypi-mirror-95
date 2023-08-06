# pylint: disable=C0103
from typing import Optional, Union
from dataclasses import dataclass
import numpy as np

from pyrealm.params import PARAM

# TODO - Note that the typing currently does not enforce the dtype of ndarrays
#        but it looks like the upcoming np.typing module might do this.


def check_input_shapes(*args):
    """This helper function validates inputs to check that they are either
    scalars or arrays and then that any arrays of the same shape. It either
    raises an error or returns the common shape or 1 if all arguments are
    scalar.

    Parameters:

        *args: A set of numpy arrays or scalar values

    Returns:

        The common shape of any array inputs or 1 if all inputs are scalar.

    Examples:

        >>> check_input_shapes(np.array([1,2,3]), 5)
        (3,)
        >>> check_input_shapes(4, 5)
        1
        >>> check_input_shapes(np.array([1,2,3]), np.array([1,2]))
        Traceback (most recent call last):
        ...
        ValueError: Inputs contain arrays of different shapes.
    """

    # Collect the shapes of the inputs
    shapes = set()

    for val in args:
        if isinstance(val, np.ndarray):
            shapes.add(val.shape)
        elif val is None or isinstance(val, (float, int)):
            pass  # No need to track scalars and optional values pass None
        else:
            raise ValueError(f'Unexpected input to check_input_shapes: {type(val)}')

    # shapes can be an empty set (all scalars) or contain one common shape
    # otherwise raise an error
    if len(shapes) > 1:
        raise ValueError('Inputs contain arrays of different shapes.')

    if len(shapes) == 1:
        return shapes.pop()

    return 1


def calc_density_h2o(tc: Union[float, np.ndarray],
                     patm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Calculates the **density of water** as a function of temperature and
    atmospheric pressure, using the Tumlirz Equation and coefficients calculated
    by :cite:`Fisher:1975tm`.

    Parameters:

        tc: air temperature, °C
        patm: atmospheric pressure, Pa

    Other Parameters:

        lambda_: polynomial coefficients of Tumlirz equation (`PARAM.FisherDial.lambda_`).
        Po: polynomial coefficients of Tumlirz equation (`PARAM.FisherDial.Po`).
        Vinf: polynomial coefficients of Tumlirz equation (`PARAM.FisherDial.Vinf`).

    Returns:

        Water density as a float in (g cm^-3)

    Examples:

        >>> round(calc_density_h2o(20, 101325), 4)
        998.2056
    """

    # check inputs, shape not used
    _ = check_input_shapes(tc, patm)

    # Get powers of tc, including tc^0 = 1 for constant terms
    tc_pow = np.power.outer(tc, np.arange(0, 10))

    # Calculate lambda, (bar cm^3)/g:
    lambda_val = np.sum(np.array(PARAM.FisherDial.lambda_) * tc_pow[..., :5], axis=-1)

    # Calculate po, bar
    po_val = np.sum(np.array(PARAM.FisherDial.Po) * tc_pow[..., :5], axis=-1)

    # Calculate vinf, cm^3/g
    vinf_val = np.sum(np.array(PARAM.FisherDial.Vinf) * tc_pow, axis=-1)

    # Convert pressure to bars (1 bar <- 100000 Pa)
    pbar = 1e-5 * patm

    # Calculate the specific volume (cm^3 g^-1):
    spec_vol = vinf_val + lambda_val / (po_val + pbar)

    # Convert to density (g cm^-3) -> 1000 g/kg; 1000000 cm^3/m^3 -> kg/m^3:
    rho = 1e3 / spec_vol

    return rho


def calc_ftemp_arrh(tk: Union[float, np.ndarray],
                    ha: float) -> Union[float, np.ndarray]:
    r"""Calculates the temperature-scaling factor :math:`f` for enzyme kinetics
    following an Arrhenius response for a given temperature (``tk``, :math:`T`)
    and activation energy (`ha`, :math:`H_a`).

    Arrhenius kinetics are described as:

    .. math::

        x(T)= exp(c - H_a / (T R))

    The temperature-correction function :math:`f(T, H_a)` is:

      .. math::
        :nowrap:

        \[
            \begin{align*}
                f &= \frac{x(T)}{x(T_0)} \\
                  &= exp \left( \frac{ H_a (T - T_0)}{T_0 R T}\right)\text{, or equivalently}\\
                  &= exp \left( \frac{ H_a}{R} \cdot \left(\frac{1}{T_0} - \frac{1}{T}\right)\right)
            \end{align*}
        \]

    Parameters:

        tk: Temperature (in Kelvin)
        ha: Activation energy (in :math:`J \text{mol}^{-1}`)

    Other Parameters:

        To: a standard reference temperature (:math:`T_0`, `PARAM.k.To`)
        R: the universal gas constant (:math:`R`, `PARAM.k.R`)

    Returns:

        A float value for :math:`f`

    Examples:

        >>> # Relative rate change from 25 to 10 degrees Celsius (percent change)
        >>> round((1.0-calc_ftemp_arrh( 283.15, 100000)) * 100, 4)
        88.1991
    """

    # Note that the following forms are equivalent:
    # exp( ha * (tk - 298.15) / (298.15 * kR * tk) )
    # exp( ha * (tc - 25.0)/(298.15 * kR * (tc + 273.15)) )
    # exp( (ha/kR) * (1/298.15 - 1/tk) )

    tkref = PARAM.k.To + PARAM.k.CtoK

    return np.exp(ha * (tk - tkref) / (tkref * PARAM.k.R * tk))


def calc_ftemp_inst_rd(tc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Calculates the **temperature-scaling factor for dark respiration**
    at a given temperature (``tc``, :math:`T` in °C), relative to the standard
    reference temperature :math:`T_o` (:cite:`Heskel:2016fg`).

    .. math::

            fr = exp( b (T_o - T) -  c ( T_o^2 - T^2 ))

    Parameters:

        tc: Temperature (degrees Celsius)

    Other parameters:

        To: standard reference temperature (:math:`T_o`, `PARAM.k.To`)
        b: empirically derived global mean coefficient (:math:`b`, Table 1, ::cite:`Heskel:2016fg`)
        c: empirically derived global mean coefficient (:math:`c`, Table 1, ::cite:`Heskel:2016fg`)


    Returns:

        A float value for :math:`fr`

    Examples:

        >>> # Relative percentage instantaneous change in Rd going from 10 to 25 degrees
        >>> val = (calc_ftemp_inst_rd(25) / calc_ftemp_inst_rd(10) - 1) * 100
        >>> round(val, 4)
        250.9593
    """

    return np.exp(PARAM.Heskel.b * (tc - PARAM.k.To) -
                  PARAM.Heskel.c * (tc ** 2 - PARAM.k.To ** 2))


def calc_ftemp_inst_vcmax(tc: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    r"""This function calculates the **temperature-scaling factor :math:`f` of
    the instantaneous temperature response of :math:`V_{cmax}`** given the
    temperature (:math:`T`) relative to the standard reference temperature
    (:math:`T_0`), following modified Arrhenius kinetics.

    .. math::

       V = f V_{ref}

    The value of :math:`f` is given by :cite:`Kattge:2007db` (Eqn 1) as:

    .. math::

        f = g(T, H_a) \cdot
                \frac{1 + exp( (T_0 \Delta S - H_d) / (T_0 R))}
                     {1 + exp( (T \Delta S - H_d) / (T R))}

    where :math:`g(T, H_a)` is a regular Arrhenius-type temperature response
    function (see :func:`calc_ftemp_arrh`). The term :math:`\Delta S` is the
    entropy factor, calculated as a linear function of :math:`T` in °C following
    :cite:`Kattge:2007db` (Table 3, Eqn 4):

    .. math::

        \Delta S = a + b T

    Parameters:

        tc:  temperature, or in general the temperature relevant for
            photosynthesis (°C)

    Other parameters:

        Ha: activation energy (:math:`H_a`, `PARAM.KattgeKnorr.Ha`)
        Hd: deactivation energy (:math:`H_d`, `PARAM.KattgeKnorr.Hd`)
        To: standard reference temperature expressed in Kelvin (`T_0`, `PARAM.k.To`)
        R: the universal gas constant (:math:`R`,`PARAM.k.R`)
        a: intercept of the entropy factor(:math:`a`, `PARAM.KattgeKnorr.a_ent`)
        b: slope of the entropy factor (:math:`b`, `PARAM.KattgeKnorr.b_ent`)

    Returns: A float value for :math:`f`

    Examples:

        >>> # Relative change in Vcmax going (instantaneously, i.e. not
        >>> # not acclimatedly) from 10 to 25 degrees (percent change):
        >>> val = ((calc_ftemp_inst_vcmax(25)/calc_ftemp_inst_vcmax(10)-1) * 100)
        >>> round(val, 4)
        283.1775

    """

    # Convert temperatures to Kelvin
    tkref = PARAM.k.To + PARAM.k.CtoK
    tk = tc + PARAM.k.CtoK

    # Calculate entropy following Kattge & Knorr (2007): slope and intercept
    # are defined using temperature in °C, not K!!! 'tcgrowth' corresponds
    # to 'tmean' in Nicks, 'tc25' is 'to' in Nick's
    dent = PARAM.KattgeKnorr.a_ent + PARAM.KattgeKnorr.b_ent * tc
    fva = calc_ftemp_arrh(tk, PARAM.KattgeKnorr.Ha)
    fvb = ((1 + np.exp((tkref * dent - PARAM.KattgeKnorr.Hd) /
                       (PARAM.k.R * tkref))) /
           (1 + np.exp((tk * dent - PARAM.KattgeKnorr.Hd) /
                       (PARAM.k.R * tk))))

    return fva * fvb


def calc_ftemp_kphio(tc: Union[float, np.ndarray],
                     c4: bool = False) -> Union[float, np.ndarray]:
    r"""Calculates the **temperature dependence of the quantum yield
    efficiency**, as a quadratic function of temperature (:math:`T`). The values
    of the coefficients depend on whether C3 or C4 photosynthesis is being
    modelled

    .. math::

        \phi(T) = a + b T - c T^2

    The factor :math:`\phi(T)` is to be multiplied with leaf absorptance and the
    fraction of absorbed light that reaches photosystem II. In the P-model these
    additional factors are lumped into a single apparent quantum yield
    efficiency parameter (argument `kphio` to the class :class:`~pyrealm.pmodel.PModel`).

    Parameters:

        tc: Temperature, relevant for photosynthesis (°C)
        c4: Boolean specifying whether fitted temperature response for C4 plants
            is used. Defaults to \code{FALSE}.

    Other parameters:

        C3: the parameters (:math:`a,b,c`, `PARAM.kphio.C3`) are taken from the
            temperature dependence of the maximum quantum yield of photosystem
            II in light-adapted tobacco leaves determined by :cite:`Bernacchi:2003dc`.
        C4: the parameters (:math:`a,b,c`, `PARAM.kphio.C4`) are taken from unpublished
            work.

    Returns:

        A float value for :math:`\phi(T)`

    Examples:

        >>> # Relative change in the quantum yield efficiency between 5 and 25
        >>> # degrees celsius (percent change):
        >>> val = (calc_ftemp_kphio(25.0) / calc_ftemp_kphio(5.0) - 1) * 100
        >>> round(val, 5)
        52.03969
        >>> # Relative change in the quantum yield efficiency between 5 and 25
        >>> # degrees celsius (percent change) for a C4 plant:
        >>> val = (calc_ftemp_kphio(25.0, c4=True) /
        ...        calc_ftemp_kphio(5.0, c4=True) - 1) * 100
        >>> round(val, 5)
        432.25806

    """

    if c4:
        coef = PARAM.kphio.C4
    else:
        coef = PARAM.kphio.C3

    ftemp = coef[0] + coef[1] * tc + coef[2] * tc ** 2
    ftemp = np.clip(ftemp, 0.0, None)
    
    return ftemp


def calc_gammastar(tc: Union[float, np.ndarray],
                   patm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    r"""Calculates the photorespiratory **CO2 compensation point** in absence of
    dark respiration (:math:`\Gamma^{*}`, ::cite:`Farquhar:1980ft`) as:

    .. math::

        \Gamma^{*} = \Gamma^{*}_{0} \cdot \frac{p}{p_0} \cdot f(T, H_a)

    where :math:`f(T, H_a)` modifies the activation energy to the the local
    temperature following an Arrhenius-type temperature response function
    implemented in :func:`calc_ftemp_arrh`.

    Parameters:

        tc: Temperature relevant for photosynthesis (:math:`T`, °C)
        patm: Atmospheric pressure (:math:`p`, Pascals)

    Other Parameters:

        To: the standard reference temperature (:math:`T_0` )
        Po: the standard pressure (:math:`p_0` )
        gs_0: the reference value of :math:`\Gamma^{*} at standard temperature
            (:math:`T_0`) and pressure (:math:`P_0`)  (:math:`\Gamma^{*}_{0}`,
            ::cite:`Bernacchi:2001kg`, `PARAM.Bernacchi.gs25_0`)
        ha: the activation energy (:math:`\Delta H_a`, ::cite:`Bernacchi:2001kg`,
            `PARAM.Bernacchi.dha`)

    Returns:

        A float value for :math:`\Gamma^{*}` (in Pa)

    Examples:

        >>> # CO2 compensation point at 20 degrees Celsius and standard
        >>> # atmosphere (in Pa) >>> round(calc_gammastar(20, 101325), 5)
        3.33925
    """

    # check inputs, return shape not used
    _ = check_input_shapes(tc, patm)

    return (PARAM.Bernacchi.gs25_0 * patm / PARAM.k.Po *
            calc_ftemp_arrh((tc + PARAM.k.CtoK), ha=PARAM.Bernacchi.dha))


def calc_ns_star(tc: Union[float, np.ndarray],
                 patm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:

    r"""Calculates the relative viscosity of water (:math:`\eta^*`), given the
    standard temperature and pressure, using :func:`~pyrealm.pmodel.calc_viscosity_h20`
    (:math:`v(t,p)`) as:

    .. math::

        \eta^* = \frac{v(t,p)}{v(t_0,p_0)}

    Parameters:

        tc: Temperature, relevant for photosynthesis (:math:`T`, °C)
        patm: Atmospheric pressure (:math:`p`, Pa)

    Other parameters:

        To: standard temperature (:math:`t0`, `PARAM.k.To`)
        Po: standard pressure (:math:`p_0`, `PARAM.k.Po`)

    Returns:

        A numeric value for :math:`K` (in Pa)

    Examples:

        >>> # Realative viscosity at 20 degrees Celsius and standard
        >>> # atmosphere (in Pa):
        >>> round(calc_ns_star(20, 101325), 5)
        1.12536
    """

    visc_env = calc_viscosity_h2o(tc, patm)
    visc_std = calc_viscosity_h2o(PARAM.k.To, PARAM.k.Po)

    return visc_env / visc_std


def calc_kmm(tc: Union[float, np.ndarray],
             patm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    r"""Calculates the **Michaelis Menten coefficient of Rubisco-limited
    assimilation** (:math:`K`, ::cite:`Farquhar:1980ft`) as a function of
    temperature (:math:`T`) and atmospheric pressure (:math:`p`) as:

      .. math:: K = K_c ( 1 + p_{\ce{O2}} / K_o),

    where, :math:`p_{\ce{O2}} = 0.209476 \cdot p` is the partial pressure of
    oxygen. :math:`f(T, H_a)` is an Arrhenius-type temperature response of
    activation energies (:func:`calc_ftemp_arrh`) used to correct
    Michalis constants at standard temperature for both :math:`\ce{CO2}` and
    :math:`\ce{O2}` to the local temperature (Table 1, ::cite:`Bernacchi:2001kg`):

      .. math::
        :nowrap:

        \[
            \begin{align*}
                K_c &= K_{c25} \cdot f(T, H_{kc})\\
                K_o &= K_{o25} \cdot f(T, H_{ko})
            \end{align*}
        \]

    .. TODO - why this height? Inconsistent with calc_gammastar which uses P_0
              for the same conversion for a value in the same table.

    Parameters:

        tc: Temperature, relevant for photosynthesis (:math:`T`, °C)
        patm: Atmospheric pressure (:math:`p`, Pa)

    Other parameters:

        hac: activation energy for :math:`\ce{CO2}` (:math:`H_{kc}`, `PARAM.Bernacchi.dhac`)
        hao:  activation energy for :math:`\ce{O2}` (:math:`\Delta H_{ko}`, `PARAM.Bernacchi.dhao`)
        kc25: Michelis constant for :math:`\ce{CO2}` at standard temperature
            (:math:`K_{c25}`, `PARAM.Bernacchi.kc25`)
        ko25: Michelis constant for :math:`\ce{O2}` at standard temperature
            (:math:`K_{o25}`, `PARAM.Bernacchi.ko25`)

    Returns:

        A numeric value for :math:`K` (in Pa)

    Examples:

        >>> # Michaelis-Menten coefficient at 20 degrees Celsius and standard
        >>> # atmosphere (in Pa):
        >>> round(calc_kmm(20, 101325), 5)
        46.09928

    """

    # Check inputs, return shape not used
    _ = check_input_shapes(tc, patm)

    # conversion to Kelvin
    tk = tc + PARAM.k.CtoK

    kc = PARAM.Bernacchi.kc25 * calc_ftemp_arrh(tk, ha=PARAM.Bernacchi.dhac)
    ko = PARAM.Bernacchi.ko25 * calc_ftemp_arrh(tk, ha=PARAM.Bernacchi.dhao)

    # O2 partial pressure
    po = PARAM.k.co * 1e-6 * patm

    return kc * (1.0 + po/ko)


def calc_soilmstress(soilm: Union[float, np.ndarray],
                     meanalpha: Union[float, np.ndarray] = 1.0) -> Union[float, np.ndarray]:
    r"""Calculates an **empirical soil moisture stress factor**  (:math:`\beta`,
    ::cite:`Stocker:2020dh`) as a function of relative soil moisture
    (:math:`m_s`, fraction of field capacity) and average aridity, quantified by
    the local annual mean ratio of actual over potential evapotranspiration
    (:math:`\bar{\alpha}`).

    The value of :math:`\beta` is defined relative to two soil moisture
    thresholds (:math:`\theta_0, \theta^{*}`) as:

      .. math::
        :nowrap:

        \[
            \beta =
                \begin{cases}
                    q(\theta_0 - \theta^{*})^2 + 1,  & \theta_0 < m_s <= \theta^{*} \\
                    1, &  \theta^{*} < m_s,
                \end{cases}
        \]

    where :math:`q` is an aridity sensitivity parameter setting the stress
    factor at :math:`\theta_0`:

    .. math:: q=(1 - (a + b \bar{\alpha}))/(\theta^{*} - \theta_{0})^2

    Default parameters are as described in :cite:`Stocker:2020dh`.

    Parameters:

        soilm: Relative soil moisture as a fraction of field capacity
            (unitless). Defaults to 1.0 (no soil moisture stress).
        meanalpha: Local annual mean ratio of actual over potential
            evapotranspiration, measure for average aridity. Defaults to 1.0.

    Other parameters:

        theta0: lower bound of soil moisture (:math:`\theta_0`, `PARAM.soilmstress.theta0`).
        thetastar: upper bound of soil moisture (:math:`\theta^{*}`, `PARAM.soilmstress.thetastar`).
        a: aridity parameter (:math:`a`, `PARAM.soilmstress.a`).
        b: aridity parameter (:math:`b`, `PARAM.soilmstress.b`).

    Returns:

        A numeric value for :math:`\beta`

    Examples:

        >>> # Relative reduction (%) in GPP due to soil moisture stress at
        >>> # relative soil water content ('soilm') of 0.2:
        >>> round((calc_soilmstress(0.2) - 1) * 100, 5)
        -14.0
    """

    # Check inputs, return shape not used
    _ = check_input_shapes(soilm, meanalpha)

    # Calculate outstress
    y0 = (PARAM.soilmstress.a + PARAM.soilmstress.b * meanalpha)
    beta = (1.0 - y0) / (PARAM.soilmstress.theta0 - PARAM.soilmstress.thetastar) ** 2
    outstress = 1.0 - beta * (soilm - PARAM.soilmstress.thetastar) ** 2

    # Filter wrt to thetastar
    outstress = np.where(soilm <= PARAM.soilmstress.thetastar, outstress, 1.0)

    # Clip
    outstress = np.clip(outstress, 0.0, 1.0)

    return outstress


def calc_viscosity_h2o(tc: Union[float, np.ndarray],
                       patm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    r"""Calculates the **viscosity of water** (:math:`\eta`) as a function of
    temperature and atmospheric pressure (::cite:`Huber:2009fy`).

    Parameters:

        tc: air temperature (°C)
        patm: atmospheric pressure (Pa)

    Returns:

        A float giving the viscosity of water (mu, Pa s)

    Examples:

        >>> # Density of water at 20 degrees C and standard atmospheric pressure:
        >>> round(calc_viscosity_h2o(20, 101325), 7)
        0.0010016
    """

    # Check inputs, return shape not used
    _ = check_input_shapes(tc, patm)

    # Get the density of water, kg/m^3
    rho = calc_density_h2o(tc, patm)

    # Calculate dimensionless parameters:
    tbar = (tc + PARAM.k.CtoK) / PARAM.Huber.tk_ast
    rbar = rho / PARAM.Huber.rho_ast

    # Calculate mu0 (Eq. 11 & Table 2, Huber et al., 2009):
    tbar_pow = np.power.outer(tbar, np.arange(0, 4))
    mu0 = (1e2 * np.sqrt(tbar)) / np.sum(np.array(PARAM.Huber.H_i) / tbar_pow, axis=-1)

    # Calculate mu1 (Eq. 12 & Table 3, Huber et al., 2009):
    h_array = np.array(PARAM.Huber.H_ij)
    ctbar = (1.0 / tbar) - 1.0
    row_j, _ = np.indices(h_array.shape)
    mu1 = h_array * np.power.outer(rbar - 1.0, row_j)
    mu1 = np.power.outer(ctbar, np.arange(0, 6)) * np.sum(mu1, axis=(-2))
    mu1 = np.exp(rbar * mu1.sum(axis=-1))

    # Calculate mu_bar (Eq. 2, Huber et al., 2009), assumes mu2 = 1
    mu_bar = mu0 * mu1

    # Calculate mu (Eq. 1, Huber et al., 2009)
    return mu_bar * PARAM.Huber.mu_ast  # Pa s


def calc_patm(elv: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    r"""Calculates **atmospheric pressure** as a function of elevation with reference to
    the standard atmosphere.  The elevation-dependence of atmospheric pressure
    is computed by assuming a linear decrease in temperature with elevation and
    a mean adiabatic lapse rate (Eqn 3, ::cite:`BerberanSantos:2009bk`):

    .. math::

        p(z) = p_0 ( 1 - L z / K_0) ^{ G M / (R L) },

    Parameters:

        elv: Elevation above sea-level (:math:`z`, metres above sea level.)

    Other parameters:

        G: gravity constant (:math:`g`, `PARAM.k.G`)
        Po: standard atmospheric pressure at sea level (:math:`p_0`, `PARAM.k.Po`)
        L: adiabatic temperature lapse rate (:math:`L}`, `PARAM.k.L`),
        M: molecular weight for dry air (:math:`M`, `PARAM.k.Ma`),
        R: universal gas constant (:math:`R`, `PARAM.k.R`)
        Ko: reference temperature in Kelvin (:math:`K_0`, `PARAM.k.To`).

    Returns:

        A numeric value for :math:`p` in Pascals.

    Examples:

        >>> # Standard atmospheric pressure, in Pa, corrected for 1000 m.a.s.l.
        >>> round(calc_patm(1000), 2)
        90241.54

    """

    # Convert elevation to pressure, Pa. This equation uses the base temperature
    # in Kelvins, while other functions use this constant in the PARAM units of
    # °C.

    kto = PARAM.k.To + PARAM.k.CtoK

    return (PARAM.k.Po * (1.0 - PARAM.k.L * elv / kto) **
            (PARAM.k.G * PARAM.k.Ma /
             (PARAM.k.R * PARAM.k.L)))


def calc_co2_to_ca(co2: Union[float, np.ndarray],
                   patm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    r"""Converts ambient :math:`\ce{CO2}` (:math:`c_a`) in part per million to
    Pascals, accounting for atmospheric pressure.

    Parameters:
        co2 (float): atmospheric :math:`\ce{CO2}`, ppm
        patm (float): atmospheric pressure, Pa

    Returns:
        Ambient :math:`\ce{CO2}` in units of Pa

    Examples:
        >>> round(calc_co2_to_ca(413.03, 101325), 6)
        41.850265
    """

    return 1.0e-6 * co2 * patm  # Pa, atms. CO2


@dataclass
class IabsScaled:
    """
    A data class holding variables that scale linearly with absorbed
    irradiance (:math:`I_{abs}`). When a PModel instance is created, an
    instance is created (`PModel.unit_iabs`) that contains values per unit
    absorbed radiation. The PModel.scale_iabs method can then be used to
    generate a scaled instance by providing estimates for PPFD and FAPAR.

    Attributes:

        rd: Dark respiration
        vcmax: Maximum rate of carboxylation
        vcmax25: Maximum rate of carboxylation at standard temperature
        lue: Light use efficiency
        jmax: Maximum rate of electron transport.
        gs: Stomatal conductance
        gpp: Alias for light use efficiency
    """

    rd: Union[float, np.ndarray] = None
    vcmax: Union[float, np.ndarray] = None
    vcmax25: Union[float, np.ndarray] = None
    lue: Union[float, np.ndarray] = None
    jmax: Union[float, np.ndarray] = None
    gs: Union[float, np.ndarray] = None
    scaled: bool = False

    @property
    def gpp(self) -> Union[float, np.ndarray]:
        """Alias property for LUE when scaled"""
        if not self.scaled:
            raise RuntimeError('IabsScaled object has not been scaled - LUE '
                               'is still expressed per unit irradiance.')

        return self.lue

    def scale_iabs(self, fapar, ppfd):
        r"""
        This is a convenience function to scale from values per unit absorbed
        irradiance to absolute values. It finds the total absorbed irradiance
        (:math:`I_{abs}`) as the product of the photosynthetic photon flux
        density (`ppfd`) and the fraction of absorbed photosynthetically active
        radiation (`fapar`) and then uses this to scale the stored values: all
        scale linearly with :math:`I_{abs}`.

        Note that the units of PPFD determine the units of outputs: if PPFD is
        in :math:`\text{mol} m^{-2} \text{month}^{-1}`, then output values are
        scaled per square metre per month.

        Args:
            fapar: the fraction of absorbed photosynthetically active radiation
            ppfd: photosynthetic photon flux density

        Returns:
            An object of class IabsScaled, with attribute `scaled` set to True.

        """

        # Do not double scale
        if self.scaled:
            raise RuntimeError('Values have already been scaled')

        # Check input shapes against each other and an existing calculated value
        _ = check_input_shapes(ppfd, fapar, self.lue)

        # Calcuate absorbed irradiance
        iabs = fapar * ppfd

        return IabsScaled(lue=iabs * self.lue,
                          vcmax=iabs * self.vcmax,
                          vcmax25=iabs * self.vcmax25,
                          rd=iabs * self.rd,
                          jmax=iabs * self.jmax,
                          gs=iabs * self.gs,
                          scaled=True)


class PModel:

    r"""Fits the P model to a given set of environmental parameters. See the
    :meth:`~pyrealm.pmodel.PModel.__init__` documentation for the input variables.
    The calculated attributes of the class are described below. An extended
    description with typical use cases is given in :ref:`pmodel/pmodel.html`
    but the basic flow of the model is:

    1. Calculate photosynthetic variables from environmental conditions. See the
       functions :func:`~pyrealm.pmodel.calc_gammastar`,
       :func:`~pyrealm.pmodel.calc_ns_star`,
       :func:`~pyrealm.pmodel.calc_c02_to_ca` and
       :func:`~pyrealm.pmodel.calc_kmm` for details.
    2. Estimate :math:`\ce{CO2}` limitation factors and optimal internal to
       ambient :math:`\ce{CO2}` partial pressure ratios (:math:`\chi`), using
       :class:`~pyrealm.pmodel.CalcOptimalChi`.
    3. Estimate light use efficiency (LUE) and maximum carboxylation rate
       (:math:`V_{cmax}`) using :class:`~pyrealm.pmodel.CalcLUEVcmax`.
    4. Calculate corollary predictions

    **Corollary prediction details**

    These calculations use two additional functions:

    * the instantaneous temperature response of :math:`V_{cmax}` (:math:`fv(t)`),
      implemented in :func:`~pyrealm.pmodel.calc_ftemp_inst_vcmax`, and
    * the instantaneous temperature response of dark respiration :math:`V_{d}`
      (:math:`fr(t)`), implemented in :func:`~pyrealm.pmodel.calc_ftemp_inst_rd`.

    The predictions are then:

    * Intrinsic water use efficiency (iWUE, Pa), calculated as :math:`(c_a - c_i)/1.6`

    * Maximum carboxylation capacity (mol C m-2) normalised to the standard
      temperature as: :math:`V_{cmax25} = V_{cmax}  / fv(t)`

    * Dark respiration, calculated as:

        .. math::

            R_d = b_0 \frac{fr(t)}{fv(t)} V_{cmax}

        following :cite:`Atkin:2015hk` (:math:`b_0` is set in `PARAM.Atkin.rd_to_vcmax`)

    * Stomatal conductance (:math:`g_s`), calculated as:

        .. math::

            g_s = \frac{LUE}{M_C}\frac{1}{c_a - c_i}

        When C4 photosynthesis is being used, :math:`g_s \to \infty`.

    * The maximum rate of Rubsico regeneration at the growth temperature
      (:math:`J_{max}`) per unit irradiance is calculated as:

        .. math::

            J_{max} = \frac{4 \phi_0 I_{abs}}{\sqrt{\left(\frac{1}
            {\left(\frac{V_{cmax}(c_i - 2 \Gamma^*)}
            {\phi_0 I_{abs}(c_i + k_{mm})}\right)}\right)^2 - 1}}

    Attributes:

        ca: Ambient CO2 expressed as partial pressure (Pa)
        gammastar: Photorespiratory compensation point :math:`\Gamma^*`, (Pa, see
            :func:`~pyrealm.pmodel.calc_gammastar`).
        kmm: Michaelis-Menten coefficient :math:`K` for photosynthesis (Pa, see
            :func:`~pyrealm.pmodel.calc_kmm`).
        ns_star: Relative viscosity of water (unitless, see
            :func:`~pyrealm.pmodel.calc_ns_star`).
        optchi: An object of class :class:`~pyrealm.pmodel.CalcOptimalChi`
        unit_iabs: An object of class :class:`~pyrealm.pmodel.IabsScaled`
        iwue: Intrinsic water use efficiency (iWUE, Pa)

    Examples:

        >>> mod_c3 = PModel(tc=20, vpd=1000, co2=400, patm=101325.0)
        >>> # Key variables from pmodel
        >>> round(mod_c3.optchi.ci, 5)
        28.14209
        >>> round(mod_c3.optchi.chi, 5)
        0.69435
        >>> round(mod_c3.unit_iabs.scale_iabs(fapar=1, ppfd=300).gpp, 5)
        76.42545
        >>> mod_c4 = PModel(tc=20, vpd=1000, co2=400, patm=101325.0,
        ...                 c4=True, method_jmaxlim='none')
        >>> # Key variables from PModel
        >>> round(mod_c4.optchi.ci, 5)
        40.53
        >>> round(mod_c4.optchi.chi, 5)
        1.0
        >>> round(mod_c4.unit_iabs.scale_iabs(fapar=1, ppfd=300).gpp, 5)
        12.90736
    """

    def __init__(self, tc: Union[float, np.ndarray],
                 vpd: Union[float, np.ndarray],
                 co2: Union[float, np.ndarray],
                 patm: Optional[Union[float, np.ndarray]],
                 soilmstress: Optional[Union[float, np.ndarray]] = None,
                 kphio: Optional[float] = None,
                 do_ftemp_kphio: bool = True,
                 c4: bool = False,
                 method_jmaxlim: str = "wang17"):
        r"""
        Creates a PModel instance using the input parameters.

        Parameters:

            tc: Temperature, relevant for photosynthesis (°C)
            vpd: Vapour pressure deficit (Pa)
            co2: Atmospheric CO2 concentration (ppm)
            patm: Atmospheric pressure (Pa).
            kphio: (Optional) Apparent quantum yield efficiency (unitless).
            soilmstress: (Optional, default=None) A soil moisture stress factor
                calculated using :func:`~pyrealm.pmodel.calc_soilmstress`.
            c4: (Optional, default=False) Selects the C3 or C4 photosynthetic pathway.
            method_jmaxlim: (Optional, default=`wang17`) Method to use for
                :math:`J_{max}` limitation
            do_ftemp_kphio: (Optional, default=True) Include the temperature-
                dependence of quantum yield efficiency (see
                :func:`~pyrealm.pmodel.calc_ftemp_kphio`).
       """
        self.shape = check_input_shapes(tc, vpd, co2, patm, soilmstress)

        # -------------------------
        # Set soil moisture default if needed
        # -------------------------

        if soilmstress is None:
            soilmstress = 1.0
            do_soilmstress = False
        else:
            do_soilmstress = True

        # kphio defaults:
        if kphio is None:
            if not do_ftemp_kphio:
                self.kphio = 0.049977
            elif do_soilmstress:
                self.kphio = 0.087182
            else:
                self.kphio = 0.081785
        else:
            self.kphio = kphio

        # -----------------------------------------------------------------------
        # Temperature dependence of quantum yield efficiency
        # -----------------------------------------------------------------------
        # 'do_ftemp_kphio' is not actually a stress function, but is the temperature-
        # dependency of the quantum yield efficiency after Bernacchi et al., 2003

        if do_ftemp_kphio:
            self.ftemp_kphio = calc_ftemp_kphio(tc, c4)
        else:
            self.ftemp_kphio = 1.0

        # -----------------------------------------------------------------------
        # Photosynthesis model parameters depending on temperature, pressure, and CO2.
        # -----------------------------------------------------------------------

        # ambient CO2 partial pressure (Pa)
        self.ca = calc_co2_to_ca(co2, patm)
        # photorespiratory compensation point - Gamma-star (Pa)
        self.gammastar = calc_gammastar(tc, patm)
        # Michaelis-Menten coef. (Pa)
        self.kmm = calc_kmm(tc, patm)

        # viscosity correction factor relative to standards
        self.ns_star = calc_ns_star(tc, patm) # (unitless)

        # -----------------------------------------------------------------------
        # Optimal ci
        # The heart of the P-model: calculate ci:ca ratio (chi) and additional terms
        # -----------------------------------------------------------------------
        self.c4 = c4

        if self.c4:
            method_optci = "c4"
        else:
            method_optci = "prentice14"

        self.optchi = CalcOptimalChi(self.kmm, self.gammastar, self.ns_star,
                                     self.ca, vpd, method=method_optci)

        # -----------------------------------------------------------------------
        # Corollary predictions
        # -----------------------------------------------------------------------

        # intrinsic water use efficiency (in Pa)
        self.iwue = (self.ca - self.optchi.ci) / 1.6

        # -----------------------------------------------------------------------
        # Vcmax and light use efficiency
        # -----------------------------------------------------------------------
        lue_vcmax = CalcLUEVcmax(self.optchi, self.kphio,
                                 self.ftemp_kphio, soilmstress,
                                 method=method_jmaxlim)

        # -----------------------------------------------------------------------
        # Populate an instance of IabsScaled at values per unit iabs
        # -----------------------------------------------------------------------
        self.unit_iabs = IabsScaled(lue=lue_vcmax.lue, vcmax=lue_vcmax.vcmax)

        # Vcmax25 (vcmax normalized to PARAM.k.To)
        ftemp25_inst_vcmax = calc_ftemp_inst_vcmax(tc)
        self.unit_iabs.vcmax25 = self.unit_iabs.vcmax / ftemp25_inst_vcmax

        # Dark respiration at growth temperature
        ftemp_inst_rd = calc_ftemp_inst_rd(tc)
        self.unit_iabs.rd = (PARAM.Atkin.rd_to_vcmax *
                             (ftemp_inst_rd / ftemp25_inst_vcmax) *
                             self.unit_iabs.vcmax)

        # Jmax using again A_J = A_C, handling edges cases
        fact_jmaxlim = (self.unit_iabs.vcmax * (self.optchi.ci + 2.0 * self.gammastar) /
                        (self.kphio * (self.optchi.ci + self.kmm)))
        fact_jmaxlim = (1.0 / fact_jmaxlim) ** 2 - 1.0
        jmax = np.empty_like(fact_jmaxlim)
        mask = fact_jmaxlim > 0
        jmax[mask] = 4.0 * self.kphio / np.sqrt(fact_jmaxlim[mask])
        jmax[~ mask] = np.infty

        # Revert to scalar if needed and store
        self.unit_iabs.jmax = jmax.item() if np.ndim(jmax) == 0 else jmax

        # Stomatal conductance
        if c4 and self.shape == 1:
            self.unit_iabs.gs = np.infty
        elif c4:
            self.unit_iabs.gs = np.ones(self.shape) * np.infty
        else:
            self.unit_iabs.gs = ((self.unit_iabs.lue / PARAM.k.c_molmass) /
                                 (self.ca - self.optchi.ci))

    def __repr__(self):

        return (f"PModel(kphio={self.kphio}, c4={self.c4}, gammastar={self.gammastar}, "
                f"kmm={self.kmm}, ca={self.ca}, ns_star={self.ns_star}, "
                f"ftemp_kphio={self.ftemp_kphio}, iwue={self.iwue})")


class CalcOptimalChi:
    r"""Calculate the optimal :math:`\chi` and :math:`\ce{CO2}` limitation
    factors. In more details, the values are:

    - The optimal ratio of leaf internal to ambient :math:`\ce{CO2}` partial
      pressure (:math:`\chi = c_i/c_a`).
    - The :math:`\ce{CO2}` limitation term for light-limited
      assimilation (:math:`m_j`).
    - The :math:`\ce{CO2}` limitation term for Rubisco-limited
      assimilation  (:math:`m_c`).

    The chosen method is automatically used to estimate these values when an
    instance is created.

    Attributes:

        kmm (float): the Michaelis-Menten coefficient (:math:`K`, see
            :func:`calc_kmm`).
        gammastar (float): the photorespiratory :math:`\ce{CO2}` compensation point
            (:math:`\Gamma^{*}`, see :func:`calc_gammastar`).
        ns_star (float): the viscosity correction factor (:math:`\eta^{*}`,
            see :func:`calc_viscosity_H20`)
        ca (float): the ambient partial pressure of :math:`\ce{CO2}` (:math:`c_a`,
            see :func:`calc_co2_to_ca`)
        vpd (float): the vapor pressure deficit (:math:`D`)
        method (str): one of ``c4`` or ``prentice14``
        beta (float): unit cost ratio of carboxylation (see :obj:`PARAMS.stocker19.beta`)
        chi (float): the ratio of leaf internal to ambient :math:`\ce{CO2}`
            partial pressure (:math:`\chi`).
        mj (float): :math:`\ce{CO2}` limitation factor for light-limited
            assimilation (:math:`m_j`).
        mc (float): :math:`\ce{CO2}` limitation factor for RuBisCO-limited
            assimilation (:math:`m_c`).
        mjoc (float):  :math:`m_j/m_c` ratio

    Returns:

        An instance of :class:`CalcOptimalChi` where the :attr:`chi`,
        :attr:`mj`, :attr:`mc` and :attr:`mjoc` have been populated
        using the chosen method.

    Examples:

        >>> vals = CalcOptimalChi(kmm = 46.09928, gammastar = 3.33925,
        ...                       ns_star = 1.12536, ca = 40.53, vpd = 1000)
        >>> round(vals.chi, 5)
        0.69435
        >>> round(vals.mc, 5)
        0.33408
        >>> round(vals.mj, 5)
        0.7123
        >>> round(vals.mjoc, 5)
        2.13211
        >>> # The c4 method just populates these values with 1.0
        >>> c4_vals = CalcOptimalChi(kmm = 46.09928, gammastar = 3.33925,
        ...                          ns_star = 1.12536, ca = 40.53, vpd = 1000,
        ...                          method='c4')
        >>> c4_vals.chi
        1.0
    """

    def __init__(self,
                 kmm: Union[float, np.ndarray],
                 gammastar: Union[float, np.ndarray],
                 ns_star: Union[float, np.ndarray],
                 ca: Union[float, np.ndarray],
                 vpd: Union[float, np.ndarray],
                 method: str = 'prentice14'):

        # Check inputs are broadcastable
        self.shape = check_input_shapes(kmm, gammastar, ns_star, ca, vpd)

        # set attribute defaults
        self.chi = None
        self.ci = None
        self.mc = None
        self.mj = None
        self.mjoc = None

        # Identify and run the selected method
        self.method = method
        all_methods = {'prentice14': self.prentice14, 'c4': self.c4}

        if self.method in all_methods:
            this_method = all_methods[self.method]
            this_method(kmm=kmm, gammastar=gammastar, ca=ca,
                        vpd=vpd, ns_star=ns_star)
        else:
            raise ValueError(f"CalcOptimalChi: method argument '{method}' invalid.")

        # Calculate internal CO2 partial pressure
        self.ci = self.chi * ca

    def __repr__(self):

        return f"CalcOptimalChi(chi={self.chi}, ci={self.ci}, mc={self.mc}, mj={self.mj})"

    def c4(self, **kwargs):
        r"""This method simply sets :math:`\chi = m_j = m_c = m_{joc} = 1.0` to
        capture the boosted :math:`\ce{CO2}` concentrations at the chloropolast in C4
        photosynthesis.
        """

        # Dummy values to represent c4 pathway. These need to retain any
        # dimensions of the original inputs - if ftemp_kphio is set to 1.0
        # (i.e. no temperature correction) then the dimensions of tc are lost
        # and the input to soilmstress might be scalar, so enforce the shape.
        # Note that rpmodel_1.0.6 collapses array inputs at this point.

        if self.shape == 1:
            self.chi = 1.0
            self.mc = 1.0
            self.mj = 1.0
            self.mjoc = 1.0
        else:
            self.chi = np.ones(self.shape)
            self.mc = np.ones(self.shape)
            self.mj = np.ones(self.shape)
            self.mjoc = np.ones(self.shape)

    def prentice14(self, **kwargs):
        r"""This method calculates key variables as follows:

        Optimal :math:`\chi` is calculated following Equation 8 in
        :cite:`Prentice:2014bc`:

          .. math:: :nowrap:

            \[
                \begin{align*}
                    \chi &= \Gamma^{*} / c_a + (1- \Gamma^{*} / c_a)
                        \xi / (\xi + \sqrt D ), \text{where}\\
                    \xi &= \sqrt{(\beta (K+ \Gamma^{*}) / (1.6 \eta^{*}))}
                \end{align*}
            \]

        The :math:`\ce{CO2}` limitation term of light use efficiency
        (:math:`m_j`) is calculated following Equation 3 in :cite:`Wang:2017go`:

        .. math::

            m_j = \frac{c_a - \Gamma^{*}}
                       {c_a + 2 \Gamma^{*} + 3 \Gamma^{*}
                       \sqrt{\frac{1.6 D \eta^{*}}{\beta(K + \Gamma^{*})}}}

        Finally,  :math:`m_c` is calculated, following Equation 7 in
        :cite:`Stocker:2020dh`, as:

        .. math::

            m_c = \frac{c_i - \Gamma^{*}}{c_i + K},

        where :math:`K` is the Michaelis Menten coefficient of Rubisco-limited
        assimilation.
        """

        # Avoid negative VPD (dew conditions)
        vpd = np.clip(kwargs['vpd'], 0, None)

        # leaf-internal-to-ambient CO2 partial pressure (ci/ca) ratio
        xi = np.sqrt((PARAM.stocker19.beta * (kwargs['kmm'] + kwargs['gammastar']))
                     / (1.6 * kwargs['ns_star']))
        self.chi = (kwargs['gammastar'] / kwargs['ca'] +
                    (1.0 - kwargs['gammastar'] / kwargs['ca']) * xi / (xi + np.sqrt(vpd)))

        # Define variable substitutes:
        vdcg = kwargs['ca'] - kwargs['gammastar']
        vacg = kwargs['ca'] + 2.0 * kwargs['gammastar']
        vbkg = PARAM.stocker19.beta * (kwargs['kmm'] + kwargs['gammastar'])

        # Calculate mj
        # NOTE: this differs from rpmodel, which uses length not dim here, so
        # unwrapped matrix inputs. Also, rpmodel includes a check for vpd > 0,
        # but this is guaranteed by clip above (also true in rpmodel).

        vsr = np.sqrt(1.6 * kwargs['ns_star'] * vpd / vbkg)
        mj = vdcg / (vacg + 3.0 * kwargs['gammastar']* vsr)
        mj = np.where(np.logical_and(kwargs['ns_star'] > 0, vbkg > 0), mj, np.nan)
        # np.where _always_ returns an array, so catch scalars.
        self.mj = mj.item() if np.ndim(mj) == 0 else mj

        # alternative variables
        gamma = kwargs['gammastar'] / kwargs['ca']
        kappa = kwargs['kmm'] / kwargs['ca']

        # mc and mj:mv
        self.mc = (self.chi - gamma) / (self.chi + kappa)
        self.mjoc = (self.chi + kappa) / (self.chi + 2 * gamma)


class CalcLUEVcmax:
    r"""Estimate light use efficiency and maximum carboxylation rate
    :math:`V_{cmax}`. The class implements:

    - :math:`J_{max}` limitation of light use efficiency, providing two
      approaches (``wang17`` and ``smith19``),
    - soil moisture stress limitation, and
    - temperature dependence of apparent quantum yield efficiency.

    Light use efficiency (LUE) is calculated from the inputs as:

    .. math::

        \text{LUE} = \phi_0 \cdot \phi_0(T) \cdot  m_j \cdot m_{jlim} \cdot M_C \cdot \beta

    The Rubisco carboxylation capacity (:math:`V_{cmax}`) of the system is then back
    calculated from LUE as:

    .. math::

          V_{cmax} = \frac{\text{LUE}}{m_c M_C}

    Attributes:

        optchi (:class:`CalcOptimalChi`): an instance of :class:`CalcOptimalChi`
            providing the :math:`\ce{CO2}` limitation term of light use efficiency
            (:math:`\m_j`) and the  the :math:`\ce{CO2}` limitation term for
            Rubisco assimilation (:math:`m_c`).
        kphio (float): The apparent quantum yield efficiency (:math:`\phi_0`,
            unitless).
        ftemp_kphio (float): A factor to capture the temperature dependence of
            quantum yield efficiency (:math:`\phi_0(T)`), defaulting to 1.0 for
            no temperature dependence (see :func:`calc_ftemp_kphio`).
        soilmstress (float): A factor to capture the soil moisture stress
            (:math:`\beta`), defaulting to 1.0 for no soil moisture stress
            (see :func:`calc_soilmstress`).
        method (str): method to apply :math:`J_{max}` limitation (default: ``wang17``,
            or ``smith19`` or ``none``)
        mjlim (float): :math:`J_{max}` limitation factor, calculated using the method.
        lue (float): calculated light use efficiency per unit absolute irradiance.
        vcmax (float): calculated maximum carboxylation rate per unit absolute
            irradiance.
        omega (float): component of :math:`J_{max}` calculation (:cite:`Smith:2019dv`).
        omega_star (float):  component of :math:`J_{max}` calculation (:cite:`Smith:2019dv`).

    Other Parameters:

        c_molmass: the molar mass of carbon (:math:`M_C`, `PARAM.k.c_molmass`)



    Examples:

        >>> optchi = CalcOptimalChi(kmm = 46.09928, gammastar = 3.33925,
        ...                         ns_star = 1.12536, ca = 40.53, vpd = 1000)
        >>> # Using Wang et al 2017
        >>> out_wang = CalcLUEVcmax(optchi, kphio = 0.081785, ftemp_kphio = 0.656,
        ...                         soilmstress = 1, method='wang17')
        >>> round(out_wang.lue, 5)
        0.25475
        >>> round(out_wang.vcmax, 6)
        0.063488
        >>> # Using Smith et al 2019
        >>> out_smith = CalcLUEVcmax(optchi, kphio = 0.081785, ftemp_kphio = 0.656,
        ...                          soilmstress = 1, method='smith19')
        >>> round(out_smith.lue, 6)
        0.086569
        >>> round(out_smith.vcmax, 6)
        0.021574
        >>> round(out_smith.omega, 5)
        1.10204
        >>> round(out_smith.omega_star, 5)
        1.28251
        >>> # No Jmax limitation
        >>> out_none = CalcLUEVcmax(optchi, kphio = 0.081785, ftemp_kphio = 0.656,
        ...                    soilmstress = 1, method='none')
        >>> round(out_none.lue, 6)
        0.458998
        >>> round(out_none.vcmax, 6)
        0.11439

    """

    # TODO - apparent incorrectness of wang and smith methods with _ca_ variation,
    #        work well with varying temperature but not _ca_ variation (or
    #        e.g. elevation gradient David Sandoval, REALM meeting, Dec 2020)

    def __init__(self, optchi: CalcOptimalChi,
                 kphio: Union[float, np.ndarray],
                 ftemp_kphio: Union[float, np.ndarray] = 1.0,
                 soilmstress: Union[float, np.ndarray] = 1.0,
                 method: str = 'wang17'):

        self.shape = check_input_shapes(optchi.mj, optchi.mjoc, kphio,
                                        ftemp_kphio, soilmstress)

        self.optchi = optchi
        self.kphio = kphio
        self.ftemp_kphio = ftemp_kphio
        self.soilmstress = soilmstress
        self.method = method
        self.mjlim = None
        self.lue = None
        self.vcmax = None
        self.omega = None
        self.omega_star = None

        all_methods = {'wang17': self.wang17,
                       'smith19': self.smith19,
                       'none': self.none}

        if self.method == 'c4':
            raise ValueError('This class does not implement a fixed method for C4 '
                             'photosynthesis. To replicate rpmodel choose c4=True and '
                             'method="none"')

        if self.method in all_methods:

            # Use the selected method to calculate limitation factors
            this_method = all_methods[self.method]
            this_method()

            # Now calculate the LUE and V_cmax
            # Light use efficiency (gpp per unit absorbed light)
            self.lue = (self.kphio * self.ftemp_kphio * self.optchi.mj * self.mjlim *
                        PARAM.k.c_molmass * self.soilmstress)

            # Back calculate Vcmax normalised per unit absorbed PPFD (assuming iabs=1)
            self.vcmax = self.lue / (self.optchi.mc * PARAM.k.c_molmass)

        else:
            raise ValueError(f"CalcLUEVcmax: method argument '{method}' invalid.")

    def __repr__(self):

        return (f"CalcLUEVCmax(lue={self.lue}, vcmax={self.vcmax}, "
                f"mjlim={self.mjlim}, omega={self.omega}, omega_star={self.omega_star})")

    def wang17(self):
        r"""Calculate a :math:`J_{max}` limitation following
        :cite:`Wang:2017go`. The factor is described in Equation 49 of
        :cite:`Wang:2017go` and is the square root term at the end of that
        equation:

        .. math::

            m_{jmax} = \sqrt{1- \left(\frac{c^*}{m_j}\right)^{\frac{2}{3}}}

        Other parameters:

            cstar: A cost parameter for maintaining :math:`J_{max}`
                (:math:`c^*`, `PARAM.wang.c`)

        """

        # Calculate mjlim (square root term in Eqn 2 of Wang et al 2017)
        vals = 1 - (PARAM.wang17.c / self.optchi.mj) ** (2.0 / 3.0)

        # Convert to array if needed and handle negative and nan values
        vals = np.array(vals) if np.ndim(vals) == 0 else vals
        mask = vals >= 0  # Also traps np.nan
        mjlim = np.empty_like(vals)
        mjlim[mask] = np.sqrt(vals[mask])
        mjlim[~ mask] = np.nan

        # revert scalars back to a scalar value
        self.mjlim = mjlim.item() if np.ndim(mjlim) == 0 else mjlim

    def smith19(self):
        r"""Calculate a :math:`J_{max}` limitation following
        :cite:`Smith:2019dv`. The value of :math:`m_{jlim}` is taken as the
        final term of  Equation 18 of :cite:`Smith:2019dv`:

        .. math::
            :nowrap:

            \[
                \begin{align*}
                m_{jlim} &= \frac{\omega^*}{8\theta}, \text{where} \\
                \omega^* &= 1 + \omega - \sqrt{(1 + \omega) ^2 -4\theta\omega}, \text{and}\\
                \omega &= (1 - 2\theta) + \sqrt{(1-\theta)
                    \left(\frac{1}{\frac{4c}{m}(1 - \theta\frac{4c}{m})}-4\theta\right)}
                \end{align*}
            \]

        Other parameters:

            theta: A term to capture the curved relationship between light intensity
                and photosynthetic capacity :math:`J_{max}` (:math:`\theta`, `PARAM.smith19.theta`)
            c_cost: A cost parameter for maintaining :math:`J_{max}`
                (:math:`c`, `PARAM.smith19.c_cost`)

        """

        # Adopted from Nick Smith's code:
        # Calculate omega, see Smith et al., 2019 Ecology Letters  # Eq. S4
        theta = PARAM.smith19.theta
        c_cost = PARAM.smith19.c_cost

        # simplification terms for omega calculation
        cm = 4 * c_cost / self.optchi.mj
        v = 1 / (cm * (1 - PARAM.smith19.theta * cm)) - 4 * theta

        # account for non-linearities at low m values. This code finds
        # the roots of a quadratic function that is defined purely from
        # the scalar theta, so will always be a scalar. The first root
        # is then used to set a filter for calculating omega.

        cap_p = (((1 / 1.4) - 0.7) ** 2 / (1 - theta)) + 3.4
        aquad = -1
        bquad = cap_p
        cquad = -(cap_p * theta)
        roots = np.polynomial.polynomial.polyroots([aquad, bquad, cquad])

        # factors derived as in Smith et al., 2019
        m_star = (4 * c_cost) / roots[0].real
        omega = np.where(self.optchi.mj < m_star,
                         -(1 - (2 * theta)) - np.sqrt((1 - theta) * v),
                         -(1 - (2 * theta)) + np.sqrt((1 - theta) * v))

        # np.where _always_ returns an array, so catch scalars
        self.omega = omega.item() if np.ndim(omega) == 0 else omega

        self.omega_star = (1.0 + self.omega -  # Eq. 18
                           np.sqrt((1.0 + self.omega) ** 2 -
                                   (4.0 * theta * self.omega)))

        # Effect of Jmax limitation
        self.mjlim = self.omega_star / (8.0 * theta)

    def none(self):
        """No :math:`J_{max}` limitation (:math:`m_{jlim} = 1.0`)
        """

        # Set Jmax limitation to unity - could define as 1.0 in __init__ and
        # pass here, but setting explicitly within the method for clarity.
        self.mjlim = 1.0
