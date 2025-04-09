from schemas import User,PcInfo, Session
from utils.pc_info import get_pc_info,get_session_start


def verify_user(name:str,class_var:str,password:str) -> User:
    # TODO: verificar dados do usuario
    return User(name=name,class_var=class_var,password=password)

def transform_reponse(new_user: User) -> Session:
    return Session(session_start=get_session_start(),
                           user=new_user,
                           pc_info=PcInfo(**get_pc_info())
                           )
