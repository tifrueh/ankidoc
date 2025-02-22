# ankidoc

`ankidoc` is a short python script intended to make writing
[anki](https://apps.ankiweb.net) notes in asciidoc easier.

## Synopsis

```
ankidoc [-h] [ -d | -n | -l ] [-o OUT] [-a ATTR] [-L LV] files
```

## Short introduction

The script can be used to generate a text file for import into anki from notes
written in asciidoc.

The asciidoc notes need to be in a specific format in order for the script to
be able to work with them; Every note needs to be a directory with its name
ending in `.anote`, containing three files:

* `front.adoc`: An asciidoc file containing everything that should be on the
  front side of the note.

* `back.adoc`: An asciidoc file containing everything that should be on the
  back side of the note.

* `tags.txt`: A text file containing space-separated tags for the note. This
  file is optional, but its absence _will_ throw a warning.

### Anki Import File Format

When importing a file generated with `ankidoc` into anki, the following points
should be considered

1. `ankidoc` separates note fields with a semicolon (`;`).
2. `ankidoc` creates all notes with *four* fields: the ID of the note (the
   filename of the note without ".anote"), the front side, the back side and
   the tags. It is recommended to use a note type with some kind of ID field in
   the import, so that the note ID can be used to avoid duplicates and update
   already present notes instead.

## More information

For more information and generally more detailed documentation, please refer to
the manual page.

If you want to view the manual page without installing it, clone the repository
and navigate your terminal to it. You can then use the `man` command on
`ankidoc.1` to display the manual page as usual.

## Dependencies

* [asciidoctor](https://docs.asciidoctor.org/asciidoctor/latest/)
