![CortadaScript Logo](./assets/github-header-dark.svg#gh-dark-mode-only)
![CortadaScript Logo](./assets/github-header-light.svg#gh-light-mode-only)

CortadaScript is an interpreted language, whose design is inspired by basic and python and name by coffee. I am building this as my high school final year project. It is very much rough around the edges (and even at the core) but it serves a great learning experience.

To try it, clone the repo, and run the cli. The syntax highlighting is currently available for vscode, in the language directory. To install it, use the 'Developer: Install Extension From Location...' command from the command palette, and select the 'language' directory

Here are some examples of CortadaScript (files in the examples directory):

Hello world:

```
fn main do 
    hello_world()
end

main()
```

Fibonacci:

```
var memo = []

fn fib(n) do
    var a = 1
    var b = 0
    var c = 0
    
    if length(memo) > n then
        return memo @ n
    end

    var i = 0; while i < n  do
        c = a + b
        a = b
        b = c
        i ++
    end
    
    ~ memo[n] = c
    return c
end

fn main do
    ~ var n = input("enter n: ")
    var i = 0; while i < 10 do
        print(fib(i))
        i++
    end
end

main()
```

Calculator:
```
fn calculator do 
    var num1 = to_int(input("num 1: "))
    var num2 = to_int(input("num 2: "))
    var op = input("op: ")

    var res = 0

    if op == "+" then
        res = num1 + num2
    elif op == "-" then
        res = num1 - num2
    elif op == "*" then
        res = num1 * num2
    elif op == "/" then
        res = num1 / num2
    end

    return res
end

fn main do
    var run = true

    while run do
        print(calculator())
        run = input("\nagain? [y/n]: ") == "y"
    end
end

main()
```
