# macal

[![PyPI - Version](https://img.shields.io/pypi/v/macal.svg)](https://pypi.org/project/macal)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/macal.svg)](https://pypi.org/project/macal)

-----

**Table of Contents**

- [Whats new](#Whats-new)
- [Installation](#Installation)
- [License](#License)
- [About](#About)
- [Howto](#Howto)
- [Variables](#Variables)
- [Strings](#Strings)
- [Const](#Const)
- [Libraries](#Libraries)
- [Creating variables](#Creating)
- [If, elif, else](#If)
- [Functions](#Functions)
- [Foreach](#Foreach)
- [Select](#Select)
- [Break](#Break)
- [Halt](#Halt)
- [Continue](#Continue)
- [Csv Library](#CsvLibrary)
- [Io Library](#IoLibrary)
- [Math Library](#MathLibrary)
- [Strings library](#strings-library)
- [Syslog Library](#Syslog-library)
- [System Library](#System-library)
- [Time Library](#Time-library)
- [Creating an addon library](#Creating-an-addon-library)

## Whats new

In version 5.0 we have rewritten the lexer, parser and the interpreter, we have also introduced a compiler.
- The lexer is simplified
- Recursion is greatly reduced in the parser
- The interpreter is now a bytecode interpreter that interprets bytecode that is compiled with the compiler.
- Clarity of error messages has unfortunately suffered from this.
- There is less type checking done, a small bit of type checking is done at runtime, but error messages
  typically won't provide hints as to where in the code the problem is.
- The bytecode interpreter/runtime is faster than the previous interpreter as it's standalone and doesn't need
  to first lex/parse before running the scripts.
- Creating an addon library, specifically external libraries is greatly simplified.
- Added switch statement to the language
- Added print statement to the language, depricating the Console and Print functions from the system library,
  although they still exist.

- mc program added -> Macal compiler
- md program added -> Macal decompiler
- mi program now does lex, parse, compile, run
- mr program added -> Macal runtime (bytecode interpreter)

- mc and mi can reserve variables on the stack with the -r option. -r --reserved_vars takes a string with a csv
  list with the names of the variables to reserve. 
  Please note that you need to set the values for these variables before executing the script.
  Typically you do this only if you use Macal integrated in your own project and not when running scripts with mi/mr.

- system library has new functions for cli arguments and environment variables
  Args() -> gets the cli arguments as a list
  ArcCount() -> gets the length of the cli arguments list, although you can also use Len from the string library for this.
  Arg(index: int) -> get cli argument [index]
  Env(varname: str) -> get the value from environment variable varname
  SetEnv(varname: str, value: any) -> set the value of the environment variable varname.

- New keyring library
- Meraki_v1 library now included in this distribution, it contains a limited subset of the Meraki Dashboard API.
  I am unsure if this will make it in the final release as it's likely that this library needs more maintenance than Macal itself.  

TODO:
 - type checker
 - code optimizer


## Installation


```bash
python3 -m pip install macal
```


## License


`macal` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.



## About


Macal is a special purpose scripting language for Python.
It's main function is to read, transform and output data using an SQL like SELECT statement.
The instructionset of Macal is limited so it's easy to learn. 
It's possible to extend the language by using libraries.

For those wondering where the name came from: Macal is the name of a river in Belize.
Macal is about controlling the flow of "the river of data".

The following chapters will contain code examples.

Macal comes with an interpreter called 'mi'.

```bash
./mi <path/filename>
```


## Howto


Below is a minimal code example on how to use Macal:

```python
import macal

lang = macal.Macal()
try:
	lang.Run("./test2.mcl"); 
except macal.LexError as ex:
	print(ex)
except macal.SyntaxError as ex:
	print(ex)
except macal.RuntimeError as ex:
	print(ex)
```


## Libraries


There are several libraries included in the macal package.

- csv
- debug
- io
- math
- strings
- syslog
- system
- time

To use a library it needs to be included in the source:

```c
include system;

console("Hello World!");
```

Include can have multiple libraries separated by comma's.



## Variables


A variable is a 'container' for data values.
Macal is a loosely typed language.
This means that you don't explicitly declare a variable to be of a specific type, the type is inferred from the value it has.

The following data types are recognized:

- array     (a list in Python)
- boolean   (true/false lower case)
- float     (a double if you are used to languages as C#)
- function  (when you assign a function to a variable)
- integer
- nil       (None in Python)
- params    (a special type for function definitions)
- record    (a dict in Python)
- string
- variable  (a special type for function definitions)

A variable consists of a name and a value. Before you can use a variable you have to assign a value to it.

```c
include system;

var1 = 42;
var2 = 3.14;
var3 = "Hello World!";
var4 = true;
var5 = nil;
var6 = array;
var7 = record;

console($"{}, {}, {}, {}, {}, {}, {}", var1, var2, var3, var4, var5, var6, var7);
```

This will show the value of each variable on a single line, where variables 6 and 7 an 
empty array and record depicted by [] and {} respectively.

nil is special here because it is both a type and a value.
array and record are special because they are types as well as initializers.

The function type is assigned to a variable that is assigned a function.

```c
include system;

paramtest => () {
	console("test");
}
var = paramtest;
console(type(var));
```

The above example will display FUNCTION because that is the type of the value of the variable var.
In this example you could also pass the function paramtest itself as an argument to the type function with the same result.

Params is special as it is both a type and a keyword.
As a keyword it is used in a function definition to indicate that an argument is to be considered a params type argument.
With this set, all arguments provided in a call to this function will be put into the params argument as if it was an array.

```c
include system, math;

paramtest => (params val) {
	console(type(val));
	foreach val {
		console(it);
	}
}
paramtest(PI, 'PI');
```

The above example will display PARAMS wich is the type of the argument val, followed by the value of the system variable PI as well as the string 'PI'.
A params argument has to be the first and only argument in a function definition.

Variable like params is also both a type and a keyword and used in a function definition.
This makes that the argument that is passed into the function call is required to be a variable. You can't pass any literals like a string or an integer.
You can of course pass a variable that is a string or an integer.

Example:

```console
include system, math;

vartest => (variable var) {
	console(type(var));
}

vartest(PI);
vartest('PI');
```
In the example above, the first call to vartest will display VARIABLE, which is the type of the argument.
Getting the value of the variable that was passed as an argument requires however the use of a the special function getValue(variable)
Getting the type of the value of the variable that was passed as an argument requires the use of the special function getType(variable)



## Strings


A string is a literal value containing text.
When assigning a string it can span over multiple lines.
New lines in the code, will also be in the string.

Example:

```c
include system;

str = "This is a string
Multi line
string.";

console(str);
```

This example will show 3 lines of text:
```console
This is a string
Multi line
string.
```

Concatenation of strings is handled by the + operator.

Example:
```c
include system;

str_a = "string a ";
str_b = "string b";

var = str_a + str_b;
console(var)
```

This will display a single string.

While variables of various types can be converted to a string with the to_string(var) function 
from the strings library, there is a more powerfull way to put values of variables into strings.

This is string interpolation.

An example is:

```c
a=1;
b=2;

str= $"{b} = {a} * 2";
```

The value of the variables a and b will be put into string str.
Macal also supports function calls and expressions inside the curley brackets of string interpolation ({}).


## Const


Const is a special instruction that will create a readonly "variable".
This means that the value of a const can be set at creation time, but can't be changed afterwards.

As an example, the following code will cause a runtime error.

```c

const THEANSWERTOLIFETHEUNIVERSYANDEVERYTHING = 42;

THEANSWERTOLIFETHEUNIVERSYANDEVERYTHING = "Forty Two";

```

Other than the fact that a const is readonly it can be used like a variable.


## Creating Variables


There is no specific command to declare a variable.
A variable is created when a value is assigned to it.

```c
include system;

x = 42;
y = 1.1;
hello = "Hello World";
test = true;
undefined = nil;
data = array;
data[] = 10;
data[] = 1.1;
moredata = record;
moredata["test"] = 1;
moredata["hitchhikers"] = "guidetothegalaxy";

// Display the values:
console(x, " ", y);
console(hello);
console(test);
console(undefined);
console(data[0], " : ", data[1]);
console(moredata["test"]);
console(moredata["hitchhikers"]);
```



## If, elif, else


If and elif are conditional branching statements.
Else is the final branch taken if previous conditions are not met.

The if statement can be used on it's own, or followed by one or more elif statements, 
and finally followed by an optional else statement.

The conditions can be made from logical mathematical equasions like == for equals, != for not equal, > for greater than etc.

It is not required to enclose the condition with brackets ().
If you are mixing mathematical equasions and boolean equasons then you should use brackets.
For example with "(a == 1) and (b == 2)". 
If you don't supply brackets there, the equivalent of this gets processed: "a == (1 and b) == 2", which is something completely different.

```c
a = 1;

if a == 1 {
	console("Hello World!");	
}
elif a == 2 {
	console("Change a = 1 to 2 to be able to see this message.");
}
else {
	console("This should show up only if a is not 1 or 2.");
}
```



## Functions


Functions are "first class" in Macal. Which means you can assign functions to variables, and functions can be returned from functions.
Functions can also be passed in as arguments to other functions.

Function arguments are of "type" any, which means you can pass anything you want into a function parameter.
If your code relies on parameters being a certain type, you should test that.
The System library has several "isXXX" functions that you can use to determine the type of the variable/parameter that you pass in.

The resulting value that is returned by the function using the return statement will have the type specific to the value that is provided after the return statement.


```c
print => (arg) {
    c = arg();
    return c; 
}

fourty_two => () {
  return 42;
}

result = print(fourty_two);
console(result);
```

Above example shows a two functions being defined (print and forty_two) and then one function is passed as a parameter to the other function.
Finally the result is displayed: 42.

It is not required to provide a value in the return statement.

```c
def => (){
	a = 1;
	if a == 1 {
		console("a is 1.");
		return;
	}
	console("a was not 1");
}

def();
```

The result of return in the above example is that the function will stop execution.
The console statement after return is never reached.


There are two special keywords that can change the way that Macal processes arguments passed into a function.

The first is the params keyword.
Consider the function definition:  fncname => (param1, param2, param3) {...}

This function fncname has 3 arguments, param1, param2 and param3.
These arguments can be used inside the function as if they were variables.
When this function is called, 3 arguments are required to be provided.

However for some functions, like a print function, need the ability to have a dynamic amount of arguments.
The params keyword helps with this.

The definition for the function fncname with params becomes:
fncname => (params args) {...}

The function can still be called with 3 arguments: fncname(param1, param2, param3);

However, now inside the code block of the function definition the arguments aren't accessed individually anymore.
Their values are consolidated in the args argument which acts like an array of arguments.
Please note that it's perfectly legal that zero arguments are passed into such a function.
With the len function from the strings library the number of arguments in the args argument can be retrieved.

The second special keyword is variable.
For a normal function definition any type of variable, literal or function can be passed into the function arguments.

With the variable keyword the type of the argument always has to be a variable or a function.
Examples for these are given in the variables chapter.



## Foreach


Foreach is an iterative statement, which means it will iterate over a record, an array or even a string and it will 
repeat it's block of statements as many times as there are "items".

It's only parameter is the object that it will iterate over. Within it's scope there is a variable called 'it' that contains the current 'item' value.

The following code will populate a variable in a array/record structure and is used as the base for other examples in this chapter and the next.

```c
include system;

var  = array;
var[] = record;
var[] = record;
var[] = record;
var[] = record;
var[0]["id"] = 1;
var[1]["id"] = 2;
var[2]["id"] = 3;
var[3]["id"] = 4;
var[0]["title"] = "The Hobbit";
var[1]["title"] = "Foundation";
var[2]["title"] = "The Hitch Hikers Guide to the Galaxy";
var[3]["title"] = "The Lord of The Rings";
var[0]["author"] = "J.R.R. Tolkien";
var[1]["author"] = "Isaac Asimov";
var[2]["author"] = "Douglas Adams";
var[3]["author"] = "J.R.R. Tolkien";
```

Using the above code to populate the variable, lets see some examples of foreach:

```c

foreach var {
	console(it)
}

```
This will iterate over the records in var and output them on the console.

When iterating over a record, the 'it' variable will contain the key index of the record.
This is much like Python's for .. in dict construction.


```c

foreach var[1] {
	console($"'{}' : {}", it, var[1][it]);
}
```

This will display the items of the 2nd record in the array.
It is the equivalent of this:

```c

foreach keys(var[1]) {
	console($"'{}' : {}", it, var[1][it]);
}
```
In the above example you explicitly extract the keys of the record into an array and iterate over that resulting array.


The following example is testing to iterate over a string.
```c
foreach "Runtime" {
	console(it);
}
```
As you can see you can pass the string as a literal instead of having it in a variable.


The next example shows you that you can also use functions that return a value as an operand for foreach:

```c
test => () {
	return "test";
}

foreach test() {
	console(it);
}
```

When you are iterating over a record, you can need to have both the key as well as the value of each item in the record.
You can do this with the special function items() that is in the system library, combined with the special functions key and value.

```c
foreach items(var[2]) {
	console($"Key: {}, Value: {}", key(it), value(it));
}
```

The items function returns the record as an array of key/value pairs.
With the key function you get the key part and with the value function you get the value part of that key/value pair.



## Select


The select statement lies at the core of the Macal language.
It can be used to retrieve data from a data source much like an SQL statement would in a database.
The difference with SQL is that Macal's select statement has variables and functions as data source 
instead of just the database.


It is possible to write a function/library that allows retrieving data from a database and use that function in this select statement as a data source.
An example of how to write a simple library is provided in another chapter.

The output of the select statement is either a record or an array of records.

The way to ensure that the output is always a record is to use the distinct keyword after select.
Where a normal select statement would return an array of records, with distinct only the fist record is returned.

To select all fields the * symbol is used.
To select individual fields (keys in a record), use the name of that field.
For multiple fields use a comma to separate them.
The name of the field in the resulting record can be changed by using the as keyword.

To filter data based on a specific condition use the where keyword.

The variable name after the into keyword indicates into which variable the result of the select statement is stored.

Below are the examples of using the select statement.
The examples all use the same starting template as mentioned in the previous chapter.

```c
select * from var into y;

foreach y {
	console(it);
}
```

The above is the most simple form of the select statement and would be equivalent to: y = var.

A more advanced and interresting form is the following:

```c
select author as Author, title as Title from var where author == 'J.R.R. Tolkien' into y;

foreach y {
	console(it);
}
```

The above select statement selects the author and title fields of the record and renames them with a capital letter first.
It will also filter the result to only contain those records for which the value of the author field is J.R.R. Tolkien.


```c
select distinct author as Author, title as Title from var where author == 'J.R.R. Tolkien' into y;
console(y);
```

With the distinct method the output is limited to just a record.
In the previous example you see that the output of the query without distinct is a list of 2 records.
In this example only the first record will be returned.

It is possible to combine the results of multiple select statements together by using the merge keyword.

```c
select distinct author as Author, title as Title from var where author == 'J.R.R. Tolkien' into y;
select distinct author as Author, title as Title from var where author == 'Douglas Adams' merge into y;

foreach y {
	console(it);
}
```

This will result in y containing an array of 2 records, one from each of the two select statements.

Please note that merge ensures a record is added.
Consider this example:

```c
select distinct author as Author, title as Title from var where author == 'J.R.R. Tolkien' into y;
select distinct author as Author, title as Title from var where author == 'Douglas Adam' merge into y;
```

Notice that the second select has an error in the author's name.
This would result in the record from the first select and an empty record where the field values are nil.


The same is true for fields.
If you provide a list of fields in the select statement, the resulting record(s) will always have all of those fields.
Even so, if the fields don't actually exist in the data source. The value of non existing fields that are returned is nil.



## Break


Break is used to stop the execution of a foreach loop.

The following example uses the same setup code as the ones in the foreach chapter.

```c
foreach var {
	console(it["title"]);
	break;
	console("this doesn’t show");
}

```

The text "this doesn't show" is not displayed. Also only 1 title is shown.

The break statement is usually combined with a condition.

```c
foreach var {
	console(it["title"]);
	if it["title"] == "Foundation" {
		break;
	}
	console("this only shows once");
}
console("This line will show.")
```

The above example would result in two book titles being displayed, separated by the line "this only shows once."
The line "This line will show" will be displayed because break doesn't stop the application from running, it only stops the loop.



## Halt


The halt statement is used to stop execution of the application.
Unlike the break statement that only stops a loop, halt stops everything.
Also halt requires an integer value as an argument.
This is to set the 'exit' variable of the application to a value other than it's default value.

```c
var = "a";
if var == "a" {
	console("This is shown.");
	halt 1;
	console("This does not show.");
}
console("This also is not shown.");
```

In above example the only text that is displayed is "This is shown."
The rest is not shown as the application is terminated at the halt instruction, setting the exit variable (on the root scope) to 1.



## Continue


The continue statement is used in a loop to skip the rest of the loop block and continue with the next iteration.

An example:

```c
lst = list('item 1', 'item 2', 'item 3', false, 'item 4', 'item 5');

foreach lst {
	if it == false { continue; }
	console(it);
}
```

The above example will show all elements in the array, with the exception of the element that has false as value.




## Csv library


headersToCsv(record)

Returns the keys of the record (records are key/value pairs) as a CSV string.

valueToCsv(record)

Returns the values of the record as a CSV string.

arrayToCsv(array)

Returns the element values of the array as a CSV string.



## Io library


load(filename)

Loads a text file returns it as a string.


ReadJSON(filename)

Reads a JSON file and returns it as the apropriate type (record/array).


exists(filename)

Returns true if the file/path exists, otherwise false.


save(filename, content)

Saves the content into the file.
Returns true if successfull, otherwise raises RuntimeError.


WriteJSON(filename, content)

Write the content into a json file.
Returns true if successfull, otherwise raises RuntimeError.


get_last_run(org_name, iso_now)

Checks the /temp for a file (org_name) and loads it, returns the iso timestamp in that file.
If the file doesn't exist returns iso_now
This is handy when you deal with data that collects over time (a log file for example) so you 
know from which point on you have to start processing.


set_last_run(org_name, iso_now)

Stores the iso_now timestamp into a file (org_name) in /temp


## Math library


The math library contains functions and constants that are mathematical in origin.

constant: E 	
constant: PI
constant: TAU

round(arg, digits)

If no digits are supplied:
returns arg rounded to the nearest integer (<.5 rounds down, >= .5 rounds up).
If digits are supplied:
returns arg rounded to the nearest float with digits number of digits.

Please note that the number of digits should fall within the range that a double can represent. Giving a larger number can give undesirable effects.

ceil(arg)

returns arg rounded up to the next whole number.

floor(arg)

returns arg rounded down to the next whole number.

cos(x)

returns cosinus of x where x is a numberic value between between -PI/2 and PI/2  radians.

sin(x)

returns sinus of x where x is a numberic value between between -PI/2 and PI/2  radians.

tan(x)

returns tangent of x where x is a numberic value between between -PI/2 and PI/2  radians.

acos(x)

returns arc cosinus of x where x is a numberic value between between -PI/2 and PI/2  radians.

asin(x)

returns arc sinus of x where x is a numberic value between between -PI/2 and PI/2  radians.

atan(x)

returns arc tangent of x where x is a numberic value between between -PI/2 and PI/2  radians.

pow(x, y)

returns x to the power of y.

sqrt(x)

returns the square root of x.

log(x)

returns the natural logarithm of x.

log2(x)

returns the base 2 logarithm of x.

log10(x)

returns the base 10 logarithm of x.

exp(x)

returns E raised to the power of x.

expm1(x)

returns E raised to the power of x minus 1.
This function is more accurate than calling exp(x) and subtracting 1.



## Strings library


len(x)

Returns the length of x, where x can be an array, a record or a string.
For an array it returns the number of elements. For a record it returns the number of key/value pairs.
For a string it returns the number of characters.


left(str, length)

Returns the left length characters of the string.


mid(str, start, length)

Returns length characters from starting character start of the string.


tostring(arg)

Converts an integer or a float to a string.


format(format, arg)

Like Python's format but unlike that it can only have a single arg value not multiple.

contains(needle, haystack)

Returns true if needle is in haystack, otherwise false.


replace(var, from, with)

Returns a string from the original with from replaced by with.


startswith(str, first)

Returns true if the string starts with first, false if not.


removeNonAscii(str)

Removes all non-ascii characters from the string, but tries to replace these with ascii characters where possible.


replaceEx(var, repl, by)

The same as replace, but repl is an array of strings.

padLeft(string, char, amount)

returns string padded on the left side with amount number of char.

padRight(string, char, amount)

returns string padded on the right side with amount number of char.



## Syslog library



syslog_init(remote)

Initializes the syslog functionality. Remote indicates if the syslog server is supposed to be running on localhost or elsewhere.

syslog_set_address(address, port)

Set the IP address/Host name and Port number for the syslog server if it is a remote server.


syslog(level, message)

Sends the message to the syslog server with the given level (debug, info, warn, error, critical)



## System library


console(params)

Outputs given argument(s) to the console. Multiple arguments are separated by a comma.
String interpolation is also supported, albeit that it's limited to substitution, it does not include formatting.
Because Macal has 2 string terminator types (' and ") it is possible to have a string interpolation inside a string interpolation.

Example:


```c
include system;

a = 7;
b = 6;
c = 42;

console($"This example shows interpolation. {a}*{b}={c}.");

```

Array(params)

Alternate way to define an array. Returns an array of elements made of the arguments given to this function.

```c
include system;

lst = Array('item1'. 2, 'item3', 'the fourth item');

console(lst);

```


record_has_field(record, fieldname)

Returns true if the record has a key fieldname, otherwise returns false.


type(variable)

Returns the variable type of var.


isString(variable)

Returns true if var is a string, false otherwise.

isInt(variable)

Returns true if var is an integer, false otherwise.

isFloat(variable)

Returns true if var is a float, false otherwise.

isBool(variable)

Returns true if var is a boolean, false otherwise.

isArray(variable)

Returns true if var is an array, false otherwise.

isRecord(variable)

Returns true if var is a record, false otherwise.

isFunction(variable)

Returns true if var is a function, false otherwise.

isNil(variable)

Returns true if var has a nil value, false otherwise.

platform()

Returns the current platform the application is running on (Linux, Windows).

ShowVersion()

Prints the version info, author and credits to the console.

items(record)

Returns the items of the record as an array of key/value pairs.
Is to be used in conjunction with key and value functions.

key(keyvalueitem)

returns the key of a key/value pair. Key/value pair aray is generated with the items function.

value(keyvalueitem)

returns the value of a key/value pair. Key/value pair array is generated with the items function.

keys(record)

returns all the keys in the record as an array.

values(record)

returns all the values in the record as an array.

getValue(variable)

Special function only to be used in a function definition, only for getting the value of the variable that was passed into  variable argument.

getType(variable)

Special function only to be used in a function definition, only for getting the type of a the value of the variable that was passed into the variable argument.



## Time library


utcnow()

Returns the current utc date/time.

utcisonow()

Returns the current utc date/time in iso format.

isonow()

Returns the current local date/time in iso format.


now()

Returns the current local date/time.


date_to_unix(date_str)

Returns the unix representation (# of seconds) of the given date string.


iso_to_unix(isodate_str)

Returns the unix representation of the given iso formatted date string.


date_from_unix(seconds)

Returns a date string from the given unix representation.

iso_from_unix(secods)

Returns an iso formatted date string from the given unix representation.


perf_counter()

Returns the value of the system performance counter.
Can be used for a simple stopwatch.



## Creating an addon Library


Creating a new "library" is pretty much the same as creating a normal .mcl file.
In the below example a library test is implemented.
It consists of 2 files: demolib.mcl and demolib.py.

Test.mcl contains the definition of the function print.
The external keyword is used to indicate that this function is implemented in an external python file, specifically in the function Print.

The actual implementation of the function is in the demolib.py python file in the function Print.


File: demolib.mcl
```c

/*
 Author: Marco Caspers
 
 The Demo library is a demonstration on how to create a library for macal.
*/

const DEMOCONST = 'The Demo constant.';

print => (text) external "demolib", "Print";

```

File: demolib.py
```python

# demolib
# Author: Marco Caspers
# Demo Library implementation

import macal


def Print(func:macal.FunctionDefinition, scope: macal.Scope, filename: str):
	"""Implementation of print function for demolib."""
	macal.ValidateFunctionArguments(func, scope, filename)
	text  = scope.GetVariable("text").GetValue()
	ttext = scope.GetVariable("text").GetType()
	print(f"The value of the argument is: {text}")
	print(f"The Type of the argument is: {ttext}")
	scope.SetReturnValue(True)

```

Any function that is callable from a macal library via external has to conform to the interface as shown above.

The ValidateFunctionArguments is not strictly needed, but it is recommended to use it.
It validates if the number of arguments that is passed into the function conforms to the function's definition.
It also validates if the arguments have to correct type of value if the function definition uses special types like params.
It also ensures that all parameters in the function definition exist in the scope as variables.

The scope.GetVariable(<argname>) function is used to get the variable that contains the value of the argument in the function.

The GetVariable() function returns an actual Macal variable type.
You cannot access the value for this variable directly from within Python because the value of a variable in Macal is a metadata structure.

To be able to convert the metadata structure to a Python value you need to call the GetValue() function on the variable.
Likewise for getting the type of the function you call GetType(). 


SetReturnValue sets the return value of the function to the specified value, Macal will figure out what type this Python value will be in inside of Macal.

Please note that when you need to get a Nil value in Macal you will need to set the return value to Python's None.

The following demo shows how to use the demo library in code:

```c
/*

Author: Marco Caspers
This demo shows how to use the demolib library.

*/

include demolib;

var = print(DEMOCONST);
print("A literal string.");
print(var);

```

