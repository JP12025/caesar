# Caesar

<img src="https://cs50.harvard.edu/x/2024/psets/2/caesar/cipher.jpg" alt="Caesar Code" width="300">

# What to Do

Supposedly, Julius Caesar used to “encrypt” (i.e., conceal in a reversible way) confidential 
messages by shifting each letter therein by some number of places. For instance, he might 
write A as B, B as C, C as D, …, and, wrapping around alphabetically, Z as A. 

And so, to say `HELLO` to someone, Caesar might write `IFMMP` instead. 
Upon receiving such messages from Caesar, recipients would have to “decrypt” them by shifting 
letters in the opposite direction by the same number of places.

The secrecy of this “cryptosystem” relied on only Caesar and the recipients knowing a secret, 
the number of places by which Caesar had shifted his letters (e.g., 1). Not particularly secure 
by modern standards, but, hey, if you’re perhaps the first in the world to do it, pretty secure!

Unencrypted text is generally called plaintext. Encrypted text is generally called ciphertext. 
And the secret used is called a key.

To be clear, then, here’s how encrypting `HELLO` with a key of `1` yields `IFMMP`:

| **plaintext** | `H` | `E` | `L` | `L` | `O` |
| ------------- | --- | --- | --- | --- | --- |
| index | 7 | 4 | 11 | 11 | 14 |
| + key 1 | 8 | 5 | 12 | 12 | 15 |
| = ciphertext | `I` | `F` | `M` | `M` | `P` |

Caesar’s algorithm (i.e., cipher) encrypts messages by “rotating”
each letter by $k$ positions. More formally, if $p$ is some plaintext (i.e., an unencrypted message), 
$p_i$ is the $i^{th}$ character in $p$, and $k$ is a secret key (i.e., a non-negative integer), 
then each letter $c_i$ in the ciphertext $c$, is computed as

$$ c_i = (p_i+k) \% 26 $$

wherein $\% 26$ here means “remainder when dividing by 26.” 
This formula perhaps makes the cipher seem more complicated than it is, 
but it’s really just a concise way of expressing the algorithm precisely. 
Indeed, for the sake of discussion, think of A (or a) as `0`, B (or b) as `1`, …, 
H (or h) as `7`, I (or i) as `8`, …, and Z (or z) as `25`. 

Suppose that Caesar just wants to say Hi to someone confidentially using, this time, a key of 3. 
And so his plaintext is `HI`, so his ciphertext is `KL`. Make sense?

In a file called `caesar.py`, write a Python program that enables you to encrypt messages using Caesar’s cipher.
At the time the user executes the program, they should decide, by providing a command-line argument,
what the key should be in the secret message they’ll provide at runtime.

First, your program asks `plaintext : ` (notice the space before the colon) and waits for the user's text.
```bash
$ python caesar.py 3
plaintext : 
```
Then, it prints the `ciphertext`, the encrypted version of `plaintext` with the key.
```bash
$ python caesar.py 3
plaintext : Hi
ciphertext: Kl
```

Only letters are shifted, and they keep their case: an uppercase letter stays uppercase, a lowercase letter stays lowercase.
Every other character (spaces, digits, punctuation…) is copied unchanged.

```bash
$ python caesar.py 13
plaintext : Hi there!
ciphertext: Uv gurer!
```

There must be exactly one command-line argument, and it must be a non-negative integer (`0`, `1`, `2`, … `26`, `27`, …).
If not, the program should print `Usage: python caesar.py key` and stop, without asking anything.

```bash
$ python caesar.py
Usage: python caesar.py key
$ python caesar.py HELLO
Usage: python caesar.py key
```

> [!TIP]
> The command-line arguments are stored in the list `sys.argv` (after `import sys`).
> `sys.argv[0]` is the name of the script, so for `python caesar.py 3`, `sys.argv` is `['caesar.py', '3']`.
> Notice that `'3'` is a `str`, not an `int`.
> To stop your program right away, you may use `sys.exit()`.

> [!TIP]
> To find the position of a letter in the alphabet, you may use a string such as `"abcdefghijklmnopqrstuvwxyz"` and its method `index()`.
> The methods `isupper()`, `islower()`, `upper()` and `lower()` will help you keep the case of each letter.
> What happens with the key `27`? And with the letter `z`?

## Bonus

Let your program accept an optional second argument `-r` at the end of the command line that lets you decrypt a message.
If the `-r` flag is present (notice the term *flag*), your program should ask for the `ciphertext` first and print
the `plaintext`.

```bash
$ python caesar.py 13 -r
ciphertext: Uv gurer!
plaintext : Hi there!
```

Any other second argument (e.g. `python caesar.py 13 -x`) prints the usage message.

# How to Test

Test your program from the exercise folder with:

```bash
python test_caesar.py
```

(use `python3` instead of `python` if that is how you run Python on your computer).

The script runs your program as a user would: it gives it a key on the command line, types a message, then checks what your program prints.
When a test fails, it explains what is wrong and shows the first letter that is not correctly encrypted.
The tests of the bonus are shown separately: if you did not do the bonus, you can ignore them.

Don't forget it's important to test your program yourself too.
What happens if :
* there is no key at all?
* there are two or three arguments?
* the key is a word, a negative number or a decimal number?
* the key is `0`? `26`? `27`?
* the message contains a `z` or a `Z`?
* the message contains spaces, digits or punctuation?

```bash
$ python caesar.py 1 2 3
Usage: python caesar.py key
$ python caesar.py 1
plaintext : Ab
ciphertext: Bc
$ python caesar.py 2
plaintext : Ab, cD
ciphertext: Cd, eF
$ python caesar.py 1
plaintext : Zz
ciphertext: Aa
```

# How to Submit

Once you're done with all tasks, submit all your python files on Moodle.

# Licence

This course is freely inspired by [CS50’s Introduction to Computer Science](https://cs50.harvard.edu/x/2025/) Harvard. It is licensed under a [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.
