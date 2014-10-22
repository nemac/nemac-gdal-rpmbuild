This project containst the files necessary to build a custom RPM package of GDAL (http://www.gdal.org)
for use on NEMAC's cloud servers.

Here's how to do it:

* Configure a cloud server with the relevant software for building
  rpms; this can be done with the _rpmbuilder_ puppet manifest in
  NEMAC's _cloudconf_ project.
  
* Make yourself an account on that server, and add your account to the
  _mock_ group; this can be done with the commands (which must be run
  as root):
  
      % sudo /usr/sbin/useradd USERNAME
      % sudo usermod -a -G mock USERNAME
      
* NOTE: everything else in these instructions should be done using
  your account on the server, not the root account.  NEVER build an
  rpm using the root user.
      
* Clone this project into your account's home directory on the server;
  this will create the directory `/nemac-gdal-rpmbuild`.
  
* Run the command:

```
      rpmbuild --define "_topdir $HOME/nemac-gdal-rpmbuild" --define "_smp_mflags -j8" -bb $HOME/nemac-gdal-rpmbuild/SPECS/nemac-gdal.spec
```

  Note: the `-define "_smp_mflags -j8"` part of the above command says
  to use up to 8 processes in parallel when compiling the source code;
  on a multiprocessor server (most servers are multiprocessor) this
  will greatly speed up the build process.  You can adjust the number
  8 to a different number that is more appropriate for the server you
  are using if you w

  When the `rpmbuild` command above finishes, the RPMs that it created will be in the
  `$HOME/nemac-gdal-rpmbuild/RPMS/x86_64` directory.  There will be three of them:

    * nemac-gdal-*.x86_64.rpm
    * nemac-gdal-debuginfo-1.11.1-1.*.x86_64.rpm
    * nemac-gdal-devel-*.x86_64.rpm
    
* Copy these RPMs to NEMAC's yum repository using the following commands:    

```
      scp $HOME/nemac-gdal-rpmbuild/RPMS/x86_64/*.rpm dev.nemac.org:/var/dev.nemac.org/html/yum-repo/x86_64/RPMS
      ssh dev.nemac.org /var/dev.nemac.org/html/yum-repo/updaterepos
```
