# This file is part of PySunsSpec-Read
#
# PySunSpec-Read is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     PySunSpec-Read is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with PySunSpec-Read.  If not, see <https://www.gnu.org/licenses/>.
#
# Copyright 2020 David Smith applies to this and each file in this project
import logging
from datamx.utils.groups_util import write_groups_with_dated_filename
from sunspec.core import client as client
from .options import ConnectOptions, ReadOptions
from .to_datamx import to_datamx

logger = logging.getLogger(__name__)

class Reader:

    def read(self, connect_options: ConnectOptions, read_options: ReadOptions = None):
        self.connect(connect_options)
        logger.info("Reading from inverter")
        self.client.read()
        data = to_datamx(self.client, read_options)
        self.client.close()
        if read_options is not None and read_options.output_path is not None:
            write_groups_with_dated_filename(data, read_options.output_path)
        return data

    def connect(self, connect_options: ConnectOptions):
        logger.info("Connecting to inverter ip: %s, port: %s, slave_id: %s, device_type: %s, ", connect_options.ip_address,
                    connect_options.ip_port, connect_options.slave_id, connect_options.device_type)

        if connect_options.device_type.lower() == client.TCP.lower():
            self.client = client.SunSpecClientDevice(client.TCP, connect_options.slave_id, connect_options.name, connect_options.pathlist,
                                                     connect_options.baudrate, connect_options.parity, connect_options.ip_address, connect_options.ip_port,
                                                     connect_options.timeout, connect_options.trace, connect_options.scan_progress, connect_options.scan_delay)
        elif connect_options.device_type.lower() == client.RTU.lower():
            self.client =  client.SunSpecClientDevice(client.RTU, connect_options.slave_id, connect_options.name, connect_options.pathlist, connect_options.baudrate,
                                                      connect_options.parity, connect_options.ip_address, connect_options.ip_port,
                                                      connect_options.timeout, connect_options.trace, connect_options.scan_progress, connect_options.scan_delay)
        elif connect_options.device_type.lower() == client.MAPPED.lower():
            self.client =  client.SunSpecClientDevice(client.MAPPED, connect_options.slave_id, connect_options.name, connect_options.pathlist, connect_options.baudrate,
                                                      connect_options.parity, connect_options.ip_address, connect_options.ip_port,
                                                      connect_options.timeout, connect_options.trace, connect_options.scan_progress, connect_options.scan_delay)
        else:
            raise NameError("Unknown device type " + connect_options.device_type)