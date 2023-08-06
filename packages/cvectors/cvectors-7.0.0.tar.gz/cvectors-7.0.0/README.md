# Cvectors

Cvectors is a Python package for 2D vectors. It provides a class,
`Vector`, which uses `complex` internally.

Usage is as follows:

```python
>>> from cvectors import Vector, angle
>>> foo = Vector(4, 3)
>>> foo
Vector(4.0, 3.0)
>>> foo.x
4.0
>>> foo.y
3.0
>>> foo.r
5.0
>>> bar = Vector(4, 5)
>>> foo + bar
Vector(8.0, 8.0)
>>> foo.dot(bar)
31.0
>>> foo.rotate(angle(90, "deg"))
Vector(-2.999999999999999, 4.000000000000001)
>>> Vector.from_polar(r=3, theta=5) - Vector.from_polar(r=5, theta=2)
Vector(2.9317207391253906, -7.423259958117824)
>>> Vector(5, 6).perp_dot(Vector(-6, 1))
41.0
>>> abs(foo)
5.0
>>> Vector(1, -9).rec()
(1.0, -9.0)
>>> Vector(1, -9).pol()
(9.055385138137417, -1.460139105621001)
>>> Vector(3, 2).perp()
Vector(-2.0, 3.0)
>>> Vector(3.142, 2.718).round()
(3.0, 3.0)
>>> Vector(3.142, 2.718).round(1)
(3.1, 2.7)
```
