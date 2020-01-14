import datetime

import bibo
import pybibs
import click

@click.command('todo', short_help='Modify a TODO note against an entry.')
@click.argument('search_term')
@click.pass_context
def todo(ctx, search_term):
    data = ctx.obj['data']
    entry = bibo.query.get(data, search_term)

    curr_note = entry['fields'].get('todo', '')
    upd_note = click.edit(text=curr_note).strip()

    if upd_note == curr_note:
        click.echo('No changes to TODO note: "{}"'.format(upd_note))
        return
    elif upd_note:
        entry['fields']['todo'] = upd_note
        click.echo('Added/Modified TODO note: "{}"'.format(upd_note))
    else:
        del entry['fields']['todo']
        click.echo('Removed TODO note: "{}"'.format(curr_note)
    
    pybibs.write_file(data, ctx.obj['database'])
