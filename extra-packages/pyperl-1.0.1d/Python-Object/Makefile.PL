use ExtUtils::MakeMaker;

my $PY_VERSION = '';

if ( $ENV{'PY_VERSION'} ) { $PY_VERSION=$ENV{'PY_VERSION'}; };

chomp(my $pyinc = `python$PY_VERSION-config --includes`);
chomp(my $pylib = `python$PY_VERSION-config --libs`);
chomp(my $pysitelib = `python$PY_VERSION -c 'from distutils.sysconfig import get_python_lib; print get_python_lib(1)'`);

print "Using python$PY_VERSION\n";
print "INC: $pyinc\n";
print "LIB: $pylib\n";
print "site-packages: $pysitelib\n";


my @define;
my @libs;

push(@define, "MULTI_PERL") if -f "../MULTI_PERL";

if (-f "../BOOT_FROM_PERL") {
    push(@define, "BOOT_FROM_PERL");
    push(@libs, $pylib);
    push(@extra, OBJECT => "Object.o $pysitelib/perl.so");
}

if ($^O eq 'MSWin32') {
    my $pylib;
    for (15,16,20) {
	$pylib = "$pyinc\\..\\libs\\python$_.lib";
	last if -f $pylib;
    }
    push(@libs, "\"$pylib\"", "..\\perlpyd.lib");
}

if (@define) {
    push(@extra, DEFINE => join(" ", map "-D$_", @define));
}
if (@libs) {
    if ($^O eq 'MSWin32') {
	push(@extra, LIBS => join(" ", @libs));
    } else {
	push(@extra, LIBS => \@libs);
    }
}

WriteMakefile(
    NAME	 => 'Python::Object',
    VERSION_FROM => 'Object.pm',
    INC          => $pyinc,
    @extra,
    dist         => { COMPRESS => 'gzip -9f', SUFFIX => 'gz', },
);
