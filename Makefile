PACKAGE_NAME := openwisp-vpn-deployer
VERSION := 1.0.0
ARCH := $(shell dpkg --print-architecture)

SOURCE_FILES := cli.py api.py websocket_client.py main.py setup_config.json
SOURCE_DIRS := openvpn wireguard vxlan_wireguard zerotier

.PHONY: all deb rpm snap clean
all: deb rpm snap

deb:
	@echo "Building DEB package for $(PACKAGE_NAME)..."
	rm -rf deb
	mkdir -p deb/DEBIAN
	mkdir -p deb/usr/local/bin/$(PACKAGE_NAME)
	@echo "Copying files..."
	@for file in $(SOURCE_FILES); do \
		cp -v $$file deb/usr/local/bin/$(PACKAGE_NAME)/; \
	done
	@for dir in $(SOURCE_DIRS); do \
		cp -R $$dir deb/usr/local/bin/$(PACKAGE_NAME)/; \
	done
	@echo "Creating control file..."
	@echo "Package: $(PACKAGE_NAME)" > deb/DEBIAN/control
	@echo "Version: $(VERSION)" >> deb/DEBIAN/control
	@echo "Section: admin" >> deb/DEBIAN/control
	@echo "Priority: optional" >> deb/DEBIAN/control
	@echo "Architecture: $(ARCH)" >> deb/DEBIAN/control
	@echo "Maintainer: Eeshu <eeshuyadav123@gmail.com>" >> deb/DEBIAN/control
	@echo "Description: OpenWISP VPN Deployer Linux Package. Automates deployment and synchronization of VPN servers integrated with OpenWISP." >> deb/DEBIAN/control
	@echo "Building DEB package..."
	dpkg-deb --build deb $(PACKAGE_NAME)_$(VERSION)_$(ARCH).deb
	@echo "DEB package created: $(PACKAGE_NAME)_$(VERSION)_$(ARCH).deb"
	rm -rf deb

rpm:
	@echo "RPM packaging not implemented yet."

snap:
	@echo "Snap packaging not implemented yet."

clean:
	rm -rf deb
	rm -f $(PACKAGE_NAME)_$(VERSION)_$(ARCH).deb
