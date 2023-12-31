---
eleventyNavigation:
    key: viewtsv Annotated
    order: 99
Date: 2017-12-27
Version: 1.0
---


# viewtsv

[viewtsv.py](https://github.com/saulpw/visidata/blob/stable/bin/viewtsv.py)
is a great example of a minimal VisiData application.  This is an extremely functional utility in 25 lines of code, leveraging the essence of the VisiData architecture.  Here it is in its entirety, with line by line annotations:

    #!/usr/bin/env python3

VisiData 2.x requires Python 3.6+.

    import sys
    from visidata import Sheet, ColumnItem, options, asyncthread, run

Import the relevant components used below.

    class TsvSheet(Sheet):
        rowtype = 'rows'  # rowdef: tuple of values

All tabular data sheets inherit from `Sheet`.  The rowtype is displayed on the right status bar.  The `rowdef` comment declares the structure of every row object, and should be present for every Sheet.

        columns = [ColumnItem('tsv', 0)]

An initial column.  Generally the class-level `columns` is set to the actual columns of the sheet, but in this case, the columns aren't known until the source is loaded.
(See the `reload()` function below where they are set from the contents of the first row.)  This line is not strictly necessary but makes loading feel a bit more responsive.


        @asyncthread

@[asyncthread](/docs/async) marks the function to spawn a new thread whenever it is called.

        def reload(self):

The [`reload()`](/docs/loaders) function collects data from the source and puts it into `rows`.  It's called once automatically when first pushed, and manually with `^R`.

            self.rows = []

`rows` is a list of Python objects.  The row definition ('rowdef') for the TsvSheet is a tuple of values, with each position corresponding to one column.

            with open(self.source, encoding=options.encoding) as fp:

`source` is the filename, which has been passed to the constructor (see the last line with `run()`).

                for line in fp:
                    line = line[:-1]
                    if line:
                        self.addRow(line.split('\t'))

For each line, strip the included newline character, and filter out any blank lines.  Add each split tuple to `rows`.

            for i, colname in enumerate(self.rows[0]):
                self.addColumn(ColumnItem(colname, i))

The actual columns are set from the first (header) row.
`ColumnItem` is a builtin, which creates a column to use getitem/setitem with the given key/index.

            self.rows = self.rows[1:]

The header row is removed from the list of rows.  (Column names are displayed on the first row anyway).

    run(*(TsvSheet(fn, source=fn) for fn in sys.argv[1:]))

`run(*sheets)` is the toplevel entry point for a VisiData application.



---

