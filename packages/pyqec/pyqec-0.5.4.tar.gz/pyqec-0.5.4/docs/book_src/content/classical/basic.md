# Review of basic concepts

In this section,
I present a review of the basic notions
of classical error correction that are useful 
to use `pyqec`.
This is a concise review and I invite any
unfamiliar reader to refer to one of the following books:

- [Error Correction Coding: Mathematical Methods and Algorithms by Todd K. Moon](https://www.wiley.com/en-gb/Error+Correction+Coding%3A+Mathematical+Methods+and+Algorithms-p-9780471739142)
- [Modern Coding Theory by Tom Richardson and Rüdiger Urbanke](https://www.cambridge.org/core/books/modern-coding-theory/A08C3B7B15351BF9C956CDFE5BE4846B)

If you are already familiar with those notions,
you can safely skip this section.


## Binary numbers

Through this book,
I use \\(\mathbb{F}_2 = (\lbrace 0, 1 \rbrace, +, \cdot)\\) to denote the 
Galois Field of order 2.
For this field, 
the addition operator is defined as
\begin{align}
    0 + 0 = 1 + 1 = 0, \\
    0 + 1 = 1 + 0 = 1
\end{align}
and the multiplication operator is defined with the standard relation.

I use \\( \mathbb{F}_2^n \\) to denote a vector space 
of dimension \\( n \\) over \\( \mathbb{F}_2 \\).
For simplicity,
I often use a shortcut notation to reprensent elements of \\( \mathbb{F}_2^n \\).
For example,
I may write 00101 to represent the vector 
\begin{align}
    \begin{pmatrix}
        0 \\ 0 \\ 1 \\ 0 \\ 1
    \end{pmatrix}.
\end{align}

The Hamming weight \\( |x| \\) of a binary vector 
\\( x \in \mathbb{F}_2^n \\) 
is the number of 1s in \\( x \\).


## Linear codes

A linear code \\( C \\) of length \\( n \\) and dimension \\( k \\) is a linear subspace 
of \\( \mathbb{F}_2^n \\) containing \\( 2^k \\) elements.
By linear, 
I mean that if \\( x, y \in C \\), then \\( x + y \in C \\).
For brevity,
I often denote a code by the set of its elements which are called codewords.
For example,
this is a code of length 5 and dimension 2:
\\[
    C = 
    \lbrace
        00000,
        10101,
        01010,
        11111
    \rbrace.
\\]
You can verify that the sum of any pair of codewords is also a codeword.

The minimum distance \\(d \\) of a code is the minimum Hamming weight
of the non-zero codewords.

I often use \\( [n, k] \\) to talk about a linear code
of length \\( n \\)
and \\( [n, k, d] \\) to specify that the code has minimum distance \\( d \\).


## Generator matrices

A \\( [n, k] \\) linear code if often described from a \\( k \times n \\) binary matrix
called a generator matrix.
Given a generator matrix \\( G \\),
a code is defined as 
\\[
    C(G) = 
    \lbrace
        G^T x
        \ | \ 
        x \in \mathbb {F}_2^k
    \rbrace.
\\]
For example,
the code in the previous example can be defined from the generator matrix
\\[
    G =
    \begin{pmatrix}
        1 & 0 & 1 & 0 & 1 \\\\
        0 & 1 & 0 & 1 & 0
    \end{pmatrix}.
\\]
This choice is not unique
and any generator matrix that can be obtained from \\( G \\)
via standard gaussian row operations defines the same code.


## Parity check matrices

An other convenient description of a \\( [n, k] \\) linear code
is from an \\( m \times n \\) binary matrix of rank \\( k \\), 
with \\( m \geq n - k \\),
called a parity check matrix.
Given a parity check matrix \\( H \\),
a code is defined as 
\\[
    C(H) = 
    \lbrace
        x \in \mathbb {F}_2^n
        \ | \ 
        Hx = 0
    \rbrace.
\\]
For example,
the code in the previous example can be defined from the parity check matrix
\\[
    H =
    \begin{pmatrix}
        1 & 1 & 1 & 1 & 1 \\\\
        0 & 1 & 0 & 1 & 0
    \end{pmatrix}.
\\]
Again, 
this choice is not unique
and any parity check matrix that can be obtained from \\( H \\)
via standard gaussian row operations defines the same code.

If the parity check matrix \\( H \\) and the generator matrix \\( G \\)
define the same code,
they satisfy the relation
\\[
    H \cdot G^T = 0.
\\]

The syndrome \\( \sigma(x) \\) of a binary vector \\( x \in \mathbb{F}_2^n \\)
is the value
\\[
    \sigma(x) = Hx.
\\]
Thus, \\( x \\) is a codeword if and only if it has a zero syndrome.


## Binary noise channels

Well, 
it is not called error correction for nothing.
A binary noise channel is a stochastic map \\( N: \mathbb{F}_2^n \to \mathbb{F}_2^n \\).
That is,
it takes a binary vector and randomly map it to an other binary vector.
If a binary noise channel acts independtly on each bit,
we say that it is memoryless,
otherwise with say that it is a channel with memory.

```{note}
There exists other types of noise channels such as
the erasure channel. However, they are not (yet) implemented
in pyqec.
```


### The binary symmetric channel

The binary symmetric channel is the simplest binary noise channel.
It is a memoryless channel flipping the value of a bit with a given 
probability \\( p \\).
For example,
given the input 000, 
a binary symmetric channel outputs the followings:

| Output        | Probability                |
|:-------------:|:--------------------------:|
| 000           | \\( (1 - p)^3 \\)          |
| 001, 010, 100 | \\( (1 - p)^2 \cdot p \\)  |
| 110, 101, 011 | \\( (1 - p) \cdot p^2 \\)  |
| 111           | \\( p^3 \\)                |


## Decoding

For a code \\( C \\), 
a classical decoder is a map \\( D: \mathbb{F}_2^n \to C \\).
Any sane decoder should map a codeword to itself.

Given a binary noise channel \\( N \\),
the failure rate of a decoder is the probability that,
given any codeword \\(x \\),
the decoder fails to recover \\(x \\) from \\( N(x) \\).

For the code 
\\[
    C = 
    \lbrace
        00000,
        11111
    \rbrace,
\\]
a good decoder maps all binary vectors with Hamming weight at most 2 to the 
00000 codeword and the other binary vectors to the 11111 codeword.

Given a binary symmetric channel with probability \\( p < 1/2 \\),
this decoder is optimal,
that is, 
it has the minimum failure rate.
However,
if \\( p > 1/2 \\),
this decoder has the maximum failure rate.
We say that \\( p = 1/2 \\) is the threshold value of the decoder.
