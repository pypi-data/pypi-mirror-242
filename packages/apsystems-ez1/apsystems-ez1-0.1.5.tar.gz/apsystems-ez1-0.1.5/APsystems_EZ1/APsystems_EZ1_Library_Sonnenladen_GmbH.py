import requests


class APsystemsEZ1M:
    """
    This class represents an EZ1 Microinverter and provides methods to interact with it
    over a network. The class allows for getting and setting various device parameters like
    power status, alarm information, device information, and power limits.

    Attributes:
    - base_url (str): The base URL for the API endpoints of the microinverter.
    - session (requests.Session): A session object for making HTTP requests.

    Methods:
    - __init__(self, ip_address, port=8050): Initializes a new EZ1Microinverter instance.
    - _request(self, endpoint, method='GET', data=None, timeout=10): A private method for
      making HTTP requests to the microinverter's API.
    """

    def __init__(self, ip_address, port=8050):
        """
        Initializes a new instance of the EZ1Microinverter class with the specified IP address
        and port.

        :param ip_address: The IP address of the EZ1 Microinverter.
        :param port: The port on which the microinverter's server is running. Default is 8050.
        """
        self.base_url = f"http://{ip_address}:{port}"
        self.session = requests.Session()

    def _request(self, endpoint, method='GET', data=None, timeout=10):
        """
        A private method to send HTTP requests to the specified endpoint of the microinverter.
        This method is used internally by other class methods to perform GET or POST requests.

        :param endpoint: The API endpoint to make the request to.
        :param method: The HTTP method to use for the request. Default is 'GET'.
        :param data: Optional data to be sent in the request body, typically used for POST requests.
        :param timeout: The timeout in seconds for the request. Default is 10 seconds.

        :return: The JSON response from the microinverter as a dictionary.
        :raises: Prints an error message if the HTTP request fails for any reason.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.request(method, url, json=data, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error: {err}")
        except requests.exceptions.Timeout as err:
            print(f"Timeout error: {err}")
        except Exception as err:
            print(f"Error: {err}")


    def get_device_info(self):
        """
        Retrieves detailed information about the device. This method sends a request to the
        "getDeviceInfo" endpoint and returns a dictionary containing various details about the device.

        The returned data includes the device ID, device version, the SSID it is connected to, its IP
        address, and its minimum and maximum power settings. This information can be used for monitoring
        and configuring the device.

        :return: A dictionary with the following structure:
                 {
                     'data': {
                         'deviceId': [Device ID as a string],
                         'devVer': [Device Firmware Version as a string],
                         'ssid': [SSID the device is connected to as a string],
                         'ipAddr': [IP address of the device as a string],
                         'minPower': [Minimum power setting of the device, in watts, as a string],
                         'maxPower': [Maximum power setting of the device, in watts, as a string]
                     },
                     'message': [Status message indicating 'SUCCESS' or 'FAILED'],
                     'deviceId': [Device ID as a string, repeated from data]
                 }

        The keys in the 'data' object include:
        - 'deviceId': The unique identifier for the device.
        - 'devVer': The version of the device firmware or software.
        - 'ssid': The SSID of the network to which the device is currently connected.
        - 'ipAddr': The current IP address of the device.
        - 'minPower': The minimum power output that the device can be set to, measured in watts.
        - 'maxPower': The maximum power output that the device can be set to, also in watts.
        """
        return self._request("getDeviceInfo")

    def get_alarm_info(self):
        """
        Retrieves the alarm status information for various components of the device. This method
        makes a request to the "getAlarm" endpoint and returns a dictionary containing the alarm
        status for different parameters.

        The 'data' field in the returned dictionary includes the status of several components,
        each represented as a string indicating whether there is an alarm ('1') or normal operation ('0').

        :return: A dictionary with the following structure:
                 {
                     'data': {
                         'og': [Off grid status - '0' for normal, '1' for alarm],
                         'isce1': [DC 1 Short Circuit Error status - '0' for normal, '1' for alarm],
                         'isce2': [DC 2 Short Circuit Error status - '0' for normal, '1' for alarm],
                         'oe': [Output fault status - '0' for normal, '1' for alarm]
                     },
                     'message': [Status message indicating 'SUCCESS' or 'FAILED'],
                     'deviceId': [Device ID as a string]
                 }

        The keys in the 'data' object are as follows:
        - 'og': Indicates the off grid status.
        - 'isce1': Indicates a short circuit error in DC 1.
        - 'isce2': Indicates a short circuit error in DC 2.
        - 'oe': Indicates an output fault.
        Each key maps to a string value, where '0' denotes normal operation and '1' denotes an alarm state.
        """
        return self._request("getAlarm")

    def get_output_data(self):
        """
        Retrieves the output data from the device. This method calls a private method `_request`
        with the endpoint "getOutputData" to fetch the device's output data.

        The returned data includes various parameters such as power output status ('p1', 'p2'),
        energy readings ('e1', 'e2'), and total energy ('te1', 'te2') for two different inputs
        of the inverter. Additionally, it provides a status message and the device ID.

        :return: A dictionary containing the output data. The structure of the returned data is as follows:
                 {
                     'data': {
                         'p1': [Power output status of inverter input 1],
                         'e1': [Energy reading for inverter input 1],
                         'te1': [Total energy for inverter input 1],
                         'p2': [Power output status of inverter input 2],
                         'e2': [Energy reading for inverter input 2],
                         'te2': [Total energy for inverter input 2]
                     },
                     'message': [Status message],
                     'deviceId': [Device ID]
                 }
        """
        return self._request("getOutputData")

    def get_p1_output(self):
        """
        Get the power output status of inverter input 1. This method retrieves the 'p1' value
        from the output data of the inverter. If the 'p1' value is not available, a message is
        printed indicating the absence of this value.

        :return: The 'p1' value as an integer if it is found, otherwise None.
        :raises: Specific exceptions related to data retrieval, if any.
        """
        p1_value = self.get_output_data()['data']['p1']
        if p1_value is not None:
            return int(p1_value)
        else:
            print("p1 value not found in the output data.")

    def get_p2_output(self):
        """
        Get the power output status of inverter input 2. This method retrieves the 'p2' value
        from the output data of the inverter. If the 'p2' value is not available, a message is
        printed indicating the absence of this value.

        :return: The 'p2' value as an integer if it is found, otherwise None.
        :raises: Specific exceptions related to data retrieval, if any.
        """
        p2_value = self.get_output_data()['data']['p2']
        if p2_value is not None:
            return int(p2_value)
        else:
            print("p2 value not found in the output data.")

    def get_total_output(self):
        """
        Retrieves and calculates the combined power output status of inverter inputs 1 and 2.
        This method first calls get_output_data() to fetch the output data from the device, which
        includes individual power output values for 'p1' and 'p2'. It then sums these values to
        provide the total combined power output.

        :return: The sum of power output values 'p1' and 'p2' as an integer, if both values are found.
                 If either 'p1' or 'p2' value is not found in the output data, None is returned and
                 a message is printed indicating the missing value.

        Note: The method assumes that 'p1' and 'p2' values in the output data are integers or can
        be converted to integers. If these values are missing, the method alerts the user and
        does not perform the summation.
        """
        data = self.get_output_data()
        p1_value = data['data']['p1']
        p2_value = data['data']['p2']
        if p1_value is not None and p2_value is not None:
            return int(p1_value) + int(p2_value)
        else:
            print("p1 or p2 value not found in the output data.")

    def get_p1_energy_today(self):
        """
        Retrieves the total energy generated today by inverter input 1. This method calls
        get_output_data() to fetch the output data from the device, specifically looking for the
        'e1' value, which represents the energy in kilowatt-hours (kWh) generated by inverter input 1.

        :return: The 'e1' value as a float, representing the total energy generated today in kWh by
                 inverter input 1. If the 'e1' value is not found in the output data, None is returned,
                 and a message is printed indicating the missing value.

        Note: This method assumes that the 'e1' value in the output data is a number or can be
        converted to a float. If the 'e1' value is missing, the method alerts the user and does
        not perform the conversion.
        """
        e1_value = self.get_output_data()['data']['e1']
        if e1_value is not None:
            return float(e1_value)
        else:
            print("e1 value not found in the output data.")

    def get_p2_energy_today(self):
        """
        Retrieves the total energy generated today by inverter input 2. This method calls
        get_output_data() to fetch the output data from the device, specifically looking for the
        'e2' value, which represents the energy in kilowatt-hours (kWh) generated by inverter input 2.

        :return: The 'e2' value as a float, representing the total energy generated today in kWh by
                 inverter input 2. If the 'e2' value is not found in the output data, None is returned,
                 and a message is printed indicating the missing value.

        Note: This method assumes that the 'e2' value in the output data is a number or can be
        converted to a float. If the 'e2' value is missing, the method alerts the user and does
        not perform the conversion.
        """
        e2_value = self.get_output_data()['data']['e2']
        if e2_value is not None:
            return float(e2_value)
        else:
            print("e2 value not found in the output data.")

    def get_total_energy_today(self):
        """
        Retrieves and calculates the total energy generated today by both inverter inputs, 1 and 2.
        This method first calls get_output_data() to fetch the output data from the device, which
        includes individual energy readings for 'e1' and 'e2', each representing the energy in
        kilowatt-hours (kWh) generated by the respective inverter inputs.

        :return: The sum of the energy readings 'e1' and 'e2' as a float, representing the total energy
                 generated today in kWh by both inverter inputs. If either 'e1' or 'e2' value is not
                 found in the output data, None is returned, and a message is printed indicating the
                 missing value.

        Note: This method assumes that the 'e1' and 'e2' values in the output data are numbers or can
        be converted to floats. If either of these values is missing, the method alerts the user and
        does not perform the summation.
        """
        data = self.get_output_data()
        e1_value = data['data']['e1']
        e2_value = data['data']['e2']
        if e1_value is not None and e2_value is not None:
            return float(e1_value) + float(e2_value)
        else:
            print("e1 or e2 value not found in the output data.")

    def get_p1_energy_lifetime(self):
        """
        Retrieves the total lifetime energy generated by inverter input 1. This method calls
        get_output_data() to fetch the output data from the device, specifically looking for the
        'te1' value. The 'te1' represents the total lifetime energy generated by inverter input 1,
        reported in kilowatt-hours (kWh).

        :return: The 'te1' value as a float, indicating the total lifetime energy in kWh generated
                 by inverter input 1. If the 'te1' value is not found in the output data, None is
                 returned, and a message is printed indicating the missing value.

        Note: This method assumes that the 'te1' value in the output data is a number or can be
        converted to a float. If the 'te1' value is missing, the method alerts the user and does
        not perform the conversion.
        """
        te1_value = self.get_output_data()['data']['te1']
        if te1_value is not None:
            return float(te1_value)
        else:
            print("te1 value not found in the output data.")

    def get_p2_energy_lifetime(self):
        """
        Retrieves the total lifetime energy generated by inverter input 2. This method calls
        get_output_data() to fetch the output data from the device, specifically looking for the
        'te2' value. The 'te2' represents the total lifetime energy generated by inverter input 2,
        reported in kilowatt-hours (kWh).

        :return: The 'te2' value as a float, indicating the total lifetime energy in kWh generated
                 by inverter input 2. If the 'te2' value is not found in the output data, None is
                 returned, and a message is printed indicating the missing value.

        Note: This method assumes that the 'te2' value in the output data is a number or can be
        converted to a float. If the 'te2' value is missing, the method alerts the user and does
        not perform the conversion.
        """
        te2_value = self.get_output_data()['data']['te2']
        if te2_value is not None:
            return float(te2_value)
        else:
            print("te2 value not found in the output data.")

    def get_total_energy_lifetime(self):
        """
        Retrieves and calculates the total lifetime energy generated by both inverter inputs 1 and 2.
        This method first calls get_output_data() to fetch the output data from the device, which
        includes individual lifetime energy readings for 'te1' and 'te2'. Each of these values
        represents the total lifetime energy generated by the respective inverter inputs, reported
        in kilowatt-hours (kWh).

        :return: The sum of the lifetime energy readings 'te1' and 'te2' as a float, representing the
                 total lifetime energy in kWh generated by both inverter inputs. If either 'te1' or
                 'te2' value is not found in the output data, None is returned, and a message is
                 printed indicating the missing value.

        Note: This method assumes that the 'te1' and 'te2' values in the output data are numbers or can
        be converted to floats. If either of these values is missing, the method alerts the user and
        does not perform the summation.
        """
        data = self.get_output_data()
        te1_value = data['data']['te1']
        te2_value = data['data']['te2']
        if te1_value is not None and te2_value is not None:
            return float(te1_value) + float(te2_value)
        else:
            print("te1 or te2 value not found in the output data.")

    def get_max_power(self):
        """
        Retrieves the set maximum power setting of the device. This method makes a request to the
        "getMaxPower" endpoint and returns a dictionary containing the maximum power limit of the device set by the user.

        The 'data' field in the returned dictionary includes the 'maxPower' key, representing the maximum
        power output that the device is set to, measured in watts.

        :return: A dictionary with the following structure:
                 {
                     'data': {
                         'maxPower': [Maximum set power limit of the device, in watts, as a string]
                     },
                     'message': [Status message indicating 'SUCCESS' or 'FAILED'],
                     'deviceId': [Device ID as a string]
                 }

        The key in the 'data' object is:
        - 'maxPower': Indicates the maximum power output set for the device in watts.
        """
        return self._request("getMaxPower")

    def set_max_power(self, power_limit):
        """
        Sets the maximum power limit of the device. This method sends a request to the "setMaxPower"
        endpoint with the specified power limit as a parameter. The power limit must be an integer
        within the range of 30 to 800 watts.

        If the provided power limit is outside this range, the method raises a ValueError.

        :param power_limit: The desired maximum power setting for the device, in watts.
                            Must be an integer between 30 and 800.
        :return: A dictionary with the following structure if the power limit is successfully set:
                 {
                     'data': {
                         'maxPower': [Set maximum power setting of the device, in watts, as a string]
                     },
                     'message': [Status message indicating 'SUCCESS' or 'FAILED'],
                     'deviceId': [Device ID as a string]
                 }
        :raises ValueError: If 'power_limit' is not within the range of 30 to 800.

        The key in the 'data' object is:
        - 'maxPower': Indicates the newly set maximum power output of the device in watts.
        """
        if 30 <= int(power_limit) <= 800:
            return self._request("setMaxPower?p=" + str(power_limit), method='GET')
        else:
            raise ValueError("Invalid setMaxPower value: expected int between '30' and '800', got '" + str(power_limit) + "'")

    def get_device_power_status(self):
        """
        Retrieves the current power status of the device. This method sends a request to the
        "getOnOff" endpoint and returns a dictionary containing the power status of the device.

        The 'data' field in the returned dictionary includes the 'status' key, representing the
        current power status of the device, where '0' indicates that the device is on, and '1'
        indicates that it is off.

        :return: A dictionary with the following structure:
                 {
                     'data': {
                         'status': [Current power status of the device, '0' for on, '1' for off, as a string]
                     },
                     'message': [Status message indicating 'SUCCESS' or 'FAILED'],
                     'deviceId': [Device ID as a string]
                 }

        The key in the 'data' object is:
        - 'status': Indicates the current power status of the device, with '0' meaning the device is on
                    and '1' meaning the device is off.
        """
        return self._request("getOnOff")

    def set_device_power_status(self, power_status):
        """
        Sets the power status of the device to either on or off. This method sends a request to the
        "setOnOff" endpoint with a specified power status parameter. The power status accepts multiple
        string representations: '0' or 'ON' to start the inverter, and '1', 'SLEEP', or 'OFF' to stop
        the inverter.

        If the provided power status does not match any of the accepted representations, the method
        raises a ValueError with a descriptive message.

        :param power_status: The desired power status for the device, specified as '0', 'ON' for
                             starting the inverter, or '1', 'SLEEP', 'OFF' for stopping it.
        :return: A dictionary with the following structure if the power status is successfully set:
                 {
                     'data': {
                         'status': [Set power status of the device, '0' for on, '1' for off, as a string]
                     },
                     'message': [Status message indicating 'SUCCESS' or 'FAILED'],
                     'deviceId': [Device ID as a string]
                 }
        :raises ValueError: If 'power_status' does not match the accepted values. The error message
                            explains the valid values and their meanings.

        Note: Internally, the method treats '0' and 'ON' as equivalent, both setting the power status
        to '0'. Similarly, '1', 'SLEEP', and 'OFF' are treated as equivalent, setting the power status
        to '1'.
        """
        if str(power_status) == "1" or str(power_status) == "SLEEP" or str(power_status) == "OFF":
            return self._request("setOnOff?status=1", method='GET')
        if str(power_status) == "0" or str(power_status) == "ON":
            return self._request("setOnOff?status=0", method='GET')
        else:
            raise ValueError("Invalid power status: expected '0', 'ON' or '1','SLEEP' or 'OFF', got '" + str(
                power_status) + "'\n Set '0' or 'ON' to start the inverter | Set '1' or 'SLEEP' or 'OFF' to stop the inverter.")