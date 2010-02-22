
==================================
 Debian packages and repositories
==================================


Installing package dependencies for building packages
=====================================================

::

  sudo aptitude install dpkg-dev file make patch dh-make \
  	debhelper devscript fakeroot gnupg lintian pbuilder

Creating a package
==================

An example on howto make a debian from sources from svn. This package
only copies files to the filesystem. 

::

  package=spec
  version=0.1
  cd ~/archi
  svn co svn://rd.anevia.com/svn/archi/$package
  mv $package{,-$version}
  cd $package-*
  dh_make -e jeandaniel.browne@anevia.com --createorig
  rm -rf ../$package-*.orig debian/*.ex debian/*.EX debian/dirs debian/docs
  
  cat > debian/rules <<EOF
  #!/usr/bin/make -f
  # -*- makefile -*-
  
  build: 
  
  clean: 
  	dh_clean
  
  binary-indep:
  	dh_testdir
  	dh_testroot
  	dh_prep  
  	dh_install
  	dh_gencontrol
  	dh_builddeb
  
  binary-arch: 
  
  binary: binary-indep binary-arch
  EOF
  
  cat > debian/$package.install <<EOF
  $package.pdf usr/share/doc/anevia
  EOF
  svn add ./debian
  svn ci -m 'Debianized sources : ready to make a package'
  dpkg-buildpackage
  ls ../*.deb

.. todo::

    Update the packaging example with the latest files

Howto set up a repository
=========================

::

  sudo aptitude install openbsd-inetd proftpd
  cd

  # for an official debian repository mirror
  # mkdir -p dists/{stable,testing,unstable}/{main,contrib,non-free}/{source,binary-{all,i386}}

  mkdir -p /home/ftp/dists/{released,review,experimental}/{main,non-free}/{source,binary-i386}
  
  sudo addgroup ftp
  sudo usermod -g ftp ftp
  sudo adduser jdbrowne ftp
  sudo chown ftp:ftp /home/ftp/dists/
  sudo chmod -R g+w .
  
  # install a proftp server here serving /home/ftp/ to anonymous

Provision new packages into the repository
==========================================

::

  # $ftproot is the root of the ftp server the index files will be
  # broken if dpkg-scan* are executed from anything else than the ftp
  # root: the "filename" fields must point to a file with a path
  # relative to the ftproot

  rootftp=/home/ftp/

  package=`sed -n 's/Package: \(.*\)/\1/p' debian/control`

  bin=dists/review/non-free/binary-i386
  bin64=dists/review/non-free/binary-amd64
  source=dists/review/non-free/source

  dpkg-buildpackage
  dpkg-buildpackage -aamd64

  mv ../$package_*amd64.deb     $rootftp/$bin64
  mv ../$package_*i386.deb      $rootftp/$bin
  mv ../$package_*.{dsc,tar.gz} $rootftp/$source


  ( cd  $rootftp
    dpkg-scanpackages $bin   /dev/null > $bin/Packages
    dpkg-scanpackages $bin   /dev/null | gzip -9c > $bin/Packages.gz

    dpkg-scanpackages $bin64 /dev/null > $bin64/Packages
    dpkg-scanpackages $bin64 /dev/null | gzip -9c > $bin64/Packages.gz

    dpkg-scansources $source /dev/null > $source/Sources
    dpkg-scansources $source /dev/null | gzip -9c > $source/Sources.gz
  )
  
Use the repository
==================

::

  sudo -s
  echo "deb ftp://jdbrowne.anevia.com/ review non-free" >> /etc/apt/sources.list
  echo "deb-src ftp://jdbrowne.anevia.com/ review non-free" >> /etc/apt/sources.list
  aptitude update spec
  aptitude show spec
  aptitude install spec
  


Release a new version
=====================


::

  cd 


Checklist for software release
==============================

When deciding to release version x.y, great care should be taken
regarding the version and the changelog:

#. check the todo list in the specs, the tickets on trac to be sure it
   is the right time to release

#. the debian/changelog must be updated

#. the debian/changelog version must be provisioned into the conf.py,
   into the man pages and into the binary -v option

#. the debian changelog must make its way to the changes section of
   the rst and must be formatted for the commit message

#. the trunk must be commited with the commit message

#. the sources must be built (the pdf must mentions it is a draft
   except in the case of stable release) the packages must be uploaded
   to review, the pdf version should appear in the filename (fixed
   double digits for x and also for y). Maybe older pdf should be
   erased evince spec.pdf dpkg-deb -c ../\*.pdf ./debian/rules clean
   svn propset svn:mime-type application/octet-stream allp-vodrtp.pdf,
   the logs levels must be set to 'production' (must be turned to info)

.. Here a manual review may be necessary
   dpkg-deb -c ../\*.deb
   evince *.{ps,pdf}
   svn propset svn:mime-type application/octet-stream *.{pdf,ps}
   find -name '*.pdf' -exec svn propset svn:mime-type application/octet-stream {} \;

#. If the reviewers validate the package, the source and binary
   packages are copied from review to release. It is these steps in
   which developers and peer architect should be consulted

#. a correct directory must be created in svn://specs the resulting pdf
   must be copied there with the changelog files augmented by the vcs
   version with which the sources were commited.

#. the release can be commited in specs with the changelog

#. the fixed tickets of the changelogs should be closed. Would be
   great if the changelog bullet for the bug ends up in the trac
   'closed' comment.

#. pick another spec and back to 1.

.. A sphinx builder can retrieve the rst changelogs and provision the
   debian/changelog and prepare an svn commit message file or a sphinx
   extension can retrieve the debian/changelog to generate the
   specification extension. It seems simpler to format to
   debian/changelog than parsing debian changelog to docutils.	

.. I need to retrieve the upstream sources manipulating the packaging
   system, the difficulty then is to bridge the gap between trunk and
   the source package to make it easy to apply a patch from the source
   package to upstream

Open questions
==============

- How to know which package can be upgraded from the command line

- How to know which repository holds this or that software
