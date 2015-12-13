#!/usr/bin/env python

import click
import steering_api

@click.command()
@click.argument('workdir')
@click.argument('analysis')
def main(workdir,analysis):
  steering_api.run_cap_analysis(workdir,analysis)


if __name__ == '__main__':
  main()

