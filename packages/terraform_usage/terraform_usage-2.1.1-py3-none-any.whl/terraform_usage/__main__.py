#!/usr/bin/env python3
# -*- coding: latin-1 -*-

"""
Get Terraform Workspace and Run usage statistics.

Call the Terraform Cloud API to retrieve Workspace and Run data.
Visualization functions are available, but not recommended.
Better to use the CSV output and plot the charts / tables elsewhere.

USAGE

Command line:
python \
    terraform_usage.py \
    -o <organization> \
    -t <token> \
    -k <keyword> \
    -f <filename> \
    -s <start_date> \
    -e <end_date> \
    -m <mode> \
    -u <api_url> \
    -p <page_size> \
    -d <delay>

Python shell:
import terraform_usage as tfu
workspaces = tfu.list_workspaces(
    <organization>,
    <token>,
    <keyword>,
    <api_url>,
    <page_size>,
    <delay>
)
runs = tfu.analyze_runs(
    workspaces,
    <token>,
    <start_date>,
    <end_date>,
    <mode>,
    <api_url>,
    <page_size>,
    <delay>
)
create_csv(
    [run.values() for run in runs],
    <filename>,
    <mode>
)

Arguments:
<organization> - Terraform Cloud Organization name.
<token> - Terraform Cloud API token.
<keyword> - Workspace name keyword to filter by (use "all" for no filter).
<filename> - CSV filename to save the output data to.
<start_date> - Start date for Run lookups (use "all" for no filter).
<end_date> - End date for Run lookups (use "all" for no filter).
<mode> - Execution mode ("simple" or "advanced").

Dependencies:
requests - https://pypi.org/project/requests/
matplotlib - https://pypi.org/project/matplotlib/

API documentation:
https://developer.hashicorp.com/terraform/cloud-docs/api-docs

CAUTION
This may take a while to run if the Organization
has a large number of Workspaces and / or Runs.
"""
import __init__

if __name__ == "__main__":
    __init__.main()
