# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:daly

v1 = '/user/del/(\\d+)/'#正则

current_url ="/user/del/1/"

import re

result = re.match(v1,current_url)
print(result)
#打印结果  <_sre.SRE_Match object; span=(0, 12), match='/user/del/1/'>
#匹配失败  None
