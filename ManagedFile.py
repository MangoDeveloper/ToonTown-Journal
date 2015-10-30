import urllib2
import bsdiff4
import hashlib
import os
import bz2
 
class ManagedFile:
    def __init__(self, name, installBase=None, hash=None, compHash=None, dl=None, progressCallback=None):
        self.name = name
        self.installBase = installBase
        if self.installBase:
            self.loc = os.path.join(installBase, name)
            self.ensureDirectoriesExist()
        self.progressCallback = progressCallback
        self.hash = hash
        self.compHash = compHash
        if not dl:
            self.dl = self.name
        else:
            self.dl = dl
 
    def ensureDirectoriesExist(self):
        # For any directory tree structures this file is under, create those directories.
        dirs = self.name.split('/')[:-1] # Our manifest will always use /
        base = self.installBase
        for dir in dirs:
            base = os.path.join(base, dir)
            if not os.path.isdir(base):
                os.makedirs(base)
 
    def update(self, urls, patches=None):
        if not self.loc:
            raise Exception("Cannot update a ManagedFile that has no filesystem location")
 
        if not self.hash:
            raise Exception("Cannot update a ManagedFile that doesn't know its hash")
 
        for url in urls:
            if url and url[-1:] != '/':
                # We want a trailing slash on the base URL
                fixedurl = url + '/'
                # Toss back in list
                urls[urls.index(url)] = fixedurl
 
        # Main thingy. Makes sure the file is up-to-date
        if not os.path.exists(self.loc):
            # file didn't exist, just get fresh
            print 'File did not exist, downloading fresh...'
            self.obtainFresh(urls)
        else:
            if self.hash == self.currentHash():
                print 'File is up to date.'
                return # all good
            # oh noes we're out of date
            patch = self.getPatch(patches)
            if not patch:
                # oh noes no patch found just do it fresh
                print 'No patch found! Downloading fresh...'
                self.obtainFresh(urls)
            else:
                # neat let's patch
                print 'Patch located! Patching...'
                patchIsGood = self.doPatch(patch, urls)
                # are we up to date now?
                if not patchIsGood:
                    # fuck
                    print 'Patching failed! Downloading fresh...'
                    self.obtainFresh(urls)
                else:
                    print 'Patched file.'
 
    # Try all available mirrors to obtain file
    def obtainFresh(self, urls):
        # Make a temporary copy to use, as if mirrors fail we remove them from the parent list
        urlsToTry = [x for x in urls]
        for url in urlsToTry:
            # Try to update from this mirror
            try:
                self._obtainFresh(url + self.dl)
                return
            except Exception, e:
                # Bad mirror
                print 'Mirror %s failed integrity checks, removing... %s' % (url, e)
                urls.remove(url)
 
    # Actually do the downloading and writing of the fresh file
    def _obtainFresh(self, url):
        # Just download the file anew
        freshFile = urllib2.urlopen(url)
        totalSize = freshFile.info().getheader('Content-Length').strip()
        totalSize = int(totalSize)
        totalDownloaded = 0
        progress = 0
        ffContents = ''
        while 1:
            chunk = freshFile.read(8192)
            totalDownloaded += len(chunk)
            if not chunk:
                break
            ffContents += chunk
            oldProgress = progress
            progress = float(totalDownloaded) / totalSize
            progress = int(round(progress*100, 0))
            if progress > oldProgress:
                if self.progressCallback is not None:
                   self.progressCallback(progress)
        if self.__hash(ffContents) != self.compHash:
            raise Exception('Downloaded and compressed fresh file did not match compHash! This is not good!')
        ffContents = bz2.decompress(ffContents)
        if self.__hash(ffContents) != self.hash:
            raise Exception('Downloaded and decompressed fresh file did not match hash! This is not good!')
        f = self._getFile('wb')
        f.write(ffContents)
        f.close()
 
    def _getFile(self, flags='rb'):
        try:
            return open(self.loc, flags)
        except:
            # We don't exist :>
            print ''
            return None
 
    def getContents(self):
        if not self.loc:
            raise Exception("Cannot read contents of a ManagedFile that has no filesystem location")
        f = self._getFile('rb')
        fc = f.read()
        f.close()
        return fc
 
    def __hash(self, input):
        # Do the actual hashing
        return hashlib.sha1(input).hexdigest()
 
    def currentHash(self):
        return self.__hash(self.getContents())
 
    def doPatch(self, patch, urls):
        # First download the patch
        patchContents = self.downloadPatch(patch, urls)
        if not patchContents:
            raise Exception('Error in procuring patch')
        # Then prepare to do the patch
        oldContents = self.getContents()
        # Now do the lib stuff
        patchedContents = bsdiff4.patch(oldContents, patchContents)
        # Delete the old and patch contents to conserve memory, as they can be large with big files
        del oldContents
        del patchContents
        # Alright, what's the hash, broseph? Is it good?
        if self.hash != self.__hash(patchedContents):
            # Oh, that's not good...
            raise Exception('In-memory patch did not have correct hash after patching! Patching failed!')
        # Sweet, now write the patched contents to disk
        fileHandle = self._getFile('wb')
        fileHandle.write(patchedContents)
        fileHandle.close()
        del patchedContents
        return True

    def downloadPatch(self, patch, urls):
        urlsToTry = [x for x in urls]
        for url in urlsToTry:
            # Try to update from this mirror
            try:
                return self._downloadPatch(patch, url)
            except Exception, e:
                # Bad mirror
                print 'Mirror %s failed integrity checks, removing... %s' % (url, e)
                urls.remove(url)

    def _downloadPatch(self, patch, url):
        # Download a patch and return its contents
        if 'filename' not in patch or 'patchHash' not in patch or 'compPatchHash' not in patch:
            raise Exception('Patch descriptor is not fully qualified; it has missing parameters')
        patchfileDlHandle = urllib2.urlopen(url + patch.get('filename'))
        patchfile = patchfileDlHandle.read()
        # Perform a hash check
        patchHash = self.__hash(patchfile)
        if patchHash != patch.get('compPatchHash'):
            raise Exception("Hash of downloaded and compressed patch was invalid!")
        # decompress
        patchfile = bz2.decompress(patchfile)
        if self.__hash(patchfile) != patch.get('patchHash'):
            raise Exception("Hash of downloaded and decompressed patch was invalid!")
        return patchfile
 
 
    def getPatch(self, patches):
        hash = self.currentHash()
        if hash in patches:
            return patches.get(hash)
        return None
 
    # Patch creation
    def diff(self, oldFiles):
        # Create a patch in the target directory, if need be, and then return our entry in the manifest
        # First of all, is there a current version of this file?
        if not os.path.exists(self.loc):
            print "Current version of file %s does not exist, aborting! You should've told me this file isn't managed any more :(" % self.name
            exit(1)
 
        currentHash = self.currentHash()
        # bz2 myself and toss it on disk
        me = self.getContents()
        me = bz2.compress(me)
        compHash = self.__hash(me)
        compressedSelf = open(self.loc + '.bz2', 'wb')
        compressedSelf.write(me)
        compressedSelf.close()
 
        # if this is a first-time manifest
        if not oldFiles:
            # New file, don't have patches or anything
            return {'hash': currentHash, 'dl': self.name + '.bz2', 'compHash': compHash, 'patches': {}}
        fileEntry = {'hash': currentHash, 'dl': self.name + '.bz2', 'compHash': compHash, 'patches': {}}
 
        # iterate through all the old versions we'll be diffing against
        for oldFile in oldFiles:
            oldFileHandle = oldFile._getFile('rb')
            if oldFileHandle is None:
                # Old file doesn't exist, w/e
                continue
            oldFileHandle.close()
            oldHash = oldFile.currentHash()
            if oldHash == currentHash:
                # easy
                continue
            # Does a patch already exist?
            if oldHash in fileEntry['patches']:
                # Yep, it does
                continue
            # ooooooh, we have to make a patch. start by setting up where the patch will go
            patchName = '%s_%s_to_%s.patch.bin' % (os.path.basename(self.name), oldHash[:5], currentHash[:5])
            print 'Diffing file %s: %s/%s -> %s' % (self.name, oldFile.installBase, oldHash[:5], currentHash[:5])
            patchPath = os.path.join(os.path.join(self.installBase, os.path.split(self.name)[0]), patchName)
            # Then, do the diff in-memory
            patchContents = bsdiff4.diff(oldFile.getContents(), self.getContents())
            # Figure out the hash of the patch
            patchHash = self.__hash(patchContents)
            # Then compress it!
            patchContents = bz2.compress(patchContents)
            # Then hash it again! Isn't this fun?
            compPatchHash = self.__hash(patchContents)
            # Then finally write it to disk
            patchHandle = open(patchPath, 'wb')
            patchHandle.write(patchContents)
            patchHandle.close()
            fileEntry['patches'][oldHash] = {'filename': os.path.join(os.path.dirname(self.name), patchName), 'patchHash': patchHash, 'compPatchHash': compPatchHash}
        return fileEntry