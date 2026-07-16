while True:
    op = input("Enter +, -, *, / or 'exit' to stop: ")
    
    if op == "exit":
        print("Goodbye!")
        break
    
    if op not in ['+', '-', '*', '/']:
        print("Invalid operation! Exiting...")
        break
    
    numbers = input("Enter numbers separated by space: ").split()
    nums = [float(n) for n in numbers]
    
    result = nums[0]
    for n in nums[1:]:
        if op == "+":
            result += n
        elif op == "-":
            result -= n
        elif op == "*":
            result *= n
        elif op == "/":
            if n == 0:
                print("Cannot divide by zero!")
                break
            result /= n
    else:
        print("Result:", result)
