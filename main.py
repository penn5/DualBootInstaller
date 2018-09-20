#!/usr/bin/env python3

#Copyright 2018 Penn Mackintosh
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
print('This script expects to find a file "rom.zip" in the cwd')
print('This file requires the following modules from pypi')
print('brotlipy')
import brotli
print('zipfile')
import zipfile



#uncompress zip
with zipfile.ZipFile('rom.zip', 'r') as zip:
    zip.extractall('rom')
if os.path.isfile('rom/system.new.dat.br'):
#    data=open('rom/system.new.dat.br', 'rb').read()
#    data = brotli.decompress(data)
    d = brotli.Decompressor()
    f=open('rom/system.new.dat.br', 'rb')
    f2=open('rom/system.new.dat', 'wb')
    dat=f.read(128) #128mb
    while len(dat):
        f2.write(d.decompress(dat))
        dat=f.read(128)
    d.finish()
#    print(data)
#    with open('rom/system.new.dat', 'wb') as f:
#        f.write(data)

print('decompressed brotli')

import sdat2img
sdat2img.main('rom/system.transfer.list', 'rom/system.new.dat', './system.img')


print('sdat2img complete')

input('Reboot the device into TWRP and connect USB, then press enter')

from adb import adb_commands as adb

device = adb.AdbCommands()
device.ConnectDevice()
device.Push('./system.img', '/sdcard/system.img')
print('DO NOT DISCONNECT OR REBOOT PHONE')

print(device.Shell('rm -rf /mnt/{0};mkdir /mnt/{0};mount -o loop -t auto /sdcard/system.img /mnt/{0};rm -rf /system/{0};mkdir /system/{0};cp -af /mnt/{0} /system/{0}'.format(input('Please type either a or b and press enter'))))

print('if the above was succesful or blank, it worked!')
