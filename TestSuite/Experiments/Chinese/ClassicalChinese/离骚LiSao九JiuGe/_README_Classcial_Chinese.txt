
Corpus:  Classical Chinese

The lexomics tool can be used to detect the authorship, contents, era and 
genre in classical Chinese texts. Here we analyze several different texts written
in different dynasties and authors, which include genres of Chuci (verses of Chu),
Tangshi (poems from Tang Dynasty), Songci (lyrics from Song Dynasty), Yuanqu 
(opera from Yuan Dynasty), and historical biographies from Han Dynasty. Here our
cluster analysis (dendrogram) identifies the similarities between the texts.

These test files are:
                            Era(Dynasty)          Genre             Author
*九歌JiuGe.txt             Zhanguo (475 BC)        Chuci            Qu Yuan
*离骚LiSao.txt             Zhanguo (475 BC)        Chuci            Qu Yuan
*孔子世家KongZiShiJia.txt   Han (104-91 BC)   Historical Biography  Sima Qian
*项羽本纪XiangYuBenJi.txt   Han (104-91 BC)   Historical Biography  Sima Qian
*长恨歌ChangHenGe.txt       Tang (807 AD)          Tangshi           Bai Juyi
*琵琶行PiPaXing.txt         Tang (816 AD)          Tangshi           Bai Juyi
*赤壁赋ChiBiFu.txt          Song (1082 AD)         Songci            Su Shi
*后赤壁赋HouChiBiFu.txt     Song (1082 AD)         Songci             Su Shi
*窦娥冤DouEYuan.txt         Yuan (1271-1368 AD)    Yuanqu         Guan Hanqing  
*西厢记XiXiangJi.txt        Yuan (1271-1368 AD)    Yuanqu          Wang Shifu

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/ directory, you should
be able to produce a dendrogram as shown in ResultsToExpect/.

Steps:
=====================================================================
(0) UPLOAD 
    (a) 九歌JiuGe(Zhanguo).txt 
    (b) 离骚LiSao(Zhanguo).txt 
    (c) 孔子世家KongZiShiJia(Han).txt
    (d) 项羽本纪XiangYuBenJi(Han).txt
    (e) 长恨歌ChangHenGe(Tang).txt
    (f) 琵琶行PiPaXing(Tang).txt 
    (g) 赤壁赋ChiBiFu(Song).txt
    (h) 后赤壁赋HouChiBiFu(Song).txt
    (i) 窦娥冤DouEYuan(Yuan).txt
    (j) 西厢记XiXiangJi(Yuan).txt
=====================================================================
(1) SCRUB both:
    (a) Remove punctuation
    (b) Remove Digits

    Apply Scrubbing
=====================================================================
(5) ANALYZE - Dendrogram
     (a) Use the default metrics Distance Method: Euclidean and Linkage Method: Average
     (b) Give a Title
     (c) Choose Tokenize - 1 - gram, by Characters, check the box Only within words
     (d) Choose normalize - Proportional Counts

     (e) Get Dendrogram
     (f) compare your result with the .pdf found in the ResultsToExpect/ directory.
=====================================================================

jg - June 10, 2014