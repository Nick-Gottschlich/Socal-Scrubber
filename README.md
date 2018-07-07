# Social Amnesia
Social Amnesia aims to make your social media only exist within a time period that you choose. For many people, there is no reason they want to have years old facebook statuses or reddit comments existing and making it easier for online marketers and jilted ex-lovers to profile you. With Social Amnesia, set the time period you want to keep, whitelist posts and items you want to preserve indefinitely, and let Social Amnesia wipe the rest out of existence.

This is in very early versions, this readme will contain a list of what sites are usable and what features are available on each one.

## How to build/run Social Amnesia

### Executables

This is the simplest option. Bundled and easily usable files are available in the zip files on the [releases](https://github.com/Nick-Gottschlich/Social-Amnesia/releases) page.

### How to run Social Amnesia from the command line
*NOTE:* As of 7.07.18 the project is not compatible with Python 3.7 yet - [related tweepy issue](https://github.com/tweepy/tweepy/pull/1042).

* Clone the repo
* Set up a new [virtualenv](https://virtualenv.pypa.io/en/stable/) and activate it
* Run:
```
pip3 install -r requirements.txt
python3 SocialAmnesia.py
```
* Have fun!

### How to build the executable for Social Amnesia

Install the requirements using pip3 (see above).
Then you can build the executable by running `python3 setup.py bdist_msi` (Windows) or `python3 setup.py bdist_dmg` (macOS). 
This will create a folder called `build`, in which you should find a folder with a name starting with 'exe.'. 
There should be a 'Social Amnesia' executable waiting inside. Run that executable to start the program.

Note: On windows you may have to copy `tcl86t.dll` and `tk86t.dll` from your `Python3X/DLLs` into the folder with the executable to get this to run.

## Sites and Features

### Reddit
* Can delete comments and submissions.
* Edits your posts before deleting them. According to [the reddit admins](https://www.reddit.com/r/blog/comments/1dhw2j/reddits_privacy_policy_has_been_rewritten_from/c9qgbbb/) this is an effective way to remove content from reddit.
* Can keep a time range of comments and submissions (in hours)
* Can keep comments or submissions that are above a certain amount of upvotes.
* Can skip gilded comments/submissions.
* Trial run - do a run showing what would be deleted, without actually doing it.

#### How to set up your reddit account
Reddit requires accounts to create a "script" in order for Social Amnesia to run. Don't worry, this is actually quite simple to do. You can see reddit's docs on how to do this [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps). Doing this provides you with the reddit "Client ID" and "Client Secret" you will need to log in within the Social Amnesia app.

### Twitter
* Can delete tweets, retweets, replies and remove "favorites" (aka ❤️'s).
* Can keep a time range of tweets, retweets, replies and favorites.
  * In the case of favorites, this is done by the time the favorited item was created, NOT the time it was favorited at.
* Can keep tweets that have a certain amount of retweets or favorites.
  * This option ignores retweets, these will be removed no matter what if they are out of the time range.
* Trial run - do a run showing what would be deleted, without actually deleting it.

#### How to set up your twitter account
Twitter requires you to set up an "app" in order to get Social Amnesia to run. Do this by heading to https://apps.twitter.com/ while logged in, and clicking "Create New App". Then, fill in whatever you'd like for the Name, Description, and Website. Once it's created, click the "Keys and Access Tokens" tab. This will have the consumer key and consumer secret you will need for Social Amnesia. You can then click "Create my Access Token" at the bottom of the page to get the access token and access token secret that Social Amnesia needs. That's it, you have everything needed to get Social Amnesia running with twitter!

### Scheduler

Social Amnesia can be scheduled to run daily at a time of your choosing. Just use the scheduler panel in any of the social media tabs to set this up.

## Contributing

Contributions are not only welcomed but greatly appreciated. If you have any idea for a new feature, or find a bug, you can open up a [new issue](https://github.com/Nick-Gottschlich/Social-Amnesia/issues/new) and report it. Better yet, fork this project, write up some code and [submit a new pull request](https://github.com/Nick-Gottschlich/Social-Amnesia/compare).

Don't feel comfortable coding? That's okay! There are plenty of other ways to contribute to this project: 
- The easiest is to just share it. Post it (ironically?) on your social media. Tell your friends and family. 
- Graphic designers are needed to make logos.
- UX people are needed to help make mockups to improve the design of the application.
- Do you have a social media account with lots of posts you would like to donate to the cause? Accounts like these can be used to help us bug hunt. Open an issue or tweet [@NickGottschlich](https://twitter.com/NickGottschlich).
- Be a user tester! Just record your experience using this the first time using screen recording software and upload it as [an issue](https://github.com/Nick-Gottschlich/Social-Amnesia/issues/new). Better yet if you can record yourself talking through your thoughts as you try out the software for the first time.

## Limitations

- Reddit
  - reddit API currently only indexes ~1k items back (as far as I can tell)
- Twitter
  - twitter API currently only indexes 3200 tweets back (not sure if it's the same for favorites or not)

## Links

- [Official Website](https://socialamnesia.com) - currently redirects to this github repo.
- [Official Twitter Account](https://twitter.com/social_amnesia)
- [Official Subreddit](http://reddit.com/r/socialamnesia)

## Related software

- [Shreddit](https://github.com/x89/Shreddit) - a python program to delete reddit posts/submissions.
- [Reddit Overwrite](https://greasyfork.org/en/scripts/10380-reddit-overwrite) - a greasey fork program to overwrite reddit comments.
- [Reddit Secure Delete](https://userscripts-mirror.org/scripts/show/166415) - a userscript program to delete reddit comments.
- [Nuke Reddit History](https://www.reddit.com/r/NukeRedditHistory/) - a web extension to erase reddit history.
- [Twitter Archive Eraser](https://github.com/martani/Twitter-Archive-Eraser) - tweet deletion tool
