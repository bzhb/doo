# Author:  2016 Renan Fargetton < email >

pkgname=doo
pkgver=0.0.1
pkgrel=1
epoch=
pkgdesc="Utility to run user-predefined commands (from a small .doo file)"
arch=('any')
url=""
license=('GNU GPLv3 or later')
depends=('python')
optdepends=()
install="doo.install"

build() {
	#mkdir -p $srcdir/
	cd $srcdir/
}

package() {
	cd $srcdir/
	install -D -m 0755 doo "$pkgdir/usr/bin/doo"
	install -D -m 0644 doo.conf "$pkgdir/usr/share/doo/doo.conf"
}

