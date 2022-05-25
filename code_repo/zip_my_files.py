from zipfile import ZipFile
import os

os.makedirs('zips', exist_ok=True)
os.chdir('code')
for f in os.listdir():
    file = f.split('.')
    
    if file[1] == 'py':
        try:
            zf = ZipFile(os.path.join('..','zips', f'{file[0]}.zip'), mode='w')
            zf.write(f)
            zf.close()
        except Exception as e:
            print(e)
