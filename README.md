WARCMerge
=========

Tool to allow merging of multiple WARC files into a single WARC 


##Dependencies

* Tested on Ubuntu Linux
* Requires Python 2.7+ 
* Requires Java to run Jwattools for validating WARC files
* Requires [the warc python library](https://github.com/internetarchive/warc) from Internet Archive to work with WARC files and WARC records.

##Running WARCMerge.py

WARCMerge can be executed using one of three different methods:

### Method 1
```python
 %python WARCMerge.py <input-directory> <output-directory>
```

 This will merge all WARC files found in "input-directory" and store the resulting output file(s) in "output-directory".

### Method 2
```python
 %python WARCMerge.py <file1> <file2> <file3> ... <output-directory>
```

 Here, all listed WARC files will be merged and stored the resulting output file(s) in "output-directory". 

### Method 3
```python
 %python WARCMerge.py  -a <source-file> <dest-file>
```

 The purpose of "-a" flag is to make sure that any changes in "dest-file" are done intentionally.The command line above appends the source WARC file "source-file" to the end of the destination WARC file "dest-file".
 
 In all cases, the program checks to see whether or not the resulting WARCs are valid! 

##Examples

###Example 1: Merging WARC files (found in "input-directory") into new WARC file(s):
```python
 %python WARCMerge.py ./collectionExample/ my-output-dir

	Merging the following WARC files: 
	----------------------------------: 
	[ Yes ]./collectionExample/world-cup/20140707174317773.warc
	[ Yes ]./collectionExample/warcs/20140707160258526.warc
	[ Yes ]./collectionExample/warcs/20140707160041872.warc
	[ Yes ]./collectionExample/world-cup/20140707183044349.warc

	Validating the resulting WARC files: 
	----------------------------------: 
	- [ valid ]     my-output-dir/WARCMerge20140806040712197944.warc
```	

###Example 2: Merging all listed WARC files into new WARC file(s)
```python
 %python WARCMerge.py 585.warc 472.warc ./dir1/113.warc ./warcs/449.warc mydir

Merging the following WARC files: 
----------------------------------: 
[ Yes ] ./warcs/449.warc
[ Yes ] ./585.warc
[ Yes ] ./dir1/113.warc
[ Yes ] ./472.warc

Validating the resulting WARC files: 
----------------------------------: 
- [ valid ]     mydir/WARCMerge20140806040546699431.warc
```

### Example 3: Appending a WARC file to another WARC file:

```python
	%python WARCMerge.py -a ./test/src/20258526.warc ./test/dest/20141872.warc

	The resulting (./test/dest/20141872.warc) is valid WARC file
```

###Example 4: Giving incorrect arguments, the following message will be shown: 
```python
  %python WARCMerge.py -n 20160041872.warc new-dir

	usage: WARCMerge [ -a <source-file> <dest-file> ]
					 [ <input-directory> <output-directory> ]
					 [ <file1> <file2> <file3> ...  <output-directory> ] 
```


##Relevant Linkage

The following are links to the archived pages in the example above:
```	
	https://github.com/iipc/openwayback/wiki/How-OpenWayback-handles-revisit-records-in-WARC-files
	http://www.openplanetsfoundation.org/blogs/2014-03-24-arc-warc-migration-how-deal-de-duplicated-records
	http://econpapers.repec.org/paper/innwpaper/2014-17.htm
	http://articles.latimes.com/2013/mar/26/sports/la-sp-sn-us-mexico-soccer-game-updates-20130326	
```	
