--- pyperl-1.0.1d/setup.py.norebuild	2007-10-16 11:42:41.000000000 +0200
+++ pyperl-1.0.1d/setup.py	2007-10-20 07:37:16.000000000 +0200
@@ -2,6 +2,7 @@
 
 from distutils.core import setup, Extension
 from distutils.command.install import install
+from distutils.command.build import build
 
 DEBUG = 0
 perl = 'perl'
@@ -142,6 +143,23 @@ ext_modules.append(Extension(name = ext_
                              ))
 ext_modules.extend(extra_ext)
 
+class build_perl(build):
+    def run(self):
+	os.chdir('Python-Object')
+	build.spawn(self, ['perl','Makefile.PL', 'INSTALLDIRS=vendor'], 'Python-Object')
+	build.spawn(self, ['make'])
+	os.chdir('..')
+	build.run(self)
+
+class test(build):
+    def run(self):
+	cwd=os.getcwd()
+	ldpath = '%s/Python-Object/blib/arch/auto/Python/Object' % cwd
+	perllib = '%s/Python-Object/blib/lib' % cwd
+	pypath = '%s/%s' % (cwd, self.build_lib)
+	os.system('LD_LIBRARY_PATH="%s" PERL5LIB="%s" PYTHONPATH="%s" python test.py' % (ldpath, perllib, pypath))
+	build.run(self)
+
 class my_install(install):
 
     def run(self):
@@ -150,17 +168,15 @@ class my_install(install):
         if os.access(multi_perl, os.F_OK):
             os.unlink(multi_perl)
 
-        os.chdir(os.path.join(cur_dir, 'Python-Object'))
-        retcode = subprocess.call(['perl', 'Makefile.PL'])
-        retcode = subprocess.call(["make", "install"])
-        os.chdir(cur_dir)
+        os.chdir('Python-Object')
+        install.spawn(self, ["make", "DESTDIR=%s" % self.root, "install"])
+        os.chdir('..')
         if "-DMULTI_PERL" in cc_extra:
             cc_extra.pop(cc_extra.index("-DMULTI_PERL"))
             sources.pop(sources.index('thrd_ctx.c'))
         # Run actual install
         install.run(self)
 
-
 setup (name        = "pyperl",
        version     = "1.0.1",
        description = "Embed a Perl interpreter",
@@ -169,5 +185,5 @@ setup (name        = "pyperl",
        author_email= "gisle@ActiveState.com",
        py_modules  = ['dbi', 'dbi2', 'perlpickle', 'perlmod'],
        ext_modules = ext_modules,
-       cmdclass    = { 'install': my_install }
+       cmdclass    = { 'install': my_install, 'build': build_perl, 'test': test }
       )
