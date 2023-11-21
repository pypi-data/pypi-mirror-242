import argparse
import csv
from collections.abc import Iterable, Sequence
from typing import Any

from prometheus_client.core import GaugeMetricFamily, Metric
from prometheus_client.openmetrics.exposition import (
    generate_latest as generate_latest_openmetrics,
)
from prometheus_client.registry import REGISTRY, Collector, CollectorRegistry

DEFAULT_OPENMETRICS_FILE = "./metrics.txt"


def normalize_failures_ratio(locust_stats: dict[str, str]) -> float:
    failure_count = int(locust_stats["Failure Count"])
    request_count = int(locust_stats["Request Count"])
    if request_count == 0:  # avoid divide-by-zero errors
        return 0.0

    return failure_count / request_count


def normalize_response_time(val: str) -> float:
    if val == "N/A":  # no requests have been made during test time
        return 0.0

    return int(val) / 1000  # convert [milliseconds] to [seconds]


def parse_locust_csv_stats_file(path: str) -> dict[str, str]:
    with open(path) as locust_report_csv:
        for row in csv.DictReader(locust_report_csv):
            if (
                row["Name"] == "Aggregated"
            ):  # we only care about aggregated locust results
                return row

    raise ValueError(f"No 'Aggregated' locust results found in {path}")  # noqa: TRY003


class LocustStatsCollector(Collector):
    _METRIC_PREFIX = "locust_"

    def __init__(self, registry: CollectorRegistry = REGISTRY) -> None:
        self.failures_ratio = GaugeMetricFamily(
            name=f"{self._METRIC_PREFIX}failures_ratio",
            documentation="ratio of failed to total requests",
            unit="ratio",
        )
        self.requests_per_second = GaugeMetricFamily(
            name=f"{self._METRIC_PREFIX}requests_per_second",
            documentation="average number of requests per second",
        )
        self.response_time_p50 = GaugeMetricFamily(
            name=f"{self._METRIC_PREFIX}response_time_p50",
            documentation="50% (aka median) response time",
            unit="seconds",
        )
        self.response_time_p95 = GaugeMetricFamily(
            name=f"{self._METRIC_PREFIX}response_time_p95",
            documentation="95% response time",
            unit="seconds",
        )

        registry.register(self)

    def observe(
        self,
        locust_stats: dict[str, str],
        labels: dict[str, str] | None = None,
        timestamp: int | None = None,
    ) -> None:
        labels = labels or {}

        self.failures_ratio.add_sample(
            name=self.failures_ratio.name,
            labels=labels,
            value=normalize_failures_ratio(locust_stats),
            timestamp=timestamp,
        )
        self.requests_per_second.add_sample(
            name=self.requests_per_second.name,
            labels=labels,
            value=float(locust_stats["Requests/s"]),
            timestamp=timestamp,
        )
        self.response_time_p50.add_sample(
            name=self.response_time_p50.name,
            labels=labels,
            value=normalize_response_time(locust_stats["50%"]),
            timestamp=timestamp,
        )
        self.response_time_p95.add_sample(
            name=self.response_time_p95.name,
            labels=labels,
            value=normalize_response_time(locust_stats["95%"]),
            timestamp=timestamp,
        )

    def collect(self) -> Iterable[Metric]:
        return [
            self.failures_ratio,
            self.requests_per_second,
            self.response_time_p50,
            self.response_time_p95,
        ]


def collect_locust_stats(
    csv_stats_path: str,
    labels: dict[str, str] | None = None,
    timestamp: int | None = None,
    registry: CollectorRegistry = REGISTRY,
) -> LocustStatsCollector:
    collector = LocustStatsCollector(registry)
    collector.observe(
        locust_stats=parse_locust_csv_stats_file(csv_stats_path),
        labels=labels,
        timestamp=timestamp,
    )

    return collector


def write_openmetrics_to_textfile(path: str, registry: CollectorRegistry) -> None:
    """
    Fork of `prometheus_client.exposition.write_to_textfile` as the project
    didn't provide an OpenMetrics variant of this helper function, until
    https://github.com/prometheus/client_python/issues/957 is resolved.
    """
    with open(path, "wb") as fp:
        fp.write(generate_latest_openmetrics(registry))


class ParseDict(argparse.Action):
    """
    Based on
    https://gist.github.com/fralau/061a4f6c13251367ef1d9a9a99fb3e8d#gistcomment-3040978
    """

    def __call__(
        self,
        parser: argparse.ArgumentParser,  # noqa: ARG002
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,  # noqa: ARG002
    ) -> None:
        d = getattr(namespace, self.dest) or {}

        if values:
            for item in values:
                split_items = item.split("=", 1)
                key = split_items[
                    0
                ].strip()  # we remove blanks around keys, as is logical
                value = split_items[1]

                d[key] = value

        setattr(namespace, self.dest, d)


def parse_cli_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Converts locust's load test CSV formatted reports into the OpenMetrics text format.",
    )
    parser.add_argument(
        "csv_file",
        help="Locust's load test '{CSV_PREFIX}_stats.csv' report",
    )
    parser.add_argument(
        "-o",
        "--openmetrics-file",
        metavar="FILENAME",
        default=DEFAULT_OPENMETRICS_FILE,
        help=f"Store OpenMetrics text formatted metrics to the selected FILENAME, '{DEFAULT_OPENMETRICS_FILE}' by default",
    )
    parser.add_argument(
        "-t",
        "--timestamp",
        type=int,
        help="OpenMetrics timestamp added to all metrics, in Unix epoch seconds",
    )
    parser.add_argument(
        "-l",
        "--labels",
        action=ParseDict,
        metavar="KEY=VALUE",
        nargs="*",
        help="OpenMetrics label(s) added to all metrics",
    )
    return parser.parse_args(args)


def main(cli_args: list[str] | None = None) -> None:
    parsed_args = parse_cli_args(cli_args)

    registry = CollectorRegistry(auto_describe=True)
    collect_locust_stats(
        csv_stats_path=parsed_args.csv_file,
        labels=parsed_args.labels,
        timestamp=parsed_args.timestamp,
        registry=registry,
    )
    write_openmetrics_to_textfile(
        path=parsed_args.openmetrics_file,
        registry=registry,
    )


if __name__ == "__main__":
    main()
