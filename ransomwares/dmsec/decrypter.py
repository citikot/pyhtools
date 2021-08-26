from cryptography.fernet import Fernet
from sys import exit
from os import walk
from os.path import join
from psutil import disk_partitions

class DMSECDecrypter:
    def __init__(self, key:str=None, paths:list=None) -> None:
        # check key
        if key == None:
            print('[!] Invalid KEY')
            exit()
        if type(key)==str:
            key = bytes(key, encoding='utf-8')
        self.KEY = key
        print('[!] KEY :', self.KEY)

        # generate fernet obj for file encryption
        self.fernet = Fernet(self.KEY)

        if paths == None:
            self.PATHS = self.__get_partitions_path()
        else:
            self.PATHS = paths
        print('[!] PATHS to be decrypted :\n', self.PATHS)



    def __get_partitions_path(self) -> list:
        '''
        returns all mounted partition's mount points as a list
        '''
        mount_points = []
        for partition in disk_partitions():
            mount_points.append(partition.mountpoint)
        return mount_points


    def decrypt_file(self, file_path:str):
        '''
        decrypts single file
        '''
        try:
            # read file data
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # decrypt file data
            dec_data = self.fernet.decrypt(file_data)

            # write file data
            with open(file_path, 'wb') as f:
                f.write(dec_data)
            print(f'[*] File {file_path} decrypted.')
            return True

        except Exception:
            print(f'[!] Failed to decrypt {file_path}')
            return False


    def decrypt_files(self, path:str):
        '''
        decrypts all the files in the specified path
        '''
        for root, dirs, files in walk(path):
            print('-'*40)
            print('ROOT :',root)
            for file in files:
                file_path = join(root, file)
                self.decrypt_file(file_path=file_path)
            print('-'*40)


    def start(self):
        for path in self.PATHS:
            self.decrypt_files(path)


if __name__ == '__main__':
    PATHS = [r'C:\Users\there\Desktop\tools\TermuxCustomBanner',]
    KEY = input('[+] Enter KEY : ')
    encrypter = DMSECDecrypter(KEY, PATHS)
    encrypter.start()
