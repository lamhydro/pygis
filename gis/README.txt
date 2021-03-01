Notes about Python

#Installing GDAL/OSGEO
1) Download gdal executable from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal or (even better):
http://www.gisinternals.com/sdk/PackageList.aspx?file=release-1600-gdal-1-10-mapserver-6-4.zip
2) Execute the file. GDAL is usually installed in: "C:\\Python27\\Lib\\site-packages"

#Importing GDAL/OSGEO from iPhyton in windows
1) Type
import sys, os # Import those libraries
2) Type (this check is the gdal path is already in the system path. if it is not, it is appended. )
if "C:\\Python27\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\Lib\\site-packages")
3) Import osgeo, (or even gdal) 
from osgeo import ogr

#Running a python script in iPhyton
Type: run script.py
Type: Eg.: run "C:\Users\Luis\Documents\Python Scripts\createShpFile.py"

#Change a directory in iPhyton when the name is separaged by gaps.
cd Python Scripts (remove the backslash after the first word)

Python Programming Notes

Source: http://www.greenteapress.com/thinkpython/thinkCSpy/html/chap08.html
String
a = "luis"
a[0]
yield l
An important difference between string and list is that elements in the first one are no modificable, but it is true in lists, so
a[0] = L is not posible
but if a = [1,2,3,4,5]
a[2]= 100
yield a = [1,2,100,4,5]
so that, list are mutables and string are imnutables
List
List characteristics include:
- can store objects of different types
- can store elements of different sizes.
To slice a list
a = [1,3,4,5]
a[1:]
will yield [3,4,5]
a[1:2]
will yield [3,4]
A range of list elements can be deleted using:
a[1:3] = []
yield a[1,5]
Individual elements can be deleted as
del a[1] 
or
a[1:2] = []
yield a[1,4,5]
New elements can be included into the list as
a[1:1] = [-1] (remember the parenthesi)
yield a = [1,-1,3,4,5]
also
a[3:3]=['luis']
yield a = [1,3,4,'luis',5]
insted
a[3:3] = 'luis'
yield [1, 3, 4, 'l', 'u', 'i', 's', 5], iterate along the string.
Object: It is something in memory at which one or more variables point to. So for example:
a = 'luis'
b = 'luis'
here a and b point to the object luis (check using id(a) = id(b)). In the case of list it does not work similarly, so
a = [1,2,3]
b = [1,2,3]
both point to different objects. However if you make
b = a
here both point to the same place. So to clone(or copy) a list we must slice the whole vector:
a = [1,2,3]
b = a[:]
The split function in the string module break string into a list of words. so
import string
name = "Luis Alejandro Morales Marin"
string.split(name)
["Luis","Alejandro","Morales","Marin"]

Tuples
These are similar to list but are immnutable. Elements are separated by commans and can be created as
tuple = 'l','u','i','s'
or
tuple = ('l','u','i','s')
a tuple of a 1 element have to be created as
t1 = ('a',)
no included the comma, yield t1 being a string. Accessing tuple elements are similar than for lists. To modify an element of a tuple, we need to replacce it with a different tuple:
tuple = ('L',) + tuple[1:]
yield ['L','u','i','s']
Tuple assignment that solves the problem of interchange values between two tuples is
a, b = b, a 
left are tuples, and right are values.
Functions can return tuples as return values. For example, we could write a function that swaps two parameters:
def swap(x, y): 
  return y, x 
Then we can assign the return value to a tuple with two variables:
a, b = swap(a, b) 

Dictionaries
The compound types you have learned about     strings, lists, and tuples     use integers as indices. If you try to use any other type as an index, you get an error.
Dictionaries are similar to other compound types except that they can use any immutable type as an index. As an example, we will create a dictionary to translate English words into Spanish. For this dictionary, the indices are strings.
One way to create a dictionary is to start with the empty dictionary and add elements. The empty dictionary is denoted {}:

eng2sp = {} 
eng2sp['one'] = 'uno' 
eng2sp['two'] = 'dos' 

The first assignment creates a dictionary named eng2sp; the other assignments add new elements to the dictionary. 

eng2sp = {'one': 'uno', 'two': 'dos', 'three': 'tres'} 

If we print the value of eng2sp again, we get a surprise:

print eng2sp 
{'one': 'uno', 'three': 'tres', 'two': 'dos'} 

The key-value pairs are not in order! Fortunately, there is no reason to care about the order, since the elements of a dictionary are never indexed with integer indices. Instead, we use the keys to look up the corresponding values:

print eng2sp['two'] 
'dos' 

The key 'two' yields the value 'dos' even though it appears in the third key-value pair.
To change a value associate with a element with make
eng2sp['two'] = 'none'
yield {'one': 'uno', 'three': 'tres', 'two': 'none'}
To delete a element, we make
del eng2sp['one']
yield {'three': 'tres', 'two': 'dos'}

Dictionary method
A method is similar to a function     it takes arguments and returns a value     but the syntax is different. For example, the keys method takes a dictionary and returns a list of the keys that appear, but instead of the function syntax keys(eng2sp), we use the method syntax eng2sp.keys().

eng2sp.keys() 
['one', 'three', 'two'] 

A method call is called an invocation; in this case, we would say that we are invoking keys on the object eng2sp.

The values method is similar; it returns a list of the values in the dictionary:

eng2sp.values() 
['uno', 'tres', 'dos'] 

The items method returns both, in the form of a list of tuples     one for each key-value pair:

eng2sp.items() 
[('one','uno'), ('three', 'tres'), ('two', 'dos')] 

Aliasing and copying
Because dictionaries are mutable, you need to be aware of aliasing. Whenever two variables refer to the same object, changes to one affect the other.

If you want to modify a dictionary and keep a copy of the original, use the copy method. For example, opposites is a dictionary that contains pairs of opposites:

opposites = {'up': 'down', 'right': 'wrong', 'true': 'false'} 
alias = opposites 
copy = opposites.copy() 

alias and opposites refer to the same object; copy refers to a fresh copy of the same dictionary. If we modify alias, opposites is also changed:

alias['right'] = 'left' 
opposites['right'] 
'left' 

If we modify copy, opposites is unchanged:

copy['right'] = 'privilege' 
opposites['right'] 
'left' 

Sparse matrices
In Section 8.14, we used a list of lists to represent a matrix. That is a good choice for a matrix with mostly nonzero values, but consider a sparse matrix like this one:



The list representation contains a lot of zeroes:

matrix = [ [0,0,0,1,0], 
           [0,0,0,0,0], 
           [0,2,0,0,0], 
           [0,0,0,0,0], 
           [0,0,0,3,0] ] 

An alternative is to use a dictionary. For the keys, we can use tuples that contain the row and column numbers. Here is the dictionary representation of the same matrix:

matrix = {(0,3): 1, (2, 1): 2, (4, 3): 3} 

We only need three key-value pairs, one for each nonzero element of the matrix. Each key is a tuple, and each value is an integer.

To access an element of the matrix, we could use the [] operator:

matrix[0,3] 
1 

Notice that the syntax for the dictionary representation is not the same as the syntax for the nested list representation. Instead of two integer indices, we use one index, which is a tuple of integers.

There is one problem. If we specify an element that is zero, we get an error, because there is no entry in the dictionary with that key:

matrix[1,3] 
KeyError: (1, 3) 

The get method solves this problem:

matrix.get((0,3), 0) 
1 

The first argument is the key; the second argument is the value get should return if the key is not in the dictionary:

matrix.get((1,3), 0) 
0 
get definitely improves the semantics of accessing a sparse matrix. Shame about the syntax.

Dictionaries provide an elegant way to generate a histogram:

letterCounts = {} 
for letter in "Mississippi": 
...   letterCounts[letter] = letterCounts.get (letter, 0) + 1 
... 
letterCounts 
{'M': 1, 's': 4, 'p': 2, 'i': 4} 

We start with an empty dictionary. For each letter in the string, we find the current count (possibly zero) and increment it. At the end, the dictionary contains pairs of letters and their frequencies.

It might be more appealing to display the histogram in alphabetical order. We can do that with the items and sort methods:

letterItems = letterCounts.items() 
letterItems.sort() 
print letterItems 
[('M', 1), ('i', 4), ('p', 2), ('s', 4)] 

You have seen the items method before, but sort is the first method you have encountered that applies to lists. There are several other list methods, including append, extend, and reverse. Consult the Python documentation for details.