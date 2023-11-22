import asyncio
import argparse
import aiohttp
from datetime import datetime, timedelta
from getpass import getpass

from pymymeter.pymymeter import MyMeter


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--username",
        help="Username for logging into the utility's website. "
        "If not provided, you will be asked for it",
    )
    parser.add_argument(
        "--password",
        help="Password for logging into the utility's website. "
        "If not provided, you will be asked for it",
    )
    parser.add_argument(
        "--filename",
        help="Filename to output fetched data to. Does not need file extension."
        "If not provided, no file output will be generated.",
    )
    parser.add_argument(
        "--start_date",
        help="Start datetime for historical data. Defaults to 30 days ago",
        type=lambda s: datetime.fromisoformat(s),
        default=datetime.now() - timedelta(days=30),
    )
    parser.add_argument(
        "--end_date",
        help="end datetime for historical data. Defaults to now",
        type=lambda s: datetime.fromisoformat(s),
        default=datetime.now(),
    )

    args = parser.parse_args()
    filename = args.filename
    username = args.username or input("Username: ")
    password = args.password or getpass("Password: ")
    start_time = args.start_date
    end_time = args.end_date
    async with aiohttp.ClientSession() as session:
        mymeter = MyMeter(session, username, password)
        await mymeter.async_login()
        # Test Usage Reads
        usage_results = await mymeter.async_get_usage_reads(start_time, end_time)
        if usage_results:
            for result in usage_results:
                print(result)
            print("Total Usage Results:", len(usage_results))
        if filename:
            await mymeter.print_data(
                start_date=start_time,
                filename=f"{filename}-consumption",
                end_date=end_time,
                cost_or_consumption="consumption",
            )
        # Test Cost Reads
        cost_results = await mymeter.async_get_cost_reads(start_time, end_time)
        if cost_results:
            for result in cost_results:
                print(result)
            print("Total Cost Results:", len(cost_results))
        if filename:
            await mymeter.print_data(
                start_date=start_time,
                filename=f"{filename}-cost",
                end_date=end_time,
                cost_or_consumption="cost",
            )


asyncio.run(main())
