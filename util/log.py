from datetime import datetime
from env_vars import *
from exit_codes import *
from orjson import dumps
from os import getenv
from sys import exit
from typing import *
from urllib3 import PoolManager
from uuid import uuid4, UUID
from re import compile

DEBUG = "debug"
INFO = "info"
WARN = "warn"
ERROR = "error"
OFF = "off"

LogLevel = Union[DEBUG, INFO, WARN, ERROR, OFF]

_correlationId = getenv(CORR_ID, str(uuid4()))

_uuidRegex = compile("^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$")

class Log:
    def __init__(self, name: str, level: Optional[LogLevel] = None, values: Optional[Dict[str, any]] = None):
        self.values = values if values else dict()
        self.levels = {
            DEBUG: 1,
            INFO: 2,
            WARN: 3,
            ERROR: 4,
            OFF: 5
        }
        self.name = name
        self.level = level if level else getenv("LOG_LEVEL", DEBUG)
        self.http = PoolManager()

    def _log(self, level: LogLevel, location: str, err: Optional[Exception], msg: str, values: Dict[str, any]) -> None:
        if not _uuidRegex.search(location):
            raise ValueError(f"location must be a lowercase guid, got: '{location}'")
        other_level = self.levels[level]
        if other_level < self._curLevel():
            return
        clef = self._clef(level, location, err, msg, values)
        self._send(clef)

    def _clef(self, level: LogLevel, location: str, err: Optional[Exception], msg: str, values: Dict[str, any]):
        global _correlationId
        data = dict(self.values)
        data.update(values)
        clef = {
            "@t": datetime.utcnow().isoformat() + "Z",
            "@m": msg,
            "@l": level,
            "@i": self.name,
            "@loc": location,
            "@c": _correlationId,
            "data": data,
        }
        if err:
            clef["@x"] = err
        return clef

    def _send(self, clef):
        encoded = dumps(clef)
        r = self.http.request("POST", "http://127.0.0.1:5341/api/events/raw", body=encoded, headers={
            "Content-Type": "application/vnd.serilog.clef"
        })
        if r.status != 201:
            print(f"Failed to send log, got status={r.status}")
            exit(LOG_SEND_FAILED)

    def _curLevel(self):
        return self.levels[self.level]

    def debug(self, location: str, msg: str, values: Optional[Dict[str, any]] = None):
        if values is None:
            values = {}
        self._log(DEBUG, location, None, msg, values)

    def info(self, location: str, msg: str, values: Optional[Dict[str, any]] = None):
        if values is None:
            values = {}
        self._log(INFO, location, None, msg, values)

    def warn(self, location: str, err: Optional[Exception], msg: str, values: Optional[Dict[str, any]] = None):
        if values is None:
            values = {}
        self._log(WARN, location, err, msg, values)

    def error(self, location: str, err: Optional[Exception], msg: str, values: Optional[Dict[str, any]] = None):
        if values is None:
            values = {}
        self._log(ERROR, location, err, msg, values)


"""
{"@t":"2023-03-05T18:18:21.8683500Z","@mt":"This is a test","@m":"This is a test","@i":"ad80e510","@@i":"main",
"""
