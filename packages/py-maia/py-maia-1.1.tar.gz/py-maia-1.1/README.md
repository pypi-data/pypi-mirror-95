maia
======================
## About "maia"
This python module was created to make code clear and easy.
This page will be updated quite often, like the project itself, so I recommend checking for updates often

## Version 1.0
### AutoInstaller
That function will help you install packages without using a console command "pip install ..."<br/>
***Example***

    from maia import AutoInstaller
    try:
        import colorama
    except ImportError:
       AutoInstaller()
    print("Hello, AutoInstaller" + colorama.Fore.GREEN)