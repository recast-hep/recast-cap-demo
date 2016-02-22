#!/usr/bin/env python

import click
import steering_api

@click.command()
@click.argument('workdir')
@click.argument('analysis')
@click.argument('global_context')
def main(workdir,analysis,global_context):
    steering_api.run_cap_analysis(workdir,analysis,global_context)


if __name__ == '__main__':
  main()

