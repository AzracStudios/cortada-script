![CortadaScript Logo](./assets/github-header-dark.svg#gh-dark-mode-only)
![CortadaScript Logo](./assets/github-header-light.svg#gh-light-mode-only)

CortadaScript is an interpreted language, whose design is inspired by basic and python and name by coffee. I am building this as my high school final year project. It is very much rough around the edges (and even at the core) but it serves a great learning experience.

To try it, clone the repo, and run the cli. The syntax highlighting is currently available for vscode, in the language directory. To install it, use the 'Developer: Install Extension From Location...' command from the command palette, and select the 'language' directory

Here are some examples of CortadaScript (files in the examples directory):

Hello world:

```
include core

fn main do
    core.ascii_cup()
    print(`${' ' * 20}Hello world!`)
end
```

Fibonacci:

```
var memo = {}

fn fib(n) do
    var a, b, c, i = 1, 0, 0, 0
    
    if n in memo then
        return memo[n]
    end

    do until i < n 
        a, b = b, c
        c = a + b
        i ++
    stop
    
    memo[n] = c
    return c
end

fn main do
    var n = input("enter n: ") cast int
    print(fib(n))
end
```

Calculator:
```
fn calculator() do 
    var num1 = input("num 1: ") cast int
    var num2 = input("num 2: ") cast int
    var op = input("op: ") cast int

    var res = 0

    switch op do
        case "+" do
            res = num1 + num2
        end

        case "-" do 
            res = num1 - num2
        end

        case "*" do
            res = num1 * num2
        end

        case "/" do
            if num2 == 0 then
                throw ("Division by 0!")
            end

            res = num1 / num2
        end
    end

    return res
end

fn main do
    var run = true

    do until run
        print(calculator())
        run = input("again? [y/n]: ") == "y"
    stop
end
```