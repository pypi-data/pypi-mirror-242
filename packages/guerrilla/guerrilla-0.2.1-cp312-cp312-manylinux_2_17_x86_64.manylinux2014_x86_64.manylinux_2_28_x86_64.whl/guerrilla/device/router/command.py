from enum import Enum

import comm
from termcolor import RESET

"""
Commands for Router Platform.
"""

class Commands:
    class SHOW(Enum):
        SYSTEM = "show system"
        VERSION = "show version"
        USERS = "show users"
        AUTO_BACKUP = "show auto-backup"
        PORT = "show port"
        CONFIG_FILE = "show config-file"
        CLOCK = "show clock"
        NTP_AUTH_KEYS = "show ntp-auth-keys"
        SETTING_CHECK = "show settingcheck"
        ARP = "show arp"

        class IP(Enum):
            PROXY_ARP = "show ip proxy-arp"
            DHCP = "show ip dhcp"
            AUTO_ASSIGN = "show ip auto-assign"
            DHCP_RELAY = "show ip dhcp-relay"
            DDNS = "show ip ddns"
            ROUTE = "show ip route"
            RIP = "show ip rip"
            OSPF = "show ip ospf"
            class MROUTE(Enum):
                KERNEL = "show ip mroute kernel"
                STATIC = "show ip mroute static"
                
            BROADCAST_FORWARD = "show ip broadcast-forward"
            DIRECTED_BROADCAST = "show ip directed-broadcast"
            NAT = "show ip nat"
            IGMP = "show ip igmp"
            HTTP_SERVER = "show ip http-server"
            TELNET = "show ip telnet"

        class INTERFACES(Enum):
            """Commands related to interfaces."""

            ETHERNET = "show interfaces ethernet"
            COUNTERS = "show interfaces counters"
            TRUNK = "show interfaces trunk"
            TRUSTED_ACCESS = "show interfaces trusted-access"
            BRIDGE = "show interfaces bridge"
            ZONE_BASE_BRIDGE = "show interfaces zone-base-bridge"
            LAN = "show interfaces lan"
            WAN = "show interfaces wan"
            VLAN = "show interfaces vlan"

        class AUTH(Enum):
            MODE = "show auth mode"
            RADIUS = "show auth radius"
            TACACS = "show auth tacacs"

    class MAIN(Enum):
        EXIT = "exit"
        CONFIGURE = "configure"
        RELOAD = "reload"
        RELOAD_FACTORY_DEFAULT = "reload factory-default"
        RELOAD_FACTORY_DEFAULT_WITHOUT_CERT = "reload factory-default no cert"

    class CONFIG:
        
        class HOSTNAME:
            RESET = "no hostname"
            def SET(hostname) -> str:
                return f"hostname {hostname}"      
        class USER:
            def ADD(username, password, privilege) -> str:
                return f"username {username} password {password} privilege {privilege}"
            
            def MODIFY(username, password, privilege) -> str:
                command: str = f'username {username}'
                if password:
                    command += f' password {password}'
                if privilege is not None:
                    command += f' privilege {privilege}'
                return command
            
            def DELETE(username) -> str:
                return f"no username {username}"
        class SNMP:
            RESET_CONTACT = "no snmp-server contact"
            RESET_DESCRIPTION = "no snmp-server description"
            RESET_LOCATION = "no snmp-server location"
            
            def CONTACT(contact) -> str:
                return f"snmp-server contact {contact}"
            
            def DESCRIPTION(description) -> str:
                return f"snmp-server description {description}"
            
            def LOCATION(location) -> str:
                return f"snmp-server location {location}"
        class CLOCK:
            RESET_TIMEZONE = "no clock timezone"
            RESET_SUMMER_TIME = "no clock summer-time"
            
            def TIMEZONE(offset_hour) -> str:
                return f'clock timezone gmt {offset_hour}'
            
            def SUMMER_START_TIME(month, week, day, hh, mm) -> str:
                return f'clock summer-time start-date {month} {week} {day} {hh} {mm}'
            
            def SUMMER_END_TIME(month, week, day, hh, mm) -> str:
                return f'clock summer-time end-date {month} {week} {day} {hh} {mm}'
            
            def SUMMER_TIME_OFFSET(offset_hour) -> str:
                return f'clock summer-time offset {offset_hour}'
            
            def SET(hh, mm, ss, month, day, year) -> str:
                return f'clock set {hh}:{mm}:{ss} {month} {day} {year}'
        
        class AUTOBACKUP:
            ENABLE_CONFIG = "auto-backup config"
            DISABLE_CONFIG = "no auto-backup config"
            ENANBLE_AUTOBACKUP = "auto-backup enable"
            DISABLE_AUTOBACKUP = "no auto-backup enable"
            ENABLE_AUTO_LOAD_CONFIG = "auto-backup auto-load config"
            DISABLE_AUTO_LOAD_CONFIG = "no auto-backup auto-load config"
        
        class FIRMWARECHECK:
            ENABLE = "config-fwr-ver-check"
            DISABLE = "no config-fwr-ver-check"
        
        class PASSWORDPOLICY:
            def SET_LENGTH(length: int) -> str:
                return f'password-policy minimum-length {length}'
            
            RESET_LENGTH =  'no password-policy minimum-length'
            
            ENABLE_COMPLEXITY =  'password-policy complexity-check'
            
            DISABLE_COMPLEXITY = 'no password-policy complexity-check'
            
            def SET_COMPLEXITY(complexity_rule: str) -> str:
                return f'password-policy complexity-check {complexity_rule}'
            
            def RESET_COMPLEXITY(complexity_rule: str) -> str:
                return f'no password-policy complexity-check {complexity_rule}'
            
            def SET_MAXLIFE_TIME(maxlife_time: int) -> str:
                
                return f'password-policy password max-life-time {maxlife_time}'
        
        class IP:
            class HTTPSERVER:
                ENABLE = "ip http-server"
                DISABLE = "no ip http-server"
                ENABLE_HTTPS = "ip http-server secure"
                DISABLE_HTTPS = "no ip http-server secure"
                RESET_MAX_LOGIN_USERS = "no ip http-server max-login-users"
                
                def SET_HTTP_PORT(port: int) -> str:
                    return f'ip http-server port {port}'
                
                def SET_HTTPS_PORT(port: int) -> str:
                    return f'ip http-server secure port {port}'
                
                def SET_MAX_LOGIN_USERS(max_login_users: int) -> str:
                    return f'ip http-server max-login-users {max_login_users}'
                
            class TELNET:
                ENABLE = "ip telnet"
                DISABLE = "no ip telnet"
                RESET_MAX_LOGIN_USERS = "no ip telnet max-login-users"
                
                def SET_PORT(port: int) -> str:
                    return f'ip telnet port {port}'

                def SET_MAX_LOGIN_USERS(max_login_users: int) -> str:
                    return f'ip telnet max-login-users {max_login_users}'
        
            class SSH:
                ENABLE = "ip ssh"
                DISABLE = "no ip ssh"
                
                def SET_PORT(port: int) -> str:
                    return f'ip ssh port {port}'
            
            class PING:
                ENABLE = "ip ping-response"
                DISABLE = "no ip ping-response"
        
        
        @staticmethod
        def COPY(transfer_method, ip, cfg_path_name, account, password, command_type) -> str:
            """
            Constructs the command to be executed based on the transfer method and other details.
            """
            method: str = transfer_method.lower()
            command: str = "copy "
            if method == 'tftp':
                command += f"tftp {ip} {command_type} {cfg_path_name}"
            elif method in ['scp', 'sftp']:
                command += f"{method} {account} {password} {ip} {command_type} {cfg_path_name}"
            elif method == 'usb':
                command += f"usb {cfg_path_name}"
            else:
                # Not support method, but don't raise error here, let the router cli handle and catch it.
                pass

            
            return command
            
        @staticmethod
        def EXPORT(transfer_method, ip, cfg_path_name, account, password) -> str | None:
            method: str = transfer_method.lower()
            command: str = "copy running-config "
            if method == 'tftp':
                command += f"tftp {ip} {cfg_path_name}"
            elif method in ('scp', 'sftp'):
                command += f"{method} {account} {password} {ip} {cfg_path_name}"
            elif method == 'usb':
                command += f"usb {cfg_path_name}"
            else:
                # Not supported method, but don't raise error here, let the router CLI handle and catch it.
                pass

                
            return command
                
