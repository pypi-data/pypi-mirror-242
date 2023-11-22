import dataclasses
from datetime import datetime, timedelta
import json
from typing import Literal, Optional, Any
import aiohttp

from bs4 import BeautifulSoup, Tag

from .exceptions import DataException, InvalidAuth, TokenErrorException


@dataclasses.dataclass
class UsageRead:
    start_time: datetime
    end_time: datetime
    consumption: float
    unit_of_measurement: str


@dataclasses.dataclass
class CostRead:
    start_time: datetime
    end_time: datetime
    provided_cost: float


UsageInterval = Literal["15minute", "30minute", "day", "hour", "week", "month", "bill"]
UsageType = Literal["cost", "consumption"]


update_interval_dict: dict[UsageInterval, str] = {
    "15minute": "3",
    "30minute": "4",
    "hour": "5",
    "day": "6",
    "week": "8",
    "bill": "7",
    "month": "9",
}

usage_type_dict: dict[UsageType, "str"] = {"cost": "3", "consumption": "1"}


class MyMeter:
    """Class that can get historical data from utility."""

    def __init__(
        self, session: aiohttp.ClientSession, username: str, password: str
    ) -> None:
        self.session: aiohttp.ClientSession = session
        self.username: str = username
        self.password: str = password

    async def _async_get_verification_token(self) -> str | None:
        url = "https://mymeter.lge-ku.com/"
        async with self.session.get(url) as response:
            text = await response.text()
        soup = BeautifulSoup(text, "html.parser")
        input_element = soup.find("input", {"name": "__RequestVerificationToken"})
        if type(input_element) is Tag:
            token = input_element.get("value", None)
            if type(token) is str:
                return token

    async def _async_set_chart_data(
        self,
        usage_interval: UsageInterval = "hour",
        usage_type: UsageType = "consumption",
    ):
        interval = update_interval_dict[usage_interval]
        type = usage_type_dict[usage_type]
        token = await self._async_get_verification_token()

        url = "https://mymeter.lge-ku.com/Dashboard/Chart/"
        data = {}
        data["__RequestVerificationToken"] = token

        data["UsageInterval"] = interval
        data["UsageType"] = type
        data["jsTargetName"] = "StorageType"
        data["EnableHoverChart"] = "true"
        data["Start"] = "2023-11-01"
        data["End"] = "2023-11-15"
        data["IsRangeOpen"] = "False"
        data["MaintainMaxDate"] = "true"
        data["SelectedViaDateRange"] = "False"

        data["ChartComparison"] = "1"
        data["ChartComparison2"] = "0"
        data["ChartComparison3"] = "0"
        data["ChartComparison4"] = "0"

        async with self.session.post(url, data=data) as response:
            return await response.text()

    async def _async_login(self) -> None:
        """Login and set session for data extraction."""
        login_url = "https://mymeter.lge-ku.com/Home/Login"
        login_data = {"LoginEmail": self.username, "LoginPassword": self.password}
        token = await self._async_get_verification_token()
        if token:
            login_data["__RequestVerificationToken"] = token
        else:
            raise TokenErrorException

        resp = await self.session.post(login_url, data=login_data)
        if txt := await resp.text():
            json_txt = json.loads(txt)
            if json_txt.get("Data") is not None:
                error_msg = json_txt.get("Data").get("LoginErrorMessage")
                if error_msg:
                    raise InvalidAuth

    async def async_login(self) -> None:
        await self._async_login()
        # await self._async_set_chart_data()

    async def _fetch_page(self, url) -> Any:
        async with self.session.get(url) as response:
            return await response.text()

    async def async_get_usage_reads(
        self, start_date: datetime, end_date: Optional[datetime] = None
    ) -> list[UsageRead] | None:
        """Return Usage Reads."""
        reads = await self._async_get_dated_data(start_date, end_date, "consumption")
        if not reads:
            raise DataException("No usage data returned.")
        data_series = reads.get("data", [])
        result: list[UsageRead] = []
        # Calculate the time diff
        if len(data_series) > 2:
            t1 = datetime.utcfromtimestamp(data_series[0].get("x") / 1000)
            t2 = datetime.utcfromtimestamp(data_series[1].get("x") / 1000)
            time_diff = t2 - t1
        else:
            time_diff = timedelta(minutes=60)
        # Unit of measure
        unit_of_measurement = reads.get("tooltip").get("valueSuffix").strip()
        # Loop over data
        for data in data_series:
            s = data.get("x")
            start_time = datetime.utcfromtimestamp(s / 1000)
            end_time = start_time + time_diff
            consumption = data.get("y")
            result.append(
                UsageRead(
                    start_time=start_time,
                    end_time=end_time,
                    consumption=consumption,
                    unit_of_measurement=unit_of_measurement,
                )
            )
        return result

    async def async_get_cost_reads(
        self, start_state: datetime, end_date: Optional[datetime] = None
    ) -> list[CostRead] | None:
        """Return Cost Reads."""
        reads = await self._async_get_dated_data(
            start_date=start_state, end_date=end_date, cost_or_consumption="cost"
        )
        if not reads:
            raise DataException("No cost data returned.")
        data_series = reads.get("data", [])
        result: list[CostRead] = []
        if len(data_series) > 2:
            t1 = datetime.utcfromtimestamp(data_series[0].get("x") / 1000)
            t2 = datetime.utcfromtimestamp(data_series[1].get("x") / 1000)
            time_diff = t2 - t1
        else:
            time_diff = timedelta(minutes=60)

        # Loop over data
        for data in data_series:
            s = data.get("x")
            start_time = datetime.utcfromtimestamp(s / 1000)
            end_time = start_time + time_diff
            cost = data.get("y")
            result.append(
                CostRead(
                    start_time=start_time,
                    end_time=end_time,
                    provided_cost=cost,
                )
            )
        return result

    async def _async_get_dated_data(
        self,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        cost_or_consumption: UsageType = "consumption",
        print_data: bool = False,
    ) -> Any | None:
        """Gets data between two dates."""
        # Set start and end times.
        start = int(start_date.timestamp() * 1000)
        if end_date:
            end = int(end_date.timestamp() * 1000)
        else:
            end = int(datetime.now().timestamp() * 1000)

        # Set chart type (cost or consumption)
        await self._async_set_chart_data(usage_type=cost_or_consumption)

        data_url = f"https://mymeter.lge-ku.com/Dashboard/ChartData?_=1&unixTimeStart={start}&unixTimeEnd={end}"
        data = json.loads(await self._fetch_page(data_url))
        if print_data:
            return data
        series_data_list = data.get("Data").get("series")
        # Filter out to only get the data desired.
        for series_data in series_data_list:
            if series_data.get("name"):
                data_series = series_data.get("data", [])
                if len(data_series) > 1:
                    y_data = data_series[0].get("y", 0)
                    tr_data = data_series[0].get("tr", None)
                else:
                    y_data = 0
                    tr_data = None
                if len(data_series) > 1 and y_data > 0 and not tr_data:
                    return series_data

    async def print_data(
        self,
        start_date: datetime,
        filename: str = "meter_data",
        end_date: Optional[datetime] = None,
        cost_or_consumption: UsageType = "consumption",
    ) -> None:
        data = await self._async_get_dated_data(
            start_date=start_date,
            end_date=end_date,
            cost_or_consumption=cost_or_consumption,
            print_data=True,
        )
        if "." in filename:
            filename = filename.split(".")[0]
        full_filename = f"{filename}.json"
        if data:
            with open(full_filename, "w") as f:
                f.write(json.dumps(data))
