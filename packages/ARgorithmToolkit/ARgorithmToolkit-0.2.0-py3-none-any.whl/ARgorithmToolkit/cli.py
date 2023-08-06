# pylint: disable=no-self-use
# pylint: disable=too-many-statements
# pylint: disable=raise-missing-from
"""CLI tool for ARgorithm made using typer
"""
import os
import re
import json
import requests
import typer
from halo import Halo
import ARgorithmToolkit
from ARgorithmToolkit.parser import ARgorithmConfig,ValidationError,input_data
from ARgorithmToolkit.security import injection_check,execution_check

CLOUD_URL = "https://argorithm.el.r.appspot.com"
CACHE_DIR = typer.get_app_dir("ARgorithm")

if not os.path.isdir(CACHE_DIR):
    os.mkdir(CACHE_DIR)

class Messager():
    """Class for pretty printing messages using typer
    """
    def msg(self,tag:str,title:str,message:str,color:str):
        """Pretty messaging for standard log messages
        """
        code = typer.style(f"[{tag.upper()}]: {title.upper()}" , fg=color , bold=True)
        typer.echo(code)
        if message:
            typer.echo(message)

    def info(self,title:str,message:str=""):
        """Information message
        """
        self.msg("info",title,message,typer.colors.BLUE)

    def warn(self,title:str,message:str=""):
        """Warning message
        """
        self.msg("error",title,message,typer.colors.YELLOW)

    def fail(self,title:str,message:str=""):
        """Error message
        """
        self.msg("critical error",title,message,typer.colors.RED)

    def good(self,title:str,message:str=""):
        """Success message
        """
        self.msg("success",title,message,typer.colors.GREEN)

    def menuitem(self,argorithm):
        """pretty print argorithm details
        """
        head = typer.style(f"- {argorithm['argorithmID']}",fg=typer.colors.GREEN)
        typer.echo(head)
        typer.secho(f"\tby {argorithm['maintainer']}",fg=typer.colors.CYAN)
        typer.echo("\tParameters")
        for key in argorithm['parameters']:
            typer.echo(f"\t\t{key} : {argorithm['parameters'][key]['description']}")

    def state(self,states):
        """pretty print states
        """
        states = states['data']
        for state in states:
            typer.echo('\n'+'-'*50)
            typer.secho(state['state_type'],bold=True)
            typer.secho('\t'+state['comments'],fg=typer.colors.CYAN)
            if state['state_def']:
                for key in state['state_def']:
                    typer.echo(f"\t{key} : {state['state_def'][key]}")

msg = Messager()

class Settings():
    """handles endpoint settings"""
    local:bool = False
    endpoint:str=CLOUD_URL

    def get_endpoint(self):
        """returns required endpoint"""
        if self.local:
            return "http://127.0.0.1"
        config_file = os.path.join(CACHE_DIR , "config")
        if os.path.isfile(config_file):
            with open(config_file,"r") as conf:
                self.endpoint = conf.read()
        return self.endpoint

    def set_endpoint(self,url):
        """set up cloud endpoint"""
        try:
            with Halo(text='Connecting', spinner='dots'):
                rq = requests.get(url+"/argorithms/list")
            if rq.status_code == 200:
                msg.good("Connected",f"Cloud requests will now go to {url}")
            else:
                raise AttributeError("Not a server endpoint")
        except ValueError as ve:
            msg.warn("Please try again with proper URL")
            raise typer.Exit(1) from ve
        except AttributeError as ex:
            msg.fail(str(ex))
            raise typer.Exit(1) from ex
        except Exception as ex:
            msg.fail("Endpoint couldnt be found.")
            raise typer.Exit(2) from ex
        config_file = os.path.join(CACHE_DIR , "config")
        with open(config_file,'w') as config:
            config.write(url)

settings = Settings()

class AuthManager():
    """AuthManager handles authentication tokens for AUTH enabled servers
    """
    def __init__(self):
        """sets up credfile to store credentials
        """
        self.credfile = os.path.join(CACHE_DIR,".credentials")

    def register(self):
        """registers account
        """
        email = typer.prompt("Enter email address")
        msg.info("Password criteria",'- between 8 to 25 characters\n - contains atleast one number\n - contains atleast lower case alphabet\n - contains atleast uppercase alphabet')
        rules = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,25}$"
        password = typer.prompt("Enter password",confirmation_prompt=True,hide_input=True)
        if not re.search(rules,password):
            msg.warn("password unacceptable")
            typer.Exit(1)
            return
        url = settings.get_endpoint()+'/programmers/register'
        data = {
            "username" : email,
            "password" : password
        }
        try:
            with Halo(text='Connecting', spinner='dots'):
                rq = requests.post(url,data)
        except requests.RequestException as rqe:
            msg.fail("Connection failed",str(rqe))
            raise typer.Abort()
        if rq.status_code == 200:
            msg.good("Account created","These credentials will be used as both programmer and user credentials")
            return
        if rq.status_code == 409:
            msg.warn("Invalid email","email is already in use. Try login")
            typer.Exit(0)
        msg.fail("Error","Contact developer")

    def login_prompt(self):
        """login prompt to enter credentials
        """
        email = typer.prompt("Enter email address")
        password = typer.prompt("Enter password",hide_input=True)
        url = f"{settings.get_endpoint()}/programmers/login"
        data = {
            "username" : email,
            "password" : password
        }
        try:
            with Halo(text='Connecting', spinner='dots'):
                rq = requests.post(url,data)
        except requests.RequestException as rqe:
            msg.fail("Connection failed",str(rqe))
            raise typer.Abort()
        if rq.status_code == 404:
            msg.warn("User not found","please enter valid email")
        elif rq.status_code == 500:
            msg.fail("Server error","contact developer")
        elif rq.status_code == 401:
            msg.warn("incorrect password")
        elif rq.status_code == 200:
            msg.good("logged in successfully","credentials saved in cache")
            token = json.loads(rq.content)['access_token']
            with open(self.credfile,'w+') as cred:
                cred.write(token)
            return token
        raise typer.Exit(1)

    def get_token(self):
        """returns valid authorization token
        """
        url = settings.get_endpoint()
        if os.path.isfile(self.credfile):
            with open(self.credfile,'r') as cred:
                token = cred.read()
            try:
                with Halo(text='Connecting', spinner='dots'):
                    rq = requests.post(f"{url}/programmers/verify" , headers = {"authorization" : "Bearer "+token})
            except requests.RequestException as rqe:
                msg.fail("Connection failed",str(rqe))
                raise typer.Abort()
            if rq.status_code == 200:
                return token
            msg.warn("Token expired","Please enter login credentials again")
        token = self.login_prompt()
        with open(self.credfile,'w+') as cred:
            cred.write(token)
        return token

    def auth_check(self):
        """checks if AUTH is enabled on server
        """
        try:
            url = settings.get_endpoint() + "/auth"
            try:
                with Halo(text='Connecting', spinner='dots'):
                    rq = requests.get(url)
            except requests.RequestException as rqe:
                msg.fail("Connection failed",str(rqe))
                raise typer.Abort()
            if rq.status_code == 200:
                return True
            return False
        except Exception as ex:
            msg.warn("authentication error",str(ex))
            raise typer.Abort()

authmanager = AuthManager()

app = typer.Typer(help="ARgorithm CLI")

@app.callback()
def main(
        local:bool = typer.Option(False,"--local",'-l',help="Connects to server running on localhost",show_default=False)
    ):
    """callback that adds the local option to app
    """
    settings.local = local

def name_check(value:str):
    """checks validity of argorithmID
    """
    rules = r"^[A-Za-z_]+$"
    m = re.search(rules,value)
    if m is None:
        msg.fail("Invalid name" , "argorithm name should be [A-Za-z_]")
        raise typer.Exit(code=1)
    return value

@app.command()
def init(
        name:str = typer.Argument(...,help="The name given to the argorithm [A-Za-z_]",callback=name_check),
        create_config:bool = typer.Option(False,'--config','-c',help="creates blank config file as well",show_default=False)
    ):
    """
    Create Blank code template and config template for ARgorithm
    """
    typer.echo(f"Creating empty template for {name}")

    with open(os.path.join(ARgorithmToolkit.__path__[0],'data/template.py',),'rb') as template:
        starter = template.read()

    filename = f"{name}.py"
    with open(filename , "wb") as codefile:
        codefile.write(starter)

    if create_config:
        config = {
            "argorithmID" : name,
            "file" : name+".py",
            "function" : "run",
            "parameters" : {},
            "default" : {},
            "description" : ""
        }
        config_file=f"{name}.config.json"
        with open(config_file, "w") as configfile:
            json.dump(config,configfile)

    msg.good("Template generated","refer documentation at https://argorithm.github.io/toolkit/ to learn how to use it\nchech out examples at https://github.com/ARgorithm/toolkit/tree/master/examples")

@app.command()
def connect():
    """
    Connect to your endpoint
    """
    endpoint = typer.prompt("Enter server endpoint",default=settings.get_endpoint())
    settings.set_endpoint(endpoint)

def autocomplete(incomplete:str):
    """autocomplete function for finding argorithms"""
    files = os.listdir('.')
    res = []
    l = len(incomplete)
    for filename in files:
        if filename[:l] == incomplete and filename[-3:] == '.py':
            res.append(filename[:-3])
    return res

def file_reader(filename):
    """finds anf checks argorithm files"""
    directory = os.getcwd()
    if os.path.isfile( os.path.join(directory,filename+".py")):
        try:
            data = ARgorithmConfig(f"{filename}.config.json")
            injection_check(os.path.join(directory,filename+".py"))
        except FileNotFoundError:
            msg.warn("config missing",f"you can use edit the {filename}.config.json \nor use CLI based config generator")
            raise typer.Exit()
        except ValidationError:
            msg.warn("config file is not configured properly","try the configure command to fix it \ncheck out docs for more info")
            raise typer.Exit(1)
        except ARgorithmToolkit.ARgorithmError:
            msg.warn("possible code injection","- remove imports other than ARgorithmToolkit\n- rename user-defined objects,classes and functions")
            raise typer.Exit(1)
    else:
        msg.warn(f"{filename}.py not found")
        raise typer.Exit(1)
    msg.good("Files Verified")
    try:
        execution_check(os.path.join(directory,filename+".py"),data.config)
    except AssertionError:
        msg.warn('Testing Failed','Function should return ARgorithmToolkit.StateSet object')
        raise typer.Exit(1)
    except Exception:
        msg.warn('Testing Failed','ARgorithm execution with example kwargs failed')
        raise typer.Exit(1)
    msg.good("Files Tested")
    return data.config

@app.command()
def configure(filename:str=typer.Argument(... , help="name of argorithm" , autocompletion=autocomplete)
    ):
    """Starts CLI config generator"""
    codefile = filename.split('.')[0] + ".py"
    if not os.path.isfile(os.path.join(os.getcwd(),codefile)):
        msg.warn("Python file not found",'use the init command first')
        raise typer.Abort()
    filepath = filename.split('.')[0] + ".config.json"
    try:
        existing_config = {
            "argorithmID" : filename,
            "file" : filename+".py",
            "function" : "run",
            "parameters" : {},
            "default" : {},
            "description" : ""
        }
        if os.path.isfile( os.path.join(os.getcwd() , f"{filepath}") ):
            with open(os.path.join(os.getcwd(), f"{filepath}") , 'r') as configfile:
                existing_config = json.load(configfile)
            os.remove(os.path.join(os.getcwd() , f"{filepath}"))
        ARgorithmConfig(filepath)
    except FileNotFoundError:
        msg.warn("Operation cancelled by user")
        with open(os.path.join(os.getcwd(), f"{filepath}") , 'w') as configfile:
            json.dump(existing_config,configfile)
        typer.Abort()
    except Exception:
        msg.fail("Some error occured, try again")
        with open(os.path.join(os.getcwd(), f"{filepath}") , 'w') as configfile:
            json.dump(existing_config,configfile)

@app.command()
def submit(
        filename:str=typer.Argument(... , help="name of argorithm" , autocompletion=autocomplete)
    ):
    """submit argorithms to server"""

    filename = filename.split('.')[0]
    data = file_reader(filename)

    header=None
    if authmanager.auth_check():
        token = authmanager.get_token()
        header={"authorization":"Bearer "+token}

    url = settings.get_endpoint()+"/argorithms/insert"
    local_file = filename+".py"
    files = [
        ('file', (local_file, open(local_file, 'rb'), 'application/octet')),
        ('data', ('data', json.dumps(data), 'application/json')),
    ]
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,files=files,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.good("Submitted")
    elif rq.status_code == 409:
        msg.warn("Already exists","An argorithm with this name already exists,try another argorithm name")
    elif rq.status_code == 406:
        msg.warn("File name was invalid","The name shoud be of type [A-Za-z_]")
    elif rq.status_code == 400:
        msg.warn("Incorrect file format","please refer documentation")
    else:
        msg.fail("Application error")

@app.command()
def update(
        filename:str=typer.Argument(... , help="name of argorithm" , autocompletion=autocomplete)
    ):
    """updates pre existing argorithms to server"""

    filename = filename.split('.')[0]
    data = file_reader(filename)

    header=None
    if authmanager.auth_check():
        token = authmanager.get_token()
        header={"authorization":"Bearer "+token}

    url = settings.get_endpoint()+"/argorithms/update"
    local_file = filename+".py"
    files = [
        ('file', (local_file, open(local_file, 'rb'), 'application/octet')),
        ('data', ('data', json.dumps(data), 'application/json')),
    ]
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,files=files,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.good("updated")
    elif rq.status_code == 404:
        msg.warn("Not found","Try submit command to add argorithm to server")
    elif rq.status_code == 401:
        msg.warn("Unauthorized","Only author of argorithm or admin is allowed to alter argorithms")
    else:
        msg.fail("Application error")

def search(argid,show=True):
    """Searches argorithm on server
    """
    url = settings.get_endpoint()+"/argorithms/view/"+argid
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.get(url)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        data = json.loads(rq.content)
        if show:
            typer.echo("Found argorithm")
            msg.menuitem(data)
        return data
    if rq.status_code == 404:
        msg.warn("Not found",f"{argid} not found in database")
        raise typer.Exit(1)
    msg.fail("Application error")
    raise typer.Exit(1)

@app.command("list")
def list_argorithms():
    """Get list of argorithms in server
    """
    url = settings.get_endpoint()+"/argorithms/list"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.get(url)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        menu = json.loads(rq.content)
        if len(menu) == 0:
            msg.warn("No argorithms")
            raise typer.Exit(1)
        for item in menu:
            msg.menuitem(item)

@app.command()
def test(
    argorithm_id:str = typer.Argument(... , help="argorithmID of function to be called. If not passed then menu will be presented"),
    output:bool = typer.Option(False,'--output','-o',help="print results in json format",show_default=False),
    user_input:bool = typer.Option(False,'--user-input','-u',help="if present, takes input from user",show_default=False)
    ):
    """test argorithms stored in server
    """
    params = search(argorithm_id,show=not output)
    header=None
    if authmanager.auth_check():
        token = authmanager.get_token()
        header={"authorization":"Bearer "+token}

    data = {
        "argorithmID" : params["argorithmID"],
        "parameters" : params["example"]
    }
    if user_input:
        data["parameters"] = input_data(params["parameters"])
    url = settings.get_endpoint()+"/argorithms/run"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        if output:
            print(rq.text)
        else:
            msg.state(json.loads(rq.content))
    elif rq.status_code == 401:
        msg.warn("Authentication failed",json.loads(rq.content)['detail'])
    else:
        msg.fail("application error")

@app.command()
def delete(
    argorithm_id:str = typer.Argument(... , help="argorithmID of function to be called. If not passed then menu will be presented")
    ):
    """Deletes argorithm from server
    """
    params = search(argorithm_id)
    flag = typer.confirm("Are you sure you want to delete it?")
    if not flag:
        typer.echo("Not deleting")
        raise typer.Abort()
    header=None
    if authmanager.auth_check():
        token = authmanager.get_token()
        header={"authorization":"Bearer "+token}

    data = {
        "argorithmID" : params["argorithmID"],
    }
    url = settings.get_endpoint()+"/argorithms/delete"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.info("Deleted successfully",)
    elif rq.status_code == 401:
        msg.warn("Not authorized","only author of argorithm or admin can delete it")
    else:
        msg.fail("application error")


account_app = typer.Typer(help="Manages account")
app.add_typer(account_app,name="account")

@account_app.command()
def login(
        override:bool=typer.Option(False,'--override','-o',show_default=False,help="Enter new credentials")
    ):
    """Log in to ARgorithmServer. Only is AUTH is enabled on server.
    """
    if not authmanager.auth_check():
        msg.warn("AUTH disabled at server")
        raise typer.Exit(0)
    if override:
        authmanager.login_prompt()
    else:
        authmanager.get_token()

@account_app.command()
def new():
    """Create new programmer and user account in ARgorithmServer. Only is AUTH is enabled on server.
    """
    if not authmanager.auth_check():
        msg.warn("AUTH disabled at server")
        raise typer.Exit(0)
    authmanager.register()

admin_app = typer.Typer(help="Administrator level methods")
app.add_typer(admin_app,name="admin")

@admin_app.command()
def grant(
        email:str=typer.Argument( ... , help="The account email that would be granted admin access")
    ):
    """grants admin acess
    """
    if not authmanager.auth_check():
        msg.warn("AUTH is disabled at this endpoint")
        raise typer.Exit(1)
    data = {
        "email" : email
    }
    token = authmanager.get_token()
    header={"authorization":"Bearer "+token}
    url = settings.get_endpoint()+"/admin/grant"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.good("granted admin priveleges")
    elif rq.status_code == 401:
        msg.warn("Not authorized","You need admin priveleges")
    elif rq.status_code == 406:
        msg.warn("Blacklisted email","This email is blacklisted thus cannot be granted admin priveleges")
    elif rq.status_code == 404:
        msg.warn("Not found","No such email registered")
    else:
        msg.fail("Application Error")

@admin_app.command()
def revoke(
        email:str=typer.Argument( ... , help="The account email that would be granted admin access")
    ):
    """grants admin acess
    """
    if not authmanager.auth_check():
        msg.warn("AUTH is disabled at this endpoint")
        raise typer.Exit(1)
    data = {
        "email" : email
    }
    token = authmanager.get_token()
    header={"authorization":"Bearer "+token}
    url = settings.get_endpoint()+"/admin/revoke"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.good("revoked admin priveleges")
    elif rq.status_code == 401:
        msg.warn("Not authorized","You need admin priveleges")
    elif rq.status_code == 404:
        msg.warn("Not found","No such email registered")
    else:
        msg.fail("Application Error")

@admin_app.command("delete")
def account_delete(
        email:str=typer.Argument( ... , help="The account email that would be granted admin access"),
        programmer:bool=typer.Option(False,'-p','--programmer',help="If flag is present, it will delete the programmer account")
    ):
    """Deletes account. Requires admin priveleges
    """
    if not authmanager.auth_check():
        msg.warn("AUTH is disabled at this endpoint")
        raise typer.Exit(1)
    data = {
        "email" : email
    }
    token = authmanager.get_token()
    header={"authorization":"Bearer "+token}
    if programmer:
        url = settings.get_endpoint()+"/admin/delete_programmer"
    else:
        url = settings.get_endpoint()+"/admin/delete_user"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.good("deleted account")
    elif rq.status_code == 401:
        msg.warn("Not authorized","You need admin priveleges")
    elif rq.status_code == 404:
        msg.warn("Not found","No such email registered")
    else:
        msg.fail("Application Error")

@admin_app.command()
def blacklist(
        email:str=typer.Argument( ... , help="The account email that would be granted admin access")
    ):
    """blacklists account. Requires admin priveleges
    """
    if not authmanager.auth_check():
        msg.warn("AUTH is disabled at this endpoint")
        raise typer.Exit(1)
    data = {
        "email" : email
    }
    token = authmanager.get_token()
    header={"authorization":"Bearer "+token}
    url = settings.get_endpoint()+"/admin/black_list"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.good("blacklisted account")
    elif rq.status_code == 401:
        msg.warn("Not authorized","You need admin priveleges")
    elif rq.status_code == 404:
        msg.warn("Not found","No such email registered")
    else:
        msg.fail("Application Error")

@admin_app.command()
def whitelist(
        email:str=typer.Argument( ... , help="The account email that would be granted admin access")
    ):
    """whitelist accounts. Requires admin priveleges
    """
    if not authmanager.auth_check():
        msg.warn("AUTH is disabled at this endpoint")
        raise typer.Exit(1)
    data = {
        "email" : email
    }
    token = authmanager.get_token()
    header={"authorization":"Bearer "+token}
    url = settings.get_endpoint()+"/admin/white_list"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.good("whitelisted account")
    elif rq.status_code == 401:
        msg.warn("Not authorized","You need admin priveleges")
    elif rq.status_code == 404:
        msg.warn("Not found","No such email registered")
    else:
        msg.fail("Application Error")
