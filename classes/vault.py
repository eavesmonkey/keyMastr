import pyperclip, os
import classes.password
import json

class Vault:
    def __init__(self):
        self.vaultPath = os.path.expanduser('~') + '/.vault'
        self.accountFile = self.vaultPath + '/accounts.json'
        self.password = classes.password.Password()

    def getAllAccounts(self):
        with open(self.accountFile) as json_data:
            return json.load(json_data)

    def getAccounPassword(self, masterPass, account):
        accounts = self.getAllAccounts()
        if account in accounts:
            accountPass = self.password.getPassword(masterPass, account)
            pyperclip.copy(accountPass)
            print('Password for ' + account + ' copied to clipboard.')
        else:
            print('There is no account named ' + account)

    def addAccount(self, name, length=10, hasSymbols=True):
        accounts = self.getAllAccounts()
        if name not in accounts:
            accounts[name]={'length': length, 'symbols': hasSymbols}
            self.saveFile(accounts)

    def deleteAccount(self, name):
        accounts = self.getAllAccounts()
        del accounts[name]
        self.saveFile(accounts)

    def saveFile(self, content):
        open(self.accountFile, 'w').write(json.dumps(content))
