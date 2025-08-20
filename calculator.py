def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "오류: 0으로 나눌 수 없습니다."
    return x / y

def main():
    while True:
        print("\n=== 간단한 계산기 ===")
        print("1. 더하기")
        print("2. 빼기") 
        print("3. 곱하기")
        print("4. 나누기")
        print("5. 종료")
        
        choice = input("선택하세요 (1-5): ")
        
        if choice == '5':
            print("계산기를 종료합니다.")
            break
            
        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("첫 번째 숫자를 입력하세요: "))
                num2 = float(input("두 번째 숫자를 입력하세요: "))
                
                if choice == '1':
                    result = add(num1, num2)
                    print(f"결과: {num1} + {num2} = {result}")
                elif choice == '2':
                    result = subtract(num1, num2)
                    print(f"결과: {num1} - {num2} = {result}")
                elif choice == '3':
                    result = multiply(num1, num2)
                    print(f"결과: {num1} * {num2} = {result}")
                elif choice == '4':
                    result = divide(num1, num2)
                    print(f"결과: {num1} / {num2} = {result}")
                    
            except ValueError:
                print("오류: 유효한 숫자를 입력하세요.")
        else:
            print("오류: 1-5 사이의 번호를 선택하세요.")

if __name__ == "__main__":
    main()