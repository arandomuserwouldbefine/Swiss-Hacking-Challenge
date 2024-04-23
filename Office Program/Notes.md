**Category: Pwn**

# Description
![[Pasted image 20240423200657.png]]

We are given the binary only, let's fire up ghidra to begin analyzing the binary.

![[Pasted image 20240423200754.png]]
So, first of all it just prints a simple menu and stores the choice in the `choice` variable with the type of `int`. If the value is less than 0 then the if condition convert negative `choice` to positive one. Later, it increments choice by 5. The bug here is, we can overflow the integer, but since it's incrementing `choice` by 5, we cannot directly provide an overflowed value like `2147483648`. If we straight off provide that value, it will be overflowed and converted to negative and then the `if` condition converts *negative* to *positive* `choice`, so in order to print the flag, we need to *decrement* the choice value by 5 before it gets *overflow*. The value we will be sending is `2147483643`.
![[Pasted image 20240423201524.png]]

`Flag: shc2024{monica_please_send_me_the_tax_statement_by_tomorrow}`
