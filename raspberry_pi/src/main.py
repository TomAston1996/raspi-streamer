'''
App entry point
Author: Tom Aston
'''
import random
import time

def main() -> None:
    '''
    Main function
    '''
    while True:
        mock_cpu_utilisation = random.randint(0, 100)
        print(f"CPU Utilisation: {mock_cpu_utilisation}%")
        time.sleep(1)

if __name__ == "__main__":
    main()


