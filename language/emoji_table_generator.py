# -*- coding: utf-8 -*-
#%%
"""
Created on Sun Aug 23 17:06:37 2020
split off on Thu Jan 27 05:53 2022
Updated and last run on 2022-11-28

@author: RobertWinslow

The first version of this code was meant to scrap the unicode emoji list 
and place the emoji codepointss into a dictionary.

This is a modification that I made to generate a markdown-formatted table for display on github pages.
"""

import urllib.request
from bs4 import BeautifulSoup

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#%% Grab the info

def urlToStr(url):
    "This function returns a webpage's source as just a big ol' string."
    #load Url text
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    urlStr = mybytes.decode("utf8")
    fp.close()  
    return urlStr

#sourceUrl = "https://www.unicode.org/Public/emoji/14.0/emoji-test.txt"
#sourceUrl = "https://www.unicode.org/Public/emoji/13.1/emoji-test.txt"
#sourceUrl = "https://www.unicode.org/Public/emoji/13.0/emoji-test.txt"
sourceUrl = "https://www.unicode.org/Public/emoji/15.0/emoji-test.txt"
sourceStr = urlToStr(sourceUrl)
sourceLines = sourceStr.split('\n')


#%% Jankily parse the info to create a list of tuples
# format is (group, subgroup, codepoint, shortname, version)

emojilist = []
skincolorList = []
currentGroup = ''
currentSubgroup = ''

for line in sourceLines:
    #If a line gives us a group or subgroup name, change the cooresponding variable
    if line.startswith('# group: '):
       currentGroup = line[9:]
    elif line.startswith('# subgroup: '):
       currentSubgroup = line[12:]
    #Now we need to parse the nonempty lines which start with a unicode code point.
    elif (line != '' and line[0] !='#'):
        #only add to the list if the character is 'fully-qualified'
        #statussnippet = line[57:62] only works for 13.1 onwards
        statsnipstart = line.index(';') + 2
        statussnippet = line[statsnipstart:statsnipstart+5] 
        if statussnippet != 'fully':
            continue
        else:
            #strip out the codepoint
            codepoint = line[:line.index(';')].rstrip()
            #pull out the CLDR short name, which occurs after E#.# 
            shortname = line[line.index('.'):].lstrip('1234567890. ')
            # I also want to version number so missing characters don't jank things up
            suffix = line[line.index('#'):]
            version = int(suffix[suffix.index('E')+1:suffix.index('.')])
            #exclude the skin tone variants, because that adds 1699 entries (nearly half of them!).
            if 'skin tone' in shortname:
                #continue
                skincolorList.append((currentGroup, currentSubgroup, codepoint, shortname, version))
            else:
                #now add it to our list
                emojilist.append((currentGroup, currentSubgroup, codepoint, shortname, version))
        




#%% Build the Markdwon tables v2.
# This time, we are checking sets instead of just the version.

def codepoint_to_string(codepoint):
    hexcodes = codepoint.split()
    glyph = ''.join(chr(int(hexcode,16)) for hexcode in hexcodes)
    return glyph

def codepoint_to_html(codepoint):
    hexcodes = codepoint.split()
    html = ''.join("&#x"+hexcode+";" for hexcode in hexcodes)
    return html

def checkforcodepoint(emojiset,codepoint):
    if codepoint in emojiset:
        return True
    elif codepoint.replace(' FE0F','').replace(' 200D','') in emojiset:
        return True
    else:
        return False

# data for versions of columns.
# EmojiTwo Support is spotty and hardcoded. Other sets are based on version number.
EmojiTwoSupportSet = {'1F611 1F3FD', '1F614 1F3FF', '1F1EE 1F1F3', '1F60A 1F3FB', '1F608', '1F1F9 1F1F2', '1F1F8 1F1F7', '1F69D', '2602', '1F641 1F3FD', '1F1ED 1F1F7', '1F630 1F3FF', '1F927 1F3FE', '2763', '23EF', '1F51B', '1F645', '1F937 1F3FB', '1F7E3', '2660', '1F1EA 1F1F7', '1F36D', '1F1EC 1F1EE', '1F597 1F3FF', '1F46F 1F3FE', '270C', '1F5B6', '1F3E7', '1F5AC', '1F35F', '1F3C3 1F3FE', '1F5C2', '25AA', '1F461', '266C', '269A', '1F3E8', '1F485', '1F48F 1F3FE', '2639 1F3FF', '1F7E0', '1F6B9', '1F1F8 1F1FB', '1F3CC 1F3FC', '1F6A4 1F3FE', '2615', '1F616', '1F418', '1F610 1F3FD', '1F435', '1F1F2 1F1E8', '1F31E 1F576', '26C9', '1F7E7', '1F1E6 1F1F4', '1F1F9 1F1EF', '1F917 1F3FC', '1F443 1F3FC', '1F64F', '1F6B6 1F3FE', '1F52F', '261C 1F3FC', '1F6CC 1F3FD', '1F62D 1F3FF', '1F4EC', '1F438', '1F450 1F3FE', '1F3F4 2620', '1F604 1F3FD', '262F', '1F482 1F3FE', '1F1F0 1F1EE', '1F30C', '1F483 1F3FD', '1F1E6 1F1EC', '1F1F0 1F1FC', '1F346', '2B55', 'E254', '26D6', '1F933 1F3FD', '1F607 1F3FB', '1F93B', '1F60C 1F3FF', '1F688', '1F6A3 1F3FD', '2139', '1F6A2', '1F1FB 1F1E8', '1F643 1F3FB', '1F496', '1F44A 1F3FE', '1F626 1F3FF', '1F6E2', '1F689', '2648', '1F382', '1F645 1F3FE', '1F5DC', '1F64E 1F3FF', '1F91D 1F3FE', '1F409', '1F683', '1F1E9 1F1EC', '1F93B 1F3FE', '1F239', '1F3F4 E0067 E0062 E006E E0069 E0072 E007F', '1F475 1F3FF', '1F912 1F3FD', '1F5C1', '1F339', '1F60F 1F3FD', '1F468', '1F936 1F3FC', '1F46B', '1F617 1F3FD', '1F4F7', '1F7E2', '1F633 1F3FE', '261E', '1F40E', '1F1F5 1F1EB', '1F491 1F3FF', '26E7', '1F61D 1F3FB', '1F481 1F3FC', '1F3C2 1F3FD', '1F44F', '1F1F5 1F1F9', '1F601 1F3FC', '1F6B4 1F3FB', '1F4C4', '1F6C1', '1F599 1F3FF', '1F45D', '1F615 1F3FB', '1F40B', '1F627 1F3FE', '1F1FB 1F1EE', '1F469 1F469 1F467', '1F1F8 1F1F1', '1F55F', '1F413', '26B1', '1F330', '2627', '1F970 1F3FE', '1F1F2 1F1F7', '1F637 1F3FB', '1F64F 1F3FD', '26FF', '1F924 1F3FE', '263B 1F3FB', '1F1FA 1F1FE', '1F475 1F3FE', '1F402', '1F1F5 1F1F7', '1F1EE 1F1F2', '1F1FB 1F1E6', '1F4B4', '1F603 1F3FC', '1F598 1F3FB', '1F6B3', '2934', '2628', '1F5AF', '1F4EA', '1F538', '1F64D', '1F467', '1F614 1F3FD', '1F1F5', '1F64F 1F3FC', '1F1F1 1F1E8', '1F58C', '1F93A 1F3FC', '1F615 1F3FC', '1F44B 1F3FF', '1F933 1F3FF', '1F39E', '1F93D', '1F95D', '1F380', '1F497', '1F44C', '1F62F 1F3FE', '1F1F1', '1F196', '2669', '1F3E4', '1F629 1F3FE', '1F1EC 1F1F2', '1F61C 1F3FF', '1F250', 'FEE31', '267B', '1F598 1F3FE', '1F4B0', '1F1F2 1F1EB', '1F446 1F3FF', '1F1F4 1F1F2', '1F643', '1F1F3 1F1F7', '1F618 1F3FE', '1F4DF', '1F60C 1F3FC', '3299', '1F1FE 1F1EA', '1F934 1F3FD', '1F392', '1F3A2 1F3FD', '1F480', '1F913', '1F3A5', '1F3A2 1F3FC', '1F478 1F3FC', '26F4', '1F627 1F3FC', '1F5E0', '264E', '1F95E', 'FEE11', '1F469 1F3FE', '26F7', '1F3F4 E0067 E0062 E0065 E006E E0067 E007F', '1F6AD', '1F534', '1F614 1F3FE', '1F59B', '1F60D 1F3FD', '26AB', '2621', '1F699', '1F3F7', '1F3C3', '1F503', '1F47C 1F3FF', '263B 1F3FF', '1F980', '1F623', '1F6B8', '1F473 1F3FE', '1F4C0', '1F631 1F3FD', '261D 1F3FD', '1F61E 1F494', '1F450 1F3FC', '1F590 1F3FE', '1F547', '1F597 1F3FB', '1F1EC 1F1F5', '1F927 1F3FD', '261F 1F3FE', '26A0', '1F455', '1F476 1F3FE', '1F644 1F3FE', '1F342', '1F46D', '1F61C 1F3FB', '1F1F1 1F1FA', '1F634 1F3FE', '1F3E9', '1F62D', '269C', 'FEE32', '1F30E', '1F600 1F3FC', '1F3AC', '270A 1F3FE', '1F485 1F3FD', '1F598 1F3FF', '1F46F 1F3FD', '1F61A 1F3FD', '1F93C 1F3FD', '1F910 1F3FE', '1F473 1F3FC', '1F410', '1F46C 1F3FF', '1F618 1F3FD', '1F491 1F3FD', '1F389', '1F1F1 1F1F8', '1F606 1F3FD', '1F612', '1F1EE 1F1F8', '1F353', '1F5FA', '1F630 1F3FD', '1F1E7 1F1EA', '271D', '2699', '1F51E', '1F487', '1F624 1F3FD', '1F3CA', '1F6A1', '1F36E', '1F5EF', '1F60F', '1F1E7 1F1F7', '1F3D1', '1F4DD', '1F546', '270B 1F3FD', '1F1E6 1F1E9', '1F440', '1F3CA 1F3FD', '26C4 1F464', '1F4F4', '1F4A2', '1F98C 1F6A8', '1F1FA 1F1F2', '1F91B 1F3FD', '1F91D 1F3FB', '1F62E', '1F561', '1F3D9', '1F491 1F3FC', '1F6EB', '1F443 1F3FE', '1F97A 1F3FF', '1F91C 1F3FC', '1F604 1F3FE', '1F626 1F3FC', '267C', '1F6CB', '1F622 1F3FD', '1F304', '1F635 1F3FD', '1F433', '1F43D', '267D', '1F46F 1F3FC', '1F468 2764 1F468', '1F3DC', '1F60B 1F3FC', '1F981', '1F1F5 1F1EC', '1F631 1F3FE', '1F61F 1F3FF', '1F98C 2642', '1F62E 1F3FB', '1F937 1F3FE', '1F602', '2B95', '1F628 1F3FF', '1F948', '1F93C 1F3FC', '1F3BF', '1F1E7 1F1E7', '1F618', '263B 1F3FE', '1F3DD', '1F595', '1F600 1F3FE', '1F1F1 1F1EE', '1F466', '1F44F 1F3FC', '1F1F6 1F1E6', '1F690', '1F597 1F3FE', '1F472 1F3FD', '1F5D9', '1F698', '1F620 1F3FC', '1F5EE', '1F4AA 1F3FF', 'FEE19', '1F41A', '1F1F5 1F1F0', '1F1F8 1F1FD', '1F471 1F3FD', '1F605 1F3FD', '1F1EA 1F1ED', '1F62A 1F3FD', '1F64C 1F3FC', '1F468 1F468 1F466', '1F601 1F3FB', '1F60B 1F3FF', '1F1FB 1F1EA', '1F920 1F3FC', '1F956', '1F52A', '1F521', '1F347', '1F93B 1F3FD', '1F48E', '23FA', '1F3C3 1F3FD', '1F647 1F3FE', '1F46F 1F3FB', '1F484', '1F59B 1F3FC', '1F911 1F3FF', '1F4D3', '1F41D', '1F46D 1F3FC', '1F44D 1F3FC', '1F44D 1F3FE', 'FEE46', '26DF', '1F641', '1F1EA 1F1EA', '1F3AF', '1F385 1F3FB', '1F927 1F3FC', '1F930 1F3FD', '1F44D 1F3FF', '1F5C8', '1F3EA', '1F645 1F3FB', '1F1E8 1F1FF', '1F61E 1F3FD', '2639 1F3FE', '2609', '1F61E 1F3FF', '1F6A3 1F3FE', '0030', '1F3D7', '3030', '1F6D0', '1F419', 'E50A', '2B1B', '1F57A 1F3FC', '1F924 1F3FD', '1F1ED 1F1F3', '1F44B 1F3FB', '1F97A 1F3FE', '267F', '1F348', '1F1F0 1F1EA', '1F3FE', '1F60D 1F3FC', '1F42B', '1F6F3', '1F481', '1F61F 1F3FD', '0031 20E3', '1F603 1F3FE', '1F617 1F3FC', '1F487 1F3FD', '1F599 1F3FE', '2328', '1F631 1F3FF', '1F3BA', '1F60F 1F3FB', '1F59A 1F3FE', '1F448', '23E9', '1F919 1F3FD', '1F5E2', '1F63F', '1F6B5 1F3FE', '1F1EF 1F1F2', '1F3E1', '1F541', '1F60E 1F3FF', '262A', '1F53B', '1F91D 1F3FC', '1F626', '268B', '1F604 1F3FC', '1F1F2 1F1FE', '1F1FA 1F1F8', '1F60C', '26F7 1F3FC', '270B 1F3FB', '1F91E 1F3FC', '1F417 1F464', '1F917 1F3FE', '1F1FF 1F1E6', '1F910 1F3FC', '1F5AB', '1F55E', '1F1E8', '1F504', '1F468 1F3FB', '1F62D 1F3FE', '1F633', '1F4AE', 'FEE47', '1F5A0 1F3FD', '1F91E 1F3FF', '1F45E', '1F1E9', '1F1F2 1F1FA', '1F61F 1F3FC', '1F93E', '1F171', '2049', '2197', '1F477 1F3FD', '1F949', '2680', '1F471 1F3FF', '1F944', '1F365', '1F926 1F3FE', '1F4A5', '1F4A0', '1F43C', '1F59E 1F3FC', '26FE', '2935', '1F236', '1F473', '1F467 1F3FF', '1F446 1F3FC', '1F4A3', '1F1E8 1F1E9', '1F6AE', '1F384', 'FEE1F', '1F448 1F3FC', '1F51D', '1F4CE', '1F47B', '1F4AA 1F3FD', '1F1F8 1F1E8', '1F1E8 1F1FD', '1F371', '1F47F', '1F93C 1F3FE', '1F626 1F3FD', '1F4AA 1F3FB', '1F694', '1F1F3 1F1FF', '1F32E', '1F34D', '1F5EC', '1F639', '1F47C 1F3FB', '1F43F', '1F925 1F3FF', '1F3B9', '1F468 1F3FF', '1F539', '261E 1F3FF', '23EA', '1F396', '1F450 1F3FB', '2682', '1F386', '1F4D1', '1F53A', '1F56D', '1F923 1F3FB', '1F62E 1F3FD', '1F1F2 1F1EC', '1F633 1F3FC', '1F476 1F3FC', '1F622 1F3FB', '26CF', '1F4BF', '1F1F3 1F1FA', '0030 20E3', '26D4', '26F2', '263B 1F3FC', '1F3CB 1F3FF', '1F933 1F3FB', '1F355', '1F1F0 1F1F5', '1F3F5', '1F59D', '1F629 1F3FD', '2622', '2604', '1F474 1F3FC', '1F507', '1F31A', '1F59E', '1F6CE', '1F1F8 1F1FA', '1F49E', '261F 1F3FD', '1F1E7 1F1FB', '268D', '1F450', '1F5A5', '1F1F0 1F1F7', '1F449 1F3FC', '002A', '1F1F3 1F1EE', '261C 1F3FE', '1F381', '1F6B6 1F3FB', '262E', '1F318', '1F60C 1F3FE', '1F4B8', '1F631 1F3FB', '1F485 1F3FB', '1F564', '1F385 1F3FC', '1F4D5', '1F617', '1F959', '1F1E7 1F1F4', '1F61A 1F3FB', '1F4AA 1F3FC', '1F3B7', '261E 1F3FC', '1F912 1F3FC', '1F3DE', '2635', '1F466 1F3FB', '270C 1F3FC', '1F377', '0035', '1F1E7 1F1FC', '1F945', '1F540', '1F626 1F3FE', '1F6D1', '1F429', '1F363', '1F442 1F3FC', '1F3DF', '1F637', '1F939', '1F326', '1F447 1F3FE', '1F42A 1F464', '1F3CC 1F3FD', '1F475 1F3FD', '1F590 1F3FB', '1F606 1F3FE', '1F537', '1F636 1F3FF', '1F511', '1F430', '1F6A4 1F3FF', '1F47D', '1F4BD', '1F506', '1F926 1F3FD', '1F535', '1F91C 1F3FF', '1F938', '1F620 1F3FB', '1F361', '1F60F 1F3FC', '1F32A', '1F416', '1F1FD 1F1F0', '1F356', '1F935 1F3FE', '1F472', '2626', '1F1E6 1F1FD', '1F62A 1F3FE', '2705', '1F61B', '1F34B', '1F1E6 1F1FF', '1F574 1F3FC', '1F4EF', '1F1F9 1F1E9', '2708', '1F470 1F3FD', '1F9C0', '270D 1F3FB', '1F1F2 1F1F8', '1F3E0', '1F924 1F3FB', '1F1E7 1F1FE', '1F1EB 1F1F0', '1F590', '1F1E7 1F1E9', '1F34F', '23F8', '25A9', '2665', '1F1EE 1F1F4', '1F925', '1F300', '1F479', '1F6B5 1F3FF', '1F5BF', '1F50E', '1F46B 1F3FE', '1F1F1 1F1F0', '1F920 1F3FD', '1F3C2 1F3FE', '1F43B', '1F1F7 1F1F4', '1F936 1F3FB', '2710', '1F449', '1F518', '1F5E8', '1F62C 1F3FB', '1F60F 1F3FE', '1F4E2', '1F1FC', '1F478', '1F623 1F3FE', '1F917 1F3FD', '25A6', '1F940', '1F6E5', '1F375', '1F5B7', '1F1E6 1F1E8', '1F602 1F3FF', '1F4D0', '1F349', '1F919', '26F7 1F3FE', '26F9', '1F42B 1F464', '1F1F1 1F1F7', '1F528', '1F64B 1F3FE', '261F 1F3FB', '1F6A9', '1F910 1F3FF', '1F421', '1F91E 1F3FB', 'FEE23', '1F48F 1F3FB', '1F3CC 1F3FF', '261A 1F3FD', '1F542', '1F60E 1F3FE', '1F343', '1F4B6', '1F957', '1F4DE', '1F1EC 1F1FA', '1F6A5', '1F914 1F3FF', '1F485 1F3FC', '1F46B 1F3FF', '1F611', '1F60B', '25A7', '1F470 1F3FF', '1F5EA', '1F604', '1F32F', '1F64B 1F3FB', '1F620 1F3FE', '1F466 1F3FC', '1F64D 1F3FB', '26CB', '1F5A0 1F3FB', '1F59F 1F3FE', '1F44D', '1F468 1F469 1F467 1F466', '1F1F5 1F1F3', '1F4C9', '1F3EB', 'FEE13', '1F62E 1F3FE', '1F1F3 1F1F1', '1F509', '1F1EC 1F1F6', '1F986 2642', '1F629 1F3FC', '1F37C', '1F40A', '1F1F2 1F1ED', '261A 1F3FE', '261A', '2B50', '1F194', '1F520', '1F4D9', '1F470 1F3FB', '1F3AE', '1F93D 1F3FF', '1F4ED', '1F7EB', '1F50C', '1F640', '1F6F4', '1F476 1F3FD', '1F628', '1F648', '25A0', '1F418 1F464', '1F35A', '1F37F', '1F925 1F3FB', '1F367', '1F1F5 1F1E6', '1F1EC 1F1F7', '1F46A 1F3FC', '2605', '26F1', '1F596 1F3FD', '1F502', '1F691', '1F417', '1F64D 1F3FC', '1F38F', '1F59B 1F3FD', '1F406', '1F1F2 1F1EA', '1F1EE', '1F590 1F3FF', '1F939 1F3FF', '1F623 1F3FB', '1F637 1F3FF', '1F6BC', '1F487 1F3FB', '1F40A 1F464', '1F460', '1F422', '1F59B 1F3FB', '1F37A', '1F555', '1F350', '1F1EA', '1F7E1', '1F597', '1F619 1F3FE', '1F23A', '1F51A', '2198', '1F1EC 1F1FC', '1F644 1F3FB', '1F341', '1F443 1F3FD', '1F632 1F3FF', '2697', '1F920', '1F1E9 1F1F2', '1F6C4', '1F601 1F3FF', '1F595 1F3FE', '1F552', '1F635 1F3FC', '1F687', '2689', '1F637 1F3FD', '1F39F', '1F628 1F3FC', '1F585', '1F447 1F3FF', '1F632 1F3FE', '1F474 1F3FD', '1F935', '1F447', '1F1EB 1F1F7', '1F551', '1F5A6', '1F5D3', '1F649', '1F530', '270C 1F3FE', '1F60E 1F3FB', '1F1E9 1F1F0', '1F926 1F3FF', '1F61D 1F3FD', '1F469 1F3FB', '1F60A 1F3FC', '1F619 1F3FC', '1F604 1F3FB', '2721', '1F60A 1F3FE', '1F523', '1F63E', '1F934', '1F91B 1F3FC', '264C', '1F605', '1F61D 1F3FF', '261B', '1F488', '1F647 1F3FB', '23F9', '1F1F9 1F1ED', '1F913 1F3FE', '1F3CB', '1F915 1F3FF', '1F63B', '1F93C 1F3FB', '2667', '1F3ED', '1F59E 1F3FF', '1F68D', '1F315', 'FE82D', '1F3D0', '1F612 1F3FE', '1F308', '26F3', '1F1EE 1F1F1', '1F3F9', '1F3D8', '1F638', '1F3C4 1F3FB', '1F5B8', '1F95C', '1F1F2 1F1F3', '2199', '1F4AC', '1F952', '2639 1F3FD', '263A 1F3FE', '1F475', '1F39D', '1F6AA', '1F462', '1F483 1F3FC', '1F486 1F3FB', '1F393', '263B 1F3FD', '1F5A1 1F3FD', '261A 1F3FF', '1F6AC', '1F91C 1F3FB', '1F1E7 1F1F1', '1F344', '1F42A', '1F1ED 1F1F9', '1F3F1', '1F17E', '1F598 1F3FC', '1F1EA 1F1E6', '1F1F9 1F1FB', '1F3A0', '1F481 1F3FE', '1F57A 1F3FF', '1F625 1F3FC', '1F602 1F3FE', '1F912 1F3FB', '1F58E 1F3FB', '1F30A', '1F1EA 1F1EC', '1F469 1F469 1F467 1F467', '263B', '1F697', '2691', '1F613 1F3FB', '1F93B 1F3FB', '1F313', '1F5A7', '270A 1F3FB', '1F3FF', '1F306', '1F631', '1F1E8 1F1FE', '1F625 1F3FB', '1F30B', '1F4F5', '1F6A4 1F3FC', '1F4FB', 'FEE2C', '1F364', '1F618 1F3FB', '26FC', '1F6B6', '1F3C4', '1F60F 1F3FF', '1F616 1F3FB', '1F6BA', '1F415', '1F390', '1F312', '1F62B 1F3FD', '1F447 1F3FB', '270C 1F3FD', '1F633 1F3FF', '1F911 1F3FC', '1F399', '1F918 1F3FD', '1F958', '1F1E6 1F1FC', '1F3FB', '1F925 1F3FD', '23EE', '1F197', '1F48F 1F3FC', '1F4EE', '23F0', '1F1F9 1F1F9', '1F357', '1F616 1F3FF', '25A4', '26DE', '1F918 1F3FE', '1F46B 1F3FC', '1F529', '1F642 1F3FE', '1F603 1F3FF', '1F64D 1F3FE', '1F475 1F3FC', '1F472 1F3FF', '2702', '1F337', '1F44E 1F3FB', '1F637 1F3FE', '26D1', '1F508', '1F352', '1F609 1F3FD', '1F936 1F3FF', '261E 1F3FE', '1F471 1F3FE', '1F1F0 1F1EC', '1F1F2 1F1F1', '1F32D', '1F487 1F3FC', '1F57B', '1F468 1F468 1F467 1F466', '1F596 1F3FB', '1F599 1F3FD', '1F59A 1F3FD', '1F3C1', '1F40F', '1F695', '1F563', '1F644', '1F490', '1F91A 1F3FC', '1F232', '1F919 1F3FE', '1F1F8 1F1F2', '1F378', '2695', '1F468 1F469 1F467', '1F93C 1F3FF', '1F54D', '1F5A1 1F3FC', '1F3C4 1F3FC', '1F5FE', 'FEE21', '2616', '1F478 1F3FF', '1F6B4 1F3FC', '1F4E3', '1F616 1F3FC', '00AE', '26E4', '1F3AA', '1F370', '1F449 1F3FE', '1F97A 1F3FD', '1F646 1F3FB', '1F55B', '1F94B', '270A', 'FEE49', '268C', '1F3A3', '1F566', '1F3CA 1F3FE', '1F301', '2764', '1F1F8 1F1E6', '1F59F', '1F47C 1F3FE', '261B 1F3FE', '1F442 1F3FE', '1F62C 1F3FD', '002A 20E3', '1F610', '1F1EB 1F1EF', '1F1F0 1F1F2', '1F170', '1F610 1F3FC', '1F46B 1F3FB', '2617', '1F1F9 1F1E8', '1F519', '1F1E8 1F1F4', '1F31E', '1F590 1F3FD', '1F3C7 1F3FC', '0036', '1F4FD', 'FEE27', '1F336', '1F62B 1F3FC', '1F428', '1F3A2 1F3FB', '1F4B2', '1F915 1F3FE', '1F1F1 1F1E7', '1F575 1F3FE', '1F1EA 1F1F8', '1F914 1F3FE', '1F938 1F3FF', '1F351', '1F477 1F3FE', '1F558', '1F4A6', '1F1F3 1F1EB', '1F4CB', '1F970 1F3FB', '1F1F1 1F1FE', '1F1EB 1F1F2', '1F354', '1F951', '1F3C3 1F3FF', 'E255', '1F38B', '1F44A 1F3FB', '1F6AB', '1F918', '1F611 1F3FC', '1F527', '1F947', '1F1E6 1F1F1', '1F46C', '2650', '1F372', '1F3B3', '1F447 1F3FD', '1F45B', '1F536', '1F233', '2685', '1F1F0', '1F3F8', '261A 1F3FC', '1F4A1', '1F1EC 1F1EB', '1F926 1F3FB', '1F6CC 1F3FB', '1F938 1F3FC', '1F5B2', '1F924 1F3FF', '1F468 1F3FD', '2744', '1F59E 1F3FB', '1F446 1F3FD', '1F915 1F3FC', '1F635 1F3FB', '1F910 1F3FB', '1F46A 1F3FB', '2631', '1F60A 1F3FD', '1F485 1F3FE', '1F5D2', '1F478 1F3FD', '26F5', '1F5A1 1F3FB', '1F938 1F3FB', '26C6', '1F647', '1F475 1F3FB', '1F565', '1F3D5', '1F98A', '1F624 1F3FE', '2733', '23ED', '1F6E0', '1F1F5 1F1F2', '1F570', '1F41F', '1F4E1', '1F61E 1F3FC', '1F302', '1F18E', '1F933 1F3FE', '270B', '1F58A', '1F986 2640', '1F93E 1F3FD', '1F625 1F3FD', '26CA', '1F436', '1F69C', '2661', '1F1FB 1F1EC', '1F319', '1F91C 1F3FE', '1F59C', '1F93B 1F3FF', '1F407', '1F1EC', '1F549', '1F7E5', '1F1EC 1F1ED', '1F643 1F3FE', '264D', '1F46A', '1F4D4', 'E256', '1F448 1F3FB', '1F61F 1F3FB', '2687', '1F619 1F3FF', '1F3B5', '1F510', '1F1E8 1F1FA', '2618', '1F42D', '303D', '1F605 1F3FC', '1F62E 1F3FC', '1F595 1F3FC', '1F602 1F3FC', '270D 1F3FC', '1F61D 1F3FC', '2684', '1F47A', '1F607 1F3FE', '261E 1F3FD', '1F235', '23F2', '1F46D 1F3FB', '1F450 1F3FF', '1F615', '1F64E 1F3FD', '1F3C7 1F3FF', 'FEE1C', '1F623 1F3FC', '1F3A7', '1F1EC 1F1F1', '1F926 1F3FC', '1F553', '1F571', '1F473 1F3FB', '1F61A', '1F610 1F3FB', '1F985', 'FEE2E', '1F4BA', '1F627', '1F425', '25AB', '1F5B3', '2666', '2194', '1F442 1F3FD', 'FEE20', '1F44E 1F3FC', '1F607', '1F6EC', '1F930 1F3FC', '2754', '1F5C0', '1F629', 'FEE28', '1F1EA 1F1F9', '1F3BC', '1F611 1F3FF', '1F622 1F3FE', '1F3D3', '1F1FC 1F1EB', '1F4BB', '266A', '1F64C 1F3FB', '1F1E7 1F1F2', '1F3BB', '1F1EE 1F1EA', '1F955', '2639 1F3FC', '1F611 1F3FB', '1F45F', '1F1EB 1F1EE', '1F4CF', '1F989', '270B 1F3FF', '1F4A4', '1F647 1F3FF', '1F459', '1F911 1F3FE', '1F5FB', '1F1F2 1F1FF', '1F1FF 1F1F2', '1F3D4', '1F970 1F3FC', '1F31B', '1F1F0 1F1ED', '1F632', '1F1F8', '261D 1F3FC', '1F1E7', '2610', '274C', '2620', '1F443 1F3FF', '1F64D 1F3FD', 'FEE30', '1F522', '1F58D', '1F6B2', '1F1EB 1F1F4', '1F64E 1F3FB', '268A', '2714', '1F62C 1F3FF', '1F64F 1F3FE', '1F33E', '1F636', '1F62A 1F3FC', '1F925 1F3FC', '1F334', '1F50B', '1F6C0 1F3FC', '1F6C5', '1F387', '1F44E 1F3FF', '1F567', '1F62F', '1F471', '1F6C3', '1F1F0 1F1FF', '1F42F', '1F1F3 1F1F5', '1F444', '1F445', '2629', '1F1F1 1F1E6', '270C 1F3FF', '1F1F2 1F1F5', '25A5', '1F474', '270A 1F3FC', '1F685', '1F4C8', '1F55C', '1F93C', '1F477', '2630', '1F3A8', '1F468 1F469 1F466 1F466', '1F446 1F3FE', '1F914', '1F498', '1F91A', '1F923 1F3FF', '1F610 1F3FF', '1F46C 1F3FC', '1F936 1F3FE', 'FEE2D', '1F58E 1F3FF', '1F1E8 1F1F1', '1F6C0 1F3FF', 'FEE1D', '2795', '1F635 1F3FF', '1F468 1F469 1F467 1F467', '1F91D 1F3FD', '1F192', '1F453', '1F482', '1F4C7', '2640', '1F603 1F3FD', '1F486 1F3FC', '1F3CB 1F3FE', '1F642 1F3FB', '1F633 1F3FD', '1F620', '1F46F', '1F62F 1F3FB', '1F59E 1F3FD', '1F473 1F3FF', '2642', '1F3CB 1F3FC', '263A 1F3FC', '1F602 1F3FB', '1F37E', '1F48A', '1F60B 1F3FD', '1F630 1F3FC', '1F46A 1F3FE', '1F1F5 1F1ED', '1F482 1F3FB', '1F332', '1F556', '1F622 1F3FF', '1F575 1F3FC', '1F3CA 1F3FF', '1F516', '1F481 1F3FD', '1F4AF', '1F93D 1F3FD', '1F6BE', '1F918 1F3FC', '1F934 1F3FE', '1F1F2 1F1F6', '1F423', '1F609', '1F61A 1F3FC', '1F6C0', '1F4D8', '1F64F 1F3FF', '1F634 1F3FB', '1F33A', '1F1FA 1F1E6', '23F3', '1F3B1', '1F98D', '1F970 1F3FF', '1F636 1F3FD', '1F937 1F3FD', '1F6A4 1F3FB', '1F59A 1F3FB', '1F1F3 1F1F4', '1F47C', '1F93E 1F3FB', '1F97A 1F3FB', '1F584', '1F6B6 1F3FC', '2606', '1F4C6', '1F1F1 1F1F9', '1F93A 1F3FF', '1F5FC', '0039', '1F91B 1F3FF', '270A 1F3FF', '1F91D', '1F55D', 'FEE25', '1F1E7 1F1EB', '1F494', '1F3B4', '1F443', '1F1E8 1F1EE', '1F385', '1F6B5 1F3FC', '1F21A', '1F596 1F3FE', '1F1EE 1F1F9', '26D7', '1F988', '1F987', '1F64C 1F3FE', '1F920 1F3FB', '1F1F2 1F1E9', '1F48D', '1F939 1F3FE', '1F385 1F3FE', '1F469 1F3FC', '1F60A', '1F3E3', '1F6A3', '1F6B0', '1F1F8 1F1F4', '1F604 1F3FF', '1F914 1F3FC', '1F927', '24C2', '1F5A8', '1F474 1F3FE', '1F574 1F3FD', '1F557', '1F6C0 1F3FB', '1F3C2 1F3FF', '1F7E9', '1F4C1', '1F30D', '1F5FF', '2649', '1F4CA', '1F562', '1F91A 1F3FD', '1F937 1F3FF', '1F58E 1F3FE', '1F4DC', '1F464', '1F6A0', '1F1F8 1F1E7', '1F1F2 1F1FB', '1F627 1F3FF', '274E', '1F912', '1F388', '1F1ED', '1F647 1F3FD', '1F647 1F3FC', '1F1F8 1F1EF', '1F397', '1F600', '1F615 1F3FE', '1F64B', '1F7E6', '261C 1F3FD', '1F6B6 1F3FF', '1F911 1F3FB', '1F446 1F3FB', '1F98F', '1F954', '1F5AA', '1F629 1F3FF', '1F41E', '1F5A1', '1F46E', '1F36A', '1F1EE 1F1E8', '1F474 1F3FF', '1F45A', '1F46E 1F3FC', '1F47C 1F3FD', '203C', '1F441 1F5E8', '1F1F2', '1F1E7 1F1FF', '1F62E 1F3FF', '1F4B1', '1F469', '1F469 2764 1F48B 1F469', '1F6A4', '1F39C', '1F61C 1F3FD', '1F605 1F3FE', '1F6B5', '1F531', '1F915 1F3FD', '1F98C 2640', '1F5C3', '26D3', '1F49F', '1F59A', '2796', '1F5D8', '1F1E7 1F1EF', '1F3C4 1F3FF', '1F368', '1F587', '1F911', '1F1E6 1F1FA', '1F629 1F3FB', '1F61C', '1F3C7', '1F64C 1F3FD', '1F383', '1F44C 1F3FB', '1F5AE', '1F47E', '26BE', '2636', '1F495', '1F4A7', '1F645 1F3FF', '1F937 1F3FC', '1F60D 1F3FF', '1F54B', '1F57A 1F3FB', '1F35E', '1F919 1F3FC', '1F35D', '1F31C', '1F1ED 1F1F0', '1F935 1F3FD', '1F501', '1F559', '1F1E9 1F1FF', '26DB', '1F1FB 1F1FA', '1F64C 1F3FF', '1F362', '1F49C', '1F1F2 1F1F2', '2747', '1F1EC 1F1EC', '1F910', '1F612 1F3FD', '261D', '2623', '1F1FB', '1F3C4 1F3FE', '1F3C8', '1F5A0', '1F634 1F3FD', '1F323', '1F58E', '1F919 1F3FB', '1F61E 1F3FE', '1F472 1F3FE', '1F1F9', '1F60C 1F3FD', '1F693', '1F486 1F3FF', '1F469 2764 1F469', '1F1F3 1F1EA', '1F601 1F3FE', '1F635', '1F34C', 'FEE2F', '1F1F9 1F1F0', '1F5C4', '1F914 1F3FD', '1F1E7 1F1F3', '1F442', '1F62D 1F3FC', '1F470 1F3FC', '1F51F', '1F3CA 1F3FC', '1F600 1F3FF', '1F643 1F3FF', '1F1F6', '1F5E9', '1F483 1F3FF', '263A 1F3FD', '1F3A2 1F3FE', '1F59F 1F3FC', '1F5A0 1F3FE', '1F22F', '1F93E 1F3FE', '1F512', '1F641 1F3FC', '1F597 1F3FC', '1F62A 1F3FF', '263D', '26C4', '1F7EA', '270C 1F3FB', '1F637 1F3FC', '1F5F3', '1F46E 1F3FF', '1F6A7', '2611', '1F68E', '21AA', '1F59F 1F3FD', '1F62A 1F3FB', '1F3F0', '2651', '1F97A', '1F642 1F3FF', '1F646 1F3FC', '0031', '2603', '1F624 1F3FF', '1F37D', '1F934 1F3FB', '1F4A9', '1F6B4', '1F63C', '1F1EC 1F1FE', '1F58E 1F3FC', '1F1F5 1F1EA', '1F467 1F3FB', '1F6B4 1F3FE', '1F68F', '263A', '0038', '1F619 1F3FD', '1F920 1F3FF', '26C8', '27B0', '1F1ED 1F1FA', '1F44B 1F3FD', '1F91A 1F3FB', '1F922', '1F420', '1F3FA', '1F40C', '270A 1F3FD', '1F62C', '1F483', '1F1F2 1F1FD', '1F3FD', '26A1', '1F6A4 1F3FD', 'FEE10', '1F609 1F3FC', '1F918 1F3FF', '1F5A1 1F3FE', '1F1FE', '1F1E7 1F1F8', '261B 1F3FF', '1F33D', '1F1E9 1F1F4', '2B05', '1F33F', '25FB', '1F400', '1F49D', '1F3CC 1F3FE', '1F4C3', '1F493', '1F680', '1F934 1F3FF', '1F1F7 1F1F8', '1F4F1', '264A', '1F3CD', '1F469 1F3FF', '1F62B 1F3FF', '1F33C', '1F915 1F3FB', '1F44D 1F3FB', '1F305', '1F635 1F3FE', '1F4AB', '1F431', '1F1E7 1F1EE', '1F643 1F3FC', '1F359', '1F613 1F3FC', '1F560', '1F46D 1F3FD', '1F93A', '261F', '1F59F 1F3FB', '1F3EC', '1F1EE 1F1F7', '1F1E7 1F1EC', '1F0CF', '1F481 1F3FF', '2757', '1F385 1F3FD', '1F920 1F3FE', '26F0', '26F9 1F3FC', '1F1F3 1F1E6', '1F3C9', '1F31F', '1F1E7 1F1F6', '1F1F9 1F1FC', '1F1E8 1F1FC', '1F476 1F3FB', '1F451', 'FEE2B', '1F4D2', '1F44F 1F3FF', '1F309', '1F38C', '0035 20E3', '2634', '1F482 1F3FD', '1F1E6 1F1EA', '2709', '1F623 1F3FF', '1F579', '1F6B1', '1F57C', '2755', '1F1EF 1F1F4', '1F468 1F469 1F466', '1F630 1F3FE', '1F36C', '1F59A 1F3FC', '1F476', '26C5', '1F1E6 1F1EB', '1F478 1F3FE', '1F923 1F3FE', '1F44A 1F3FC', '1F1E8 1F1EB', '1F4B3', '1F935 1F3FB', '2693', '1F3F3 1F308', '1F40F 1F464', '0034 20E3', '1F50F', '1F6CD', '1F631 1F3FC', '1F4EB', '1F58B', '1F1F9 1F1F3', '1F46C 1F3FD', '1F486', '1F46C 1F3FE', '1F632 1F3FD', '1F6A3 1F3FB', '1F595 1F3FB', '1F61C 1F3FE', '1F44E 1F3FD', '1F46E 1F3FE', '1F477 1F3FC', '1F405', '1F457', '1F470 1F3FE', '1F004', '1F44A', '1F605 1F3FB', '1F466 1F3FE', '1F926', '1F4F0', '1F617 1F3FF', '1F234', '26FA', '1F5B5', '1F458', '1F4E6', '1F53C', '26DD', '1F345', '1F358', '1F38E', '1F934 1F3FC', '1F33B', '1F468 1F3FC', '1F923 1F3FC', '1F47C 1F3FC', '1F58E 1F3FD', '1F201', '1F41C', 'E257', '1F40D', '1F61A 1F3FF', '2688', '1F610 1F3FE', '1F68B', '1F3D6', '1F1EC 1F1F8', '1F478 1F3FB', '1F53D', '1F303', '1F935 1F3FF', '1F471 1F3FB', '2601', '261F 1F3FF', '1F91B 1F3FE', '1F3C7 1F3FD', '25B6', '1F1FA 1F1EC', '1F41B', '1F44C 1F3FE', '1F64B 1F3FC', '1F54E', '1F6E3', '1F62D 1F3FB', '1F3C6', '1F636 1F3FB', '1F917', '0037', '1F6EA', '1F612 1F3FC', '1F1EE 1F1F6', '1F628 1F3FE', '1F63A', '2694', '1F470', '1F3C2', '1F195', '1F917 1F3FF', '2639', '1F93A 1F3FD', '1F991', '1F573', '1F1F8 1F1EA', '1F52D', '1F578', '1F61B 1F3FE', '1F550', '1F414 1F464', '1F52B', '1F602 1F3FD', '1F984', '1F32C', '1F3D2', '1F935 1F3FC', '1F4C2', '1F607 1F3FD', '26FD', '1F1E7 1F1F9', '1F411', '1F682', '270B 1F3FC', '1F1E8 1F1FB', '1F622', '1F471 1F3FC', '1F1E8 1F1F0', '1F199', '1F6A8', '1F93E 1F3FF', '261C 1F3FB', '1F46F 1F3FF', 'FEB89', '1F5BC', '0038 20E3', '1F94A', '1F4F8', '1F6CF', '0023 20E3', '1F576', '2716', '1F48F 1F3FF', '1F1F2 1F1F0', '1F466 1F3FD', '1F628 1F3FD', '1F467 1F3FD', '1F61B 1F3FD', '1F622 1F3FC', '1F614 1F3FC', '1F61F', '1F64E 1F3FE', '1F500', '1F69E', '261B 1F3FB', '261F 1F3FC', '1F1F8 1F1F8', 'FEE1A', '27BF', '1F1EB', '1F325', '1F43A', '1F642 1F3FC', '1F598 1F3FD', '1F6BF', '1F3CB 1F3FD', '1F1EA 1F1E8', '261C 1F3FF', '1F626 1F3FB', '1F4E9', '1F6BB', '1F98C', '1F366', '1F525', '1F56F', '1F6F0', '1F55A', '1F191', '1F432', '1F596 1F3FC', '1F60E 1F3FC', '1F482 1F3FF', '1F1EA 1F1FA', '1F56B', '1F3C2 1F3FC', '1F340', '1F237', '1F6C0 1F3FE', '1F3A2 1F3FF', '1F57D', '2607', '1F42C', '1F619 1F3FB', '1F69F', '1F46B 1F3FD', '1F615 1F3FF', '1F91C', '2696', '261D 1F3FB', '1F1EC 1F1E7', '1F644 1F3FD', '1F628 1F3FB', '1F6B5 1F3FB', '1F598', '1F606 1F3FB', '1F938 1F3FE', '1F524', '2652', '1F193', '1F486 1F3FD', '1F617 1F3FE', '1F632 1F3FB', '1F43E', '1F1E6 1F1F8', '1F3C3 1F3FB', '1F3F2', '1F915', '1F60D', '1F412', '1F4E5', '1F5A1 1F3FF', '1F913 1F3FB', '1F62F 1F3FC', '1F91D 1F3FF', '1F3F4', '26F8', '1F1F7 1F1FC', '1F1F8 1F1FE', '1F612 1F3FF', '2765', '1F310', '1F937', '1F56C', '1F5E1', '26F9 1F3FD', '1F44D 1F3FD', '1F49B', '1F4C5', '1F930 1F3FB', '1F439', '1F4F2', '1F6B4 1F3FF', '1F64B 1F3FF', '1F93B 1F3FC', '1F36B', '1F1E8 1F1F3', '2632', '23EB', '1F64E 1F3FC', '1F93D 1F3FC', '1F630 1F3FB', '1F1E6 1F1F6', '1F644 1F3FF', '3297', '1F3B0', '1F492', '1F938 1F3FD', '263C', '1F62B 1F3FE', '1F93A 1F3FB', '1F329', '1F49A', '1F60D 1F3FB', '1F6A6', '1F331', '1F990', '1F45C', '1F57A 1F3FE', '1F599 1F3FB', '2670', '1F532', '1F6AF', '1F574 1F3FB', '261B 1F3FD', '1F38D', '1F64E', '1F607 1F3FC', '1F1FD', '1F469 1F3FD', '1F3F4 E0067 E0062 E0073 E0063 E0074 E007F', 'FEE44', '1F1EC 1F1F3', '1F3CC 1F3FB', '1F1E6 1F1F2', '1F3C7 1F3FE', '1F31D', '1F1E6 1F1F9', '1F5A4', '1F646 1F3FD', '1F52C', '1F91B', '1F91E 1F3FD', '1F4B5', '1F4AD', '1F98E', '26F7 1F3FF', '1F328', '1F465', '2692', '1F684', '260E', '1F1E6 1F1EE', '1F452', '1F1E7 1F1E6', '2663', '1F913 1F3FF', '1F93D 1F3FE', '261D 1F3FF', '1F1E8 1F1F5', '1F6C2', '1F3BD', '1F321', '269B', '1F1E8 1F1F7', '1F3E5', '1F93E 1F3FC', '263A 1F3FB', '1F477 1F3FB', '2698', '1F317', '1F1E8 1F1EC', '2638', '1F6B6 1F3FD', 'FEE29', '1F38A', '1F577', '1F61F 1F3FE', '1F597 1F3FD', '2653', '261A 1F3FB', '1F61E 1F3FB', '1F618 1F3FC', '1F3B6', '1F3C3 1F3FC', '1F60E 1F3FD', '1F61D 1F3FE', '261C', '1F476 1F3FF', '1F95A', '26F7 1F3FD', '1F54C', '1F408', '1F1F8 1F1E9', '1F950', '1F46E 1F3FD', '1F621', '1F238', '1F472 1F3FC', '1F641 1F3FB', '1F307', '1F98B', '270D 1F3FE', '25A8', '268F', '1F1F5 1F1FC', '1F487 1F3FF', '1F1EC 1F1E6', '0032 20E3', '1F3AB', '1F605 1F3FF', '1F472 1F3FB', '1F44F 1F3FD', '1F91B 1F3FB', '1F624', '1F6E4', '1F1F8 1F1F9', '270F', '1F373', 'FEE16', '1F5A0 1F3FF', '1F3F4 E0067 E0062 E0077 E006C E0073 E007F', '1F641 1F3FE', '1F930 1F3FF', '1F481 1F3FB', 'FEE17', 'FEE40', '231B', '1F473 1F3FD', '1F7E4', 'FEE1B', '1F517', '1F1FA', '1F491 1F3FE', '26F9 1F3FB', '1F314', '1F60E', '2600', '1F469 1F469 1F466 1F466', '1F4BC', '1F311', '1F933', '1F3AD', '1F48C', '1F924', '1F1FF 1F1FC', '270E', '1F93D 1F3FB', '1F320', '1F623 1F3FD', '1F50A', '1F1F1 1F1FB', '2728', '1F391', '1F61B 1F3FB', '1F627 1F3FB', '1F1F8 1F1F3', '1F39B', '270D 1F3FF', '26BD', '1F62A', '1F485 1F3FF', '1F513', '1F1F8 1F1EE', '1F634', '1F925 1F3FE', 'FEE26', '1F401', '1F61A 1F3FE', '1F918 1F3FB', '1F1F8 1F1F0', '1F404', '1F644 1F3FC', '1F692', '1F911 1F3FD', '2712', '25FE', '1F4E0', '1F51C', '1F379', '1F467 1F3FC', '1F3C4 1F3FD', '1F505', '1F454', '1F515', '1F4AA 1F3FE', '1F5B1', '1F630', '1F1F9 1F1F7', '1F6CC', '1F34A', '1F1E8 1F1ED', '1F376', '1F424', '1F1F5 1F1F8', '1F4E4', '1F4DA', '1F609 1F3FB', '1F93A 1F3FE', '1F46D 1F3FF', '25FC', '1F499', '1F6C7', '1F6B4 1F3FD', '1F3E6', '1F3BE', '1F4CD', '1F6CC 1F3FC', '1F589', '1F59B 1F3FF', '1F62C 1F3FC', '26CE', '1F1EC 1F1F9', '1F5B0', '1F338', '1F917 1F3FB', '1F468 1F3FE', '1F1E8 1F1E8', '1F450 1F3FD', '1F477 1F3FF', '26F9 1F3FF', '1F44B 1F3FE', '1F56A', '1F34E', '1F1E9 1F1EA', '1F1EC 1F1EA', '1F3C2 1F3FB', '1F3E2', '1F69B', '2681', '1F1F9 1F1EC', '1F449 1F3FB', '1F1F4', '1F1E6', '1F5A0 1F3FC', '263E', '2195', '1F1F2 1F1FC', '1F4D6', '1F1F3 1F1EC', '1F61E', '2668', '0034', '2664', '1F4F3', '1F64B 1F3FD', '1F324', '1F1EF 1F1F5', '1F603 1F3FB', '266B', '1F616 1F3FE', '1F574 1F3FE', '1F514', '1F526', '1F686', '1F614 1F3FB', '1F63D', '1F619', '1F4E7', '1F627 1F3FD', '1F600 1F3FB', '1F1F9 1F1F1', '1F42E', '1F91E', '2614', '1F618 1F3FF', '1F374', '1F3CE', '1F3A6', '1F4FF', '1F554', '0033', '1F912 1F3FE', '1F939 1F3FB', '1F60B 1F3FB', '1F385 1F3FF', '1F91C 1F3FD', '261E 1F3FB', '1F3CC', '1F3EE', '1F60A 1F3FF', '1F50D', '1F625 1F3FE', '1F44E 1F3FE', '1F369', '1F59A 1F3FF', '25A1', '1F456', '1F6CC 1F3FE', '1F633 1F3FB', '1F57A', '1F46D 1F3FE', '1F942', '26BF', '1F443 1F3FB', '1F4DB', '1F91A 1F3FE', '1F569', '1F48F', '1F61C 1F3FC', '1F912 1F3FF', '1F56E', '1F322', '1F3A2', '1F601', '1F468 1F468 1F467 1F467', '2672', '1F921', '1F1F8 1F1FF', '1F606 1F3FF', '1F1F5 1F1FE', '1F1EF 1F1EA', '1F251', '1F919 1F3FF', '1F1FB 1F1F3', '1F54A', '231A', '1F5ED', '1F1F7 1F1FA', '1F3FC', '1F64A', '1F335', '1F491', '1F927 1F3FF', '266D', '1F6CC 1F3FF', '1F936', '1F413 1F464', '1F6C6', '1F3A9', '2797', '1F469 1F469 1F466', '2690', '1F590 1F3FC', '1F52E', '23F1', '1F59B 1F3FE', '1F36F', '1F946', '1F1ED 1F1F2', '1F913 1F3FD', '1F923', '1F603', '1F595 1F3FF', '1F44A 1F3FF', '1F3C5', '1F617 1F3FB', '1F483 1F3FB', '1F447 1F3FC', '2624', '2608', '26E9', '1F3DB', '0033 20E3', '1F48B', '1F44E', '1F575', '26AA', '1F1F2 1F1F4', '264B', '1F44C 1F3FC', '1F913 1F3FC', '1F606', '1F943', '1F1FA 1F1FF', '1F57A 1F3FD', '1F44B 1F3FC', '26C7', '1F634 1F3FC', '1F681', '1F646 1F3FE', '1F696', '1F1F3 1F1E8', '1F427', '1F91A 1F3FF', '1F5DE', '0036 20E3', '1F930', '1F6C0 1F3FD', '1F44C 1F3FF', '1F596', '2686', '1F548', '1F4E8', '1F6A3 1F3FC', '1F327', '1F3F3', '1F4FC', '0039 20E3', '1F636 1F3FC', '2662', '1F489', '1F333', '1F607 1F3FF', '1F59E 1F3FE', '1F62F 1F3FF', '266F', '1F35B', '1F449 1F3FF', '1F4A8', 'FEE14', '1F68A', '1F5A3', '1F5D1', '1F69A', '1F64D 1F3FF', '1F3DA', '1F4CC', '1F467 1F3FE', '1F615 1F3FD', '1F19A', '1F574', '1F5E3', '1F35C', '1F62B', '1F44F 1F3FE', '1F3A4', '263A 1F3FF', '1F927 1F3FB', 'FEE33', '2B07', '1F599 1F3FC', '1F936 1F3FD', '1F6A3 1F3FF', '1F636 1F3FE', '1F924 1F3FC', '1F930 1F3FE', '2612', '1F6B7', '1F46C 1F3FB', '1F575 1F3FD', '1F609 1F3FF', '1F61D', 'FEE4A', '21A9', '1F44B', '266E', '1F59F 1F3FF', '1F449 1F3FD', '1F469 1F469 1F467 1F466', '1F646', '1F4D7', '1F588', '1F360', '1F3CF', '1F609 1F3FE', '1F1FF', '262D', 'FEEA0', '1F614', '1F642 1F3FD', '1F983', 'FEE15', '1F582', '00A9', '1F1FE 1F1F9', '1F5A2', '1F60B 1F3FE', '1F1FC 1F1F8', '1F575 1F3FB', '1F62B 1F3FB', '1F448 1F3FF', '1F1F9 1F1F4', '1F68C', '1F486 1F3FE', '1F468 1F468 1F466 1F466', '1F6E1', '1F1F9 1F1E6', '1F986', '1F914 1F3FB', '1F446', '1F933 1F3FC', '1F442 1F3FB', '2683', '0037 20E3', '1F60C 1F3FB', '1F641 1F3FF', '23CF', 'FEE12', '1F533', '1F4AA', '1F643 1F3FD', '1F466 1F3FF', '1F442 1F3FF', '1F48F 1F3FD', '260F', '2637', '270D', '1F61B 1F3FC', '268E', '1F4FA', 'FEE22', '1F403', '1F970', '1F1E8 1F1F2', '1F448 1F3FD', '1F4B7', '1F448 1F3FE', '1F3CB 1F3FB', '0023', '1F1F9 1F1EB', '27A1', '1F30F', '1F91E 1F3FE', '261B 1F3FC', '1F1F3', '1F4BE', '1F970 1F3FD', '1F64F 1F3FB', '2753', '1F441', '26F7 1F3FB', '1F316', '1F923 1F3FD', 'FEE45', '1F941', '1F1E8 1F1E6', '1F1EC 1F1E9', '1F1EE 1F1E9', '1F95B', '261D 1F3FE', '1F1F8 1F1EC', 'FE83C', '1F487 1F3FE', '1F468 1F468 1F467', '1F624 1F3FB', '1F414', '1F491 1F3FB', '1F595 1F3FD', '1F645 1F3FD', '1F616 1F3FD', '1F3B8', '2122', '1F434', '0032', '1F97A 1F3FC', '25C0', '1F3CA 1F3FB', '2633', '1F39A', '1F572', '1F395', '1F1F5 1F1F1', '1F60D 1F3FE', '1F634 1F3FF', '1F468 2764 1F48B 1F468', '1F46E 1F3FB', '1F575 1F3FF', '1F625 1F3FF', '1F474 1F3FB', '1F606 1F3FC', '2B06', '1F44F 1F3FB', '1F1E7 1F1ED', '1F1F0 1F1F3', '1F5DD', '1F599', '1F601 1F3FD', '1F6B5 1F3FD', '1F3B2', '1F1F2 1F1E6', '1F6D2', '1F1F7', '1F482 1F3FC', 'FEE18', '1F625', '1F3EF', '2734', '1F46A 1F3FF', '1F17F', '2639 1F3FB', '1F1EF', '1F6E9', '2196', '1F37B', '1F1F2 1F1F9', '270B 1F3FE', '1F3C0', '1F1F0 1F1FE', '23EC', '1F645 1F3FC', '25FD', '1F982', '1F62C 1F3FE', '1F576 1F535 1F534', '1F596 1F3FF', '1F428 1F464', '1F642', '26EA', '1F613 1F3FE', '1F624 1F3FC', '1F1F7 1F1EA', '1F939 1F3FC', '1F613 1F3FF', '264F', '1F62F 1F3FD', '1F620 1F3FD', '1F620 1F3FF', '1F6BD', '1F5FD', '1F939 1F3FD', '1F1E6 1F1F7', '1F6C8', '1F613 1F3FD', '1F1F9 1F1FF', 'FEE1E', '1F3A1', '1F44C 1F3FD', '1F646 1F3FF', '1F568', '1F916', '1F600 1F3FD', 'FEE2A', '1F62D 1F3FD', '1F46A 1F3FD', '1F6F6', '1F64C', '1F5EB', '1F61B 1F3FF', 'FEE24', '1F426', '1F612 1F3FB', '1F3C7 1F3FB', '1F463', '1F4F6', '1F4B9', '1F1E9 1F1EF', '1F953', '26B0', '1F32B', '1F4F9', '1F910 1F3FD', '1F611 1F3FE', '1F7E8', '2671', '1F483 1F3FE', '1F202', '1F44A 1F3FD', '1F613', '1F632 1F3FC', '270D 1F3FD', '1F429 1F464', '2B1C', '1F6F5', '1F1F8 1F1ED', '1F574 1F3FF', '1F437', '1F198', '26F9 1F3FE'}
Emoji14SupportSet = set(emoji[2] for emoji in emojilist if emoji[4] <= 14)
fullemojiset = set(emoji[2] for emoji in emojilist)
COLUMNSETS = [EmojiTwoSupportSet,Emoji14SupportSet,Emoji14SupportSet]

currentSubgroup = ''
currentgroup = ''
for group, subgroup, codepoint, shortname, version in emojilist:
    glyph = codepoint_to_html(codepoint)
    if group != currentgroup:
        print ('\n\n### '+group+'')
        currentgroup = group
    if subgroup != currentSubgroup:
        print ('\n#### '+subgroup+'\n')
        print('| name | EmojiTwo | Twemoji | OpenMoji |')
        print('|:-:|'+':-:|'*len(COLUMNSETS))
        currentSubgroup = subgroup
    linestring = f'| <small>{codepoint}</small><br>{shortname}<br>{glyph} | '
    for columnset in COLUMNSETS:
        if checkforcodepoint(columnset,codepoint):
            linestring += glyph
        linestring += ' | '
    print(linestring)
    #print(f'| {shortname} | {glyph} | {glyph} | {glyph} |')











# %% Now do the same for skin color variants.

Emoji14SupportSet = set(emoji[2] for emoji in skincolorList if emoji[4] <= 14)
fullemojiset = set(emoji[2] for emoji in skincolorList)
COLUMNSETS = [EmojiTwoSupportSet,Emoji14SupportSet,Emoji14SupportSet]

currentSubgroup = ''
currentgroup = ''
for group, subgroup, codepoint, shortname, version in skincolorList:
    glyph = codepoint_to_html(codepoint)
    if group != currentgroup:
        print ('\n\n### '+group+'')
        currentgroup = group
    if subgroup != currentSubgroup:
        print ('\n#### '+subgroup+'\n')
        print('| name | EmojiTwo | Twemoji | OpenMoji |')
        print('|:-:|'+':-:|'*len(COLUMNSETS))
        currentSubgroup = subgroup
    linestring = f'| <small>{codepoint}</small><br>{shortname}<br>{glyph} | '
    for columnset in COLUMNSETS:
        if checkforcodepoint(columnset,codepoint):
            linestring += glyph
        linestring += ' | '
    print(linestring)
    #print(f'| {shortname} | {glyph} | {glyph} | {glyph} |')


# %%
