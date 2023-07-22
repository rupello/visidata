import json
import datetime

from visidata import Sheet, Column, ExprColumn, date

def toj(payload):
    return json.loads(payload)


def ms2date(ts) -> datetime:
    """
    ts is a UTC timestamp in millis
    """
    d = datetime.datetime.utcfromtimestamp(int(ts)/1000.0)
    return d.replace(tzinfo=datetime.timezone.utc)


def s2date(ts) -> datetime:
    """
    ts is a timestamp in seconds
    """
    d = datetime.datetime.utcfromtimestamp(int(ts))
    return d.replace(tzinfo=datetime.timezone.utc)


def truncate_timestamp(ts:datetime, by='day'):
    methods = {
        'year': {
            'month': 1,
            'day': 1,
            'hour': 0,
            'second': 0,
            'minute': 0,
            'microsecond': 0
        },
        'month': {
            'day': 1,
            'hour': 0,
            'minute': 0,
            'second': 0,
            'microsecond': 0
        },
        'day': {
            'hour': 0,
            'minute': 0,
            'second': 0,
            'microsecond': 0
        },
        'hour': {
            'minute': 0,
            'second': 0,
            'microsecond': 0
        },
        'minute': {
            'second': 0,
            'microsecond': 0
        },
        'second': {
            'microsecond': 0
        },
    }
    return ts.replace(**(methods[by]))


@Sheet.api
def timeTrunc(sheet:Sheet, by:str):
    class TruncatedTimeColumn(Column):
        def __init__(self, name:str, source:Column, by:str):
            super().__init__(name=name)
            self.source = source
            self.by=by

        def calcValue(self, row):
            return truncate_timestamp(self.source.getTypedValue(row),by=self.by)

    source_col = sheet.visibleCols[sheet.cursorVisibleColIndex]
    c = TruncatedTimeColumn(name=f'{source_col.name}_trunc_{by}', source=source_col, by=by)
    sheet.addColumn(c, index=sheet.cursorVisibleColIndex+1)


@Sheet.api
def timeFromEpoch(sheet:Sheet, units:str):
    class TimeFromEpochColumn(Column):
        def __init__(self, name:str, source:Column, units:str):
            super().__init__(name=name)
            self.source = source
            if units=='s':
                self.fconvert = s2date
            elif units=='ms':
                self.fconvert = ms2date
            else:
                raise Exception(f"bad conversion units: {units}")

        def calcValue(self, row):
            return self.fconvert(self.source.getTypedValue(row))

    source_col = sheet.visibleCols[sheet.cursorVisibleColIndex]
    c = TimeFromEpochColumn(name=f'{source_col.name}_timestamp', source=source_col, units=units)
    sheet.addColumn(c, index=sheet.cursorVisibleColIndex+1)


# truncation commands
for by in ["year", "month", "day", "hour", "minute", "second"]:
    Sheet.addCommand('', f'time-trunc-{by}', f'sheet.timeTrunc("{by}")')

# conversion from epoch
Sheet.addCommand('', f'time-from-epoch', f'sheet.timeFromEpoch("s")')
Sheet.addCommand('', f'time-from-epoch-ms', f'sheet.timeFromEpoch("ms")')