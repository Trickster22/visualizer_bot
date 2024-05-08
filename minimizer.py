import condOpt
import oneDimOpt

def minimize(userData, chat_id):
    type = userData['type']
    if type == 'Метод половинного деления':
        l = userData['l'].split(";")
        return oneDimOpt.HalfDivision(userData['equation'], float(userData['e']), float(l[0]), float(l[1]), chat_id)
    elif type == 'Метод золотого сечения':
        l = userData['l'].split(";")
        return oneDimOpt.golden(userData['equation'], float(userData['e']), float(l[0]), float(l[1]), chat_id)
    elif type == "Метод штрафов":
       res = condOpt.penalty(userData)
       return res
    