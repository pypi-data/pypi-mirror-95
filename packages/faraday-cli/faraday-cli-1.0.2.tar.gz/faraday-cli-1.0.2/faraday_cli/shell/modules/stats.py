import argparse
import json
from collections import defaultdict
from datetime import datetime
import dateutil.parser

from cmd2 import with_argparser, with_default_category, CommandSet
from faraday_cli.extras.halo.halo import Halo
from faraday_cli.extras.termgraph import termgraph
from faraday_cli.shell.utils import (
    SEVERITY_COLORS,
    IGNORE_SEVERITIES,
    SEVERITIES,
)
from faraday_cli.config import active_config
from faraday_cli.api_client.filter import FaradayFilter


@with_default_category("Stats")
class StatsCommands(CommandSet):
    def __init__(self):
        super().__init__()

    stats_parser = argparse.ArgumentParser()
    stats_parser.add_argument(
        "stat_type",
        type=str,
        choices=["severity", "vulns", "date"],
        help="Type of stat",
    )
    stats_parser.add_argument(
        "-w", "--workspace-name", type=str, help="Workspace"
    )
    stats_parser.add_argument(
        "--ignore-info",
        action="store_true",
        help=f"Ignore {'/'.join(IGNORE_SEVERITIES)} vulnerabilities",
    )
    stats_parser.add_argument(
        "--severity",
        type=str,
        help=f"Filter by severity {'/'.join(SEVERITIES)}",
        default=[],
        nargs="*",
    )
    stats_parser.add_argument(
        "--confirmed", action="store_true", help="Confirmed vulnerabilities"
    )

    @with_argparser(stats_parser)
    def do_stats(self, args):
        """Vulns Stats"""
        if not args.workspace_name:
            if active_config.workspace:
                workspace_name = active_config.workspace
            else:
                self._cmd.perror("No active Workspace")
                return
        else:
            workspace_name = args.workspace_name

        def gather_vulns_stats(vulns):
            if vulns["vulnerabilities"]:
                counters = defaultdict(int)
                for vuln in vulns["vulnerabilities"]:
                    if len(vuln["value"]["hostnames"]):
                        host_identifier = vuln["value"]["hostnames"][0]
                    else:
                        host_identifier = vuln["value"]["target"]
                    counters[host_identifier] += 1
                data = list(map(lambda x: [x], counters.values()))
                termgraph_data = termgraph.TERMGRAPH_DATA_TEMPLATE.copy()
                termgraph_data[
                    "title"
                ] = f"Vulnerability stats [{workspace_name}]"
                termgraph_data["data"] = data
                termgraph_data["labels"] = [x for x in counters.keys()]
                termgraph_data["categories"] = ["vulns"]
                termgraph_data["color"] = ["red"]
                return termgraph_data
            else:
                return None

        def gather_severity_stats(vulns):
            if vulns["vulnerabilities"]:
                counters = defaultdict(
                    lambda: {"severity": {x: 0 for x in SEVERITY_COLORS}}
                )
                for vuln in vulns["vulnerabilities"]:
                    if len(vuln["value"]["hostnames"]):
                        host_identifier = vuln["value"]["hostnames"][0]
                    else:
                        host_identifier = vuln["value"]["target"]
                    counters[host_identifier]["severity"][
                        vuln["value"]["severity"]
                    ] += 1
                data = list(
                    map(
                        lambda x: list(x["severity"].values()),
                        counters.values(),
                    )
                )

                termgraph_data = termgraph.TERMGRAPH_DATA_TEMPLATE.copy()
                termgraph_data["title"] = f"Severity stats [{workspace_name}]"
                termgraph_data["data"] = data
                termgraph_data["labels"] = [x for x in counters.keys()]
                termgraph_data["categories"] = list(SEVERITY_COLORS.keys())
                termgraph_data["color"] = list(SEVERITY_COLORS.values())
                termgraph_data["stacked"] = True
                return termgraph_data
            else:
                return None

        def gather_history_stats(vulns):
            if vulns["vulnerabilities"]:
                counters = defaultdict(int)
                DATE_FORMAT = "%Y-%m-%d"
                min_date = datetime.now()
                for vuln in vulns["vulnerabilities"]:
                    vuln_date = dateutil.parser.parse(
                        vuln["value"]["metadata"]["create_time"]
                    )
                    if vuln_date.date() < min_date.date():
                        min_date = vuln_date
                    date_str = vuln_date.strftime(DATE_FORMAT)
                    counters[date_str] += 1
                data = list(map(lambda x: [x], counters.values()))
                termgraph_data = termgraph.TERMGRAPH_DATA_TEMPLATE.copy()
                min_date_str = min_date.strftime(DATE_FORMAT)
                title = f"Heatmap since {min_date_str} [{workspace_name}]"
                termgraph_data["title"] = title
                termgraph_data["data"] = data
                termgraph_data["labels"] = [x for x in counters.keys()]
                termgraph_data["start_dt"] = min_date.strftime(DATE_FORMAT)
                termgraph_data["calendar"] = True
                return termgraph_data
            else:
                return None

        @Halo(text="Gathering data", text_color="green", spinner="dots")
        def graph_stats(gather_data_func, filter_to_apply):
            vulns = self._cmd.api_client.get_vulns(
                workspace, json.dumps(filter_to_apply)
            )
            args_data = gather_data_func(vulns)
            if args_data:
                _, labels, data, colors = termgraph.read_data(args_data)
                if args_data["calendar"]:
                    termgraph.calendar_heatmap(data, labels, args_data)
                else:
                    termgraph.chart(colors, data, args_data, labels)
            else:
                self._cmd.perror(f"No data in workspace {workspace_name}")

        if workspace_name:
            if not self._cmd.api_client.is_workspace_valid(workspace_name):
                self._cmd.perror(f"Invalid workspace: {workspace_name}")
                return
            else:
                workspace = workspace_name
        else:
            if not active_config.workspace:
                self._cmd.perror("No workspace selected")
                return
            else:
                workspace = active_config.workspace
        if args.severity and args.ignore_info:
            self._cmd.perror("Use either --ignore-info or --severity")
            return
        query_filter = FaradayFilter()
        selected_severities = set(map(lambda x: x.lower(), args.severity))
        if selected_severities:
            for severity in selected_severities:
                if severity not in SEVERITIES:
                    self._cmd.perror(f"Invalid severity: {severity}")
                    return
                else:
                    query_filter.require_severity(severity)
        if args.ignore_info:
            for severity in IGNORE_SEVERITIES:
                query_filter.ignore_severity(severity)
        if args.confirmed:
            query_filter.filter_confirmed()
        gather_data_function_choices = {
            "severity": gather_severity_stats,
            "vulns": gather_vulns_stats,
            "date": gather_history_stats,
        }

        graph_stats(
            gather_data_function_choices[args.stat_type],
            query_filter.get_filter(),
        )
