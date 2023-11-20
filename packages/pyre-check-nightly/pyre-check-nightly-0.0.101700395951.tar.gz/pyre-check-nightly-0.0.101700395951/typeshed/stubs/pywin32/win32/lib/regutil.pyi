from _typeshed import Incomplete

error: str
CLSIDPyFile: str
RegistryIDPyFile: str
RegistryIDPycFile: str

def BuildDefaultPythonKey(): ...
def GetRootKey(): ...
def GetRegistryDefaultValue(subkey, rootkey: Incomplete | None = ...): ...
def SetRegistryDefaultValue(subKey, value, rootkey: Incomplete | None = ...) -> None: ...
def GetAppPathsKey(): ...
def RegisterPythonExe(exeFullPath, exeAlias: Incomplete | None = ..., exeAppPath: Incomplete | None = ...) -> None: ...
def GetRegisteredExe(exeAlias): ...
def UnregisterPythonExe(exeAlias) -> None: ...
def RegisterNamedPath(name, path) -> None: ...
def UnregisterNamedPath(name) -> None: ...
def GetRegisteredNamedPath(name): ...
def RegisterModule(modName, modPath) -> None: ...
def UnregisterModule(modName) -> None: ...
def GetRegisteredHelpFile(helpDesc): ...
def RegisterHelpFile(helpFile, helpPath, helpDesc: Incomplete | None = ..., bCheckFile: int = ...) -> None: ...
def UnregisterHelpFile(helpFile, helpDesc: Incomplete | None = ...) -> None: ...
def RegisterCoreDLL(coredllName: Incomplete | None = ...) -> None: ...
def RegisterFileExtensions(defPyIcon, defPycIcon, runCommand) -> None: ...
def RegisterShellCommand(shellCommand, exeCommand, shellUserCommand: Incomplete | None = ...) -> None: ...
def RegisterDDECommand(shellCommand, ddeApp, ddeTopic, ddeCommand) -> None: ...
