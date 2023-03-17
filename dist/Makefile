SPEC=grrreader.spec
VERSION=0.0.7
DIST_DIR=dist
TGZ_NAME=grrreader-$(VERSION).tar.gz

all: rpm
tarball: $(TGZ_NAME)

rpm: rpmbuild/SPECS/$(SPEC) rpmbuild/SOURCES/$(TGZ_NAME)
	rpmbuild --define "_topdir ${PWD}/rpmbuild" -ba $(SPEC)
	cp rpmbuild/RPMS/noarch/grrreader-$(VERSION)-*.rpm .

rpmbuild/SPECS/$(SPEC): $(SPEC) rpmbuild/SPECS
	cp $< $@

rpmbuild/SOURCES/$(TGZ_NAME): $(TGZ_NAME)
	cp $< $@

rpmbuild:
	mkdir -p rpmbuild

rpmbuild/%: rpmbuild
	mkdir -p rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

$(TGZ_NAME):
	cd ..; git archive --prefix=grrreader-$(VERSION)/ --format=tar HEAD | gzip > $(DIST_DIR)/$(TGZ_NAME)

clean:
	rm -rf rpmbuild
	rm -f $(TGZ_NAME)
	rm -f grrreader-$(VERSION)-*.rpm
	rm -f grrreader-*.tar.gz
