%global _hardened_build 1
Summary:             Mail delivery agent with filtering abilities
Name:                maildrop
Version:             3.0.3
Release:             2
License:             GPLv2 with exceptions
URL:                 https://sourceforge.net/projects/courier
Source0:             https://downloads.sourceforge.net/project/courier/%{name}/%{version}/%{name}-%{version}.tar.bz2
Source1:             https://downloads.sourceforge.net/project/courier/%{name}/%{version}/%{name}-%{version}.tar.bz2.sig
Source2:             pubkey.maildrop

Patch0:              backport-001-Convert-to-pcre2.patch
Patch1:              backport-002-Convert-to-PCRE2.patch

Requires:            courier-unicode >= 2.1
BuildRequires:       automake, libtool, autoconf gcc-c++, gdbm-devel, libdb-devel, pcre2-devel gawk
BuildRequires:       gnupg courier-unicode-devel >= 2.1 libidn-devel
%description
maildrop is the mail filter/mail delivery agent that's used by the
Courier Mail Server. This is a standalone build of the maildrop mail
filter that can be used with other mail servers.
maildrop is a replacement for your local mail delivery agent. maildrop
reads a mail message from standard input, then delivers the message to
your mailbox. maildrop knows how to deliver mail to mbox-style
mailboxes, and maildirs.
maildrop optionally reads instructions from a file, which describe how
to filter incoming mail. These instructions can direct maildrop to
deliver the message to an alternate mailbox, or forward it somewhere
else. Unlike procmail, maildrop uses a structured filtering language.
maildrop is written in C++, and is significantly larger than
procmail. However, it uses resources much more efficiently. Unlike
procmail, maildrop will not read a 10 megabyte mail message into
memory. Large messages are saved in a temporary file, and are filtered
from the temporary file. If the standard input to maildrop is a file,
and not a pipe, a temporary file will not be necessary.
maildrop checks the mail delivery instruction syntax from the filter
file, before attempting to deliver a message. Unlike procmail, if the
filter file contains syntax errors, maildrop terminates without
delivering the message. The user can fix the typo without causing any
mail to be lost.

%prep
%autosetup -p1
gpg --import %{SOURCE2}
gpg --verify %{SOURCE1} %{SOURCE0}

%build
autoreconf
%configure --disable-shared \
  --enable-use-flock=1 --with-locking-method=fcntl \
  --enable-use-dotlock=1 \
  --enable-syslog=1 \
  --enable-sendmail=%{_sbindir}/sendmail

%make_build

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} htmldir=%{_defaultdocdir}/%{name}
cp -pr COPYING COPYING.GPL AUTHORS %{buildroot}%{_defaultdocdir}/%{name}
cp -pr README README.postfix ChangeLog UPGRADE %{buildroot}%{_defaultdocdir}/%{name}

%files
%doc %{_defaultdocdir}/%{name}
%attr(6755,root,mail) %{_bindir}/maildrop
%attr(6755,root,mail) %{_bindir}/lockmail
%{_bindir}/deliverquota
%{_bindir}/mailbot
%{_bindir}/maildirmake
%{_bindir}/makemime
%{_bindir}/reformail
%{_bindir}/reformime
%{_bindir}/makedat
%{_bindir}/makedatprog
%{_bindir}/maildirkw
%{_bindir}/maildirwatch
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8*

%changelog
* Wed Jun 01 2022 gaihuiying <eaglegai@163.com> - 3.0.3-2
- switch from pcre to pcre2

* Thu Dec 16 2021 gaihuiying <gaihuiying1@huawei.com> - 3.0.3-1
- update to 3.0.3

* Mon Jan 25 2021 orange-snn <songnannan2@huawei.com> - 3.0.1-1
- update to 3.0.1

* Wed Oct 14 2020 chengzihan <chengzihan2@huawei.com> - 2.9.3-1
- Package init
