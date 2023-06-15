# Contributor(s): nigella (@nig)

# Recomend to install the libs.
# pip install urllib3
# pip install sys
# How to use: python3 Clickjacking_Tester.py listofsites.txt


from urllib.request import urlopen
from sys import argv, exit
import os

__author__ = 'D4Vinci'

def check(url):
    ''' check given URL is vulnerable or not '''

    try:
        if "http" not in url:
            url = "http://" + url

        data = urlopen(url)
        headers = data.info()

        if not "X-Frame-Options" in headers:
            return True

    except:
        return False




def create_poc(url):
    ''' create HTML page of given URL '''

    code = """
<html>
   <head><title>Clickjack test page</title></head>
   <body>
     <p>Website is vulnerable to clickjacking!</p>
     <iframe src="{}" width="500" height="500"></iframe>
   </body>
</html>
    """.format(url)

    file_name = os.path.basename(url) + ".html"  # Obtém apenas o nome do arquivo e adiciona a extensão ".html"
    file_path = os.path.join(os.getcwd(), file_name)  # Cria o caminho absoluto para o arquivo

    with open(file_path, "w") as f:
        f.write(code)
        f.close()

def main():
    ''' Everything comes together '''

    try:
        sites = open(argv[1], 'r').readlines()
    except FileNotFoundError:
        print("[*] Arquivo não encontrado. Certifique-se de fornecer um arquivo válido como argumento.")
        exit(0)
    except Exception as e:
        print("[*] Ocorreu um erro ao ler o arquivo de sites:", str(e))
        exit(0)

    for site in sites[0:]:
        print("\n[*] Checking " + site)
        status = check(site)

        if status:
            print(" [+] Website is vulnerable!")
            create_poc(site.split('\n')[0])
            print(" [*] Created a poc and saved to <URL>.html")

        elif not status:
            print(" [-] Website is not vulnerable!")
        else:
            print('Every single thing is crashed, Python got mad, dude wtf you just did?')

if __name__ == '__main__':
    main()
