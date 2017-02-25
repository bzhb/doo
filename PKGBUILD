# Author:  2016 Renan Fargetton < email >

pkgname=doo
#pkgname=doo-git
#_pkgname=doo
pkgver=0.0.3
pkgrel=1
epoch=
pkgdesc="Utility to run user-predefined commands from a list"
arch=('any')
url=""
license=('GNU GPLv3 or later')
depends=('python')
provides=('doo')
conflicts=('doo')
optdepends=()
install="doo.install"
#source=('git+https://github.com/user/doo')

build() {
	#mkdir -p $srcdir/
	cd $srcdir/
}

package() {
	cd $srcdir/
	install -D -m 0755 doo "$pkgdir/usr/bin/doo"
	install -D -m 0644 usr_share/doo.conf "$pkgdir/usr/share/doo/doo.conf"
	install -D -m 0644 usr_share/template.doo "$pkgdir/usr/share/doo/template.doo"
}

