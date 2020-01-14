import bibo
import pybibs
import click

@click.command('todo', short_help='Modify a TODO note against an entry.')
@click.argument('key', autocompletion=bibo.internals.complete_key)
@click.pass_context
def todo(ctx, key):
    data = ctx.obj['data']
    entry = bibo.query.get_by_key(data, key)

    curr_note = entry['fields'].get('todo', '')
    try:
        upd_note = click.edit(text=curr_note).strip()
    except AttributeError:
        click.echo('Error updating TODO note, did you leave it blank?')
        return

    if upd_note == curr_note:
        click.echo('No changes to TODO note: "{}"'.format(upd_note))
        return
    elif upd_note:
        entry['fields']['todo'] = upd_note
        click.echo('Added/Modified TODO note: "{}"'.format(upd_note))
    else:
        del entry['fields']['todo']
        click.echo('Removed TODO note: "{}"'.format(curr_note))
    
    pybibs.write_file(data, ctx.obj['database'])

@click.command('todo_list', short_help='List TODO notes.')
@click.argument('search_terms', nargs=-1, autocompletion=bibo.internals.complete_key)
@click.pass_context
def todo_list(ctx, search_terms):
    # TODO: Add bib style param, and unify with list command.
    entries = bibo.query.search(ctx.obj['data'], search_terms)
    entries = [e for e in entries if e['type'] != 'string']
    keys = [e['key'] for e in entries]
    try:
        citations = bibo.cite.cite(keys, ctx.obj['database'], 'plain', True)
    except cite.BibtexException as e:
        # TODO: Resolve this properly....
        pass

    # Escape if no TODO lists.
    todo_notes = sum(1 if e['fields'].get('todo') else 0 for e in entries)
    if not todo_notes:
        click.echo('Currently there are no TODO notes!')
        return

    # If search terms, list all. Else, just things with TODO lists.
    for entry in entries:
        todo = entry['fields'].get('todo')
        if search_terms or todo:
            note = '📌' if todo else ''
            todo_kwargs = {'bold':True} if todo else {'dim':True}
            parts = [
                bibo.internals.header(entry) + ' ' + note,
                citations[entry['key']],
                click.style('TODO: {}'.format(todo), fg='red', **todo_kwargs)
            ]
            click.echo('\n'.join(parts))
