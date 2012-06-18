#!/usr/bin/python

###                                ###
#                                    #
# AutoLN v1.0 by Rain724 (6-18-2012) #
#                                    #
###                                ###

import platform
import getopt
import os
import sys
import ConfigParser
import json
import re
from os.path import splitext, basename
from shutil import copyfile

def main(): 
    # Check for the existance of arguments
    if not len(sys.argv):
        usage()
        sys.exit()

    # Parse the arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:qvk:", ["help", "quiet"])
    except getopt.GetoptError, err:
        # Print help
        print str(err)
        usage()
        sys.exit(2)
    
    # Analyze the arguments
    configFile = ""
    quiet = False
    verbose = False
    for a, o in opts:
        if a in ("-h", "--help"):
            usage()
            sys.exit()
        elif a == "-c":
            configFile = o
        elif a in ("-q", "--quiet") and not verbose:
            quiet = True
        elif a == "-v":
            quiet = False
            verbose = True
        elif a == "-k" and o == "irby":
            print " <('.'<) <('.')> (>'.')> Can't touch this!!"
            sys.exit()

    # Confirm that two arguments remain; file/dir and label
    if not len(args) == 2:
        usage()
        sys.exit()
    
    # Read the config file
    config = None
    if configFile != "":
        # Read agr'ed config
        config = Config(configFile)
    elif os.path.exists(os.path.expanduser("~/.autoln")):
        # Read config from home directory
        config = Config(os.path.expanduser("~/.autoln"))
    else:
        print "Error: No config file found! Create ~/.autoln or use the -c flag."
        sys.exit()
    
    # Add argument settings to config
    config.setVerbose(verbose)
    config.setQuiet(quiet)

    if config.enable:
        if args[1] == config.tvlabel:
            handleTV(config, args)
        else:
            print "Error: This feature is not supported yet!"

def handleTV(config, args):
    filename, extension = splitext(args[0])
    filename = basename(filename)
    if extension.replace(".", "") in config.tvextensions:
        for filter in config.tvfilters:
            match = re.match(filter[0], filename, re.I)
            if match:
                destination = filter[1]
                i = 1
                for g in match.groups():
                    destination = destination.replace("${" + str(i) + "}", g)
                    i += 1
                destination = config.tvdir + destination.replace("$\\{", "${")
                if config.overwrite:
                    link(args[0], destination)
                else:
                    if os.path.exists(destination):
                        i = 1
                        d = destination.replace(extension, "." + str(i) + extension)
                        while os.path.exists(d):
                            i += 1
                            d = destination.replace(extension, "." + str(i) + extension)
                        destination = d
                if config.copy:
                    copy(args[0], destination)
                else:
                    link(args[0], destination)
                if config.verbose:
                    print "Linking: " + destination + " -> " + args[0]
                elif not config.quiet:
                    print destination
                return

# Creates a symbolic link at destination pointing at source
def link(source, destination):
    # Create the directory structure
    dirs = os.path.dirname(destination)
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    # If a link exists already, unlink it
    if os.path.exists(destination):
        os.unlink(destination)
    os.symlink(source, destination)

# Copies source to destination
def copy(source, destination):
    # Create the directory structure
    dirs = os.path.dirname(destination)
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    copyfile(source, destination)

def usage():
    print "AutoLN v1.0 by Rain724 (06-18-2012)"
    print "Usage: autoln.py [-hqv] [-c conf] file/directory label\n"
    print "Required:"
    print "    file/directory     Full path to file. If directory"
    print "                       is given, all files withen that"
    print "                       directory will be sorted."
    print "    label              The completed torrent(s) label;"
    print "                       eg: TV"
    print "Optional:"
    print "    -h, --help         Display this help information"
    print "    -c file.conf       Configuration file to use;"
    print "                       ~/.autoln used by defualt"
    print "    -q, --quiet        Supress output"
    print "    -v                 Verbose output\n"
    print "                    (This script has hidden kirby powers!!)"


# Configuration
class Config(object):
    def __init__(self, configFile):
        # Read config file
        config = ConfigParser.RawConfigParser()
        config.read(configFile)

        # Global Settings
        self.enable = Config.getboolean(config, "global", "enable", False)
        self.copy = Config.getboolean(config, "global", "copy", False)
        self.overwrite = Config.getboolean(config, "global", "overwrite", False)
        # TV Settings
        self.tvenable = Config.getboolean(config, "tv", "enable", False)
        self.tvdir = Config.get(config, "tv", "outputdir", "")
        self.tvextensions = json.loads(Config.get(config, "tv", "extensions", "[]"))
        self.tvlabel = Config.get(config, "tv", "label", "")
        # TV Filters
        self.tvfilters = []
        for k, f in config.items("shows"):
            ff = json.loads(f)
            if (len(ff) != 2):
                print "Error: Configuration: [shows]->" + k + " invalid format!"
                sys.exit(2)
            self.tvfilters.append(ff)

    # Verbose setter
    def setVerbose(self, verbose):
        self.verbose = verbose

    # Quiet setter
    def setQuiet(self, quiet):
        self.quiet = quiet

    # Get string from ConfigParser; if option does not exist, return default
    @staticmethod
    def get(config, section, option, default):
        try:
            return config.get(section, option)
        except ConfigParser.NoOptionError:
            return default
        except ConfigParser.Error:
            print "Error: Configuration: [" + section + "]->" + option + " could not be read!"
            sys.exit(2)

    # Get boolean from ConfigParser; if option does not exist, return default
    @staticmethod
    def getboolean(config, section, option, default):
        try:
            return config.getboolean(section, option)
        except ConfigParser.NoOptionError:
            return default
        except ConfigParser.Error:
            print "Error: Configuration: [" + section + "]->" + option + " could not be read!"
            sys.exit(2)

# Let's run this bitch!
if __name__ == "__main__":
    main()
