#Upload
========
Upload's max file size was changed from 1GB to 250MB because the ajax default max file size was around 250MB.
If we want to make the Lexos' max file size larger we will have to change the ajax max file size.
 For a start on that (if you really want to) see: http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/
 
The minimum number of characters read to determine encoding type was changed from 500 to 5000. 
With 5000 characters the encoding type can be determined faster. See graphs in UploadTimes.ods

In figure one you can see that there is a significant difference between the upload times using 500 and 5000 characters to determine the encoding type for Huckleberry Finn and Tom Sawyer. 
In figure two you can see that these two texts are in a different encoding type than the others. Chardet may need more characters to determine these encoding types.
Since changing the number of characters to 5000 instead of 500 doesn't make a significant difference in the upload times of the texts in other encoding types, but does for Huckleberry Finn and Tom Sawyer, it is most efficient to use the 5000 characters for the minimum encoding detect number.
