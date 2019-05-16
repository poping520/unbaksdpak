# -*- coding: utf-8 -*-
# @Function : 解包 小米手机助手 备份 微信等程序内部存储数据 生成的文件(.baksd_pak)
# @Time     : 2019/2/18
# @Author   : poping520
# @File     : unbaksdpak.py

import base64
import os
import sys


def is_python3():
    return sys.version_info.major == 3


def to_str(bytes):
    if is_python3():
        return str(bytes, encoding="utf-8")
    else:
        # 对于 python2 bytes 即为 str
        return bytes.decode("utf-8").encode("gbk")


def mk_parent_dir_if_not_exists(fpath):
    parentdir = os.path.dirname(fpath)

    if not os.path.exists(parentdir):
        os.makedirs(parentdir)


def unpack_one_file(outdir, infile):
    # 构成 "urlsafe_b64encode(name) filesize\n"
    headers = to_str(infile.readline()).split(" ")

    # 文件相对于手机 sdcard 的路径
    name = to_str(base64.urlsafe_b64decode(headers[0]))

    # 文件大小
    fsize = int(headers[1])
    print("get file: %s; size: %dB" % (name, fsize))

    # windows 文件系统
    if outdir.index("\\") > -1 or outdir.index(":") > -1:
        name = name.replace("/", "\\")
        if not outdir.endswith("\\"):
            outdir = outdir + "\\"
    else:
        if not outdir.endswith("/"):
            outdir = outdir + "/"

    # 文件输出全路径
    fname = outdir + name
    mk_parent_dir_if_not_exists(fname)

    outfile = open(fname, "wb")
    outfile.write(infile.read(fsize))
    outfile.flush()
    outfile.close()


def main(argv):
    infilepath = os.path.abspath(argv[1])
    outdir = os.path.abspath(argv[2])

    print("start unpack: " + infilepath)
    infile = open(infilepath, "rb")
    infilesize = os.path.getsize(infilepath)

    try:
        while True:
            if infilesize == infile.tell():
                print("finish")
                break

            unpack_one_file(outdir, infile)

    except Exception:
        print("This file format is corrupted and cannot continue unpacking")
    finally:
        infile.close()


if __name__ == '__main__':
    if sys.argv is None or len(sys.argv) < 2:
        print("usage: python unbaksdpak.py [*.baksd_pak file] [out dir]")
    else:
        main(sys.argv)
