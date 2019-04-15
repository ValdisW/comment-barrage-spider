#!/usr/bin/env python 
# -*- coding:utf-8 -*-


a=[1,2,3]
b=[4,5,6]
l = list(zip(a,b))
c,d = list(zip(*l))
print(list(zip(*l)))