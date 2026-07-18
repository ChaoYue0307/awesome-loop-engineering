#!/usr/bin/env python3
"""Regression checks for transient and permanent URL-checker failures."""

from __future__ import annotations

import io
import urllib.error
import urllib.request
from unittest import mock

from verify_urls import check_url


class FakeResponse:
    def __init__(self, url: str, status: int) -> None:
        self.url = url
        self.status = status

    def geturl(self) -> str:
        return self.url

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FixtureOpener:
    def __init__(self) -> None:
        self.transient_gets = 0

    def open(self, request: urllib.request.Request, timeout: float) -> FakeResponse:
        url = request.full_url
        if request.get_method() == "HEAD":
            raise urllib.error.HTTPError(url, 500, "fixture HEAD failure", {}, io.BytesIO())
        if url.endswith("/transient"):
            self.transient_gets += 1
            if self.transient_gets == 1:
                raise urllib.error.HTTPError(url, 500, "fixture transient failure", {}, io.BytesIO())
            return FakeResponse(url, 200)
        raise urllib.error.HTTPError(url, 404, "fixture missing", {}, io.BytesIO())


def main() -> int:
    opener = FixtureOpener()
    with mock.patch("verify_urls.urllib.request.build_opener", return_value=opener), mock.patch(
        "verify_urls.time.sleep"
    ):
        ok, detail = check_url("https://fixture.invalid/transient", timeout=2, attempts=2)
        if not ok or detail != "200 GET" or opener.transient_gets != 2:
            raise RuntimeError(f"transient 500 was not retried successfully: {ok=}, {detail=}")

        ok, detail = check_url("https://fixture.invalid/missing", timeout=2, attempts=3)
        if ok or detail != "404 GET":
            raise RuntimeError(f"permanent 404 was not reported: {ok=}, {detail=}")

    print("URL checker regression checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
