# AutoLN

AutoLN is a script that, in conjunction with rTorrent's event system, will
automatically sort and organize your downloads using symbolic links\* as they
complete! In its current state, the script supports the sorting of TV shows
only, but support for music, movies, and more are in the works. AutoLN can also
live along side any scripts you currently have in place.

\* Sorting/Organizing by copying is also supported.

## Installation

AutoLN is an executable Python script. It can be installed anywhere. Simply
confirm that it is executable (`chmod +x autoln.py`), make a configuration
file and you should be good to go!

## Basic Usage

Add a download complete event to your `.rtorrent.rc` similar to the
following:

	# Finished DL listener
	system.method.set_key = event.download.finished,log_finished,"execute=~/.scripts/autoln,$d.get_base_path=,$d.get_custom1="

In the above example, `$d.get_base_path=` is the full path to the completed
torrent and `$d.get_custom1=` is the torrent's label. if you do not currently
use labels, either set up proper wildcards in the AutoLN configuration or
set a place a base label in blase of `$d.get_custom1` (for example, `label`)
and properrly configure AutoLN to look for this label.

Labels can be easily added with different watch folders and settings in
`.rtorrent.rc` and/or by properally configuring the "Action" tab in
autodl-irssi (if you use both autodl-irssi and ruTorrent). There should
also be a way to configure autodl-irssi to add labels to torrents from
withen the configuration files, though this is out of the scope of this
readme.

## Configuration

The default configuration file will be loaded from ~/autoln. If you need to
use a configuration file other than the defualt, use the `-c [conf]`
argument. All other command line arguments are explained in `--help`.

AutoLN has many configuration options. For information on how to configure
AutoLN, read the `documented_conf.conf` file. There is also a basic,
undocumented config file for use once you understand how the configuration
works. Basic Regex knowledge is recommended for creating filters.

## Script usefulness

If you already have a script that runs on completed torrents and would like
to make use of AutoLN, it is easy! When AutoLN is executed, it simply outputs
the path to the file that was organized (if `-q` or `-v` is not used). This
will allow you to run AutoLN, store the sorted location of the completed file,
and continue with your script on the (now sorted and properally named) file.
