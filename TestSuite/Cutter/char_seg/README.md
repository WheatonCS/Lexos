# Characters/Segment

This function cuts the text into segments based on the number of characters in each segment.

Cutting a file using Characters/Segment:
=====================================================================
(0) UPLOAD 3_numbered.txt
=====================================================================
(1) CUT: 
    (a) Select Characters/Segment
    (b) Change the Segment Size to 3
    (c) Keep Overlap at 0
    (d) Keep Last Segment Size Threshold (%) at 50

    Results
=====================================================================
    After the cut you should have 16 different segments containing 2-3 characters 
    each. 
    



Cutting a file using Characters/Segment with Overlap:
=====================================================================
(0) UPLOAD 3_numbered.txt
=====================================================================
(1) CUT: 
    (a) Select Characters/Segment
    (b) Change the Segment Size to 5
    (c) Change Overlap to 3
    (d) Keep Last Segment Size Threshold (%) at 50

    Results
=====================================================================
    After the cut you should have 23 different segments containing 3-5 characters 
    each. 
