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
be able to work with them; The idea is that each note -- or at least each of the
notes the user wants to have in one deck -- is assigned a unique ID. It is then
split into two asciidoc files, one with the content of the front side of the
note, and one of the back side. These two files must now be saved as `ID.front`
and `ID.back`, ID being the unique note ID that was assigned to the note.

If, for example, two notes, `NoteOne` and `NoteTwo` were to be created, four
files would be needed for that:

```
NoteOne.back
NoteOne.front
NoteTwo.back
NoteTwo.front
```

Now, the list of `.front` files desired to be in the final import file can be
passed to `ankidoc`. The script will then find the corresponding `.back` files
(which have to be in the same directory), convert all files to HTML and output
a properly formatted anki import file named `out`. The name and location of the
output file can be adjusted using the `-o` option.

### Anki Import File Format

When importing a file generated with `ankidoc` into anki, the following points
should be considered

1. `ankidoc` separates note fields with a semicolon (`;`).
2. `ankidoc` creates all notes with *three* fields: the previously defined note
   ID, the front side and the back side. It is recommended to use a note type
   with three fields in the import, so that the note ID can be used to avoid
   duplicates and update already present notes instead.

## More information

For more information and generally more detailed documentation, please refer to
the manual page.

If you want to view the manual page without installing it, clone the repository
and navigate your terminal to it. You can then use the `man` command on
`ankidoc.1` to display the manual page as usual.

## Dependencies

* [asciidoctor](https://docs.asciidoctor.org/asciidoctor/latest/)
