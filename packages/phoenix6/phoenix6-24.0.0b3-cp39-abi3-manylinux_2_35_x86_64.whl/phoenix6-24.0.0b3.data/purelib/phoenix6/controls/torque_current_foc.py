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


class TorqueCurrentFOC:
    """
    Requires Phoenix Pro;
    Request a specified motor current (field oriented
    control).
    
    This control request will drive the motor to the requested motor (stator)
    current value.  This leverages field oriented control (FOC), which means greater
    peak power than what is documented.  This scales to torque based on Motor's kT
    constant.
    
    :param output:    Amount of motor current in Amperes
    :type output: ampere
    :param max_abs_duty_cycle:    The maximum absolute motor output that can be
                                  applied, which effectively limits the velocity.
                                  For example, 0.50 means no more than 50% output in
                                  either direction.  This is useful for preventing
                                  the motor from spinning to its terminal velocity
                                  when there is no external torque applied unto the
                                  rotor.  Note this is absolute maximum, so the
                                  value should be between zero and one.
    :type max_abs_duty_cycle: float
    :param deadband:    Deadband in Amperes.  If torque request is within deadband,
                        the bridge output is neutral. If deadband is set to zero
                        then there is effectively no deadband. Note if deadband is
                        zero, a free spinning motor will spin for quite a while as
                        the firmware attempts to hold the motor's bemf. If user
                        expects motor to cease spinning quickly with a demand of
                        zero, we recommend a deadband of one Ampere. This value will
                        be converted to an integral value of amps.
    :type deadband: ampere
    :param override_coast_dur_neutral:    Set to true to coast the rotor when output
                                          is zero (or within deadband).  Set to
                                          false to use the NeutralMode configuration
                                          setting (default). This flag exists to
                                          provide the fundamental behavior of this
                                          control when output is zero, which is to
                                          provide 0A (zero torque).
    :type override_coast_dur_neutral: bool
    """

    def __init__(self, output: ampere, max_abs_duty_cycle: float = 1.0, deadband: ampere = 0.0, override_coast_dur_neutral: bool = False):
        self._name = "TorqueCurrentFOC"
        self.update_freq_hz: hertz = 100.0
        
        self.output = output
        """
        Amount of motor current in Amperes
        """
        self.max_abs_duty_cycle = max_abs_duty_cycle
        """
        The maximum absolute motor output that can be applied, which effectively limits
        the velocity. For example, 0.50 means no more than 50% output in either
        direction.  This is useful for preventing the motor from spinning to its
        terminal velocity when there is no external torque applied unto the rotor.  Note
        this is absolute maximum, so the value should be between zero and one.
        """
        self.deadband = deadband
        """
        Deadband in Amperes.  If torque request is within deadband, the bridge output is
        neutral. If deadband is set to zero then there is effectively no deadband. Note
        if deadband is zero, a free spinning motor will spin for quite a while as the
        firmware attempts to hold the motor's bemf. If user expects motor to cease
        spinning quickly with a demand of zero, we recommend a deadband of one Ampere.
        This value will be converted to an integral value of amps.
        """
        self.override_coast_dur_neutral = override_coast_dur_neutral
        """
        Set to true to coast the rotor when output is zero (or within deadband).  Set to
        false to use the NeutralMode configuration setting (default). This flag exists
        to provide the fundamental behavior of this control when output is zero, which
        is to provide 0A (zero torque).
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
        ss.append("class: TorqueCurrentFOC")
        ss.append("output: " + str(self.output))
        ss.append("max_abs_duty_cycle: " + str(self.max_abs_duty_cycle))
        ss.append("deadband: " + str(self.deadband))
        ss.append("override_coast_dur_neutral: " + str(self.override_coast_dur_neutral))
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

        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlTorqueCurrentFOC(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, self.update_freq_hz, cancel_other_requests, self.output, self.max_abs_duty_cycle, self.deadband, self.override_coast_dur_neutral))

    
    def with_output(self, new_output: ampere) -> 'TorqueCurrentFOC':
        """
        Modifies this Control Request's output parameter and returns itself for
        method-chaining and easier to use request API.
    
        :param new_output: Parameter to modify
        :type new_output: ampere
        :returns: Itself
        :rtype: TorqueCurrentFOC
        """
        self.output = new_output
        return self
    
    def with_max_abs_duty_cycle(self, new_max_abs_duty_cycle: float) -> 'TorqueCurrentFOC':
        """
        Modifies this Control Request's max_abs_duty_cycle parameter and returns itself for
        method-chaining and easier to use request API.
    
        :param new_max_abs_duty_cycle: Parameter to modify
        :type new_max_abs_duty_cycle: float
        :returns: Itself
        :rtype: TorqueCurrentFOC
        """
        self.max_abs_duty_cycle = new_max_abs_duty_cycle
        return self
    
    def with_deadband(self, new_deadband: ampere) -> 'TorqueCurrentFOC':
        """
        Modifies this Control Request's deadband parameter and returns itself for
        method-chaining and easier to use request API.
    
        :param new_deadband: Parameter to modify
        :type new_deadband: ampere
        :returns: Itself
        :rtype: TorqueCurrentFOC
        """
        self.deadband = new_deadband
        return self
    
    def with_override_coast_dur_neutral(self, new_override_coast_dur_neutral: bool) -> 'TorqueCurrentFOC':
        """
        Modifies this Control Request's override_coast_dur_neutral parameter and returns itself for
        method-chaining and easier to use request API.
    
        :param new_override_coast_dur_neutral: Parameter to modify
        :type new_override_coast_dur_neutral: bool
        :returns: Itself
        :rtype: TorqueCurrentFOC
        """
        self.override_coast_dur_neutral = new_override_coast_dur_neutral
        return self

    def with_update_freq_hz(self, new_update_freq_hz: hertz) -> 'TorqueCurrentFOC':
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
        :rtype: TorqueCurrentFOC
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
        control_info["max_abs_duty_cycle"] = self.max_abs_duty_cycle
        control_info["deadband"] = self.deadband
        control_info["override_coast_dur_neutral"] = self.override_coast_dur_neutral
        return control_info
