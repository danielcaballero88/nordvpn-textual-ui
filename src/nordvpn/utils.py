# pylint: disable-all
# flake8: noqa
import functools
import re

from . import commands


def check_account() -> dict[str, str]:
    """Run nordvpn account.

    This function is used to check if it is currently logged in by the wrapper function
    is_logged_in, so do not require being logged in within this one or there will be an
    infinite recursion.
    """
    # Initialize result
    result = {
        "email": None,
        "expiration": None,
    }
    completed = commands.nordvpn_account()
    output = completed.stdout.decode("utf-8").replace("\r", "")
    if "not logged in" in output:
        raise NotLoggedInError()

    def _extract_email(_line: str) -> str | None:
        if not _line.startswith("Email"):
            return None
        re_match = re.search(":\s*(\w+?@\w+?\.com)", _line)
        if not re_match:
            raise ValueError("Couldn't extract email with regex.")
        email = re_match.groups()[0]
        return email

    def _extract_expiration(_line: str) -> str | None:
        if not _line.startswith("VPN Service"):
            return None
        re_match = re.search("Active \((.+?)\)", _line)
        if not re_match:
            raise ValueError("Couldn't extract expire date with regex.")
        expiration = re_match.groups()[0]
        return expiration

    lines = output.split("\n")
    for line in lines:
        if _email := _extract_email(line):
            result["email"] = _email
        if _expiration := _extract_expiration(line):
            result["expiration"] = _expiration

    return result


class NotLoggedInError(Exception):
    ...


class NotLoggedOutError(Exception):
    ...


def is_logged_in() -> bool:
    try:
        check_account()
    except Exception as exc:
        print(exc)
        return False
    else:
        return True


def login_required(func):
    """Decorator to require being logged in before a function call."""

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        # Check for logged in status.
        if not is_logged_in():
            msg = f"function {func.__name__} requires to be logged in."
            raise NotLoggedInError(msg)
        # Execute function.
        func_result = func(*args, **kwargs)
        # Done.
        return func_result

    return wrapped_func


def logout_required(func):
    """Decorator to require being logged in before a function call."""

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        # Check for logged in status.
        if is_logged_in():
            msg = f"function {func.__name__} requires to be logged out."
            raise NotLoggedOutError(msg)
        # Execute function.
        func_result = func(*args, **kwargs)
        # Done.
        return func_result

    return wrapped_func


@login_required
def run_logout() -> str:
    completed = commands.nordvpn_logout()
    if completed.returncode != 0:
        raise ValueError(f"nordvpn_logout returned code {completed.returncode}")
    output = completed.stdout.decode("utf-8")
    return output


@logout_required
def run_login():
    completed = commands.nordvpn_login()
    if completed.returncode != 0:
        raise ValueError(f"nordvpn_login returned ccode {completed.returncode}")
    output = completed.stdout.decode("utf-8")
    return output


@login_required
def get_status():
    result = {
        "Status": None,
        "Country": None,
        "City": None,
        "IP": None,
        "Uptime": None,
    }
    completed = commands.nordvpn_status()
    output = completed.stdout.decode("utf-8")
    output = output.replace("\r", "")
    lines = output.split("\n")
    for line in lines:
        re_match = re.search("(\w+?):\s*([\w\s.]+)$", line)
        if re_match:
            key, val = re_match.groups()
            if key in result:
                result[key] = val
    return result


@login_required
def get_countries() -> list[str]:
    completed = commands.nordvpn_countries()
    result = completed.stdout.decode("utf-8")
    result = result.replace("\r", "").replace("\n", "\t")
    result = re.sub("\t+", ";", result)
    result = result.split(";")
    countries = []
    for country_raw in result:
        re_match = re.search("(\w+)", country_raw)
        if re_match:
            countries.append(re_match.groups()[0])
    return countries


@login_required
def get_cities(country: str) -> list[str]:
    completed = commands.nordvpn_cities(country)
    result = completed.stdout.decode("utf-8")
    result = result.replace("\r", "").replace("\n", "\t")
    result = re.sub("\t+", ";", result)
    result = result.split(";")
    cities = []
    for country_raw in result:
        re_match = re.search("(\w+)", country_raw)
        if re_match:
            cities.append(re_match.groups()[0])
    return cities


@login_required
def connect_to_country(location: str):
    completed = commands.nordvpn_connect(location)
    result = completed.stdout.decode("utf-8")
    print(result)


if __name__ == "__main__":
    # run_login()
    get_status()
