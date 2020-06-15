
The datetime module supplies classes for manipulating dates and times.

While date and time arithmetic is supported, the focus of the implementation is on efficient attribute extraction for output formatting and manipulation.

See also

Module calendar

    General calendar related functions.
Module time

    Time access and conversions.
Package dateutil

    Third-party library with expanded time zone and parsing support.

Aware and Naive Objects

Date and time objects may be categorized as “aware” or “naive” depending on whether or not they include timezone information.

With sufficient knowledge of applicable algorithmic and political time adjustments, such as time zone and daylight saving time information, an aware object can locate itself relative to other aware objects. An aware object represents a specific moment in time that is not open to interpretation. 1

A naive object does not contain enough information to unambiguously locate itself relative to other date/time objects. Whether a naive object represents Coordinated Universal Time (UTC), local time, or time in some other timezone is purely up to the program, just like it is up to the program whether a particular number represents metres, miles, or mass. Naive objects are easy to understand and to work with, at the cost of ignoring some aspects of reality.

For applications requiring aware objects, datetime and time objects have an optional time zone information attribute, tzinfo, that can be set to an instance of a subclass of the abstract tzinfo class. These tzinfo objects capture information about the offset from UTC time, the time zone name, and whether daylight saving time is in effect.

Only one concrete tzinfo class, the timezone class, is supplied by the datetime module. The timezone class can represent simple timezones with fixed offsets from UTC, such as UTC itself or North American EST and EDT timezones. Supporting timezones at deeper levels of detail is up to the application. The rules for time adjustment across the world are more political than rational, change frequently, and there is no standard suitable for every application aside from UTC.
Constants

The datetime module exports the following constants:

datetime.MINYEAR

    The smallest year number allowed in a date or datetime object. MINYEAR is 1.

datetime.MAXYEAR

    The largest year number allowed in a date or datetime object. MAXYEAR is 9999.

Available Types

class datetime.date

    An idealized naive date, assuming the current Gregorian calendar always was, and always will be, in effect. Attributes: year, month, and day.

class datetime.time

    An idealized time, independent of any particular day, assuming that every day has exactly 24*60*60 seconds. (There is no notion of “leap seconds” here.) Attributes: hour, minute, second, microsecond, and tzinfo.

class datetime.datetime

    A combination of a date and a time. Attributes: year, month, day, hour, minute, second, microsecond, and tzinfo.

class datetime.timedelta

    A duration expressing the difference between two date, time, or datetime instances to microsecond resolution.

class datetime.tzinfo

    An abstract base class for time zone information objects. These are used by the datetime and time classes to provide a customizable notion of time adjustment (for example, to account for time zone and/or daylight saving time).

class datetime.timezone

    A class that implements the tzinfo abstract base class as a fixed offset from the UTC.

    New in version 3.2.

Objects of these types are immutable.

Subclass relationships:

object
    timedelta
    tzinfo
        timezone
    time
    date
        datetime

Common Properties

The date, datetime, time, and timezone types share these common features:

    Objects of these types are immutable.

    Objects of these types are hashable, meaning that they can be used as dictionary keys.

    Objects of these types support efficient pickling via the pickle module.

Determining if an Object is Aware or Naive

Objects of the date type are always naive.

An object of type time or datetime may be aware or naive.

A datetime object d is aware if both of the following hold:

    d.tzinfo is not None

    d.tzinfo.utcoffset(d) does not return None

Otherwise, d is naive.

A time object t is aware if both of the following hold:

    t.tzinfo is not None

    t.tzinfo.utcoffset(None) does not return None.

Otherwise, t is naive.

The distinction between aware and naive doesn’t apply to timedelta objects.
timedelta Objects

A timedelta object represents a duration, the difference between two dates or times.

class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

    All arguments are optional and default to 0. Arguments may be integers or floats, and may be positive or negative.

    Only days, seconds and microseconds are stored internally. Arguments are converted to those units:

        A millisecond is converted to 1000 microseconds.

        A minute is converted to 60 seconds.

        An hour is converted to 3600 seconds.

        A week is converted to 7 days.

    and days, seconds and microseconds are then normalized so that the representation is unique, with

        0 <= microseconds < 1000000

        0 <= seconds < 3600*24 (the number of seconds in one day)

        -999999999 <= days <= 999999999

    The following example illustrates how any arguments besides days, seconds and microseconds are “merged” and normalized into those three resulting attributes:
    >>>

    >>> from datetime import timedelta
    >>> delta = timedelta(
    ...     days=50,
    ...     seconds=27,
    ...     microseconds=10,
    ...     milliseconds=29000,
    ...     minutes=5,
    ...     hours=8,
    ...     weeks=2
    ... )
    >>> # Only days, seconds, and microseconds remain
    >>> delta
    datetime.timedelta(days=64, seconds=29156, microseconds=10)

    If any argument is a float and there are fractional microseconds, the fractional microseconds left over from all arguments are combined and their sum is rounded to the nearest microsecond using round-half-to-even tiebreaker. If no argument is a float, the conversion and normalization processes are exact (no information is lost).

    If the normalized value of days lies outside the indicated range, OverflowError is raised.

    Note that normalization of negative values may be surprising at first. For example:
    >>>

    >>> from datetime import timedelta
    >>> d = timedelta(microseconds=-1)
    >>> (d.days, d.seconds, d.microseconds)
    (-1, 86399, 999999)

Class attributes:

timedelta.min

    The most negative timedelta object, timedelta(-999999999).

timedelta.max

    The most positive timedelta object, timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999).

timedelta.resolution

    The smallest possible difference between non-equal timedelta objects, timedelta(microseconds=1).

Note that, because of normalization, timedelta.max > -timedelta.min. -timedelta.max is not representable as a timedelta object.

Instance attributes (read-only):

Attribute
	

Value

days
	

Between -999999999 and 999999999 inclusive

seconds
	

Between 0 and 86399 inclusive

microseconds
	

Between 0 and 999999 inclusive

Supported operations:

Operation
	

Result

t1 = t2 + t3
	

Sum of t2 and t3. Afterwards t1-t2 == t3 and t1-t3 == t2 are true. (1)

t1 = t2 - t3
	

Difference of t2 and t3. Afterwards t1 == t2 - t3 and t2 == t1 + t3 are true. (1)(6)

t1 = t2 * i or t1 = i * t2
	

Delta multiplied by an integer. Afterwards t1 // i == t2 is true, provided i != 0.
	

In general, t1 * i == t1 * (i-1) + t1 is true. (1)

t1 = t2 * f or t1 = f * t2
	

Delta multiplied by a float. The result is rounded to the nearest multiple of timedelta.resolution using round-half-to-even.

f = t2 / t3
	

Division (3) of overall duration t2 by interval unit t3. Returns a float object.

t1 = t2 / f or t1 = t2 / i
	

Delta divided by a float or an int. The result is rounded to the nearest multiple of timedelta.resolution using round-half-to-even.

t1 = t2 // i or t1 = t2 // t3
	

The floor is computed and the remainder (if any) is thrown away. In the second case, an integer is returned. (3)

t1 = t2 % t3
	

The remainder is computed as a timedelta object. (3)

q, r = divmod(t1, t2)
	

Computes the quotient and the remainder: q = t1 // t2 (3) and r = t1 % t2. q is an integer and r is a timedelta object.

+t1
	

Returns a timedelta object with the same value. (2)

-t1
	

equivalent to timedelta(-t1.days, -t1.seconds, -t1.microseconds), and to t1* -1. (1)(4)

abs(t)
	

equivalent to +t when t.days >= 0, and to -t when t.days < 0. (2)

str(t)
	

Returns a string in the form [D day[s], ][H]H:MM:SS[.UUUUUU], where D is negative for negative t. (5)

repr(t)
	

Returns a string representation of the timedelta object as a constructor call with canonical attribute values.

Notes:

    This is exact but may overflow.

    This is exact and cannot overflow.

    Division by 0 raises ZeroDivisionError.

    -timedelta.max is not representable as a timedelta object.

    String representations of timedelta objects are normalized similarly to their internal representation. This leads to somewhat unusual results for negative timedeltas. For example:
    >>>

    >>> timedelta(hours=-5)
    datetime.timedelta(days=-1, seconds=68400)
    >>> print(_)
    -1 day, 19:00:00

    The expression t2 - t3 will always be equal to the expression t2 + (-t3) except when t3 is equal to timedelta.max; in that case the former will produce a result while the latter will overflow.

In addition to the operations listed above, timedelta objects support certain additions and subtractions with date and datetime objects (see below).

Changed in version 3.2: Floor division and true division of a timedelta object by another timedelta object are now supported, as are remainder operations and the divmod() function. True division and multiplication of a timedelta object by a float object are now supported.

Comparisons of timedelta objects are supported, with some caveats.

The comparisons == or != always return a bool, no matter the type of the compared object:
>>>

>>> from datetime import timedelta
>>> delta1 = timedelta(seconds=57)
>>> delta2 = timedelta(hours=25, seconds=2)
>>> delta2 != delta1
True
>>> delta2 == 5
False

For all other comparisons (such as < and >), when a timedelta object is compared to an object of a different type, TypeError is raised:
>>>

>>> delta2 > delta1
True
>>> delta2 > 5
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: '>' not supported between instances of 'datetime.timedelta' and 'int'

In Boolean contexts, a timedelta object is considered to be true if and only if it isn’t equal to timedelta(0).

Instance methods:

timedelta.total_seconds()

    Return the total number of seconds contained in the duration. Equivalent to td / timedelta(seconds=1). For interval units other than seconds, use the division form directly (e.g. td / timedelta(microseconds=1)).

    Note that for very large time intervals (greater than 270 years on most platforms) this method will lose microsecond accuracy.

    New in version 3.2.

Examples of usage: timedelta

An additional example of normalization:
>>>

>>> # Components of another_year add up to exactly 365 days
>>> from datetime import timedelta
>>> year = timedelta(days=365)
>>> another_year = timedelta(weeks=40, days=84, hours=23,
...                          minutes=50, seconds=600)
>>> year == another_year
True
>>> year.total_seconds()
31536000.0

Examples of timedelta arithmetic:
>>>

>>> from datetime import timedelta
>>> year = timedelta(days=365)
>>> ten_years = 10 * year
>>> ten_years
datetime.timedelta(days=3650)
>>> ten_years.days // 365
10
>>> nine_years = ten_years - year
>>> nine_years
datetime.timedelta(days=3285)
>>> three_years = nine_years // 3
>>> three_years, three_years.days // 365
(datetime.timedelta(days=1095), 3)

date Objects

A date object represents a date (year, month and day) in an idealized calendar, the current Gregorian calendar indefinitely extended in both directions.

January 1 of year 1 is called day number 1, January 2 of year 1 is called day number 2, and so on. 2

class datetime.date(year, month, day)

    All arguments are required. Arguments must be integers, in the following ranges:

        MINYEAR <= year <= MAXYEAR

        1 <= month <= 12

        1 <= day <= number of days in the given month and year

    If an argument outside those ranges is given, ValueError is raised.

Other constructors, all class methods:

classmethod date.today()

    Return the current local date.

    This is equivalent to date.fromtimestamp(time.time()).

classmethod date.fromtimestamp(timestamp)

    Return the local date corresponding to the POSIX timestamp, such as is returned by time.time().

    This may raise OverflowError, if the timestamp is out of the range of values supported by the platform C localtime() function, and OSError on localtime() failure. It’s common for this to be restricted to years from 1970 through 2038. Note that on non-POSIX systems that include leap seconds in their notion of a timestamp, leap seconds are ignored by fromtimestamp().

    Changed in version 3.3: Raise OverflowError instead of ValueError if the timestamp is out of the range of values supported by the platform C localtime() function. Raise OSError instead of ValueError on localtime() failure.

classmethod date.fromordinal(ordinal)

    Return the date corresponding to the proleptic Gregorian ordinal, where January 1 of year 1 has ordinal 1.

    ValueError is raised unless 1 <= ordinal <= date.max.toordinal(). For any date d, date.fromordinal(d.toordinal()) == d.

classmethod date.fromisoformat(date_string)

    Return a date corresponding to a date_string given in the format YYYY-MM-DD:
    >>>

    >>> from datetime import date
    >>> date.fromisoformat('2019-12-04')
    datetime.date(2019, 12, 4)

    This is the inverse of date.isoformat(). It only supports the format YYYY-MM-DD.

    New in version 3.7.

classmethod date.fromisocalendar(year, week, day)

    Return a date corresponding to the ISO calendar date specified by year, week and day. This is the inverse of the function date.isocalendar().

    New in version 3.8.

Class attributes:

date.min

    The earliest representable date, date(MINYEAR, 1, 1).

date.max

    The latest representable date, date(MAXYEAR, 12, 31).

date.resolution

    The smallest possible difference between non-equal date objects, timedelta(days=1).

Instance attributes (read-only):

date.year

    Between MINYEAR and MAXYEAR inclusive.

date.month

    Between 1 and 12 inclusive.

date.day

    Between 1 and the number of days in the given month of the given year.

Supported operations:

Operation
	

Result

date2 = date1 + timedelta
	

date2 is timedelta.days days removed from date1. (1)

date2 = date1 - timedelta
	

Computes date2 such that date2 + timedelta == date1. (2)

timedelta = date1 - date2
	

(3)

date1 < date2
	

date1 is considered less than date2 when date1 precedes date2 in time. (4)

Notes:

    date2 is moved forward in time if timedelta.days > 0, or backward if timedelta.days < 0. Afterward date2 - date1 == timedelta.days. timedelta.seconds and timedelta.microseconds are ignored. OverflowError is raised if date2.year would be smaller than MINYEAR or larger than MAXYEAR.

    timedelta.seconds and timedelta.microseconds are ignored.

    This is exact, and cannot overflow. timedelta.seconds and timedelta.microseconds are 0, and date2 + timedelta == date1 after.

    In other words, date1 < date2 if and only if date1.toordinal() < date2.toordinal(). Date comparison raises TypeError if the other comparand isn’t also a date object. However, NotImplemented is returned instead if the other comparand has a timetuple() attribute. This hook gives other kinds of date objects a chance at implementing mixed-type comparison. If not, when a date object is compared to an object of a different type, TypeError is raised unless the comparison is == or !=. The latter cases return False or True, respectively.

In Boolean contexts, all date objects are considered to be true.

Instance methods:

date.replace(year=self.year, month=self.month, day=self.day)

    Return a date with the same value, except for those parameters given new values by whichever keyword arguments are specified.

    Example:
    >>>

    >>> from datetime import date
    >>> d = date(2002, 12, 31)
    >>> d.replace(day=26)
    datetime.date(2002, 12, 26)

date.timetuple()

    Return a time.struct_time such as returned by time.localtime().

    The hours, minutes and seconds are 0, and the DST flag is -1.

    d.timetuple() is equivalent to:

    time.struct_time((d.year, d.month, d.day, 0, 0, 0, d.weekday(), yday, -1))

    where yday = d.toordinal() - date(d.year, 1, 1).toordinal() + 1 is the day number within the current year starting with 1 for January 1st.

date.toordinal()

    Return the proleptic Gregorian ordinal of the date, where January 1 of year 1 has ordinal 1. For any date object d, date.fromordinal(d.toordinal()) == d.

date.weekday()

    Return the day of the week as an integer, where Monday is 0 and Sunday is 6. For example, date(2002, 12, 4).weekday() == 2, a Wednesday. See also isoweekday().

date.isoweekday()

    Return the day of the week as an integer, where Monday is 1 and Sunday is 7. For example, date(2002, 12, 4).isoweekday() == 3, a Wednesday. See also weekday(), isocalendar().

date.isocalendar()

    Return a 3-tuple, (ISO year, ISO week number, ISO weekday).

    The ISO calendar is a widely used variant of the Gregorian calendar. 3

    The ISO year consists of 52 or 53 full weeks, and where a week starts on a Monday and ends on a Sunday. The first week of an ISO year is the first (Gregorian) calendar week of a year containing a Thursday. This is called week number 1, and the ISO year of that Thursday is the same as its Gregorian year.

    For example, 2004 begins on a Thursday, so the first week of ISO year 2004 begins on Monday, 29 Dec 2003 and ends on Sunday, 4 Jan 2004:
    >>>

    >>> from datetime import date
    >>> date(2003, 12, 29).isocalendar()
    (2004, 1, 1)
    >>> date(2004, 1, 4).isocalendar()
    (2004, 1, 7)

date.isoformat()

    Return a string representing the date in ISO 8601 format, YYYY-MM-DD:
    >>>

    >>> from datetime import date
    >>> date(2002, 12, 4).isoformat()
    '2002-12-04'

    This is the inverse of date.fromisoformat().

date.__str__()

    For a date d, str(d) is equivalent to d.isoformat().

date.ctime()

    Return a string representing the date:
    >>>

    >>> from datetime import date
    >>> date(2002, 12, 4).ctime()
    'Wed Dec  4 00:00:00 2002'

    d.ctime() is equivalent to:

    time.ctime(time.mktime(d.timetuple()))

    on platforms where the native C ctime() function (which time.ctime() invokes, but which date.ctime() does not invoke) conforms to the C standard.

date.strftime(format)

    Return a string representing the date, controlled by an explicit format string. Format codes referring to hours, minutes or seconds will see 0 values. For a complete list of formatting directives, see strftime() and strptime() Behavior.

date.__format__(format)

    Same as date.strftime(). This makes it possible to specify a format string for a date object in formatted string literals and when using str.format(). For a complete list of formatting directives, see strftime() and strptime() Behavior.

Examples of Usage: date

Example of counting days to an event:
>>>

>>> import time
>>> from datetime import date
>>> today = date.today()
>>> today
datetime.date(2007, 12, 5)
>>> today == date.fromtimestamp(time.time())
True
>>> my_birthday = date(today.year, 6, 24)
>>> if my_birthday < today:
...     my_birthday = my_birthday.replace(year=today.year + 1)
>>> my_birthday
datetime.date(2008, 6, 24)
>>> time_to_birthday = abs(my_birthday - today)
>>> time_to_birthday.days
202

More examples of working with date:

>>> from datetime import date
>>> d = date.fromordinal(730920) # 730920th day after 1. 1. 0001
>>> d
datetime.date(2002, 3, 11)

>>> # Methods related to formatting string output
>>> d.isoformat()
'2002-03-11'
>>> d.strftime("%d/%m/%y")
'11/03/02'
>>> d.strftime("%A %d. %B %Y")
'Monday 11. March 2002'
>>> d.ctime()
'Mon Mar 11 00:00:00 2002'
>>> 'The {1} is {0:%d}, the {2} is {0:%B}.'.format(d, "day", "month")
'The day is 11, the month is March.'

>>> # Methods for to extracting 'components' under different calendars
>>> t = d.timetuple()
>>> for i in t:     
...     print(i)
2002                # year
3                   # month
11                  # day
0
0
0
0                   # weekday (0 = Monday)
70                  # 70th day in the year
-1
>>> ic = d.isocalendar()
>>> for i in ic:    
...     print(i)
2002                # ISO year
11                  # ISO week number
1                   # ISO day number ( 1 = Monday )

>>> # A date object is immutable; all operations produce a new object
>>> d.replace(year=2005)
datetime.date(2005, 3, 11)

datetime Objects

A datetime object is a single object containing all the information from a date object and a time object.

Like a date object, datetime assumes the current Gregorian calendar extended in both directions; like a time object, datetime assumes there are exactly 3600*24 seconds in every day.

Constructor:

class datetime.datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)

    The year, month and day arguments are required. tzinfo may be None, or an instance of a tzinfo subclass. The remaining arguments must be integers in the following ranges:

        MINYEAR <= year <= MAXYEAR,

        1 <= month <= 12,

        1 <= day <= number of days in the given month and year,

        0 <= hour < 24,

        0 <= minute < 60,

        0 <= second < 60,

        0 <= microsecond < 1000000,

        fold in [0, 1].

    If an argument outside those ranges is given, ValueError is raised.

    New in version 3.6: Added the fold argument.

Other constructors, all class methods:

classmethod datetime.today()

    Return the current local datetime, with tzinfo None.

    Equivalent to:

    datetime.fromtimestamp(time.time())

    See also now(), fromtimestamp().

    This method is functionally equivalent to now(), but without a tz parameter.

classmethod datetime.now(tz=None)

    Return the current local date and time.

    If optional argument tz is None or not specified, this is like today(), but, if possible, supplies more precision than can be gotten from going through a time.time() timestamp (for example, this may be possible on platforms supplying the C gettimeofday() function).

    If tz is not None, it must be an instance of a tzinfo subclass, and the current date and time are converted to tz’s time zone.

    This function is preferred over today() and utcnow().

classmethod datetime.utcnow()

    Return the current UTC date and time, with tzinfo None.

    This is like now(), but returns the current UTC date and time, as a naive datetime object. An aware current UTC datetime can be obtained by calling datetime.now(timezone.utc). See also now().

    Warning

    Because naive datetime objects are treated by many datetime methods as local times, it is preferred to use aware datetimes to represent times in UTC. As such, the recommended way to create an object representing the current time in UTC is by calling datetime.now(timezone.utc).

classmethod datetime.fromtimestamp(timestamp, tz=None)

    Return the local date and time corresponding to the POSIX timestamp, such as is returned by time.time(). If optional argument tz is None or not specified, the timestamp is converted to the platform’s local date and time, and the returned datetime object is naive.

    If tz is not None, it must be an instance of a tzinfo subclass, and the timestamp is converted to tz’s time zone.

    fromtimestamp() may raise OverflowError, if the timestamp is out of the range of values supported by the platform C localtime() or gmtime() functions, and OSError on localtime() or gmtime() failure. It’s common for this to be restricted to years in 1970 through 2038. Note that on non-POSIX systems that include leap seconds in their notion of a timestamp, leap seconds are ignored by fromtimestamp(), and then it’s possible to have two timestamps differing by a second that yield identical datetime objects. This method is preferred over utcfromtimestamp().

    Changed in version 3.3: Raise OverflowError instead of ValueError if the timestamp is out of the range of values supported by the platform C localtime() or gmtime() functions. Raise OSError instead of ValueError on localtime() or gmtime() failure.

    Changed in version 3.6: fromtimestamp() may return instances with fold set to 1.

classmethod datetime.utcfromtimestamp(timestamp)

    Return the UTC datetime corresponding to the POSIX timestamp, with tzinfo None. (The resulting object is naive.)

    This may raise OverflowError, if the timestamp is out of the range of values supported by the platform C gmtime() function, and OSError on gmtime() failure. It’s common for this to be restricted to years in 1970 through 2038.

    To get an aware datetime object, call fromtimestamp():

    datetime.fromtimestamp(timestamp, timezone.utc)

    On the POSIX compliant platforms, it is equivalent to the following expression:

    datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=timestamp)

    except the latter formula always supports the full years range: between MINYEAR and MAXYEAR inclusive.

    Warning

    Because naive datetime objects are treated by many datetime methods as local times, it is preferred to use aware datetimes to represent times in UTC. As such, the recommended way to create an object representing a specific timestamp in UTC is by calling datetime.fromtimestamp(timestamp, tz=timezone.utc).

    Changed in version 3.3: Raise OverflowError instead of ValueError if the timestamp is out of the range of values supported by the platform C gmtime() function. Raise OSError instead of ValueError on gmtime() failure.

classmethod datetime.fromordinal(ordinal)

    Return the datetime corresponding to the proleptic Gregorian ordinal, where January 1 of year 1 has ordinal 1. ValueError is raised unless 1 <= ordinal <= datetime.max.toordinal(). The hour, minute, second and microsecond of the result are all 0, and tzinfo is None.

classmethod datetime.combine(date, time, tzinfo=self.tzinfo)

    Return a new datetime object whose date components are equal to the given date object’s, and whose time components are equal to the given time object’s. If the tzinfo argument is provided, its value is used to set the tzinfo attribute of the result, otherwise the tzinfo attribute of the time argument is used.

    For any datetime object d, d == datetime.combine(d.date(), d.time(), d.tzinfo). If date is a datetime object, its time components and tzinfo attributes are ignored.

    Changed in version 3.6: Added the tzinfo argument.

classmethod datetime.fromisoformat(date_string)

    Return a datetime corresponding to a date_string in one of the formats emitted by date.isoformat() and datetime.isoformat().

    Specifically, this function supports strings in the format:

    YYYY-MM-DD[*HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]]

    where * can match any single character.

    Caution

    This does not support parsing arbitrary ISO 8601 strings - it is only intended as the inverse operation of datetime.isoformat(). A more full-featured ISO 8601 parser, dateutil.parser.isoparse is available in the third-party package dateutil.

    Examples:
    >>>

    >>> from datetime import datetime
    >>> datetime.fromisoformat('2011-11-04')
    datetime.datetime(2011, 11, 4, 0, 0)
    >>> datetime.fromisoformat('2011-11-04T00:05:23')
    datetime.datetime(2011, 11, 4, 0, 5, 23)
    >>> datetime.fromisoformat('2011-11-04 00:05:23.283')
    datetime.datetime(2011, 11, 4, 0, 5, 23, 283000)
    >>> datetime.fromisoformat('2011-11-04 00:05:23.283+00:00')
    datetime.datetime(2011, 11, 4, 0, 5, 23, 283000, tzinfo=datetime.timezone.utc)
    >>> datetime.fromisoformat('2011-11-04T00:05:23+04:00')   
    datetime.datetime(2011, 11, 4, 0, 5, 23,
        tzinfo=datetime.timezone(datetime.timedelta(seconds=14400)))

    New in version 3.7.

classmethod datetime.fromisocalendar(year, week, day)

    Return a datetime corresponding to the ISO calendar date specified by year, week and day. The non-date components of the datetime are populated with their normal default values. This is the inverse of the function datetime.isocalendar().

    New in version 3.8.

classmethod datetime.strptime(date_string, format)

    Return a datetime corresponding to date_string, parsed according to format.

    This is equivalent to:

    datetime(*(time.strptime(date_string, format)[0:6]))

    ValueError is raised if the date_string and format can’t be parsed by time.strptime() or if it returns a value which isn’t a time tuple. For a complete list of formatting directives, see strftime() and strptime() Behavior.

Class attributes:

datetime.min

    The earliest representable datetime, datetime(MINYEAR, 1, 1, tzinfo=None).

datetime.max

    The latest representable datetime, datetime(MAXYEAR, 12, 31, 23, 59, 59, 999999, tzinfo=None).

datetime.resolution

    The smallest possible difference between non-equal datetime objects, timedelta(microseconds=1).

Instance attributes (read-only):

datetime.year

    Between MINYEAR and MAXYEAR inclusive.

datetime.month

    Between 1 and 12 inclusive.

datetime.day

    Between 1 and the number of days in the given month of the given year.

datetime.hour

    In range(24).

datetime.minute

    In range(60).

datetime.second

    In range(60).

datetime.microsecond

    In range(1000000).

datetime.tzinfo

    The object passed as the tzinfo argument to the datetime constructor, or None if none was passed.

datetime.fold

    In [0, 1]. Used to disambiguate wall times during a repeated interval. (A repeated interval occurs when clocks are rolled back at the end of daylight saving time or when the UTC offset for the current zone is decreased for political reasons.) The value 0 (1) represents the earlier (later) of the two moments with the same wall time representation.

    New in version 3.6.

Supported operations:

Operation
	

Result

datetime2 = datetime1 + timedelta
	

(1)

datetime2 = datetime1 - timedelta
	

(2)

timedelta = datetime1 - datetime2
	

(3)

datetime1 < datetime2
	

Compares datetime to datetime. (4)

    datetime2 is a duration of timedelta removed from datetime1, moving forward in time if timedelta.days > 0, or backward if timedelta.days < 0. The result has the same tzinfo attribute as the input datetime, and datetime2 - datetime1 == timedelta after. OverflowError is raised if datetime2.year would be smaller than MINYEAR or larger than MAXYEAR. Note that no time zone adjustments are done even if the input is an aware object.

    Computes the datetime2 such that datetime2 + timedelta == datetime1. As for addition, the result has the same tzinfo attribute as the input datetime, and no time zone adjustments are done even if the input is aware.

    Subtraction of a datetime from a datetime is defined only if both operands are naive, or if both are aware. If one is aware and the other is naive, TypeError is raised.

    If both are naive, or both are aware and have the same tzinfo attribute, the tzinfo attributes are ignored, and the result is a timedelta object t such that datetime2 + t == datetime1. No time zone adjustments are done in this case.

    If both are aware and have different tzinfo attributes, a-b acts as if a and b were first converted to naive UTC datetimes first. The result is (a.replace(tzinfo=None) - a.utcoffset()) - (b.replace(tzinfo=None) - b.utcoffset()) except that the implementation never overflows.

    datetime1 is considered less than datetime2 when datetime1 precedes datetime2 in time.

    If one comparand is naive and the other is aware, TypeError is raised if an order comparison is attempted. For equality comparisons, naive instances are never equal to aware instances.

    If both comparands are aware, and have the same tzinfo attribute, the common tzinfo attribute is ignored and the base datetimes are compared. If both comparands are aware and have different tzinfo attributes, the comparands are first adjusted by subtracting their UTC offsets (obtained from self.utcoffset()).

    Changed in version 3.3: Equality comparisons between aware and naive datetime instances don’t raise TypeError.

    Note

    In order to stop comparison from falling back to the default scheme of comparing object addresses, datetime comparison normally raises TypeError if the other comparand isn’t also a datetime object. However, NotImplemented is returned instead if the other comparand has a timetuple() attribute. This hook gives other kinds of date objects a chance at implementing mixed-type comparison. If not, when a datetime object is compared to an object of a different type, TypeError is raised unless the comparison is == or !=. The latter cases return False or True, respectively.

Instance methods:

datetime.date()

    Return date object with same year, month and day.

datetime.time()

    Return time object with same hour, minute, second, microsecond and fold. tzinfo is None. See also method timetz().

    Changed in version 3.6: The fold value is copied to the returned time object.

datetime.timetz()

    Return time object with same hour, minute, second, microsecond, fold, and tzinfo attributes. See also method time().

    Changed in version 3.6: The fold value is copied to the returned time object.

datetime.replace(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, * fold=0)

    Return a datetime with the same attributes, except for those attributes given new values by whichever keyword arguments are specified. Note that tzinfo=None can be specified to create a naive datetime from an aware datetime with no conversion of date and time data.

    New in version 3.6: Added the fold argument.

datetime.astimezone(tz=None)

    Return a datetime object with new tzinfo attribute tz, adjusting the date and time data so the result is the same UTC time as self, but in tz’s local time.

    If provided, tz must be an instance of a tzinfo subclass, and its utcoffset() and dst() methods must not return None. If self is naive, it is presumed to represent time in the system timezone.

    If called without arguments (or with tz=None) the system local timezone is assumed for the target timezone. The .tzinfo attribute of the converted datetime instance will be set to an instance of timezone with the zone name and offset obtained from the OS.

    If self.tzinfo is tz, self.astimezone(tz) is equal to self: no adjustment of date or time data is performed. Else the result is local time in the timezone tz, representing the same UTC time as self: after astz = dt.astimezone(tz), astz - astz.utcoffset() will have the same date and time data as dt - dt.utcoffset().

    If you merely want to attach a time zone object tz to a datetime dt without adjustment of date and time data, use dt.replace(tzinfo=tz). If you merely want to remove the time zone object from an aware datetime dt without conversion of date and time data, use dt.replace(tzinfo=None).

    Note that the default tzinfo.fromutc() method can be overridden in a tzinfo subclass to affect the result returned by astimezone(). Ignoring error cases, astimezone() acts like:

    def astimezone(self, tz):
        if self.tzinfo is tz:
            return self
        # Convert self to UTC, and attach the new time zone object.
        utc = (self - self.utcoffset()).replace(tzinfo=tz)
        # Convert from UTC to tz's local time.
        return tz.fromutc(utc)

    Changed in version 3.3: tz now can be omitted.

    Changed in version 3.6: The astimezone() method can now be called on naive instances that are presumed to represent system local time.

datetime.utcoffset()

    If tzinfo is None, returns None, else returns self.tzinfo.utcoffset(self), and raises an exception if the latter doesn’t return None or a timedelta object with magnitude less than one day.

    Changed in version 3.7: The UTC offset is not restricted to a whole number of minutes.

datetime.dst()

    If tzinfo is None, returns None, else returns self.tzinfo.dst(self), and raises an exception if the latter doesn’t return None or a timedelta object with magnitude less than one day.

    Changed in version 3.7: The DST offset is not restricted to a whole number of minutes.

datetime.tzname()

    If tzinfo is None, returns None, else returns self.tzinfo.tzname(self), raises an exception if the latter doesn’t return None or a string object,

datetime.timetuple()

    Return a time.struct_time such as returned by time.localtime().

    d.timetuple() is equivalent to:

    time.struct_time((d.year, d.month, d.day,
                      d.hour, d.minute, d.second,
                      d.weekday(), yday, dst))

    where yday = d.toordinal() - date(d.year, 1, 1).toordinal() + 1 is the day number within the current year starting with 1 for January 1st. The tm_isdst flag of the result is set according to the dst() method: tzinfo is None or dst() returns None, tm_isdst is set to -1; else if dst() returns a non-zero value, tm_isdst is set to 1; else tm_isdst is set to 0.

datetime.utctimetuple()

    If datetime instance d is naive, this is the same as d.timetuple() except that tm_isdst is forced to 0 regardless of what d.dst() returns. DST is never in effect for a UTC time.

    If d is aware, d is normalized to UTC time, by subtracting d.utcoffset(), and a time.struct_time for the normalized time is returned. tm_isdst is forced to 0. Note that an OverflowError may be raised if d.year was MINYEAR or MAXYEAR and UTC adjustment spills over a year boundary.

    Warning

    Because naive datetime objects are treated by many datetime methods as local times, it is preferred to use aware datetimes to represent times in UTC; as a result, using utcfromtimetuple may give misleading results. If you have a naive datetime representing UTC, use datetime.replace(tzinfo=timezone.utc) to make it aware, at which point you can use datetime.timetuple().

datetime.toordinal()

    Return the proleptic Gregorian ordinal of the date. The same as self.date().toordinal().

datetime.timestamp()

    Return POSIX timestamp corresponding to the datetime instance. The return value is a float similar to that returned by time.time().

    Naive datetime instances are assumed to represent local time and this method relies on the platform C mktime() function to perform the conversion. Since datetime supports wider range of values than mktime() on many platforms, this method may raise OverflowError for times far in the past or far in the future.

    For aware datetime instances, the return value is computed as:

    (dt - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()

    New in version 3.3.

    Changed in version 3.6: The timestamp() method uses the fold attribute to disambiguate the times during a repeated interval.

    Note

    There is no method to obtain the POSIX timestamp directly from a naive datetime instance representing UTC time. If your application uses this convention and your system timezone is not set to UTC, you can obtain the POSIX timestamp by supplying tzinfo=timezone.utc:

    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

    or by calculating the timestamp directly:

    timestamp = (dt - datetime(1970, 1, 1)) / timedelta(seconds=1)

datetime.weekday()

    Return the day of the week as an integer, where Monday is 0 and Sunday is 6. The same as self.date().weekday(). See also isoweekday().

datetime.isoweekday()

    Return the day of the week as an integer, where Monday is 1 and Sunday is 7. The same as self.date().isoweekday(). See also weekday(), isocalendar().

datetime.isocalendar()

    Return a 3-tuple, (ISO year, ISO week number, ISO weekday). The same as self.date().isocalendar().

datetime.isoformat(sep='T', timespec='auto')

    Return a string representing the date and time in ISO 8601 format:

        YYYY-MM-DDTHH:MM:SS.ffffff, if microsecond is not 0

        YYYY-MM-DDTHH:MM:SS, if microsecond is 0

    If utcoffset() does not return None, a string is appended, giving the UTC offset:

        YYYY-MM-DDTHH:MM:SS.ffffff+HH:MM[:SS[.ffffff]], if microsecond is not 0

        YYYY-MM-DDTHH:MM:SS+HH:MM[:SS[.ffffff]], if microsecond is 0

    Examples:
    >>>

    >>> from datetime import datetime, timezone
    >>> datetime(2019, 5, 18, 15, 17, 8, 132263).isoformat()
    '2019-05-18T15:17:08.132263'
    >>> datetime(2019, 5, 18, 15, 17, tzinfo=timezone.utc).isoformat()
    '2019-05-18T15:17:00+00:00'

    The optional argument sep (default 'T') is a one-character separator, placed between the date and time portions of the result. For example:
    >>>

    >>> from datetime import tzinfo, timedelta, datetime
    >>> class TZ(tzinfo):
    ...     """A time zone with an arbitrary, constant -06:39 offset."""
    ...     def utcoffset(self, dt):
    ...         return timedelta(hours=-6, minutes=-39)
    ...
    >>> datetime(2002, 12, 25, tzinfo=TZ()).isoformat(' ')
    '2002-12-25 00:00:00-06:39'
    >>> datetime(2009, 11, 27, microsecond=100, tzinfo=TZ()).isoformat()
    '2009-11-27T00:00:00.000100-06:39'

    The optional argument timespec specifies the number of additional components of the time to include (the default is 'auto'). It can be one of the following:

        'auto': Same as 'seconds' if microsecond is 0, same as 'microseconds' otherwise.

        'hours': Include the hour in the two-digit HH format.

        'minutes': Include hour and minute in HH:MM format.

        'seconds': Include hour, minute, and second in HH:MM:SS format.

        'milliseconds': Include full time, but truncate fractional second part to milliseconds. HH:MM:SS.sss format.

        'microseconds': Include full time in HH:MM:SS.ffffff format.

    Note

    Excluded time components are truncated, not rounded.

    ValueError will be raised on an invalid timespec argument:
    >>>

    >>> from datetime import datetime
    >>> datetime.now().isoformat(timespec='minutes')   
    '2002-12-25T00:00'
    >>> dt = datetime(2015, 1, 1, 12, 30, 59, 0)
    >>> dt.isoformat(timespec='microseconds')
    '2015-01-01T12:30:59.000000'

    New in version 3.6: Added the timespec argument.

datetime.__str__()

    For a datetime instance d, str(d) is equivalent to d.isoformat(' ').

datetime.ctime()

    Return a string representing the date and time:
    >>>

    >>> from datetime import datetime
    >>> datetime(2002, 12, 4, 20, 30, 40).ctime()
    'Wed Dec  4 20:30:40 2002'

    The output string will not include time zone information, regardless of whether the input is aware or naive.

    d.ctime() is equivalent to:

    time.ctime(time.mktime(d.timetuple()))

    on platforms where the native C ctime() function (which time.ctime() invokes, but which datetime.ctime() does not invoke) conforms to the C standard.

datetime.strftime(format)

    Return a string representing the date and time, controlled by an explicit format string. For a complete list of formatting directives, see strftime() and strptime() Behavior.

datetime.__format__(format)

    Same as datetime.strftime(). This makes it possible to specify a format string for a datetime object in formatted string literals and when using str.format(). For a complete list of formatting directives, see strftime() and strptime() Behavior.

Examples of Usage: datetime

Examples of working with datetime objects:

>>> from datetime import datetime, date, time, timezone

>>> # Using datetime.combine()
>>> d = date(2005, 7, 14)
>>> t = time(12, 30)
>>> datetime.combine(d, t)
datetime.datetime(2005, 7, 14, 12, 30)

>>> # Using datetime.now()
>>> datetime.now()   
datetime.datetime(2007, 12, 6, 16, 29, 43, 79043)   # GMT +1
>>> datetime.now(timezone.utc)   
datetime.datetime(2007, 12, 6, 15, 29, 43, 79060, tzinfo=datetime.timezone.utc)

>>> # Using datetime.strptime()
>>> dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
>>> dt
datetime.datetime(2006, 11, 21, 16, 30)

>>> # Using datetime.timetuple() to get tuple of all attributes
>>> tt = dt.timetuple()
>>> for it in tt:   
...     print(it)
...
2006    # year
11      # month
21      # day
16      # hour
30      # minute
0       # second
1       # weekday (0 = Monday)
325     # number of days since 1st January
-1      # dst - method tzinfo.dst() returned None

>>> # Date in ISO format
>>> ic = dt.isocalendar()
>>> for it in ic:   
...     print(it)
...
2006    # ISO year
47      # ISO week
2       # ISO weekday

>>> # Formatting a datetime
>>> dt.strftime("%A, %d. %B %Y %I:%M%p")
'Tuesday, 21. November 2006 04:30PM'
>>> 'The {1} is {0:%d}, the {2} is {0:%B}, the {3} is {0:%I:%M%p}.'.format(dt, "day", "month", "time")
'The day is 21, the month is November, the time is 04:30PM.'

The example below defines a tzinfo subclass capturing time zone information for Kabul, Afghanistan, which used +4 UTC until 1945 and then +4:30 UTC thereafter:

from datetime import timedelta, datetime, tzinfo, timezone

class KabulTz(tzinfo):
    # Kabul used +4 until 1945, when they moved to +4:30
    UTC_MOVE_DATE = datetime(1944, 12, 31, 20, tzinfo=timezone.utc)

    def utcoffset(self, dt):
        if dt.year < 1945:
            return timedelta(hours=4)
        elif (1945, 1, 1, 0, 0) <= dt.timetuple()[:5] < (1945, 1, 1, 0, 30):
            # An ambiguous ("imaginary") half-hour range representing
            # a 'fold' in time due to the shift from +4 to +4:30.
            # If dt falls in the imaginary range, use fold to decide how
            # to resolve. See PEP495.
            return timedelta(hours=4, minutes=(30 if dt.fold else 0))
        else:
            return timedelta(hours=4, minutes=30)

    def fromutc(self, dt):
        # Follow same validations as in datetime.tzinfo
        if not isinstance(dt, datetime):
            raise TypeError("fromutc() requires a datetime argument")
        if dt.tzinfo is not self:
            raise ValueError("dt.tzinfo is not self")

        # A custom implementation is required for fromutc as
        # the input to this function is a datetime with utc values
        # but with a tzinfo set to self.
        # See datetime.astimezone or fromtimestamp.
        if dt.replace(tzinfo=timezone.utc) >= self.UTC_MOVE_DATE:
            return dt + timedelta(hours=4, minutes=30)
        else:
            return dt + timedelta(hours=4)

    def dst(self, dt):
        # Kabul does not observe daylight saving time.
        return timedelta(0)

    def tzname(self, dt):
        if dt >= self.UTC_MOVE_DATE:
            return "+04:30"
        return "+04"

Usage of KabulTz from above:
>>>

>>> tz1 = KabulTz()

>>> # Datetime before the change
>>> dt1 = datetime(1900, 11, 21, 16, 30, tzinfo=tz1)
>>> print(dt1.utcoffset())
4:00:00

>>> # Datetime after the change
>>> dt2 = datetime(2006, 6, 14, 13, 0, tzinfo=tz1)
>>> print(dt2.utcoffset())
4:30:00

>>> # Convert datetime to another time zone
>>> dt3 = dt2.astimezone(timezone.utc)
>>> dt3
datetime.datetime(2006, 6, 14, 8, 30, tzinfo=datetime.timezone.utc)
>>> dt2
datetime.datetime(2006, 6, 14, 13, 0, tzinfo=KabulTz())
>>> dt2 == dt3
True

time Objects

A time object represents a (local) time of day, independent of any particular day, and subject to adjustment via a tzinfo object.
