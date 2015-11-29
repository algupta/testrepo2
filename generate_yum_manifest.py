#!/usr/bin/env python

import yum
import urllib2
import hashlib
from optparse import OptionParser

class GenManifest():
  def __init__(self):
    self.pkgs = []
    self.yb = yum.YumBase()
    self.yb.setCacheDir()

  def getPackages(self, filename, repolist):
    '''
    This method gets newest packages from the repo.
    Disables all existing repo and adds new repo.
    To check enabled repos
    '''
    # yb.doRepoSetup(), repos = yb.repos.listEnabled()
    self.yb.repos.disableRepo('*')
    self.yb.add_enable_repo('myrepo', repolist)
    #self.pkgs = self.yb.pkgSack.returnNewestByNameArch(patterns=[])
    self.pkgs = self.yb.pkgSack.returnPackages()
    try:
      fp = open(filename, "w")
      try:
        fp.write("---\n")
        for pkg in self.pkgs:
          fp.write("- {name: %s, sha256sum: %s}\n" % (pkg, pkg.checksum))
      finally:
        fp.close()
    except IOError:
      print "Unable to open %s for writing" %fp.name
      raise

def main():
  usage = '''
  -r REPOURL, --repourl=REPOURL
                      Repo url, e.g http://yum.messagelabs.net/repos/
  -f FILENAME, --file=FILENAME
                      Output filename to store yaml file
  '''
  parser = OptionParser(usage=usage)
  parser.add_option("-r", "--repourl", action="append", help="Repo url, e.g http://yum.messagelabs.net/repos/")
  parser.add_option("-f", "--file", type="string", help="Output filename to store yaml file")
  (options, args) = parser.parse_args()
  if not (options.file and options.repourl):
    parser.error("Wrong arguments")
  inst = GenManifest()
  inst.getPackages(options.file, options.repourl)


if __name__ == "__main__":
  main()

