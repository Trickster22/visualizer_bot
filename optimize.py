import cond_opt
import one_dim_opt

def minimize(userData, chat_id):
    type = userData['type']
    if type == 'Метод половинного деления':
        l = userData['l'].split(";")
        return one_dim_opt.HalfDivision(userData['equation'], float(userData['e']), float(l[0]), float(l[1]), chat_id)
    elif type == 'Метод золотого сечения':
        l = userData['l'].split(";")
        return one_dim_opt.golden(userData['equation'], float(userData['e']), float(l[0]), float(l[1]), chat_id)
    elif type == "Метод штрафов":
       res = cond_opt.penalty(userData)
       return res
    