# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 10:18:58 2021

@author: aitsa
"""

import pyspark
sc = pyspark.SparkContext('local[*]')

#txt = sc.textFile('file:////usr/share/doc/python/copyright')
txt = sc.textFile('debug')

print(txt.count())

python_lines = txt.filter(lambda line: 'python' in line.lower())
print(python_lines.count())


