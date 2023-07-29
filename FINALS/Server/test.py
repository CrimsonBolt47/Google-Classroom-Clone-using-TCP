import lc4
key="ptjy6wqmoc2#favx_n7gui8l9zbh3e4rds5k"
text="hello_how_are_you"
nonce="23nwzh"
m=lc4.encrypt(key, text, nonce=nonce)
print(m)
