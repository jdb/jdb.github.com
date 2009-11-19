
Subversion's cheatsheet
=======================

Installation des paquets debian::

   sudo aptitude install subversion apache2 libapache2-svn

Configuration d'une instance de dépot::

   sudo mkdir -p /var/www/svn/myproject
   chown -R www-data.www-data !$       # the wiki files belongs to apache
   svnadmin create !$
   chmod -R ug+rwx !$                  # apache may read and write
   chmod -R o-rwx !$                   # everybody else is rejected
          
   cd ; svn checkout file:///var/www/svn/myproject/
   cd myproject && svn mkdir tags branches trunk
   svn commit -m ''


Configuration d'Apache: add the following at the root of your /etc/apache2/sites-available/default ::

  <Location /svn>
    DAV svn
    SVNParentPath /var/www/svn 
  </Location>


Commandes quotidiennes::

  cd ~/my-projectcd 
  svn update
  svn status
  emacs machin.py
  svn commit --message "support de l alphabet elfique"
  
Ignorer certain fichier pas important lors des svn status, et commit::

  svn propedit svn:ignore mydir # launches a text editor

  # or, in batch

  cat >  /tmp/list << EOF
  *.pdf
  *.ps
  _build
  EOF

  svn propsset svn:ignore -F /tmp/list mydir


Correction d'un bug en utilisant des branches::

  svn copy trunk tags/1.0.0       # last release

  copy tags/1.0.0 branches/ticket-42  
                                  # bug report, hence branch
  ...
  svn ci -m 'ready for review'    # fix and commit in the branch


  v=`svn log --stop-on-copy tags/1.0.0 | sed ... `      ###                              
  cd trunk && svn update                                ###  This is the merge step
  svn merge -r $v:head branches/1.0.0                   ###
                                                        ###  $v was the 1st revision for the branch
  rm ssh							  
  svn ci -m 'fix merged'
  copy trunk tags/1.0.1 
 

