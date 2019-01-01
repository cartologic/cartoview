#!/usr/bin/env bash
# cleanup image
rm -rf ~/.cache/pip
rm -rf /root/.cache
apt-get purge --auto-remove -y gcc libgdal-dev libsasl2-dev \
	zlib1g-dev python-dev build-essential
apt autoremove --purge -y && apt autoclean -y && apt-get clean -y
rm -rf /var/lib/apt/lists/* && apt-get clean -y &&
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
echo "Yes, do as I say!" | apt-get remove --force-yes login &&
	dpkg --remove --force-depends wget
