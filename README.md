A program to revert default settings on mimetype handlers changed by Mozilla
on Firefox 98 unilaterally and without consultation of the community
(as it is too often the case).

![](https://preview.redd.it/hbirna9158n81.png?width=1220&format=png&auto=webp&s=b17e21506464f27b6e5a9bd9b1fd1dd274cb01e4)

# How it works

Firefox has changed the default actions to take when a file is downloaded from "Always ask" to "Save".
To restore the application popup you can go through the usual interface and modify at least a hundred of elements one by one (have fun).

This script edits the file responsible for mapping the file types you could download with the actions to perform.
Thus all default actions are reset to "Always ask" status.

More about the disaster of version 98:
https://www.reddit.com/r/firefox/comments/tdohiy/firefox_98_download_manager_support_thread/

# Usage

Make sure to have a working Python3 installation.

```
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

# Background (#Development_in_the_2020s)

With Firefox 98, once again changes in the browser interface
are applied unilaterally without much possibility to go back.

Firefox "community driven" development process:

- Someone has the idea to do something to avoid to maintain a part of code from someone else
(They will tell you that it was to finally close a 14 year old bug, and that's a favor for you).
- The idea is implemented and quickly pushed in nightly
- The whole thing is "tested" by a biased minority (mainly the people who developed the
new feature; so a handful of persons)
- Some rare users using beta/nightly channels spot the new behavior and an annoying modification
in their working flux.
- Any critics are in the minority and the debate is quickly quickly closed.
- 6 months later, on the day of the public release there are claims of harassment when the whole
of the users wakes up with a broken browser/UI experience.
- Developpers refuse to change their position. Pick up arguments from the following (not exhaustive) list:
    - "You know... It's implemented now, you should have come forward before,
    it will be hard to revert and it will broke our release and test process."
    - "Uh.. Chrome does the same thing so they are obviously right."
    - "We are confident to have a global view of the project and you are not, there are complex
    things that are solved now (like... things. You know... uh.)"
    - "We are sure to be right."
    - "People need to adapt their workflow to the one we will support in the future.
    If not it's possible that Firefox is not the tool for you"
    - "If you don't like it, quit Firefox or implement a patch yourself"
- If the debate is too long more spurious arguments begin to emerge. Pick from the following list:
    - Reversal of the burden of proof: "Prove to me that we are wrong".
    - Use numbers from nowhere and misuse so-called telemetry stats or stats that measure something
    else but which will serve your argument. In any case, no one will check them.
    - Use circular reasoning: "Since our change [forcing certain behaviors],
    people are using the feature more, so we were right."
    - "You are not representative of our users [insert numbers from your preconceptions here]".
    - Essentialize the claimant and make him say what he did not say:
    "I hope you don't consider me dishonest or in bad faith."
    - While people are very respectful on the threads (**despite they run into walls**),
    make sure to threat that you feel harassed.
- Some empty and non-binding promises are made (e.g. an API to allow an extension to recover the
default behavior; Note: this one is already denied in our case).
- An option is left in about:config to go back.
It will be removed in a few months, hopefully users will get bored in the meantime.
- New tickets are quickly closed because they are duplicates of the original one (closed itself as WONTFIX).

Note: How do we call a minority of people imposing their point of view on all the others at all costs,
because they are convinced that their actions are good?
The road to hell is paved with good intentions.

Hey folks, are you aware that a browser is a working tool and that
people have other things to do than develop this kind of script or spend time fixing
what was working a few minutes earlier?

Wake up! Firefox is a community project! This does not mean that it is **run by a community**
of people making unilateral decisions.

More freaking (hopeless) debate on bugzilla: https://bugzilla.mozilla.org/show_bug.cgi?id=1738574

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
