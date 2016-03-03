#!/usr/bin/env python
import click
import steering_api

@click.command()
@click.argument('workdir')
@click.option('-g','--globalwork', default = None)
@click.argument('analysis')
@click.argument('global_context')
def main(workdir,globalwork,analysis,global_context):
    steering_api.run_cap_analysis(workdir,globalwork if globalwork else workdir,analysis,global_context)

if __name__ == '__main__':
  main()

