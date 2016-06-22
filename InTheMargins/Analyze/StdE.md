## summary

Using standard error to determine outlier will give you all the documents that has file size 2 standard error away from the average file size


## standard deviation 

Standard deviation measures how far all the object is away from the average.

Here is a nice demonstration of the standard deviation: 
[Standard Deviation](http://www.mathsisfun.com/data/standard-deviation.html)

## standard error

Standard error is the estimation of standard deviation based on the sample.


## why 2 standard error away from the average?

If we assume that all the document you are interested in 
(maybe all the document belongs to a particular writer)
follows a normal distribution.

Then the probability of a random document size is 2 standard deviation away from average file size is 4.4%.
(the probability that the document size is 2 standard deviation larger than the average is 2.2%,
the probability that the document size is 2 standard deviation smaller than the average is 2.2%)

The probability is small enough for us to say that it is not normal for us to have document like that, 
therefore we call it a outlier (anomaly).

But we cannot get the exact standard deviation of the whole distribution, 
because we don't have all the documents that you are interested in.

Therefore we have to use standard error to replace standard deviation to determine which document is an anomaly.

Here is a good description on how to interpret standard deviation [standard deviation - interpretation and application](https://en.wikipedia.org/wiki/Standard_deviation#Interpretation_and_application)
