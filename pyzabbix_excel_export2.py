from pyzabbix import ZabbixAPI
from datetime import datetime
import time
import os
import sys, getopt
import array
#---------------------------------------------------------------------------------------------------------------------
time_from_arg = 0
time_till_arg = 0
tr_value = 0
flag1 = 0
flag = 0
hostgroup = ""
groupids = []
try:
	opts, args = getopt.getopt(sys.argv[1:],"g:v:",["group=", "time_from=", "time_till=", "value="])
	for opt, arg in opts:
		if opt in ("-g" , "--group"):
			flag += 1
			hostgroup = arg
		if opt in ("--time_from"):
			try:
				time_from_arg = int(arg)
			except ValueError:
				print("warning: --time_from must be integer value (seconds)!")
		if opt in ("--time_till"):
			try:
				time_till_arg = int(arg)
			except ValueError:
				print("warning: --time_till must be integer value (seconds)!")
		if opt in ("-v", "--value"):
			try:
				flag1 += 1
				tr_value = arg
			except ValueError:
				print("warning: argument -v (--value) accepted value 0 or 1 (only active triggers)")
except getopt.GetoptError:
	print ('no args')

if time_till_arg > time_from_arg:
	print("warning: time_from must be greater that time_till!")
	time_from_arg = 0
#---------------------------------------------------------------------------------------------------------------------
def getTriggers():
	if flag==0:
		#print("case 1")
		triggers = zapi.trigger.get(output=['triggerid','name','description','priority','lastchange','hostname','value','comments'],selectLastEvent=['value','acknowledged'],selectGroups='extend',sortfield=['priority','hostname'],sortorder='DESC',lastChangeSince=time_from,expandDescription=1,expandComment=1,expandExpression=1,monitored=1)
		if time_till_arg > 0:
			triggers = zapi.trigger.get(output=['triggerid','name','description','priority','lastchange','hostname','value','comments'],selectLastEvent=['value','acknowledged'],selectGroups='extend',sortfield=['priority','hostname'],sortorder='DESC',lastChangeSince=time_from,lastChangeTill=time_till,expandDescription=1,expandComment=1,expandExpression=1,monitored=1)
	elif len(hostgroup) > 0 and len(groupids) > 0 and flag1 == 0:
		#print("case 2")
		triggers = zapi.trigger.get(output=['triggerid','name','description','priority','lastchange','hostname','value','comments'],selectLastEvent=['value','acknowledged'],selectGroups='extend',groupids=groupids,sortfield=['priority','hostname'],sortorder='DESC',lastChangeSince=time_from,expandDescription=1,expandComment=1,expandExpression=1,monitored=1)
		if time_till_arg > 0:
			triggers = zapi.trigger.get(output=['triggerid','name','description','priority','lastchange','hostname','value','comments'],selectLastEvent=['value','acknowledged'],selectGroups='extend',groupids=groupids,sortfield=['priority','hostname'],sortorder='DESC',lastChangeSince=time_from,lastChangeTill=time_till,expandDescription=1,expandComment=1,expandExpression=1,monitored=1)
	elif len(hostgroup) > 0 and len(groupids) > 0 and flag1 > 0:
		#print("case 3")
		triggers = zapi.trigger.get(output=['triggerid','name','description','priority','lastchange','hostname','value','comments'],selectLastEvent=['value','acknowledged'],selectGroups='extend',groupids=groupids,sortfield=['priority','hostname'],sortorder='DESC',lastChangeSince=time_from,filter={"value":tr_value},expandDescription=1,expandComment=1,expandExpression=1,monitored=1)
		if time_till_arg > 0:
			triggers = zapi.trigger.get(output=['triggerid','name','description','priority','lastchange','hostname','value','comments'],selectLastEvent=['value','acknowledged'],selectGroups='extend',groupids=groupids,sortfield=['priority','hostname'],sortorder='DESC',lastChangeSince=time_from,lastChangeTill=time_till,filter={"value":tr_value},expandDescription=1,expandComment=1,expandExpression=1,monitored=1)
	elif len(hostgroup) == 0 and len(groupids) == 0 and flag1 > 0:
		#print("case 4")
		triggers = zapi.trigger.get(output=['triggerid','name','description','priority','lastchange','hostname','value','comments'],selectLastEvent=['value','acknowledged'],selectGroups='extend',sortfield=['priority','hostname'],sortorder='DESC',lastChangeSince=time_from,filter={"value":tr_value},expandDescription=1,expandComment=1,expandExpression=1,monitored=1)
		if time_till_arg > 0:
			triggers = zapi.trigger.get(output=['triggerid','name','description','priority','lastchange','hostname','value','comments'],selectLastEvent=['value','acknowledged'],selectGroups='extend',sortfield=['priority','hostname'],sortorder='DESC',lastChangeSince=time_from,lastChangeTill=time_till,filter={"value":tr_value},expandDescription=1,expandComment=1,expandExpression=1,monitored=1)
	elif len(hostgroup) > 0 and len(groupids) == 0 and flag1 == 0:
		#print("case 5")
		triggers = zapi.trigger.get(output=['triggerid','name','description','priority','lastchange','hostname','value','comments'],selectLastEvent=['value','acknowledged'],selectGroups='extend',group=hostgroup,sortfield=['priority','hostname'],sortorder='DESC',lastChangeSince=time_from,expandDescription=1,expandComment=1,expandExpression=1,monitored=1)
		if time_till_arg > 0:
			triggers = zapi.trigger.get(output=['triggerid','name','description','priority','lastchange','hostname','value','comments'],selectLastEvent=['value','acknowledged'],selectGroups='extend',group=hostgroup,sortfield=['priority','hostname'],sortorder='DESC',lastChangeSince=time_from,lastChangeTill=time_till,expandDescription=1,expandComment=1,expandExpression=1,monitored=1)
	elif len(hostgroup) > 0 and len(groupids) == 0 and flag1 > 0:
		#print("case 6")
		triggers = zapi.trigger.get(output=['triggerid','name','description','priority','lastchange','hostname','value','comments'],selectLastEvent=['value','acknowledged'],selectGroups='extend',group=hostgroup,sortfield=['priority','hostname'],sortorder='DESC',lastChangeSince=time_from,filter={"value":tr_value},expandDescription=1,expandComment=1,expandExpression=1,monitored=1)
		if time_till_arg > 0:
			triggers = zapi.trigger.get(output=['triggerid','name','description','priority','lastchange','hostname','value','comments'],selectLastEvent=['value','acknowledged'],selectGroups='extend',group=hostgroup,sortfield=['priority','hostname'],sortorder='DESC',lastChangeSince=time_from,lastChangeTill=time_till,filter={"value":tr_value},expandDescription=1,expandComment=1,expandExpression=1,monitored=1)
	return triggers
#---------------------------------------------------------------------------------------------------------------------
def checkGroups(hostgroup):
	hostgroup = hostgroup[:-1]
	groups = zapi.hostgroup.get(output='extend')
	groupids = []
	for i in range(len(groups)):
		if hostgroup not in groups[i]['name']:
			continue
		else:
			groupids.append(groups[i]['groupid'])
	return groupids
#---------------------------------------------------------------------------------------------------------------------
zapi = ZabbixAPI("http://46.228.248.22:2639/zabbix/api_jsonrpc.php")
zapi.login("boisteanu.dinu", "BOdi@2018")
print("Connected to Zabbix API Version %s" % zapi.api_version())
time_till = time.mktime(datetime.now().timetuple())
time_from = time_till - 60 * 60 * 2  # 2 hours
#---------------------------------------------------------#
if time_from_arg == 0:                                    #
	time_from = time_till - 60 * 60 * 2                   #  
else:                                                     #
	time_from = time_till - time_from_arg                 #
if time_till_arg > 0:                                     #
	time_till = time_till - time_till_arg                 #
#---------------------------------------------------------#

if "*" in hostgroup:
	groupids = checkGroups(hostgroup)
triggers = getTriggers()
tot = len(triggers)
if tot ==0:
	print("Problem not found")
	exit(0)
tot += 50
str_tot = str(tot)
#-------------------------------------------------------------------------------------------------------
def duration_calc(duration):
	calc_day = int(duration / 60 /60 / 24)
	calc_hour = int((duration / 60 / 60) % 24)
	calc_min = int((duration / 60) % 60)	
	calc_sec = int(duration % 60)		
	calc_result = ""
	if calc_day > 0:
		calc_result = str(calc_day)
		calc_result += "d "
	if calc_hour > 0:
		calc_result += str(calc_hour)
		calc_result += "h "
	if calc_min > 0:
		calc_result += str(calc_min)
		calc_result += "m "
	if calc_sec > 0:
		calc_result += str(calc_sec)
		calc_result += "sec"
	return calc_result
#--------------------------------------------------------------------------------------------------------
def switch_priority(argument):
	if argument == "0":
		return "    <Cell ss:StyleID=\"s90\"><Data ss:Type=\"String\">Not Classified</Data></Cell>\n"	
	if argument == "1":
		return "    <Cell ss:StyleID=\"s84\"><Data ss:Type=\"String\">Info</Data></Cell>\n"	
	if argument == "2":
		return "    <Cell ss:StyleID=\"s77\"><Data ss:Type=\"String\"> Warning</Data></Cell>\n"
	if argument == "3":
		return "    <Cell ss:StyleID=\"s99\"><Data ss:Type=\"String\">Average</Data></Cell>\n"
	if argument == "4":
		return "    <Cell ss:StyleID=\"s89\"><Data ss:Type=\"String\">High</Data></Cell>\n"
	if argument == "5":
		return "    <Cell ss:StyleID=\"s88\"><Data ss:Type=\"String\">Disaster</Data></Cell>\n"
	return "    <Cell ss:StyleID=\"s90\"><Data ss:Type=\"String\">Not Classified</Data></Cell>\n"			
#--------------------------------------------------------------------------------------------------------
buff = ""
i = 0
print("Extract problems from:",datetime.utcfromtimestamp(time_from+(3600*3)).strftime('%Y-%m-%d %H:%M:%S'))

hour = datetime.utcfromtimestamp(time_till+(3600*3)).strftime('%H_%M')
filename = "[" + hour + "] "
filename += datetime.utcfromtimestamp(time_till).strftime('%d_%m_%Y')
filename += ".xls"
# -*- coding: utf_8 -*-
f = open(filename, "w", encoding='utf8')
f.write("<?xml version=\"1.0\"?>\n")
f.write("<?mso-application progid=\"Excel.Sheet\"?>\n")
f.write("<Workbook xmlns=\"urn:schemas-microsoft-com:office:spreadsheet\"\n")
f.write(" xmlns:o=\"urn:schemas-microsoft-com:office:office\"\n")
f.write(" xmlns:x=\"urn:schemas-microsoft-com:office:excel\"\n")
f.write(" xmlns:ss=\"urn:schemas-microsoft-com:office:spreadsheet\"\n")
f.write(" xmlns:html=\"http://www.w3.org/TR/REC-html40\">\n")
f.write(" <DocumentProperties xmlns=\"urn:schemas-microsoft-com:office:office\">\n")
f.write("  <Version>16.00</Version>\n")
f.write(" </DocumentProperties>\n")
f.write(" <OfficeDocumentSettings xmlns=\"urn:schemas-microsoft-com:office:office\">\n")
f.write("  <AllowPNG/>\n")
f.write("  <RemovePersonalInformation/>\n")
f.write(" </OfficeDocumentSettings>\n")
f.write(" <ExcelWorkbook xmlns=\"urn:schemas-microsoft-com:office:excel\">\n")
f.write("  <WindowHeight>12300</WindowHeight>\n")
f.write("  <WindowWidth>29010</WindowWidth>\n")
f.write("  <WindowTopX>0</WindowTopX>\n")
f.write("  <WindowTopY>0</WindowTopY>\n")
f.write("  <ProtectStructure>False</ProtectStructure>\n")
f.write("  <ProtectWindows>False</ProtectWindows>\n")
f.write(" </ExcelWorkbook>\n")
f.write(" <Styles>\n")
f.write("  <Style ss:ID=\"Default\" ss:Name=\"Normal\">\n")
f.write("   <Alignment ss:Vertical=\"Bottom\"/>\n")
f.write("   <Borders/>\n")
f.write("   <Font ss:FontName=\"Calibri\" x:CharSet=\"204\" x:Family=\"Swiss\" ss:Size=\"11\"\n")
f.write("    ss:Color=\"#000000\"/>\n")
f.write("   <Interior/>\n")
f.write("   <NumberFormat/>\n")
f.write("   <Protection/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s62\" ss:Name=\"Гиперссылка\">\n")
f.write("   <Font ss:FontName=\"Calibri\" x:CharSet=\"204\" x:Family=\"Swiss\" ss:Size=\"11\"\n")
f.write("    ss:Color=\"#0066CC\" ss:Underline=\"Single\"/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"m2686135281952\">\n")
f.write("   <Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/>\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("   <Font ss:FontName=\"Calibri\" x:CharSet=\"204\" x:Family=\"Swiss\" ss:Size=\"11\"\n")
f.write("    ss:Color=\"#000000\" ss:Bold=\"1\"/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s70\">\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s71\">\n")
f.write("   <Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Bottom\"/>\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("   <Font ss:FontName=\"Calibri\" x:CharSet=\"204\" x:Family=\"Swiss\" ss:Size=\"11\"\n")
f.write("    ss:Color=\"#FF0000\"/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s72\">\n")
f.write("   <Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Bottom\"/>\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("   <Font ss:FontName=\"Calibri\" x:CharSet=\"204\" x:Family=\"Swiss\" ss:Size=\"11\"\n")
f.write("    ss:Color=\"#FF0000\"/>\n")
f.write("   <Interior ss:Color=\"#FFFF00\" ss:Pattern=\"Solid\"/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s73\">\n")
f.write("   <Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\" ss:WrapText=\"1\"/>\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("   <Interior ss:Color=\"#C6E0B4\" ss:Pattern=\"Solid\"/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s75\" ss:Parent=\"s62\">\n")
f.write("   <Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\" ss:WrapText=\"1\"/>\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("   <Font ss:FontName=\"Calibri\" x:CharSet=\"204\" x:Family=\"Swiss\" ss:Size=\"11\"\n")
f.write("    ss:Color=\"#000000\" ss:Underline=\"Single\"/>\n")
f.write("   <Interior ss:Color=\"#C6E0B4\" ss:Pattern=\"Solid\"/>\n")
f.write("   <NumberFormat ss:Format=\"hh:mm:ss\"/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s76\">\n")
f.write("   <Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\" ss:WrapText=\"1\"/>\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("   <Interior ss:Color=\"#C6E0B4\" ss:Pattern=\"Solid\"/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s77\">\n")
f.write("   <Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\" ss:WrapText=\"1\"/>\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("   <Font ss:FontName=\"Calibri\" x:CharSet=\"204\" x:Family=\"Swiss\" ss:Size=\"11\"\n")
f.write("    ss:Color=\"#000000\" ss:Bold=\"1\"/>\n")
f.write("   <Interior ss:Color=\"#FFE699\" ss:Pattern=\"Solid\"/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s84\">\n")
f.write("   <Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\" ss:WrapText=\"1\"/>\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("   <Font ss:FontName=\"Calibri\" x:CharSet=\"204\" x:Family=\"Swiss\" ss:Size=\"11\"\n")
f.write("    ss:Color=\"#000000\" ss:Bold=\"1\"/>\n")
f.write("   <Interior ss:Color=\"#BDD7EE\" ss:Pattern=\"Solid\"/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s88\">\n")
f.write("   <Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\" ss:WrapText=\"1\"/>\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("   <Font ss:FontName=\"Calibri\" x:CharSet=\"204\" x:Family=\"Swiss\" ss:Size=\"11\"\n")
f.write("    ss:Color=\"#000000\" ss:Bold=\"1\"/>\n")
f.write("   <Interior ss:Color=\"#FF0000\" ss:Pattern=\"Solid\"/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s89\">\n")
f.write("   <Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\" ss:WrapText=\"1\"/>\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("   <Font ss:FontName=\"Calibri\" x:CharSet=\"204\" x:Family=\"Swiss\" ss:Size=\"11\"\n")
f.write("    ss:Color=\"#000000\" ss:Bold=\"1\"/>\n")
f.write("   <Interior ss:Color=\"#C65911\" ss:Pattern=\"Solid\"/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s90\">\n")
f.write("   <Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\" ss:WrapText=\"1\"/>\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("   <Font ss:FontName=\"Calibri\" x:CharSet=\"204\" x:Family=\"Swiss\" ss:Size=\"11\"\n")
f.write("    ss:Color=\"#000000\" ss:Bold=\"1\"/>\n")
f.write("   <Interior ss:Color=\"#E7E6E6\" ss:Pattern=\"Solid\"/>\n")
f.write("  </Style>\n")
f.write("  <Style ss:ID=\"s99\">\n")
f.write("   <Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\" ss:WrapText=\"1\"/>\n")
f.write("   <Borders>\n")
f.write("    <Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("    <Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\"/>\n")
f.write("   </Borders>\n")
f.write("   <Font ss:FontName=\"Calibri\" x:CharSet=\"204\" x:Family=\"Swiss\" ss:Size=\"11\"/>\n")
f.write("   <Interior ss:Color=\"#FFC000\" ss:Pattern=\"Solid\"/>\n")
f.write("  </Style>\n")
f.write(" </Styles>\n")
f.write(" <Worksheet ss:Name=\"Foaie1\">\n")
f.write("  <Table ss:ExpandedColumnCount=\"11\" ss:ExpandedRowCount=\""+ str_tot +"\" x:FullColumns=\"1\"\n")
f.write("   x:FullRows=\"1\" ss:DefaultRowHeight=\"15\">\n")
f.write("   <Column ss:AutoFitWidth=\"0\" ss:Width=\"125\"/>\n")
f.write("   <Column ss:AutoFitWidth=\"0\" ss:Width=\"80\"/>\n")
f.write("   <Column ss:AutoFitWidth=\"0\" ss:Width=\"150\"/>\n")
f.write("   <Column ss:AutoFitWidth=\"0\" ss:Width=\"250\"/>\n")
f.write("   <Column ss:AutoFitWidth=\"0\" ss:Width=\"120\"/>\n")
f.write("   <Column ss:AutoFitWidth=\"0\" ss:Width=\"120\"/>\n")
f.write("   <Column ss:AutoFitWidth=\"0\" ss:Width=\"150\" ss:Span=\"3\"/>\n")
f.write("   <Column ss:Index=\"11\" ss:AutoFitWidth=\"0\" ss:Width=\"129\"/>\n")
f.write("   <Row ss:AutoFitHeight=\"0\" ss:Height=\"57.75\">\n")
f.write("    <Cell ss:MergeAcross=\"7\" ss:StyleID=\"m2686135281952\"><Data ss:Type=\"String\">Zabbix Monitoring Problems</Data></Cell>\n")
f.write("   </Row>\n")
f.write("   <Row ss:AutoFitHeight=\"0\" ss:Height=\"15.75\" >\n")
f.write("    <Cell ss:StyleID=\"s71\"><Data ss:Type=\"String\">HOST</Data></Cell>\n")
f.write("    <Cell ss:StyleID=\"s71\"><Data ss:Type=\"String\">IP</Data></Cell>\n")
f.write("    <Cell ss:StyleID=\"s71\"><Data ss:Type=\"String\">Problem</Data></Cell>\n")
f.write("    <Cell ss:StyleID=\"s71\"><Data ss:Type=\"String\">Description</Data></Cell>\n")
f.write("    <Cell ss:StyleID=\"s71\"><Data ss:Type=\"String\">Start time</Data></Cell>\n")
f.write("    <Cell ss:StyleID=\"s71\"><Data ss:Type=\"String\">Age</Data></Cell>\n")
f.write("    <Cell ss:StyleID=\"s71\"><Data ss:Type=\"String\">Tag</Data></Cell>\n")
f.write("    <Cell ss:StyleID=\"s72\"><Data ss:Type=\"String\">Severity</Data></Cell>\n")
f.write("   </Row>\n")
#--<---<---header---------

while i < len(triggers):
	alerts = zapi.alert.get(output='extend',eventids=[triggers[i]['lastEvent']['eventid']])
	hosts = zapi.host.get(output=['hostid','name'],selectInterfaces=['ip','port'],filter={"name":triggers[i]['hostname']})
	events = zapi.event.get(output='extend',eventids=triggers[i]['lastEvent']['eventid'],selectTags='extend')
	if not events[0]['tags']:
		buff = ""
	else:
		buff = events[0]['tags'][0]['tag'] + ": " + events[0]['tags'][0]['value']
	#----WRITE DATA IN FILE---------------------------------------------------------------------------------------------------------------------------------------------->
	f.write("   <Row ss:AutoFitHeight=\"0\" ss:Height=\"121.5\">\n")
	f.write("    <Cell ss:StyleID=\"s76\"><Data ss:Type=\"String\"> "+ triggers[i]['hostname'] +"</Data></Cell>\n")
	f.write("    <Cell ss:StyleID=\"s76\"><Data ss:Type=\"String\">" + hosts[0]['interfaces'][0]['ip'] + " </Data></Cell>\n")
	f.write("    <Cell ss:StyleID=\"s76\"><Data ss:Type=\"String\">"+ triggers[i]['description'] +"</Data></Cell>\n")
	f.write("    <Cell ss:StyleID=\"s76\"><Data ss:Type=\"String\">"+ triggers[i]['comments'] + "</Data></Cell>\n")
	f.write("    <Cell ss:StyleID=\"s76\"><Data ss:Type=\"String\">"+ datetime.utcfromtimestamp(int(triggers[i]['lastchange'])).strftime('%Y-%m-%d %H:%M:%S') +"</Data></Cell>\n")
	f.write("    <Cell ss:StyleID=\"s76\"><Data ss:Type=\"String\">"+ duration_calc((int(time_till) - int(triggers[i]['lastchange']))) +"</Data></Cell>\n")
	f.write("    <Cell ss:StyleID=\"s76\"><Data ss:Type=\"String\">"+ buff +"</Data></Cell>\n")
	f.write(switch_priority(triggers[i]['priority']))
	f.write("   </Row>\n")
	#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
	i += 1

f.write("  </Table>\n")
f.write("  <WorksheetOptions xmlns=\"urn:schemas-microsoft-com:office:excel\">\n")
f.write("   <PageSetup>\n")
f.write("    <Header x:Margin=\"0.3\"/>\n")
f.write("    <Footer x:Margin=\"0.3\"/>\n")
f.write("    <PageMargins x:Bottom=\"0.75\" x:Left=\"0.7\" x:Right=\"0.7\" x:Top=\"0.75\"/>\n")
f.write("   </PageSetup>\n")
f.write("   <Unsynced/>\n")
f.write("   <Print>\n")
f.write("    <ValidPrinterInfo/>\n")
f.write("    <PaperSizeIndex>9</PaperSizeIndex>\n")
f.write("    <HorizontalResolution>600</HorizontalResolution>\n")
f.write("    <VerticalResolution>600</VerticalResolution>\n")
f.write("   </Print>\n")
f.write("   <Selected/>\n")
f.write("   <TopRowVisible>3</TopRowVisible>\n")
f.write("   <LeftColumnVisible>2</LeftColumnVisible>\n")
f.write("   <Panes>\n")
f.write("    <Pane>\n")
f.write("     <Number>3</Number>\n")
f.write("     <ActiveRow>3</ActiveRow>\n")
f.write("     <ActiveCol>1</ActiveCol>\n")
f.write("    </Pane>\n")
f.write("   </Panes>\n")
f.write("   <ProtectObjects>False</ProtectObjects>\n")
f.write("   <ProtectScenarios>False</ProtectScenarios>\n")
f.write("  </WorksheetOptions>\n")
f.write(" </Worksheet>\n")
f.write(" <x:ExcelWorkbook>  </x:ExcelWorkbook>\n")
f.write("</Workbook>\n")
f.close()
print("SUCCESS")
