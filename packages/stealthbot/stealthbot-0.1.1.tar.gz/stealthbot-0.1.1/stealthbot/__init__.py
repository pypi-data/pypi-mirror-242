"""StealthBot: Un bot Python con tecnologia antidetect.

Questo modulo fornisce funzionalità per automatizzare compiti mantenendo
un profilo basso e evitando rilevazioni. È ideale per operazioni che richiedono
discrezione e sofisticatezza nell'elusione dei sistemi di rilevamento.
"""
__version__ = "0.1.1"
from .decorators import RetryException, stealth, request, AsyncQueueResult, AsyncResult
from .anti_detect_driver import AntiDetectDriver
from .anti_detect_requests import AntiDetectRequests
import stealthbot.bt as bt
