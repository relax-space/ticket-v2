from wmi import WMI
from hashlib import md5
from datetime import date, timedelta
import os
import sys

sys.coinit_flags = 0
from random import randint
from threading import Thread
from gmssl import sm3, func
import pythoncom


def fill_zero2(i: int) -> str:
    return f"{i:0>2}"


def str_to_int(strObj: str) -> int:
    if strObj.isdigit():
        return int(strObj)
    else:
        return 0


def reverse_by_numb(raw: str, number: int) -> str:
    raw_length = len(raw)
    result = ""
    for i in range(0, raw_length, number):
        result += "".join(reversed(raw[i : i + number]))
    return result


def reverse_by_numb_2(raw: str, number: int) -> str:
    r1 = raw[:-number]
    r2 = raw[-number:]
    r3 = r2 + r1
    raw_length = len(r3)
    result = ""
    for i in range(0, raw_length, number):
        result += "".join(reversed(r3[i : i + number]))
    return result


def reverse_by_numb_3(raw: str, number: int) -> str:
    r1 = raw[: -number - 1]
    r2 = raw[-number - 1 :]
    r3 = r2 + r1
    raw_length = len(r3)
    result = ""
    for i in range(0, raw_length, number):
        result += "".join(reversed(r3[i : i + number]))
    return result


def sm3_encrypto(raw: str) -> str:
    return sm3.sm3_hash(func.bytes_to_list(raw.encode()))


class SecretWin:
    def __init__(self):
        self.DAY = "webqmrbufyybfixtdpuqwgpkapqknhgabdzbowkgceuiorlznjzglm"
        self.list = ["", "", ""]
        pass

    def _get_unique_no(self) -> str:
        pythoncom.CoInitialize()
        try:
            w = WMI()
            cpu = w.Win32_processor()[0].ProcessorId.strip()
            disk = w.Win32_DiskDrive()[0].SerialNumber.strip()
            return f"{cpu}{disk}"
        except Exception as e:
            print(e)
            return ""
        finally:
            pythoncom.CoUninitialize()

    def get_code(self) -> str:
        unique_no = self._get_unique_no()
        if not unique_no:
            return ""
        code = f"relax{unique_no}"
        last = "b"
        code_md5 = md5(code.encode()).hexdigest().lower()
        new_code = code_md5[:-1] + last
        return new_code

    def get_code_thread(self, check_result: list):
        check_result[3] = self.get_code()
        check_result[2] = True
        return True

    def _get_pwd_1(self, lst: list, code, year: int, month: int, day: int) -> str:
        month_2 = fill_zero2(month)
        day_2 = fill_zero2(day)

        number = ord(code[-1])
        code = "".join(reversed(code))
        code = reverse_by_numb(code, number)

        pwd = f"relax{code}{year}{month_2}{day_2}"
        pwd = md5(pwd.encode()).hexdigest().lower()

        day_str = self.DAY[day : day + 6]
        pwd = f"{year}{month_2}{day_str}{pwd[0:6]}"
        lst[0] = pwd
        return pwd

    def _get_pwd_2(self, lst: list, code) -> str:
        number = ord(code[-1])
        raw = "".join(reversed(code))
        raw = reverse_by_numb_2(raw, number)
        pwd_md5 = md5(raw.encode()).hexdigest().lower()
        lst[1] = pwd_md5
        return pwd_md5

    def _get_pwd_3(self, lst: list, code) -> str:
        pwd_sm2: str = sm3_encrypto(code)
        lst[2] = pwd_sm2.lower()
        return pwd_sm2
        pass

    def get_pwd(self, code, year, month, day) -> str:
        t1 = Thread(target=self._get_pwd_1, args=(self.list, code, year, month, day))
        t2 = Thread(target=self._get_pwd_2, args=(self.list, code))
        t3 = Thread(target=self._get_pwd_3, args=(self.list, code))
        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()
        pwd = f"{self.list[0]}{self.list[1][:7]}{self.list[2][:7]}"
        return pwd

    def get_pwd_day(self, code, days: int) -> str:
        day_add = days
        current_date = date.today() + timedelta(days=day_add)
        return self.get_pwd(
            code, current_date.year, current_date.month, current_date.day
        )

    def check_pwd(self, check_result: list, code, pwd):
        check_result[0] = False
        check_result[1] = None
        if not code:
            return False, None

        if len(pwd) != 32:
            return False, None

        year = str_to_int(pwd[0:4])
        if year == 0:
            return False, None
        month = str_to_int(pwd[4:6])
        if month == 0:
            return False, None
        day_str = pwd[6:12]
        day = self.DAY.find(day_str)
        if day == -1:
            return False, None

        act_pwd = self.get_pwd(code, year, month, day)
        if act_pwd != pwd:
            return False, None
        act_date = date(year, month, day)
        now = date.today()
        if act_date < now:
            return False, None
        expired = act_date.strftime("%Y-%m-%d")
        check_result[0] = True
        check_result[1] = expired
        return True, expired
