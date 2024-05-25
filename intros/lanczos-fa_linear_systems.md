---
title: Bounds for Lanczos-FA on linear systems
author: '[Tyler Chen](https://chen.pw)'
description: We discuss some error bounds for Lanczos-FA used to solve linear systems.
bibliography: lanczos-fa_linear_systems.bib
link-citations: true
---

\renewcommand{\R}{\mathbb{R}}
\renewcommand{\tr}{\operatorname{tr}}
\renewcommand{\d}{\mathrm{d}}

\renewcommand{\vec}[1]{\mathbf{#1}}
\renewcommand{\T}{\mathsf{T}}
\renewcommand{\fA}{f(\vec{A})}
\renewcommand{\lan}[2]{\mathsf{lan}_{#1}(#2)}

## Introduction


Krylov subspace methosd are among the most widely used class of algorithms for solving $\vec{A}\vec{x} = \vec{b}$ when $\vec{A}$ is a very large-sparse matrix.
These methods work by constructing the Krylov subspace
\[
\mathcal{K}_{k}(\vec{A},\vec{b})
:= \operatorname{span}\{\vec{b}, \vec{A}\vec{b}, \ldots, \vec{A}^{k-1}\vec{b} \}.
\]
This page focuses on the Lanczos method for matrix function approximation ([Lanczos-FA](./lanczos-fa.html)) used to approximate $\vec{A}^{-1}\vec{b}$.
The Lanczos-FA iterate is defined as
\[
\lan{k}{1/x} 
:= \| \vec{b} \|_2 \vec{Q} f(\vec{T}) \vec{e}_1,
\]
where $\vec{Q} = [\vec{q}_1, \ldots, \vec{q}_k]$ is an orthonormal basis for $\mathcal{K}_k(\vec{A},\vec{b})$ such that $\operatorname{span}\{\vec{q}_1, \ldots, \vec{q}_j\} = \mathcal{K}_{j}(\vec{A},\vec{b})$ for all $j\leq k$, and $\vec{T}:=\vec{Q}^\T \vec{A} \vec{Q}$.

## Positive definite systems

In the case that $\vec{A}$ is positive definite, then the Lanczos-FA iterate is equivalent to the well-known conjugate gradient algorithm. 
The simplest proof of this amounts to showing the Lanczos-FA iterate satisfies the same optimality property as CG.

**Theorem.** *If* $\vec{A}$ *is positive definite, then*
\[
\| \vec{A}^{-1} \vec{b} - \lan{k}{1/x} \|_{\vec{A}} 
= \min_{\vec{x}\in\mathcal{K}_k(\vec{A},\vec{b})} \| \vec{A}^{-1} \vec{b} - \vec{x} \|_{\vec{A}}. 
\]

**Proof.**
An arbitrary vector in $\mathcal{K}_k(\vec{A},\vec{b})$ can be written $\vec{Q}\vec{c}$ for some $\vec{x} \in \R^k$. 
Thus, 
\[
\begin{align*}
\min_{\vec{x}\in\mathcal{K}_k(\vec{A},\vec{b})} \| \vec{A}^{-1} \vec{b} - \vec{x} \|_{\vec{A}}
&=
\min_{\vec{c}\in\R^k} \| \vec{A}^{-1} \vec{b} - \vec{Q}\vec{c} \|_{\vec{A}}. 
\\&= \min_{\vec{c}\in\R^k} \| \vec{A}^{1/2} (\vec{A}^{-1} \vec{b} - \vec{Q}\vec{c} ) \|_{2}. 
\\&= \min_{\vec{c}\in\R^k} \| \vec{A}^{-1/2} \vec{b} - \vec{A}^{1/2} \vec{Q}\vec{c} \|_{2}. 
\end{align*}
\]
Writing the solution to the normal equations, we find that the above equations are minimized for
\[
\vec{c} = ((\vec{A}^{1/2}\vec{Q} )^\T (\vec{A}^{1/2} \vec{Q}) )^{-1} (\vec{A}^{1/2} \vec{Q})^\T (\vec{A}^{-1/2} \vec{b})
= (\vec{Q}^\T \vec{A} \vec{Q})^{-1} \vec{Q}^\T \vec{b}
= \| \vec{b} \|_2 \vec{T}^{-1} \vec{e}_1.
\]
Thus, we have solution
\[
\vec{x} = \vec{Q} \vec{c} 
= \| \vec{b}\|_2 \vec{Q} \vec{T}^{-1} \vec{e}_1
= \lan{k}{1/x}.
\]
This proves the theorem.$~~~\square$

This optimality property allows us to derive a number of prior bounds for the convergence of Lanczos-FA (and equivalently CG).



## Indefinite systems


If $\vec{A}$ is not positive definite, $\vec{T}$ may have an eigenvalue at or near to zero and the error of the Lanczos-FA approximation to $\vec{A}^{-1}\vec{b}$ can be arbitrarily large.


The MINRES iterates are defined as 
\[
    \hat{\vec{y}}_k 
    := \operatornamewithlimits{argmin}_{\vec{y}\in\mathcal{K}_k(\vec{A},\vec{b})} \| \vec{b} - \vec{A} \vec{y} \|_{2}
    = \operatornamewithlimits{argmin}_{\vec{y}\in\mathcal{K}_k(\vec{A},\vec{b})} \| \vec{A}^{-1}\vec{b} -  \vec{y} \|_{\vec{A}^2}.
\]
Define the residual vectors
\[
    \vec{r}_k := \vec{b} - \vec{A} \lan{k}{1/x}
    ,\qquad
    \vec{r}_k^{\mathrm{M}} := \vec{b} - \vec{A} \hat{\vec{y}}_k,
\]
and note that the MINRES residual norms are non-increasing due to the optimality of the MINRES iterates.
In [@cullum_greenbaum_96], it is shown that the CG residual norms are near the MINRES residual norms at iterations where MINRES makes good progress. 
More precisely, the algorithms are related by
\[
    \| \vec{r}_k  \|_2
    = \frac{\| \vec{r}_{k}^{\mathrm{M}} \|_2}{\sqrt{1- \left( \| \vec{r}_{k}^{\mathrm{M}} \|_2 / \| \vec{r}_{k-1}^{\mathrm{M}} \|_2 \right)^2}}.
\]
This bound says that when MINRES makes progress ($\| \vec{r}_{k}^{\mathrm{M}} \|_2 \ll \| \vec{r}_{k-1}^{\mathrm{M}} \|_2$) the CG residual is verys similar, but when MINRES stagnates the CG residual spikes. 
However, it does not clear gurantee that the convergence of CG is similar to that of MINRES.

The following theorem from [@chen_meurant_24] does so.
To the best of our knowledge, the result is new.

**Theorem.** 
For every $k\geq 1$,
\[
    \min_{0\leq j\leq k} \|\vec{r}_{j}^{\mathrm{F}}\|_2
    \leq \sqrt{k+1} \cdot \|\vec{r}_k^{\mathrm{G}}\|_2.
\]

It also turns out the bound is sharp.
**Theorem.**
For every $k\geq 1$ and $\varepsilon > 0$, there exists a matrix $\vec{A}$ and vector $\vec{b}$ for which 
\[
\min_{j\leq k} \|\vec{r}_j^{\mathrm{F}} \|_2 
\geq 
\left( \sqrt{k+1} - \varepsilon \right) \cdot \|\vec{r}_k^{\mathrm{G}}\|_2.
\]


## References

