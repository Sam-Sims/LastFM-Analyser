import os


def run_downloader():
    print('down')

def run_analyser():
    print('ana1')


def check_directories():
    path = os.getcwd()
    if not os.path.exists(path + '\images'):
        print('Images directory does not exist! Attempting to create directory...')
        _path = path + '\images'
        os.makedirs(_path, exist_ok=True)
        print('Images directory created successfully!')
    if not os.path.exists(path + '\data'):
        print('Data directory does not exist! Attempting to create directory...')
        _path = path + '\data'
        os.makedirs(_path, exist_ok=True)
        print('Data directory created successfully!')

def check_menu_choice(ans):
    try:
        if ans == '1':
            run_downloader()
        elif ans == '2':
            run_analyser()
        elif ans == '3':
            print('Place Holder')
        elif ans == '4':
            print('Place Holder')
        else:
            print('Error, an answer was not supplied!')
    except Exception as e:
        print('An error occurred' + e)


def print_main_menu():
    print('''\

    ---------------------------------------------------------------------------------

      _               _   ______ __  __                        _                     
     | |             | | |  ____|  \/  |     /\               | |                    
     | |     __ _ ___| |_| |__  | \  / |    /  \   _ __   __ _| |_   _ ___  ___ _ __ 
     | |    / _` / __| __|  __| | |\/| |   / /\ \ | '_ \ / _` | | | | / __|/ _ \ '__|
     | |___| (_| \__ \ |_| |    | |  | |  / ____ \| | | | (_| | | |_| \__ \  __/ |   
     |______\__,_|___/\__|_|    |_|  |_| /_/    \_\_| |_|\__,_|_|\__, |___/\___|_|   
                                                                  __/ |              
                                                                 |___/               

    ---------------------------------------------------------------------------------
     ''')
    print('Please make a selection:')
    print('1: Download Data')
    print('2: Generate Graphs')
    print('3: Generate Report')
    print('4: Verify Config')

def main():
    print_main_menu()
    ans = input()
    check_directories()
    check_menu_choice(ans)

if __name__ == "__main__":
    main()