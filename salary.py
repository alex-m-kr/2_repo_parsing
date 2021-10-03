def salary_parser(line):

    if line is None:
        salary_dict = {'currency': None, 'from': None, 'to': None}
        return salary_dict

    salary_dict = {}
    currency = ''
    line = line.strip().lower()

    # ищем валюту
    if line[-1].isdigit():
        salary_dict['currency'] = None
    else:
        for c in line[::-1]:
            if not c.isdigit() and c != ' ':
                currency = c + currency
            else: 
                break
        salary_dict['currency'] = currency
        line = line.replace(currency, '')
    line = line.replace(' ', '')
    line = line.replace(chr(8239), '')  # неразрывный пробел
    
    # вариант от и до
    if 'от' in line and 'до' in line:
        line = line.replace('от', '')
        salary_dict['from'] = int(line.split('до')[0])
        salary_dict['to'] = int(line.split('до')[1])
    # вариант "от"
    elif 'от' in line:
        salary_dict['from'] = int(line.split('от')[1])
        salary_dict['to'] = None
    # вариант "до"
    elif 'до' in line:
        salary_dict['from'] = None
        salary_dict['to'] = int(line.split('до')[1])
    #вариант с 1 - 2
    elif chr(8211) in line:  # тире, а не минус
        salary_dict['from'] = int(line.split(chr(8211))[0])
        salary_dict['to'] = int(line.split(chr(8211))[1])

    return salary_dict
