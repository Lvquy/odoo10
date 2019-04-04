# -*- coding: utf-8 -*-
#
# import re
# def ktpass(mk):
#     check = True
#     for i in mk:
#         if not re.search("[0-9]", mk):
#             check = False
#         if not re.search("[a-z]",mk):
#             check = False
#         if not re.search("[A-Z]",mk):
#             check = False
#         if not re.search("[$#@]", mk):
#             check = False
#         if len(mk) > 20 or len(mk) < 6:
#             check = False
#     if check == True:
#         return True
#     else:
#         return False
# while True:
#     t = raw_input('nhap passs: ')
#     if ktpass(t) is True:
#         break
# -------------------------------------------------------------------------------

# freq = {} # frequency of words in text
# line = raw_input('nhap: ')
# for word in line.split():
#  freq[word] = freq.get(word,0)+1
# # Bài tập Python 25 Code by Quantrimang.com
# words = sorted(freq.keys())
#
# for w in words:
#     print ("%s:%d" % (w,freq[w]))

# ------------------------------------------------------------------------
def chan(a):
    if int(a)%2==0:
        return True
    else:return False
t =raw_input('nhap chuoi: ')
t =t.split(',')
print (','.join(filter((chan),t)))
