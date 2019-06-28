# Classical Chinese - 诗词歌赋The_Poems_And_Songs

The Lexos tool can be used to help detect the authorship, contents, era, and 
genre in classical Chinese texts. Here we analyze several different texts written
in different dynasties and authors, which includes the genres of Chuci (verses
of Chu), Tangshi (poems from Tang Dynasty), Songci (lyrics from Song Dynasty), Yuanqu 
(opera from Yuan Dynasty), and historical biographies from Han Dynasty. Here our
hierarchical cluster analysis (dendrogram) identifies the similarities between
the texts.

The test files are:

File|Era(Dynasty)|Genre|Author
-------------------------|--------------------|------------------|---------------                            
*九歌JiuGe.txt|Zhanguo (475 BC)|Chuci|Qu Yuan
*离骚LiSao.txt|Zhanguo (475 BC)|Chuci|Qu Yuan
*孔子世家KongZiShiJia.txt|Han (104-91 BC)|Historical Biography|Sima Qian
*项羽本纪XiangYuBenJi.txt|Han (104-91 BC)|Historical Biography|Sima Qian
*长恨歌ChangHenGe.txt|Tang (807 AD)|Tangshi|Bai Juyi
*琵琶行PiPaXing.txt|Tang (816 AD)|Tangshi|Bai Juyi
*赤壁赋ChiBiFu.txt|Song (1082 AD)|Songci|Su Shi
*后赤壁赋HouChiBiFu.txt|Song (1082 AD)|Songci|Su Shi
*窦娥冤DouEYuan.txt|Yuan (1271-1368 AD)|Yuanqu|Guan Hanqing  
*西厢记XiXiangJi.txt|Yuan (1271-1368 AD)|Yuanqu|Wang Shifu

Using the tools from:   http://lexos.wheatoncollege.edu
and the files found in the FilesToUse/ directory, you should
be able to produce a dendrogram as shown in ResultsToExpect/.

Steps:
=====================================================================
(0) UPLOAD:

    (1) 九歌JiuGe(Zhanguo).txt 
    (2) 后赤壁赋HouChiBiFu(Song).txt
    (3) 孔子世家KongZiShiJia(Han).txt
    (4) 琵琶行PiPaXing(Tang).txt
    (5) 离骚LiSao(Zhanguo).txt
    (6) 窦娥冤DouEYuan(Yuan).txt
    (7) 西厢记XiXiangJi(Yuan).txt
    (8) 赤壁赋ChiBiFu(Song).txt
    (9) 项羽本纪XiangYuBenJi(Han).txt
    (10)长恨歌ChangHenGe(Tang).txt 

(1) SCRUB:

    (a) Remove Punctuation
    (b) Remove Digits

    Apply Scrubbing
    
(2) ANALYZE - Dendrogram:

     (a) Use the following metrics:
        - Distance Method: Euclidean (default)
        - Linkage Method: Average (default)
        - Orientation: Bottom
     (b) Tokenize - By Characters
          
     Generate Dendrogram
     Compare your result with the .png found in the ResultsToExpect/ directory.

ms - June 27, 2019
mjl - May 20, 2019
jg - June 10, 2014
