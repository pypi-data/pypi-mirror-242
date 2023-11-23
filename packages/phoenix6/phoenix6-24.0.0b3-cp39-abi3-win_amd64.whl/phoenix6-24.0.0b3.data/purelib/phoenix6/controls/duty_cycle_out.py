"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
from phoenix6.units import *
import ctypes


class DutyCycleOut:
    """
    Request a specified motor duty cycle.
    
    This control mode will output a proportion of the supplied voltage which is
    supplied by the user.
    
    :param output:    Proportion of supply voltage to apply in fractional units
                      between -1 and +1
    :type output: float
    :param enable_foc:    Set to true to use FOC commutation (requires Phoenix Pro),
                          which increases peak power by ~15%. Set to false to use
                          trapezoidal commutation.  FOC improves motor performance
                          by leveraging torque (current) control.  However, this may
                          be inconvenient for applications that require specifying
                          duty cycle or voltage.  CTR-Electronics has developed a
                          hybrid method that combines the performances gains of FOC
                          while still allowing applications to provide duty cycle or
                          voltage demand.  This not to be confused with simple
                          sinusoidal control or phase voltage control which lacks
                          the performance gains.
    :type enable_foc: bool
    :param override_brake_dur_neutral:    Set to true to static-brake the rotor when
                                          output is zero (or within deadband).  Set
                                          to false to use the NeutralMode
                                          configuration setting (default). This flag
                                          exists to provide the fundamental behavior
                                          of this control when output is zero, which
                                          is to provide 0V to the motor.
    :type override_brake_dur_neutral: bool
    """

    def __init__(self, output: float, enable_foc: bool = True, override_brake_dur_neutral: bool = False):
        self._name = "DutyCycleOut"
        self.update_freq_hz: hertz = 100.0
        
        self.output = output
        """
        Proportion of supply voltage to apply in fractional units between -1 and +1
        """
        self.enable_foc = enable_foc
        """
        Set to true to use FOC commutation (requires Phoenix Pro), which increases peak
        power by ~15%. Set to false to use trapezoidal commutation.  FOC improves motor
        performance by leveraging torque (current) control.  However, this may be
        inconvenient for applications that require specifying duty cycle or voltage. 
        CTR-Electronics has developed a hybrid method that combines the performances
        gains of FOC while still allowing applications to provide duty cycle or voltage
        demand.  This not to be confused with simple sinusoidal control or phase voltage
        control which lacks the performance gains.
        """
        self.override_brake_dur_neutral = override_brake_dur_neutral
        """
        Set to true to static-brake the rotor when output is zero (or within deadband). 
        Set to false to use the NeutralMode configuration setting (default). This flag
        exists to provide the fundamental behavior of this control when output is zero,
        which is to provide 0V to the motor.
        """

    @property
    def name(self) -> str:
        """
        Gets the name of this control request.

        :returns: Name of the control request
        :rtype: str
        """
        return self._name

    def __str__(self) -> str:
        ss = []
        ss.append("class: DutyCycleOut")
        ss.append("output: " + str(self.output))
        ss.append("enable_foc: " + str(self.enable_foc))
        ss.append("override_brake_dur_neutral: " + str(self.override_brake_dur_neutral))
        return "\n".join(ss)

    def _send_request(self, network: str, device_hash: int, cancel_other_requests: bool) -> StatusCode:
        """
        Sends this request out over CAN bus to the device for
        the device to apply.

        :param network: Network to send request over
        :type network: str
        :param device_hash: Device to send request to
        :type device_hash: int
        :param cancel_other_requests: True to cancel other requests
        :type cancel_other_requests: bool
        :returns: Status of the send operation
        :rtype: StatusCode
        """

        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlDutyCycleOut(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, self.update_freq_hz, cancel_other_requests, self.output, self.enable_foc, self.override_brake_dur_neutral))

    
    def with_output(self, new_output: float) -> 'DutyCycleOut':
        """
        Modifies this Control Request's output parameter and returns itself for
        method-chaining and easier to use request API.
    
        :param new_output: Parameter to modify
        :type new_output: float
        :returns: Itself
        :rtype: DutyCycleOut
        """
        self.output = new_output
        return self
    
    def with_enable_foc(self, new_enable_foc: bool) -> 'DutyCycleOut':
        """
        Modifies this Control Request's enable_foc parameter and returns itself for
        method-chaining and easier to use request API.
    
        :param new_enable_foc: Parameter to modify
        :type new_enable_foc: bool
        :returns: Itself
        :rtype: DutyCycleOut
        """
        self.enable_foc = new_enable_foc
        return self
    
    def with_override_brake_dur_neutral(self, new_override_brake_dur_neutral: bool) -> 'DutyCycleOut':
        """
        Modifies this Control Request's override_brake_dur_neutral parameter and returns itself for
        method-chaining and easier to use request API.
    
        :param new_override_brake_dur_neutral: Parameter to modify
        :type new_override_brake_dur_neutral: bool
        :returns: Itself
        :rtype: DutyCycleOut
        """
        self.override_brake_dur_neutral = new_override_brake_dur_neutral
        return self

    def with_update_freq_hz(self, new_update_freq_hz: hertz) -> 'DutyCycleOut':
        """
        Sets the period at which this control will update at.
        This is designated in Hertz, with a minimum of 20 Hz
        (every 50 ms) and a maximum of 1000 Hz (every 1 ms).

        If this field is set to 0 Hz, the control request will
        be sent immediately as a one-shot frame. This may be useful
        for advanced applications that require outputs to be
        synchronized with data acquisition. In this case, we
        recommend not exceeding 50 ms between control calls.

        :param new_update_freq_hz: Parameter to modify
        :type new_update_freq_hz: hertz
        :returns: Itself
        :rtype: DutyCycleOut
        """
        self.update_freq_hz = new_update_freq_hz
        return self

    @property
    def control_info(self) -> dict:
        """
        Gets information about this control request.

        :returns: Dictonary of control parameter names and corresponding applied values
        :rtype: dict
        """
        control_info = {}
        control_info["name"] = self._name
        control_info["output"] = self.output
        control_info["enable_foc"] = self.enable_foc
        control_info["override_brake_dur_neutral"] = self.override_brake_dur_neutral
        return control_info
