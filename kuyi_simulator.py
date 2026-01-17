"""Simple script that uses pybroker to pull TSLA data from Alpaca.

Usage:
1. Copy `secrets_example.py` to `secrets.py` and fill your Alpaca keys, or set
   environment variables `ALPACA_API_KEY` and `ALPACA_API_SECRET`.
2. Activate your virtualenv where `pybroker` and `alpaca-py` are installed.
3. Run: `python kuyi_simulator.py`
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Optional

try:
	# Prefer a local secrets.py (ignored by git)
	import secrets as local_secrets  # type: ignore
except Exception:
	local_secrets = None

from pybroker import Alpaca


def get_alpaca_creds() -> tuple[Optional[str], Optional[str]]:
	if local_secrets is not None:
		api_key = getattr(local_secrets, "ALPACA_API_KEY", None)
		api_secret = getattr(local_secrets, "ALPACA_API_SECRET", None)
	else:
		api_key = os.environ.get("ALPACA_API_KEY")
		api_secret = os.environ.get("ALPACA_API_SECRET")
	return api_key, api_secret


def fetch_tsla():
	api_key, api_secret = get_alpaca_creds()
	if not api_key or not api_secret:
		raise RuntimeError(
			"Alpaca credentials not found. Set ALPACA_API_KEY/ALPACA_API_SECRET or create secrets.py."
		)

	# Create Alpaca data source from pybroker.
	alpaca = Alpaca(api_key=api_key, api_secret=api_secret)

	# Define date range for the data pull (adjust as desired).
	start_date = "2023-01-01"
	end_date = datetime.now().strftime("%Y-%m-%d")

	print(f"Fetching TSLA daily bars from {start_date} to {end_date}...")
	df = alpaca.query("TSLA", start_date=start_date, end_date=end_date, timeframe="1d")

	# Print a small sample.
	if df.empty:
		print("No data returned. Check credentials, date range, and Alpaca account permissions.")
	else:
		print(df.head(10).to_string(index=False))


if __name__ == "__main__":
	try:
		fetch_tsla()
	except Exception as exc:
		print("Error:", exc)
