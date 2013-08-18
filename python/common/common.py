from hotpot.hotpot.hp_config import *
from hotpot.hotdata.syntactic_node import *
import sys

enum_list = {}
def get_symbol_access_by_type_suffix(identifier, type):
	if(type.type == E_SNT_CONTAINER):
		if(type.ct == E_CT_VECTOR):
			return '[i]'
	return ''

def get_symbol_access_by_type_prefix(identifier, type, args):
	if(type.type == E_SNT_SIMPLE):
		return ''
	elif(type.type == E_SNT_CONTAINER):
		if(type.ct == E_CT_VECTOR):
			if(args.arg_list[0].type == E_SNT_SIMPLE):
				return ''
			else:
				return '&'
		elif(type.ct == E_CT_STRING):
			return ''
	elif(type.type == E_SNT_REFER):
		if(enum_list[type.ot] == nil):
			return '&'
		else:
			return ''
	return ''

def get_symbol_access_by_type_prefix_reverse(identifier, type, args):
	if(type.type == E_SNT_SIMPLE):
		return ''
	elif(type.type == E_SNT_CONTAINER):
		if(type.ct == E_CT_VECTOR):
			if(args['arg_list'][0]['type'] == E_SNT_SIMPLE):
				return ''
			else:
				return '*'
		elif(type.ct == E_CT_STRING):
			return ''
	elif(type.type == E_SNT_REFER):
		if(enum_list[type.ot] == nil):
			return '*'
		else:
			return ''
	return ''

def get_symbol_access(identifier, object):
	for v in object.parameters.par_list:
		if(v.identifier == identifier):
			prefix = get_symbol_access_by_type_prefix(identifier, v.type, v.args)
			suffix = get_symbol_access_by_type_suffix(identifier, v.type, v.args)
			return prefix + identifier + suffix

	for v in object.field_list.field_list:
		if(v.identifier == identifier):
			prefix = get_symbol_access_by_type_prefix(identifier, v.type, v.args)
			suffix = get_symbol_access_by_type_suffix(identifier, v.type, v.args)
			return prefix + 'data->' + identifier + suffix
	return identifier

def print_line(n, str):
	for i in range(0,n):
		sys.stdout.write('    ')
	print(str)

def get_val(val, object):
	if val['type'] == E_SNVT_IDENTIFIER :
		return get_symbol_access(val['val']['identifier'], object)
	elif val['type'] == E_SNVT_CHAR:
		return val['val']['c']
	elif val['type'] == E_SNVT_DOUBLE:
		return val['val']['d']
	elif val['type'] == E_SNVT_BOOL:
		return val['val']['b']
	elif val['type'] == E_SNVT_STRING:
		return val['val']['str']
	elif val['type'] == E_SNVT_INT64:
		return val['val']['i64']
	elif val['type'] == E_SNVT_UINT64:
		return val['val']['ui64']
	elif val['type'] == E_SNVT_HEX_INT64:
		return val['val']['hex_i64']
	elif val['type'] == E_SNVT_HEX_UINT64:
		return val['val']['hex_ui64']

def get_type(type, args):
	if(type['type'] == E_SNT_SIMPLE):
		if(type['st'] == E_ST_CHAR):
			return 'hpchar'
		elif(type['st'] == E_ST_DOUBLE):
			return 'hpdouble'
		elif(type['st'] == E_ST_BOOL):
			return 'hpbool'
		elif(type['st'] == E_ST_INT8):
			return 'hpint8'
		elif(type['st'] == E_ST_INT16):
			return 'hpint16'
		elif(type['st'] == E_ST_INT32):
			return 'hpint32'
		elif(type['st'] == E_ST_INT64):
			return 'hpint64'
		elif(type['st'] == E_ST_UINT8):
			return 'hpuint8'
		elif(type['st'] == E_ST_UINT16):
			return 'hpuint16'
		elif(type['st'] == E_ST_UINT32):
			return 'hpuint32'
		elif(type['st'] == E_ST_UINT64):
			return 'hpuint64'
	elif(type['type'] == E_SNT_CONTAINER):
		if(type['ct'] == E_CT_VECTOR):
			return args['arg_list'][0]['ot']
		elif(type['ct'] == E_CT_STRING):
			return 'hpchar'
	elif(type['type'] == E_SNT_REFER):
		return type['ot'];

def print_file_prefix():
	print_line(0, '/**')
	print_line(0, ' * Autogenerated by HotData (' + HOTPOT_VERSION + ')')
	print_line(0, ' *')
	print_line(0, ' * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING')
	print_line(0, ' *  @generated')
	print_line(0, ' */')
	print_line(0, '')
