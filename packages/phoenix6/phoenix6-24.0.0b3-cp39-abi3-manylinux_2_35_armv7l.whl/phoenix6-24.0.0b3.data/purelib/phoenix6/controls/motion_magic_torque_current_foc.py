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


class MotionMagicTorqueCurrentFOC:
    """
    Requires Phoenix Pro;
    Requests Motion Magic® to target a final position using a
    motion profile.  Users can optionally provide a torque current feedforward.
    
    Motion Magic® produces a motion profile in real-time while attempting to honor
    the Cruise Velocity, Acceleration, and Jerk value specified via the Motion
    Magic® configuration values.  Target position can be changed on-the-fly and
    Motion Magic® will do its best to adjust the profile.  This control mode is
    based on torque current, so relevant closed-loop gains will use Amperes for the
    numerator.
    
    :param position:    Position to drive toward in rotations.
    :type position: rotation
    :param feed_forward:    Feedforward to apply in torque current in Amperes.  User
                            can use motor's kT to scale Newton-meter to Amperes.
    :type feed_forward: ampere
    :param slot:    Select which gains are applied by selecting the slot.  Use the
                    configuration api to set the gain values for the selected slot
                    before enabling this feature. Slot must be within [0,2].
    :type slot: int
    :param override_coast_dur_neutral:    Set to true to coast the rotor when output
                                          is zero (or within deadband).  Set to
                                          false to use the NeutralMode configuration
                                          setting (default). This flag exists to
                                          provide the fundamental behavior of this
                                          control when output is zero, which is to
                                          provide 0A (zero torque).
    :type override_coast_dur_neutral: bool
    """

    def __init__(self, position: rotation, feed_forward: ampere = 0.0, slot: int = 0, override_coast_dur_neutral: bool = False):
        self._name = "MotionMagicTorqueCurrentFOC"
        self.update_freq_hz: hertz = 100.0
        
        self.position = position
        """
        Position to drive toward in rotations.
        """
        self.feed_forward = feed_forward
        """
        Feedforward to apply in torque current in Amperes.  User can use motor's kT to
        scale Newton-meter to Amperes.
        """
        self.slot = slot
        """
        Select which gains are applied by selecting the slot.  Use the configuration api
        to set the gain values for the selected slot before enabling this feature. Slot
        must be within [0,2].
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
        ss.append("class: MotionMagicTorqueCurrentFOC")
        ss.append("position: " + str(self.position))
        ss.append("feed_forward: " + str(self.feed_forward))
        ss.append("slot: " + str(self.slot))
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

        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlMotionMagicTorqueCurrentFOC(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, self.update_freq_hz, cancel_other_requests, self.position, self.feed_forward, self.slot, self.override_coast_dur_neutral))

    
    def with_position(self, new_position: rotation) -> 'MotionMagicTorqueCurrentFOC':
        """
        Modifies this Control Request's position parameter and returns itself for
        method-chaining and easier to use request API.
    
        :param new_position: Parameter to modify
        :type new_position: rotation
        :returns: Itself
        :rtype: MotionMagicTorqueCurrentFOC
        """
        self.position = new_position
        return self
    
    def with_feed_forward(self, new_feed_forward: ampere) -> 'MotionMagicTorqueCurrentFOC':
        """
        Modifies this Control Request's feed_forward parameter and returns itself for
        method-chaining and easier to use request API.
    
        :param new_feed_forward: Parameter to modify
        :type new_feed_forward: ampere
        :returns: Itself
        :rtype: MotionMagicTorqueCurrentFOC
        """
        self.feed_forward = new_feed_forward
        return self
    
    def with_slot(self, new_slot: int) -> 'MotionMagicTorqueCurrentFOC':
        """
        Modifies this Control Request's slot parameter and returns itself for
        method-chaining and easier to use request API.
    
        :param new_slot: Parameter to modify
        :type new_slot: int
        :returns: Itself
        :rtype: MotionMagicTorqueCurrentFOC
        """
        self.slot = new_slot
        return self
    
    def with_override_coast_dur_neutral(self, new_override_coast_dur_neutral: bool) -> 'MotionMagicTorqueCurrentFOC':
        """
        Modifies this Control Request's override_coast_dur_neutral parameter and returns itself for
        method-chaining and easier to use request API.
    
        :param new_override_coast_dur_neutral: Parameter to modify
        :type new_override_coast_dur_neutral: bool
        :returns: Itself
        :rtype: MotionMagicTorqueCurrentFOC
        """
        self.override_coast_dur_neutral = new_override_coast_dur_neutral
        return self

    def with_update_freq_hz(self, new_update_freq_hz: hertz) -> 'MotionMagicTorqueCurrentFOC':
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
        :rtype: MotionMagicTorqueCurrentFOC
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
        control_info["position"] = self.position
        control_info["feed_forward"] = self.feed_forward
        control_info["slot"] = self.slot
        control_info["override_coast_dur_neutral"] = self.override_coast_dur_neutral
        return control_info
