# -*- coding: utf-8 -*-

mangso = [u'không',u'một',u'hai',u'ba',u'bốn',u'năm',u'sáu',u'bảy',u'tám',u'chín']
def dochangchuc(so,  daydu):
	chuoi = ""
	chuc = so/10;
	donvi = so%10;
	if (chuc>1):
		chuoi = " " + mangso[chuc] + u" mươi"
		if (donvi==1):
			chuoi += u" mốt"
	elif (chuc==1):
		chuoi = u" mười";
		if (donvi==1):
			chuoi += u" một";
	elif (daydu and donvi>0):
		chuoi = u" lẻ"
	
	if (donvi==5 and chuc>1):
		chuoi += u" lăm"
	elif (donvi>1 or (donvi==1 and chuc==0)):
		chuoi += " " + mangso[donvi]		
	return chuoi

def docblock(so, daydu):
	chuoi = ""
	tram = so/100;
	so = so%100;
	if (daydu  or  tram>0):
		chuoi = " " + mangso[tram] + u" trăm"
		chuoi += dochangchuc(so,True)
	else:
		chuoi = dochangchuc(so,False)
	return chuoi

def dochangtrieu(so, daydu):
	chuoi = ""
	trieu = so/1000000
	so = so%1000000
	if (trieu>0):
		chuoi = docblock(trieu,daydu) + u" triệu"
		daydu = True
	nghin = so/1000
	so = so%1000
	if (nghin>0):
		chuoi += docblock(nghin,daydu) + u" nghìn"
		daydu = True
	if (so>0):
		chuoi += docblock(so,daydu)
	return chuoi

def docso(so):
	if (so==0):
		return mangso[0]
	chuoi = ""
	hauto = ""
	ty=0
	while so>0:
		ty = so%1000000000
		so = so/1000000000
		if so>0:
			chuoi = dochangtrieu(ty,True) + hauto + chuoi
		else:
			chuoi = dochangtrieu(ty,False) + hauto + chuoi
		hauto = u" tỷ"
	if chuoi[0]== ' ':
		chuoi = chuoi[1:]
	chuoi = chuoi.capitalize()

	return chuoi + u' đồng'
