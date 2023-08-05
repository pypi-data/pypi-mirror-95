`pocketsnack` is a command line application offering various commands to make your [Pocket](https://getpocket.com) account more manageable. You can de-duplicate your list, purge unwanted tags, and hide your enormous 'to be read' list in a special archive so that looking at your list doesn't become paralysing.

For help with commands see `pocketsnack --help`, or check [the README in the code repository](https://github.com/hughrun/pocketsnack).

# tl;dr

1. make sure you have installed a compatible Python version
2. `pip install pocketsnack` (you may need to use `pip3` instead)
3. `pocketsnack --config`
4. Add your Pocket API consumer key to the config file
5. `pocketsnack --authorise`
6. You are now ready to enjoy using pocketsnack from any directory

# Getting started

## Creating a Pocket consumer key for your app

1. Log in to Pocket in a web browser
2. Go to [`https://getpocket.com/developer`](https://getpocket.com/developer) and click 'CREATE NEW APP'
3. Complete the form: you will need all permissions, and the platform should be _Desktop (other)_, or _Mac_.
4. Your new app will show a **consumer key**, which you need to paste into the first line in your config file.

## Creating a configuration file

Before you can use `pocketsnack` you need to create a configuration file. If you run any command (including simply `pocketsnack` without an argument) when your configuration file doesn't exist, a new file will be created and will open in your default application for editing `yaml` files. You *must* copy in the consumer key referred to above, and *may* adjust any other settings. 

You can adjust most settings, but the defaults should be sensible for most users if you just want to get started.

| setting              | type    | description                           |  
| :------------------- | :---:   | :------------------------------------ |  
| pocket_consumer_key  | string  | the consumer key provided by Pocket when you register your 'app' (see below)|
| items_per_cycle      | integer | how many items you want to bring in to the List from your `tbr` archive when using `--lucky_dip`|
| archive_tag          | string  | the tag to use to identify items in your 'to be read' archive|
| ignore_tags          | list    | a list of tag names - items with any of these tags will be ignored by `--stash` and remain in your Pocket List|
| ignore_faves         | boolean | if set to `true` favorited items will be ignored by `--stash` and remain in your Pocket List| 
| fave_dupes         | boolean | if set to `true` the remaining (original) item will be favorited when duplicates are removed with `--dedupe`| 
| replace_all_tags     | boolean | if set to `true` all tags will be removed by `--stash` when adding the `archive_tag`, except anything in `retain_tags`|
| retain_tags          | list    | a list of tag names - these tags will not be removed by `--purge`, nor by `--stash` if `replace_all_tags` is set to `true`|
| longreads_wordcount  | integer | determines how long a 'longread' is. |
| num_videos           | integer | how many videos (if there are videos in your list) should be included in each `--lucky_dip`. This is a subset of `item_per_cycle`, not in addition to the total.|
| num_images           | integer | how many images (if there are images in your list) should be included in each `--lucky_dip`. This is a subset of `item_per_cycle`, not in addition to the total.|
| num_longreads        | integer | how many long reads (if there are long reads in your list) should be included in each `--lucky_dip`. This is a subset of `item_per_cycle`, not in addition to the total. The definition of a long read is determined by `longreads_wordcount`|
| pocket_access_token  | string  | access token required to interact with the Pocket API. This will be updated when you run `--authorise` and should not be edited manually.|

Save and close when you're done. You can edit this file again at any time by running `pocketsnack --config`.

## Authorising your app with a Pocket access token

Pocket uses OAuth to confirm that your app has permission from your user account to do stuff in your account. This means you need to authorise the app before you can do anything else. Once you have copied your app consumer key into the configuration file, run `pocketsnack --authorise` to get your token.

You should now have a line at the bottom of your config saying something like `pocket_access_token: 'aa11bb-zz9900xx'`