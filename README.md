mergewarc
=========

Merging WARCs into a single WARC file


* Dependencies
==================

** "warc" is a Python library to work with WARC files. It is used here for reading WARC records.
       It can be downloaded from https://github.com/internetarchive/warc
** "warctools" is used also to work with WARC files. One part of this library checks whether WARCs are valid!
       To download https://github.com/internetarchive/warctools

To run mergewarcs.py
	$python mergewarcs.py <WARCs-path>
        - Merges all WARC files located in <WARCs-path> and stores the result in ./merging-WARCs/
        - The program will check whether the resulting WARCs are valid!
		
Eaxmple:
	$python mergewarcs.py ./smallCollectionExample/

Output:
	Merging the following WARC files: 
	----------------------------------: 
	[ Yes ]./smallCollectionExample/alarabiya/20140624222112958.warc
	[ Yes ]./smallCollectionExample/aljazeera/20140624222245150.warc
	[ Yes ]./smallCollectionExample/goal/20140624222416231.warc
	
	Validating the resulting WARC files: 
	----------------------------------: 
	- [ valid ]  ./merging-WARCs/40739088-01a6-11e4-84ca-782bcb0f034c/4073f352-01a6-11e4-84ca-782bcb0f034c.warc