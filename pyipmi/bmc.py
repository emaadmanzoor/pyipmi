# Copyright (c) 2012, Calxeda Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of Calxeda Inc. nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.


"""Stuff about BMC's"""

__all__ = ['BMC', 'BMCInfo', 'BMCGuid', 'BMCEnables', 'LanBMC']

class BMCResult(object):
    """superclass for BMC result objects

    Sets attribute names from a dict passed to init, and allows comparison
    with other results based on dict equality.
    """
    def __init__(self, **entries):
        """each kwarg's value to an attribute of the same name"""
        self.__dict__.update(entries)

    def __eq__(self, other):
        """BMCInfo's are equivalent if their attributes are the same"""
        return self.__dict__ == other.__dict__


class BMCInfo(BMCResult):
    """Describes a BMC info record result

    "bmc info" is just the ipmitool name - this is really "get device id"
    """
    device_id = None
    device_revision = None
    firmware_revision = None
    ipmi_version = None
    is_chassis_device = None
    is_bridge = None
    is_ipmb_event_generator = None
    is_ipmb_event_receiver = None
    is_fru_inventory_device = None
    is_sel_device = None
    is_sdr_repository_device = None
    is_sensor_device = None
    manufacturer_id = None
    product_id = None
    device_available = None
    aux_firmware_revision_info = None

class BMCGuid(BMCResult):
    """Result record for bmc guid command

    this is really "get device guid" - bmc guid is the ipmitool command name.
    """
    system_guid = None
    time_stamp = None

class BMCEnables(BMCResult):
    """Result record for get command enables

    The names for the attributes here come from the command line syntax for ipmitool
    """
    recv_msg_intr = None
    event_msg_intr = None
    event_msg = None
    system_event_log = None
    oem0 = None
    oem1 = None
    oem2 = None

class BMCResetResult(BMCResult):
    """Result record for bmc reset command"""
    pass

class BMC(object):
    """A BMC - what you're talking to when you're talking IPMI

    I think this should ultimately be the interface for all commands issued
    from IPMI.. or maybe just commands "about the bmc". This needs to be
    resolved!
    """
    def __init__(self, handle_class, tool_class, command_list):
        """
        Arguments:
        handle_class -- class to use for Handles created
        tool_class -- class to use for the Tool for each handle
        command_list -- the list of commands available for this BMC
        """
        self.handle = handle_class(self, tool_class, command_list)

    def info(self):
        """Get the BMC's info"""
        return self.handle.get_device_id()

    def selftest(self):
        """Get BMC self test results"""
        return self.handle.selftest()

    def bmc_reset(self, type='warm'):
        return self.handle.bmc_reset(type=type)

    def guid(self):
        """Get the BMC's guid"""
        return self.handle.get_system_guid()

    def sdr_list(self):
        """Get a list of SDR's for the BMC"""
        return self.handle.get_sdr_list()

    def enables(self):
        """Return a BMCEnables object for the BMC"""
        return self.handle.get_command_enables()

    def set_chassis_power(self, mode):
        return self.handle.chassis_control(mode=mode)

    def set_chassis_policy(self, state):
        return self.handle.chassis_policy(state=state)

    def get_chassis_status(self):
        return self.handle.chassis_status()

    def update_socman(self, filename, partition, tftp_addr):
        return self.update_firmware(filename, partition, '3', tftp_addr)

    def update_firmware(self, filename, partition, image_type, tftp_addr):
        return self.handle.fw_download(filename=filename, partition=partition,
                                       image_type=image_type,
                                       tftp_addr=tftp_addr)


    def retrieve_firmware(self, filename, partition, image_type, tftp_addr):
        return self.handle.fw_upload(filename=filename, partition=partition,
                                     image_type=image_type,
                                     tftp_addr=tftp_addr)

    def register_firmware_read(self, filename, partition, image_type):
        return self.handle.fw_register_read(filename=filename,
                                            partition=partition,
                                            image_type=image_type)

    def register_firmware_write(self, filename, partition, image_type):
        return self.handle.fw_register_write(filename=filename,
                                             partition=partition,
                                             image_type=image_type)

    def activate_firmware(self, partition):
        return self.handle.fw_activate(partition=partition)

    def invalidate_firmware(self, partition):
        return self.handle.fw_invalidate(partition=partition)

    def set_firmware_flags(self, partition, flags):
        return self.handle.fw_flags(partition=partition, flags=flags)

    def get_firmware_status(self, tftp_handle):
        return self.handle.fw_status(tftp_handle=tftp_handle)

    def check_firmware(self, partition):
        return self.handle.fw_check(partition=partition)

    def cancel_firmware(self, job_id):
        return self.handle.fw_cancel(job_id=job_id)

    def update_raw_firmware(self, filename, offset, size, tftp_addr):
        return self.handle.fw_put(filename=filename, offset=offset,
                                  size=size, tftp_addr=tftp_addr)

    def retrieve_raw_firmware(self, filename, offset, size, tftp_addr):
        return self.handle.fw_get(filename=filename, offset=offset,
                                  size=size, tftp_addr=tftp_addr)

    def get_firmware_info(self):
        return self.handle.fw_info()

    def reset_firmware(self):
        return self.handle.fw_reset()

    def set_firmware_version(self, version):
        return self.handle.fw_version(version=version)

    def get_sel_time(self):
        """Get the time for the SEL"""
        return self.handle.get_sel_time()

    def set_sel_time(self, time):
        """Set the time for the SEL"""
        return self.handle.set_sel_time(time=time)

    def sel_info(self):
        """Get SEL info"""
        return self.handle.sel_info()

    def sel_alloc_info(self):
        """Get SEL alloc info"""
        return self.handle.sel_alloc_info()

    def sel_add(self, *records):
        """Add records to the SEL"""
        return self.handle.sel_add(records=records)

    def sel_get(self, *record_ids):
        """Get SEL Records"""
        return self.handle.sel_get(record_ids=record_ids)

    def sel_list(self):
        """List SEL entries"""
        return self.handle.sel_list()

    def sel_elist(self):
        """Extended SEL list"""
        return self.handle.sel_elist()

    def sel_clear(self):
        """Clear the SEL"""
        return self.handle.sel_clear()

    def set_sol_config_param(self, param, value):
        """Set SOL Configuration Parameter"""
        return self.handle.set_sol_config_params(param=param, value=value)

    def get_sol_config_params(self, *params):
        """Get SOL Configuration Parameters"""
        return self.handle.get_sol_config_params(params=params)

    def activate_payload(self):
        """Activate an SOL session"""
        return self.handle.activate_payload()

    def deactivate_payload(self):
        """Deactivate an SOL session"""
        return self.handle.deactivate_payload()

    def dcmi_get_capabilities(self):
        return self.handle.dcmi_get_capabilities()

    def dcmi_set_asset_tag(self, tag):
        return self.handle.dcmi_set_asset_tag(tag=tag)

    def dcmi_get_asset_tag(self):
        return self.handle.dcmi_get_asset_tag()

    def dcmi_get_controller_id(self):
        return self.handle.dcmi_get_controller_id()

    def dcmi_set_controller_id(self, controller):
        return self.handle.dcmi_set_controller_id(controller=controller)

    def dcmi_get_sensor_info(self):
        return self.handle.dcmi_get_sensor_info()

    def dcmi_get_power_statistics(self):
        return self.handle.dcmi_get_power_statistics()

    def dcmi_get_power_limit(self):
        return self.handle.dcmi_get_power_limit()

    def dcmi_set_power_limit(self):
        return self.handle.dcmi_set_power_limit()

    def dcmi_power_limit_requested(self, limit, exception=None):
        return self.handle.dcmi_power_limit_requested(limit=limit, exception=exception)

    def dcmi_correction_time_limit(self, time_limit, exception=None):
        return self.handle.dcmi_correction_time_limit(time_limit=time_limit, exception=exception)

    def dcmi_statistics_sampling_period(self, period, exception=None):
        return self.handle.dcmi_statistics_sampling_period(period=period, exception=exception)


    def dcmi_activate_power_limit(self, action):
        if action != "activate" and action != "deactivate":
            raise Exception("Invalid argument to dcmi_activate_power_limit: %s" % action)
        return self.handle.dcmi_activate_power_limit(action=action)

    def pef_get_info(self):
        return self.handle.pef_get_info()

    def pef_get_status(self):
        return self.handle.pef_get_status()

    def pef_get_policies(self):
        return self.handle.pef_get_policies()

    def pef_list_entries(self):
        return self.handle.pef_list_entries()

    def pef_config_get_info(self):
        return self.handle.pef_config_info()

    def pef_checkout(self, section=None, filename=None, key=None):
        return self.handle.pef_checkout(section=section, filename=filename,
                                        key=key)

    def pef_commit(self, section=None, filename=None, key_value_pair=None):
        return self.handle.pef_commit(section=section, filename=filename,
                                        key_value_pair=key_value_pair)

    def pef_diff(self, section=None, filename=None, key=None):
        return self.handle.pef_diff(section=section, filename=filename,
                                        key=key)

    def pef_list_sections(self):
        return self.handle.pef_list_sections()

    def generate_generic_event(self, event_type):
        return self.handle.generic_event(event_type=event_type)

    def generate_sensor_event(self, sensor_id, state):
        return self.handle.assert_sensor_event(sensor_id=sensor_id,
                                               state=state)

    def get_watchdog_status(self):
        return self.handle.watchdog_get()

    def reset_watchdog(self):
        return self.handle.watchdog_reset()

    def disable_watchdog(self):
        return self.handle.watchdog_off()

    def fru_get_inventory(self):
        return self.handle.fru_print()

    def fru_read(self, fru_id, filename):
        return self.handle.fru_read(fru_id=fru_id, filename=filename)

    def fru_write(self, fru_id, filename):
        return self.handle.fru_write(fru_id=fru_id, filename=filename)

    def fru_upg_e_key(self, fru_id, filename):
        return self.handle.fru_upg_e_key(fru_id=fru_id, filename=filename)

    def fru_show(self, filename):
        return self.handle.fru_show(filename=filename)

    def lan_print(self, channel=''):
        return self.handle.lan_print(channel=channel)

    def lan_set(self, channel, command, param):
        return self.handle.lan_set(channel=channel, command=command,
                                   param=param)

    def channel_info(self):
        return self.handle.channel_info()

    def channel_get_access(self, channel, userid=""):
        return self.handle.channel_get_access(channel=channel, userid=userid)

    def channel_set_access(self, channel, userid, callin=None, ipmi=None,
                           link=None, priv_level=None):
        return self.handle.channel_set_access(channel=channel, userid=userid,
                                              callin=callin, ipmi=ipmi,
                                              link=link, priv_level=priv_level)

    def channel_get_ciphers(self, mode='ipmi'):
        return self.handle.channel_get_ciphers(mode=mode)

    def user_list(self, channel=None):
        return self.handle.user_list(channel=channel)

    def user_set_name(self, userid, name):
        return self.handle.user_set_name(userid=userid, name=name)

    def user_set_password(self, userid, password=None):
        return self.handle.user_set_password(userid=userid, password=password)

    def user_enable(self, userid):
        return self.handle.user_enable(userid=userid)

    def user_disable(self, userid):
        return self.handle.user_disable(userid=userid)

    def user_priv(self, userid, priv_level, channel=None):
        return self.handle.user_priv(userid=userid, priv_level=priv_level,
                                     channel=channel)
    """Fabric commands

    In pyipmi/fabric.py, these commands are mapped to classes that 
    are subclasses of the Command class. Those subclasses contain the
    string arguments that are run by pyipmi/ipmitool.py

    """
    def fabric_update_config(self):
        return self.handle.fabric_updateconfig()

    def fabric_get_node_id(self):
        return self.handle.fabric_getnodeid()

    def fabric_get_ip_addr(self, nodeid="", iface=""):
        return self.handle.fabric_getipaddr(nodeid=nodeid, iface=iface)

    def fabric_get_mac_addr(self, nodeid="", iface=0):
        return self.handle.fabric_getmacaddr(nodeid=nodeid, iface=iface)

    def fabric_get_linkspeed(self, link=None, actual=None):
        return self.handle.fabric_getlinkspeed(link=link, actual=actual)

    def fabric_get_linkstats(self, filename=None, tftp_addr=None, link=None):
        return self.handle.fabric_getlinkstats(
            filename=filename,
            tftp_addr=tftp_addr,
            link=link
        )

    def fabric_get_linkmap(self, filename, tftp_addr=None):
        return self.handle.fabric_getlinkmap(filename=filename,
                                             tftp_addr=tftp_addr)

    def fabric_get_routingtable(self, filename, tftp_addr=None):
        return self.handle.fabric_getroutingtable(filename=filename,
                                                  tftp_addr=tftp_addr)

    def fabric_get_depthchart(self, filename, tftp_addr=None):
        return self.handle.fabric_getdepthchart(filename=filename,
                                                tftp_addr=tftp_addr)

    def fabric_add_macaddr(self, iface, macaddr, nodeid=None):
        return self.handle.fabric_addmacaddr(nodeid=nodeid, iface=iface, macaddr=macaddr)

    def fabric_rm_macaddr(self, iface, macaddr, nodeid=None):
        return self.handle.fabric_rmmacaddr(nodeid=nodeid, iface=iface, macaddr=macaddr)

    def fabric_get_uplink_speed(self):
        return self.handle.fabric_getuplinkspeed()

    def fabric_get_uplink_info(self):
        return self.handle.fabric_getuplinkinfo()

    """Fabric config commands

    In pyipmi/fabric_config.py, these commands are mapped to classes that 
    are subclasses of the Command class. Those subclasses contain the
    string arguments that are run by pyipmi/ipmitool.py

    """

    def fabric_config_update_config(self):
        return self.handle.fabric_config_updateconfig()

    def fabric_config_get_ip_info(self, filename, tftp_addr=None):
        return self.handle.fabric_config_getipinfo(filename=filename,
                                            tftp_addr=tftp_addr)

    def fabric_config_get_mac_addresses(self, filename, tftp_addr=None):
        return self.handle.fabric_config_getmacaddresses(filename=filename,
                                                  tftp_addr=tftp_addr)

    def fabric_config_get_uplink_info(self, filename, tftp_addr=None):
        return self.handle.fabric_config_getuplinkinfo(filename=filename,
                                                  tftp_addr=tftp_addr)

    def fabric_config_get_ip_src(self):
        return self.handle.fabric_config_getipsrc()

    def fabric_config_set_ip_src(self, ipsrc_mode):
        return self.handle.fabric_config_setipsrc(ipsrc_mode=ipsrc_mode)

    def fabric_config_factory_default(self):
        return self.handle.fabric_config_factory_default()

    def fabric_config_get_ip_addr_base(self):
        return self.handle.fabric_config_get_ipaddr_base()

    def fabric_config_set_ipaddr_base(self, ipaddr):
        return self.handle.fabric_config_set_ipaddr_base(ipaddr=ipaddr)

    def fabric_config_get_linkspeed(self):
        return self.handle.fabric_config_getlinkspeed()

    def fabric_config_set_linkspeed(self, linkspeed):
        return self.handle.fabric_config_setlinkspeed(linkspeed=linkspeed)

    def fabric_config_get_linkspeed_policy(self):
        return self.handle.fabric_config_getlinkspeedpolicy()

    def fabric_config_set_linkspeed_policy(self, ls_policy):
        return self.handle.fabric_config_setlinkspeedpolicy(ls_policy=ls_policy)

    def fabric_config_get_uplink(self, iface=0):
        return self.handle.fabric_config_getuplink(iface=iface)

    def fabric_config_set_uplink(self, uplink=0, iface=0):
        return self.handle.fabric_config_setuplink(uplink=uplink, iface=iface)

    def fabric_config_get_link_users_factor(self):
        return self.handle.fabric_config_getlinkusersfactor()

    def fabric_config_set_link_users_factor(self, lu_factor):
        return self.handle.fabric_config_setlinkusersfactor(lu_factor=lu_factor)

    def fabric_config_set_macaddr_base(self, macaddr):
        return self.handle.fabric_config_set_macaddr_base(macaddr=macaddr)

    def fabric_config_get_macaddr_base(self):
        return self.handle.fabric_config_get_macaddr_base()

    def fabric_config_set_macaddr_mask(self, mask):
        return self.handle.fabric_config_set_macaddr_mask(mask=mask)

    def fabric_config_get_macaddr_mask(self):
        return self.handle.fabric_config_get_macaddr_mask()

    def fabric_config_set_netmask(self, netmask):
        return self.handle.fabric_config_set_netmask(netmask=netmask)

    def fabric_config_set_defgw(self, ipaddr):
        return self.handle.fabric_config_set_defgw(ipaddr=ipaddr)

    def set_bootdev(self, device, options=None):
        return self.handle.bootdev_set(device=device, options=options)

    def get_bootdev(self):
        return self.handle.bootdev_get()

    def get_bootparam(self, param):
        return self.handle.bootparam_get(param=param)

    def mc_reset(self, mode):
        return self.handle.mc_reset(mode=mode)

    def mem_read(self, length, address, fmt=None):
        return self.handle.data_memread(length=length, addr=address,
                                        fmt=fmt)

    def mem_write(self, length, address, value):
        return self.handle.data_memwrite(length=length, addr=address,
                                         value=value)

    def cdb_read(self, length, cid, fmt=None):
        return self.handle.data_cdbread(length=length, cid=cid,
                                        fmt=fmt)

    def cdb_write(self, length, cid, value):
        return self.handle.data_cdbwrite(length=length, cid=cid,
                                         value=value)

    def get_info_basic(self):
        return self.handle.info_basic()

    def get_info_card(self):
        return self.handle.info_card()

    #
    # fabric info commands
    #

    def fabric_info_get_routing_table(self, filename, tftp_addr=None):
        return self.handle.fabric_info_getroutingtable(filename=filename,
                                                       tftp_addr=tftp_addr)

    def fabric_info_get_link_map(self, filename, tftp_addr=None):
        return self.handle.fabric_info_getlinkmap(filename=filename,
                                                  tftp_addr=tftp_addr)

    def fabric_info_get_depth_chart(self, filename, tftp_addr=None):
        return self.handle.fabric_info_getdepthchart(filename=filename,
                                                     tftp_addr=tftp_addr)

    def pmic_get_version(self):
        return self.handle.pmic_get_version()


class LanBMC(BMC):
    """A BMC that's accessed over the LAN"""
    def __init__(self,
                    hostname,
                    username=None,
                    password=None,
                    authtype=None,
                    level=None,
                    port=623,
                    interface='lan',
                    **kwargs):

        self.params = {
            'hostname' : hostname,
            'username' : username,
            'password' : password,
            'authtype' : authtype,
            'level'    : level,
            'port'     : port,
            'interface' : interface
        }

        super(LanBMC, self).__init__(**kwargs)
