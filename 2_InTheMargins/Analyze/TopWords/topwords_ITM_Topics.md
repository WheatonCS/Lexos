## TopWord Topic

(from Heather Fang, July 17, 2016; unedited)

In the Margins

Topword

After you suspect some similarity or difference between/among your texts, Topword can give you a close look at which words are used very differently, in the statistically significant sense, between/among your texts. Therefore, in the next step, you can focus on these picked words and run them in the Rolling Windows to see “how exactly” are those words differently used.

Topword is running a proportion z-test on the proportions of words to find the differently used words (Top Words). How does it work? Here is some quick and dirty statistics knowledge that you probably won’t hear in a decent classroom.

First, proportion z-test is a kind of hypothesis test. It is a method statisticians use to test if a hypothesis has significant evidence to be true or not. It normally requires two distinct hypotheses, the null hypothesis (noted as H0) and the alternative hypothesis (noted as H1). The null hypothesis is our current assumption while the alternative hypothesis is the one we want to test. For example, we have a new cold drug and we want to test if it is working better than the old one. Our null hypothesis should be that the new drug is the same as the old one and our alternative hypothesis should be that the new drug is indeed better. That is to say, we first assume the new drug is the same as the old one and if we find evidence against our assumption, we can say that our null hypothesis is rejected and we have evidence for that the new drug is working better. Then, where is our evidence coming from? Actually, statisticians calculate the probability of our current observation (called p-value) under our assumption (null hypothesis). If that p-value is very small (usually smaller than 0.05, as used in Topword), we consider that we find our evidence. In short, the smaller the p-value is, the stronger evidence we have. 

But, why do you see z-scores in Topword? What are those? In Topword, we use normal distribution to approximate the probability (by Central Limit Theorem). Z-scores are byproducts in this calculation process, and it is much easier to get. Specifically, let p1 and n1 be the frequency (proportion) of a word and the total word count respectively from one document or some documents, p2 and n2 be those from some documents as a whole. We have pooled sample proportion be

p = (p1 * n1 + p2 * n2) / (n1 + n2)

Then, a z-score is 

z = (p1 - p2) / sqrt{ p * ( 1 - p ) * [ (1/n1) + (1/n2) ] }

Amazingly and importantly, if the absolute value of a z-score is larger, the p-value is always smaller, and we know when the absolute value of z-score equals to 1.96, the p-value is 0.025 (half of 0.05, for larger and smaller part each). Therefore, in Topword, only words with z-scores larger than 1.96 or smaller than -1.96 are shown. 

To conclude, Topword runs a proportion z-test as following:
H0 : p1=p2
H1 : p1≠p2
The rejection rule is: 
Reject H0 if
z = (p1 - p2) / sqrt{ p * ( 1 - p ) * [ (1/n1) + (1/n2) ] } > Z0.025 (1.96)
or z = (p1 - p2) / sqrt{ p * ( 1 - p ) * [ (1/n1) + (1/n2) ] } < -Z0.025 (-1.96)

However our test has two major limitations. First, since we are approximating the p-value, by the Central Limit Theorem, n1 and n2 should be large enough. In normal cases, we need at least 100 words each document to make the result reliable. Secondly, we will have A LOT of Top Words, too many to read, so culling options are vital. Except the common culling options on the right, Topword features advanced culling options for you to cull words with certain frequencies. Note that the most frequently used words are mostly the so-called functional words while the least frequently used words are usually some random words that are strongly associated with the context. Topword has two main built-in options for separating words according to their frequencies. 

The first one is outliers by standard deviation. Here Topword is assuming the distribution of word frequencies is a normal distribution (which however is not the case for most data) and define any word with frequencies 2 standard deviation from mean is outliers. That is,
 
Top outliers: word frequency - mean > 2 * standard deviation
Low outliers: word frequency - mean < -2 * standard deviation

The second one is outliers by Interquartile Range (IQR). It is actually a common way to find outliers in statistics. First, it ranks all data in increasing order and then divides it into four equal parts. The values that divide each part are called the first, second, and third quartiles, denoted by Q1, Q2, and Q3, respectively. (Note that Q2 is the median value.) The IQR is equal to Q3 minus Q1. Therefore, outliers are defined as following:

Top outliers: word frequency > Q3 + 1.5 * IQR
Low outliers: word frequency < Q1 - 1.5 * IQR 

Outliers by standard deviation generally works better in most text-mining settings. Given most of the distribution of word frequencies is left-skewed, it normally gives more top outliers than low outliers. On the other hand, choosing by IQR is more likely to give no outliers on one or both sides when the data are skewed or compact. Given most of the data are left-skewed, outliers by IQR would have a lot of outliers and very few (even zero) low outliers. Choose wisely!


Links:
Hypothesis Test from stat trek:
http://stattrek.com/hypothesis-test/hypothesis-testing.aspx

Proportion Z-test from stat trek:
http://stattrek.com/hypothesis-test/difference-in-proportions.aspx?Tutorial=AP

Central Limit Theorem from wikipedia:
https://en.wikipedia.org/wiki/Central_limit_theorem

Normal Distribution from wikipedia:
https://en.wikipedia.org/wiki/Normal_distribution

Standard Deviation from wikipedia:
https://en.wikipedia.org/wiki/Standard_deviation

Interquartile Range from stat trek:
http://stattrek.com/statistics/dictionary.aspx?definition=Interquartile%20range

Outliers from stat trek:
http://stattrek.com/statistics/dictionary.aspx?definition=outlier

Z-test from wikipedia:
https://en.wikipedia.org/wiki/Z-test




