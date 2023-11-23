data = 'data:,{"p":"asc-20","op":"mint","tick":"aval","amt":"100000000"}'
utf8_bytes = data.encode('utf-8')
hex_str = utf8_bytes.hex()
print("0x"+hex_str)