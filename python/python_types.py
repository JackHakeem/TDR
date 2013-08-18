loadfile(lua_dir .. "lib/hotdata/syntactic_node.lua")()

function print_val(val)
	if val.type == E_SNVT_IDENTIFIER then
		io.write(val.val.identifier)
	elseif val.type == E_SNVT_CHAR then
		io.write("'")
		if(val.val.c == '\n')then
			io.write('\\n')
		else
			io.write(val.val.c)
		end
		io.write("'")
	elseif val.type == E_SNVT_DOUBLE then
		io.write(val.val.d)
	elseif val.type == E_SNVT_BOOL then
		io.write(val.val.b)
	elseif val.type == E_SNVT_STRING then
		--需要处理字符串中的转义
		io.write('"')
		io.write(val.val.str)
		io.write('"')
	elseif val.type == E_SNVT_INT64 then
		io.write(val.val.i64)
	elseif val.type == E_SNVT_UINT64 then
		io.write(val.val.ui64)
	elseif val.type == E_SNVT_HEX_INT64 then
		io.write(val.val.hex_i64)
	elseif val.type == E_SNVT_HEX_UINT64 then
		io.write(val.val.hex_ui64)
	end
end

function on_const(const)
	io.write(const.identifier)
	io.write(' = ')
	print_val(const.val)
	io.write('\n')
end

function on_enum(enum)
	for key, value in pairs(enum.enum_def_list) do
		io.write(value.identifier .. ' = ')
		print_val(value.val)
		io.write('\n')
	end
end

function main(document)
	if(ifiles ~= nil) then
		for k, v in pairs(ifiles) do
			print_line(0, 'loadfile("' .. v .. '")()')
		end
	end

	for key, value in pairs(document['definition_list']) do
		if(value.type == E_DT_CONST)then
			on_const(value.definition.de_const)
		elseif(value.type == E_DT_ENUM)then
			on_enum(value.definition.de_enum)
		end
	end
end

main(document)

