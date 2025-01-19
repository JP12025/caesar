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

More formally, Caesar’s algorithm (i.e., cipher) encrypts messages by “rotating” 
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

In a file called `caesar`, write a python program that enables you to encrypt messages using Caesar’s cipher. 
At the time the user executes the program, they should decide, by providing a command-line argument, 
what the key should be in the secret message they’ll provide at runtime.

First, your program prompts the message `plaintext : ` and waits for the user's text.
```bash
$ ./caesar 3
plaintext : 
```
Then, it should answer a `ciphertext`, the encrypted version of `plaintext` with the key.
```bash
$ ./caesar 3 
plaintext : Hi
ciphertext: Kl
```

There must be one parameter and it must be a positive integer.
If not, the program should exit with message `Usage: ./caesar key`.

```bash
$ ./caesar
Usage: ./caesar key
```

## Bonus

Let your program accept an optional second parameter `-r` at the end of the command line that let you decrypt a message.
If `-r` flag is present (notice the term *flag*), your program should ask for `ciphertext` first and prints
the `plaintext`.

```bash
$ ./caesar 13 -r
ciphertext: Uv gurer!
plaintext : Hi there! 
```

# When to Do it

By Sunday, january 26, 2025 at 11:59 PM

# How to Test

Test your script with command `./check caesar`

```bash
$ ./caesar HELLO
Usage: ./caesar key
```
```bash
$ ./caesar 1 2 3 
Usage: ./caesar key
```
```bash
$ ./caesar 1 
plaintext : AA
ciphertext: BB
```
```bash
$ ./caesar 1 
plaintext : Ab
ciphertext: Bc
```
```bash
$ ./caesar 2 
plaintext : Ab, cD
ciphertext: Cd, eF
```
```bash
$ ./caesar 13 
plaintext : Hi there! 
ciphertext: Uv gurer!
```
```bash
$ ./caesar 13 -r
ciphertext: Uv gurer!
plaintext : Hi there! 
```
# How to Submit

Once you're done with all tasks, submit all your python files for the week on Moodle.

# Licence

This course is freely inspird from [CS50’s Introduction to Computer Science](https://cs50.harvard.edu/x/2025/) Harvard. It is licensed under a [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license. 
