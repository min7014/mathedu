# -*- coding: utf-8 -*-
"""
silent_subprocess.py
====================
[Windows 백그라운드 완전 무창(Zero-Window) 실행 보장 모듈]
pythonw.exe 등 콘솔이 없는 백그라운드 데몬이나 작업 스케줄러 워커에서
ffmpeg, ffprobe, git, taskkill, powershell, node(Playwright) 등 외부 콘솔 프로그램(CUI)을 호출할 때
화면에 검은 실행창이 0.1초라도 깜빡이며 뜨는 현상을 프로세스 전역(전 라이브러리 포함)에서 100% 원천 차단합니다.
"""

import os
import subprocess

CREATE_NO_WINDOW_FLAG = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
DETACHED_PROCESS_FLAG = getattr(subprocess, "DETACHED_PROCESS", 0x00000008)
CREATE_NEW_CONSOLE_FLAG = getattr(subprocess, "CREATE_NEW_CONSOLE", 0x00000010)
CREATE_NEW_PROCESS_GROUP_FLAG = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200)
CREATE_BREAKAWAY_FROM_JOB_FLAG = 0x01000000


def install_silent_subprocess_hook() -> None:
    if os.name != "nt":
        return
    if getattr(subprocess.Popen, "_mathedu_silent_patched", False):
        return

    _orig_popen_init = subprocess.Popen.__init__

    def _silent_popen_init(self, *args, **kwargs):
        cflags = int(kwargs.get("creationflags") or 0)
        # MSDN: CREATE_NO_WINDOW is ignored if combined with DETACHED_PROCESS or CREATE_NEW_CONSOLE.
        cflags &= ~CREATE_NEW_CONSOLE_FLAG
        cflags &= ~DETACHED_PROCESS_FLAG
        cflags |= CREATE_NO_WINDOW_FLAG
        kwargs["creationflags"] = cflags

        si = kwargs.get("startupinfo")
        if si is None:
            si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE
        kwargs["startupinfo"] = si

        return _orig_popen_init(self, *args, **kwargs)

    subprocess.Popen.__init__ = _silent_popen_init
    subprocess.Popen._mathedu_silent_patched = True

    def _silent_os_system(command: str) -> int:
        res = subprocess.run(command, shell=True)
        return int(res.returncode)

    os.system = _silent_os_system


def spawn_windowless_background_python(script_path: str, extra_args: list[str] | None = None, cwd: str | None = None) -> int:
    """
    powershell.exe 중간 호출조차 없이 pythonw.exe를 완전 무창(SW_HIDE + CREATE_NO_WINDOW) 독립 프로세스로 기동합니다.
    """
    import sys
    from pathlib import Path

    py_exe = Path(sys.executable)
    pyw_exe = py_exe.with_name("pythonw.exe")
    runner = str(pyw_exe if pyw_exe.exists() else py_exe)
    cmd = [runner, "-X", "utf8", str(Path(script_path).resolve())]
    if extra_args:
        cmd.extend(extra_args)

    work_dir = cwd or str(Path(script_path).resolve().parent)
    for flags in (
        CREATE_NO_WINDOW_FLAG | CREATE_NEW_PROCESS_GROUP_FLAG | CREATE_BREAKAWAY_FROM_JOB_FLAG,
        CREATE_NO_WINDOW_FLAG | CREATE_NEW_PROCESS_GROUP_FLAG,
    ):
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=work_dir,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                creationflags=flags,
            )
            return int(proc.pid)
        except OSError:
            continue
    return 0


install_silent_subprocess_hook()
