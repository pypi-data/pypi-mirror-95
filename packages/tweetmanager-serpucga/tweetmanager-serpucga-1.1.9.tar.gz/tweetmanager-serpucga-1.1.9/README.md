# TWEET MANAGER

This application retrieves tweets directly from Twitter and then organizes them
in a structured way and offers tools to convert them to filter them or convert
them to CSV.
Project forked from the json\_to\_csv project.

## Version
version 1.1.8

## Project structure

For the moment the project was just forked from json\_to\_csv, so look at its
documentation for more info.

### Added navigational menu system

Since the project is growing up pretty big, the CLI arguments system is perhaps
becoming confusing. The old system of args invocation continues working
(although it has not been updated for the new features), but a new menu user
interface has been added (everything still runs on terminal). 
Furthermore, there is a new full category of options dedicated to "tweet
collecting tasks". From that submenu, one can add, remove, modify or display
the tweet collecting tasks that (in the future) will be used by the "workers"
to know what tweets to collect.

### Added some functionality for processing CSVs (version 1.1.0)

Some functions have been added to the format\_csv.py module, both for reasons
merely related to display of results, and also for processing and generating
useful CSV data. The most significative addition is get\_csv\_line(), which
needs both a header and a previous CSV file and allows the user to get an
adapted version of the contents of the CSV file for the header provided (the
fields that result in a match are keeped and the rest are written as blanks).
This was needed for our Twitter project.

### Version 1.1.4

More and more bugs have been fixed in the minor releases. The
"list\_of\_pairs\_format\_csv" function has been improved too, so it provides a
quite good visual feedback of large CSV tweet collections.

### Version 1.1.5
Some CSV collections were giving problems when counting lines. This was due to
carriage returns (\r) which were sometimes (but not always) interpreted as
newlines. Now they are substituted by a space in the format4180 function.
### Version 1.1.6
Just changed docs to check that the new hook works fine
### Version 1.1.7
A hidden bug appeared: the compression of arrays was done in an arbitrary,
unsorted way. This was probably unimportant for most data like hashtags and so,
but made it impossible to work properly with the coordinates. A sorting has
been added to rebuild the arrays in the proper order. Added testing for that
case too. 
### Version 1.1.8
Added a "check_flat" bool argument to json2csv. If that argument is False, the
function understands that the input is correctly formatted and doesn't check
it. This is useful to avoid the function from failing if any of the values is
formatted like a dict for whatever reason.
