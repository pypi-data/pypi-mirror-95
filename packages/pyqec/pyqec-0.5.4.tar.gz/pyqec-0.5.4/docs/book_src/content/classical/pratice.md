# Let's get some practice

Reading a tutorial is fun,
but what about running some experiments
without guidance.

As an exercise, 
you should try to obtain a performance plot for different
repetition codes with different lengths.

The repetition code of length \\(2t + 1\\) for any natural number \\(t\\)
is the linear code with codewords \\(000\ldots 0\\) and \\(111\ldots 1\\).
It is a code of dimension \\(k = 1\\) where each codeword is \\((2t + 1\\)
repetitions of the \\(0\\) or \\(1\\) bit.
The parity check matrix of this code is the \\(2t \times 2t + 1\\)
matrix
\begin{align}
    H = 
    \begin{pmatrix}
        1 & 1 & 0 & 0 & \ldots & 0 & 0 \\
        0 & 1 & 1 & 0 & \ldots & 0 & 0 \\
        0 & 0 & 1 & 1 & \ldots & 0 & 0 \\
        & \vdots & & \vdots & & \vdots & \\
        0 & 0 & 0 & 0 & \ldots & 1 & 1
    \end{pmatrix}.
\end{align}

A simple decoder for is the majority vote decoder.
Simply,
if the Hamming weight of a message is greater than \\( t \\),
returns the \\( 111 \ldots 1 \\) codeword,
else returns the \\( 000 \ldots 0 \\).

```{warning}
Don't go to the next page to fast,
it has the solution to this exercise.
```
