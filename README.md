A program to revert default settings on mimetype handlers changed by Mozilla
on Firefox 98 unilaterally and without consultation of the community
(as it is too often the case).

![](https://preview.redd.it/hbirna9158n81.png?width=1220&format=png&auto=webp&s=b17e21506464f27b6e5a9bd9b1fd1dd274cb01e4)


# Background

With Firefox 98, once again changes in the browser interface
are applied unilaterally without much possibility to go back.

The whole thing is tested by a biased minority (mainly the people who developed the
new feature), any critics are in the minority and the debate is quickly quickly closed.
On the day of the public release there are claims of harassment when the whole of the
users wakes up with a broken browser/UI experience.

#Development_in_2021

Hey folks, are you aware that a browser is a working tool and that
people have other things to do than develop this kind of script or spend time fixing
what was working a few minutes earlier?
Wake up!

# How it works

Firefox has changed the default actions to take when a file is downloaded from "Always ask" to "Save".
To restore the application popup you can go through the usual interface and modify at least a hundred of elements one by one (have fun).

This script edits the file responsible for mapping the file types you could download with the actions to perform.
Thus all default actions are reset to "Always ask" status.

More about the disaster of version 98:
https://www.reddit.com/r/firefox/comments/tdohiy/firefox_98_download_manager_support_thread/

# Usage

```bash
usage: edit_handlers.py [-h] [-o OUTPUT] [input_file]

positional arguments:
  input_file            handlers.json file path in the Firefox profile (on
                        GNU/Linux: ~/.mozilla/firefox/<my_profile/). By
                        default it will be renamed by adding a .bak suffix.
                        (default: ./handlers.json)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output filepath for the new JSON file. (default:
                        ./handlers.json)
```

# Addendum

Little reversing about some attributes in the handlers.json structure
(yes we are talking about reversing to patch a Firefox UI decision :thumbsup:):

```
"action":0      save the file (new default option...), usually goes with the parameter ask = false
"action":1      always ask
"action":2      ask to open with an application
"action":3      open in firefox
"action":4      use another application by default (thunderbird, etc)


save the file:
"application/json":{"action":0,"handlers":[{"name":"kwrite","path":"/usr/bin/kwrite"}],"extensions":["json"]}

always ask:
"application/json":{"action":1,"handlers":[{"name":"kwrite","path":"/usr/bin/kwrite"}],"extensions":["json"],"ask":true}

use kwrite:
"application/json":{"action":2,"handlers":[{"name":"kwrite","path":"/usr/bin/kwrite"}],"extensions":["json"]}

use kwrite by default:
"application/json":{"action":4,"handlers":[{"name":"kwrite","path":"/usr/bin/kwrite"}],"extensions":["json"]}
```
