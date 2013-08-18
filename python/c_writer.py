loadfile(lua_dir .. "lib/hotdata/syntactic_node.lua")();
loadfile(lua_dir .. "lib/common.lua")();

function on_enum_name(enum)
	print_line(0, 'HP_ERROR_CODE write_' .. enum.name .. '_name(HPAbstractWriter *self, const ' .. enum.name .. ' data)')
	print_line(0, '{')
	print_line(1, 'switch(data)')
	print_line(1, '{')
	for key, value in pairs(enum.enum_def_list) do
		print_line(2, 'case ' .. value.identifier .. ':')
		print_line(3, 'if(write_enum_name(self, "' ..  value.identifier .. '") != E_HP_NOERROR) goto ERROR_RET;')
		print_line(3, 'break;')
	end
	print_line(1, '}')
	print_line(0, 'return E_HP_NOERROR;')
	print_line(0, 'ERROR_RET:')
	print_line(1, 'return E_HP_ERROR;')
	print_line(0, '}')
end

function on_enum_number(enum)
	print_line(0, 'HP_ERROR_CODE write_' .. enum.name .. '_number(HPAbstractWriter *self, const ' .. enum.name .. ' data)')
	print_line(0, '{')
	print_line(1, 'return write_enum_number(self, data);')
	print_line(0, '}')
end


function on_enum(enum)
	
	on_enum_name(enum)
	on_enum_number(enum)

	print_line(0, 'HP_ERROR_CODE write_' .. enum.name .. '(HPAbstractWriter *self, const ' .. enum.name .. ' data)')
	print_line(0, '{')
	print_line(1, 'if(write_' .. enum.name .. '_name(self, data) != E_HP_NOERROR) goto ERROR_RET;')
	print_line(1, 'if(write_' .. enum.name .. '_number(self, data) != E_HP_NOERROR) goto ERROR_RET;')
	print_line(1, 'return E_HP_NOERROR;')
	print_line(0, 'ERROR_RET:')
	print_line(1, 'return E_HP_ERROR;')
	print_line(0, '}')

	enum_list[enum.name] = true
end


function on_struct(object)
	t = 0;
	line = 'HP_ERROR_CODE write_' .. object.name .. '(HPAbstractWriter *self, const ' .. object.name .. ' *data'
	for key, value in pairs(object.parameters.par_list) do
		line = line .. ' , '
		line = line .. get_type(value.type, nil)
		line = line .. ' const ' .. get_symbol_access_by_type_prefix_reverse(value.identifier, value.type) .. value.identifier
	end
	line = line .. ')'
	print_line(t, line)
	print_line(t, '{')
	t = t + 1
	print_line(t, 'if(write_struct_begin(self, "' .. object.name .. '") != E_HP_NOERROR) goto ERROR_RET;')
	for key, value in pairs(object.field_list.field_list) do
		if(value.condition.empty == false)then			
			if(value.condition.exp.oper == E_EO_AND)then
				oper = '&'
			elseif(value.condition.exp.oper == E_EO_EQUAL)then
				oper = '=='
			end
			if(value.condition.exp.neg)then
				print_line(t, 'if (!(' .. get_val(value.condition.exp.op0, object) .. ' ' .. oper .. ' '.. get_val(value.condition.exp.op1, object) .. '))')
			else
				print_line(t, 'if (' .. get_val(value.condition.exp.op0, object) .. ' ' .. oper .. ' ' .. get_val(value.condition.exp.op1, object) .. ')')
			end
			print_line(t, '{')
			t = t + 1
		end

		if(value.type.type == E_SNT_CONTAINER)then
			if(value.type.ct == E_CT_VECTOR)then
				print_line(t, 'if(write_counter(self, "' .. value.args.arg_list[3].ot .. '", data->' .. value.args.arg_list[3].ot .. ') != E_HP_NOERROR) goto ERROR_RET;');
				print_line(t, 'if(write_field_begin(self, "' .. value.identifier .. '") != E_HP_NOERROR) goto ERROR_RET;')
				print_line(t, '{')
				t = t + 1
				print_line(t, 'hpuint32 i;')
				print_line(t, 'if(write_vector_begin(self) != E_HP_NOERROR) goto ERROR_RET;')
				print_line(t, 'for(i = 0; i < data->' .. value.args.arg_list[3].ot .. '; ++i)')
				print_line(t, '{')
				t = t + 1
				print_line(t, 'if(write_vector_item_begin(self, i) != E_HP_NOERROR) goto ERROR_RET;')
				line = 'if(write_'
				line = line .. get_type(value.type, value.args)
				line = line .. '(self, ' .. get_symbol_access(value.identifier, object)
				for i=4, #value.args.arg_list do
					line = line .. ', ' .. get_symbol_access(value.args.arg_list[i].ot, object)
				end
				line = line .. ') != E_HP_NOERROR) goto ERROR_RET;'
				print_line(t, line)
				print_line(t, 'if(write_vector_item_end(self, i) != E_HP_NOERROR) goto ERROR_RET;')
				t = t - 1
				print_line(t, '}')
				print_line(t, 'if(write_vector_end(self) != E_HP_NOERROR) goto ERROR_RET;')
				t = t - 1
				print_line(t, '}')
				print_line(t, 'if(write_field_end(self, "' .. value.identifier .. '") != E_HP_NOERROR) goto ERROR_RET;')
			elseif(value.type.ct == E_CT_STRING)then
				print_line(t, 'if(write_field_begin(self, "' .. value.identifier .. '") != E_HP_NOERROR) goto ERROR_RET;')
				print_line(t, 'if(write_string(self, data->' .. value.identifier .. ') != E_HP_NOERROR) goto ERROR_RET;')
				print_line(t, 'if(write_field_end(self, "' .. value.identifier .. '") != E_HP_NOERROR) goto ERROR_RET;')
			end
		else
			print_line(t, 'if(write_field_begin(self, "' .. value.identifier .. '") != E_HP_NOERROR) goto ERROR_RET;')
			line = 'if(write_' .. get_type(value.type, value.args) .. '(self, ' .. get_symbol_access(value.identifier, object)
				for ak, av in pairs(value.args.arg_list) do
					line = line .. ', ' .. get_symbol_access(av.ot, object)
				end
			line = line .. ') != E_HP_NOERROR) goto ERROR_RET;'
			print_line(t, line)
			print_line(t, 'if(write_field_end(self, "' .. value.identifier .. '") != E_HP_NOERROR) goto ERROR_RET;')
		end

		if(value.condition.empty == false)then
			t = t - 1
			print_line(t, '}')
		end
	end
	print_line(t, 'if(write_struct_end(self, "' .. object.name .. '") != E_HP_NOERROR) goto ERROR_RET;')
	print_line(1, 'return E_HP_NOERROR;')
	print_line(0, 'ERROR_RET:')
	print_line(1, 'return E_HP_ERROR;')
	t = t - 1
	print_line(t, '}')
end


function on_union(object)
	t = 0;
	line = 'HP_ERROR_CODE write_' .. object.name .. '(HPAbstractWriter *self, const ' .. object.name .. ' *data'
	for key, value in pairs(object.parameters.par_list) do
		line = line .. ' , '
		line = line .. 'const ' .. get_type(value.type, nil)
		line = line .. ' ' .. get_symbol_access_by_type_prefix_reverse(value.identifier, value.type) .. value.identifier
	end
	line = line .. ')'
	print_line(t, line)
	print_line(t, '{')
	t = t + 1
	print_line(t, 'if(write_struct_begin(self, "' .. object.name .. '") != E_HP_NOERROR) goto ERROR_RET;')

	sw = 's'
	for key, value in pairs(object.ta.ta_list) do
		if(value.type == E_TA_SWITCH)then
			sw = value.val.val.identifier
		end
	end

	print_line(t, 'switch(' .. get_symbol_access(sw, object) .. ')')
	print_line(t, '{')
	t = t + 1
	for key, value in pairs(object.field_list.field_list) do
		print_line(t, 'case ' .. get_val(value.condition.exp.op1, object) .. ':')
		print_line(t, '{')
		t = t + 1
		print_line(t, 'if(write_field_begin(self, "' .. value.identifier .. '") != E_HP_NOERROR) goto ERROR_RET;')
		if(value.type.type == E_SNT_CONTAINER)then
			if(value.type.ct == E_CT_VECTOR)then
				print_line(t, 'hpuint32 i;')
				print_line(t, 'for(i = 0; i < data->' .. value.args.arg_list[3].ot .. '; ++i)')
				print_line(t, '{')
				t = t + 1
				line = 'if(write_' .. get_type(value.type, value.args) .. '(self, ' .. get_symbol_access(value.identifier, object)
				for ak, av in pairs(value.args.arg_list) do
					line = line .. ', ' .. get_symbol_access(av.ot, object)
				end
				line = line .. ') != E_HP_NOERROR) goto ERROR_RET;'
				print_line(t, line)
				t = t - 1
				print_line(t, '}')
			elseif(value.type.ct == E_CT_STRING)then
				print_line(t, 'if(write_string(self, data->' .. value.identifier .. ') != E_HP_NOERROR) goto ERROR_RET;')
			end
		else
			line = 'if(write_'
			line = line .. get_type(value.type, nil)
			line = line .. '(self, ' .. get_symbol_access(value.identifier, object)
			for ak, av in pairs(value.args.arg_list) do
				line = line .. ', ' .. get_symbol_access(av.ot, object) 
			end

			line = line .. ') != E_HP_NOERROR) goto ERROR_RET;'
			print_line(t, line)
		end
		print_line(t, 'if(write_field_end(self, "' .. value.identifier .. '") != E_HP_NOERROR) goto ERROR_RET;')
		print_line(t, 'break;')
		t = t - 1
		print_line(t, '}')
	end
	t = t - 1
	print_line(t, '}')
	print_line(t, 'if(write_struct_end(self, "' .. object.name .. '") != E_HP_NOERROR) goto ERROR_RET;')
	print_line(1, 'return E_HP_NOERROR;')
	print_line(0, 'ERROR_RET:')
	print_line(1, 'return E_HP_ERROR;')
	t = t - 1
	print_line(t, '}')
end
function main(document)
	print_file_prefix()
	print_line(0, '#include "hotpot/hp_platform.h"')
	print_line(0, '#include "hotprotocol/hp_abstract_writer.h"')

	if(ifiles ~= nil) then
		for k, v in pairs(ifiles) do
			print_line(0, '#include "' .. v .. '"')
		end
	end

	for key, value in pairs(document['definition_list']) do
		if(value.type == E_DT_ENUM)then
			on_enum(value.definition.de_enum)
		elseif(value.type == E_DT_STRUCT)then
			on_struct(value.definition.de_struct)
		elseif(value.type == E_DT_UNION)then
			on_union(value.definition.de_union)
		end
	end
end

main(document)
