# Illumio
Technical Assessment for Victor Ku

Downlad parser.py. This will be the main way or executing the program. This file requires two and has an optional third file path: 1) flowlogs file directory is required in order for the program to parse flowlogs 2) Lookup table is used to classify what tag to be applied 3) where the output file should be located. 

I've only tested the code using the sample flow logs/lookup table provided. The program only supports the default log format--version 2, the dstport is in col 5 and protocol in col 8 and these fields ALWAYS exist, lookup table is exactly like the sample (dstport,protocol,tag) w/ no entries empty, when tagging--"untagged" is a valid tag for unknown entries, and many skipped values if any errors persist.
