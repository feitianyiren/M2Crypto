#!/usr/bin/env python

"""DH demonstration.

Copyright (c) 1999 Ng Pheng Siong. All rights reserved."""

RCS_id='$Id: dhtest.py,v 1.1 1999/09/12 14:44:08 ngps Exp $'

from M2Crypto import DH

def test():
	print 'generating dh params:'
	a=DH.gen_params(128,2)
	b=DH.DH()
	b.set_params(a.p, a.g)
	a.gen_key()
	b.gen_key()
	print 'p = ', `a.p`
	print 'g = ', `a.g`
	print 'a.pub =', `a.pub`
	print 'a.priv =', `a.priv`
	print 'b.pub =', `b.pub`
	print 'b.priv =', `b.priv`
	print 'a.key = ', `a.compute_key(b.pub)`
	print 'b.key = ', `b.compute_key(a.pub)`

if __name__=='__main__':
	test()