from dataclasses import dataclass, field
from .hostname import Hostname
from .clock import Clock
from .snmp import Snmp
from .backup import AutoBackup
from .user import User
from .firmware_check import ConfigFirmwareCheck
from .password_policy import PasswordPolicy
from .ip_http_server import IpHttpServer
from .ip_telnet import IpTelnet
from .ip_ssh import IpSSH
from .ip_ping_response import IpPingResponse

@dataclass
class MainConfig:
    hostname: Hostname = field(default_factory=Hostname, init=False)
    clock: Clock = field(default_factory=Clock, init=False)
    snmp: Snmp = field(default_factory=Snmp, init=False)
    auto_backup: AutoBackup = field(default_factory=AutoBackup, init=False)
    user: User = field(default_factory=User, init=False)
    config_fwr_ver_check: ConfigFirmwareCheck = field(default_factory=ConfigFirmwareCheck, init=False)
    password_policy: PasswordPolicy = field(default_factory=PasswordPolicy, init=False)
    ip_http_server: IpHttpServer = field(default_factory=IpHttpServer, init=False)
    ip_telnet: IpTelnet = field(default_factory=IpTelnet, init=False)
    ip_ssh: IpSSH = field(default_factory=IpSSH, init=False)
    ip_ping_response: IpPingResponse = field(default_factory=IpPingResponse, init=False)
    
    def __post_init__(self):
        self.hostname = Hostname(self._device)
        self.clock = Clock(self._device)
        self.snmp = Snmp(self._device)
        self.auto_backup = AutoBackup(self._device)
        self.user = User(self._device)
        self.config_fwr_ver_check = ConfigFirmwareCheck(self._device)
        self.password_policy = PasswordPolicy(self._device)
        self.ip_http_server = IpHttpServer(self._device)
        self.ip_telnet = IpTelnet(self._device)
        self.ip_ssh = IpSSH(self._device)
        self.ip_ping_response = IpPingResponse(self._device)