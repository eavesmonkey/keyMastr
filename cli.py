if len(sys.argv) > 2:
    masterPass = sys.argv[1]
    account = sys.argv[2]

if len(sys.argv) > 2:
    if sys.argv[1] == '--add':
        print('Usage: [master password] [account] - copy account password')
    elif sys.argv[1] == '--list':
        print('Show list')
    elif len(sys.argv) == 2:
        getAccounPassword()
