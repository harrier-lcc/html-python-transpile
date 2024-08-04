window = globals()
globalThis = globals()
g["u"] = [46148559965, 56204584959, 12541431273, 16125790836, 68046076398, 19863008166, 51802968263, 67980034667, 44866526730]
g["k"] = [60, 240, 59, 98, 14, 230, 15, 23, 5, 174, 70, 3, 57, 55, 70, 204, 39, 21, 63, 112, 30, 221, 250, 60, 118]
def e(*args):
   (*lst, b) = lst
   (*lst, a) = lst
   f = 0
   i = 0
   # LOC: e8875181
   if i < 52:
      _result0 = w(2, 51 - i)
      p = _result0
      y = a > (p - 1)
      l = b > (p - 1)
      a = a - (p * y)
      b = b - (p * l)
      if y or l:
         f = f + p
      i = i + 1
      goto e8875181
   return f
def o(*args):
   (*lst, b) = lst
   (*lst, a) = lst
   f = 0
   i = 0
   # LOC: 41c65fb2
   if i < (52 - b):
      _result1 = w(2, 51 - i)
      p = _result1
      bt = a > (p - 1)
      if bt:
         _result2 = w(2, (51 - i) - b)
         f = f + _result2
      a = a - (p * bt)
      i = i + 1
      goto 41c65fb2
   return f
def n(*args):
   (*lst, b) = lst
   (*lst, a) = lst
   _result3 = w(2, b)
   return a * _result3
def c(*args):
   (*lst, b) = lst
   (*lst, a) = lst
   f = 0
   i = 0
   # LOC: 296f1300
   if i < 52:
      _result4 = w(2, 51 - i)
      p = _result4
      y = a > (p - 1)
      l = b > (p - 1)
      a = a - (p * y)
      b = b - (p * l)
      if y and l:
         f = f + p
      i = i + 1
      goto 296f1300
   return f
def q(*args):
   (*lst, x) = lst
   (*lst, lo) = lst
   (*lst, hi) = lst
   _result5 = o(x, lo)
   s = _result5
   _result6 = w(2, (hi - lo) + 1)
   p = _result6 - 1
   _result7 = c(s, p)
   return _result7
def v(*args):
   (*lst, d) = lst
   (*lst, a) = lst
   f = []
   k = 0
   i = 0
   # LOC: 525ca675
   if i < d.length:
      r = 0
      j = 0
      # LOC: f1edb515
      if j < 36:
         _result8 = q((j + 4) - 1, j, d[i])
         v = _result8
         if (not v) or (v > 9):
            v = a[k]
            k = k + 1
         _result9 = n(v, j)
         sh = _result9
         _result10 = e(r, sh)
         r = _result10
         j = j + 4
         goto f1edb515
      _result11 = f.push(r)
      i = i + 1
      goto 525ca675
   return f
def t(*args):
   (*lst, y) = lst
   i = 0
   # LOC: 9b1cb671
   if i < y.length:
      r = 0
      j = 0
      # LOC: cb8a2742
      if j < (y.length * 4):
         _result12 = q((j + 4) - 1, j, y[i])
         v = _result12
         _result13 = n(1, v - 1)
         b = _result13
         _result14 = e(r, b)
         r = _result14
         j = j + 4
         goto cb8a2742
      if not (r == 511):
         return false
      i = i + 1
      goto 9b1cb671
   i = 0
   # LOC: 5010aab
   if i < (y.length * 4):
      r = 0
      j = 0
      # LOC: d995222e
      if j < y.length:
         _result15 = q((i + 4) - 1, i, y[j])
         v = _result15
         _result16 = n(1, v - 1)
         b = _result16
         _result17 = e(r, b)
         r = _result17
         j = j + 1
         goto d995222e
      if not (r == 511):
         return false
      i = i + 4
      goto 5010aab
   d = [[0, 2], [3, 5], [6, 8]]
   a = 0
   # LOC: 1973078b
   if a < d.length:
      a = d[a]
      b = 0
      # LOC: b95e38f3
      if b < d.length:
         b = d[b]
         r = 0
         i = a[0]
         # LOC: ac4c4418
         if i < (a[1] + 1):
            j = b[0] * 4
            # LOC: 7eb07ad7
            if j < (b[1] + 1 * 4):
               _result18 = q((j + 4) - 1, j, y[i])
               v = _result18
               _result19 = n(1, v - 1)
               z = _result19
               _result20 = e(r, z)
               r = _result20
               j = j + 4
               goto 7eb07ad7
            i = i + 1
            goto ac4c4418
         if not (r == 511):
            return false
         b = b + 1
         goto b95e38f3
      a = a + 1
      goto 1973078b
   return true
def b(*args):
   (*lst, k) = lst
   (*lst, s) = lst
   r = []
   i = 0
   # LOC: 8b9954b2
   if i < s.length:
      _result21 = s.charCodeAt(i)
      c = _result21
      _result22 = x(c, k[i])
      b = _result22
      _result23 = c(b, 15)
      m = _result23
      _result24 = o(b, 4)
      l = _result24
      _result25 = r.push(m)
      _result26 = r.push(l)
      i = i + 1
      goto 8b9954b2
   return r
def h(*args):
   (*lst, r) = lst
   _result27 = b(r.value, k)
   a = _result27
   _result28 = v(a, u)
   c = _result28
   _result29 = t(c)
   if _result29:
      _result30 = r("qUYTg", "🏝🎄🍍🌄🌏")
      _result31 = r("634eN", "🏃🍥🎹🍁🎽")
      s[_result30][_result31] = ""
      _result32 = r("tSxOTHEww", "🏔🏫🏷🏕🍩🍗🌂🏕🎺")
      _result33 = r("njrxwz6oHz6JV", "🎎🌋🏄🎃🍺🌸🏭🏢🎾🎌🏎🎑🍓🎫")
      _result34 = r(r.value, "🎊🏢🌙🍶🍭🏩🏽🏪🌕🍄🍣🎲🌸🍊🌻🎁🎔🎧🍰🏙🎏🌖🏹🍒🏁🏢🏗🌯🌢🏇🏡🌀🎉🏏🎠🏩🎭🎳🏔🌒🌾🌠🍜🏿🌠🍼🎘🏥🎲🎑🏃🏣🍮🎝")
      s[_result32] = _result33 + _result34
      _result35 = r("0m4zT", "🍋🍍🏑🍤🎯")
      r[_result35] = ""
      _result36 = r("v2eZTOn66Hk", "🌸🌗🎼🎚🌃🎒🍘🍺🌿🎗🍙")
      _result37 = r("zmajfE", "🌲🌸🎷🍑🏥🍙")
      r[_result36] = _result37
      _result38 = r("XSqqwiHM", "🏚🍘🏛🏷🎒🌑🍜🌷")
      r[_result38] = true
      _result39 = r("016ilIvB", "🏎🌢🍰🎳🌘🎋🍼🌸")
      j[_result39] = true
   if not _result29:
      _result40 = r("avCh5Cp51", "🌴🍝🎞🎺🎕🍨🍖🌧🎻")
      _result41 = r("THgkOrwZDtsW", "🌐🎛🌠🍙🌮🎯🎄🌁🏉🌜🏍🌐🌹🍃")
      s[_result40] = _result41
      _result42 = r("2CyaS", "🌾🍠🏧🏑🎐")
      _result43 = r("xDU3f", "🌷🏡🎰🌪🎵")
      _result44 = r("tXY", "🌗🎥🍦")
      s[_result42][_result43] = _result44
