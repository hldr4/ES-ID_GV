import random
import re

entity_types = {
    'A': 'Sociedad Anónima',
    'B': 'Sociedad de Responsabilidad Limitada',
    'C': 'Sociedad Colectiva',
    'D': 'Sociedad Comanditaria',
    'E': 'Comunidad de Bienes',
    'F': 'Sociedad Cooperativa',
    'G': 'Asociación o Fundación',
    'H': 'Comunidad de Propietarios en Régimen de Propiedad Horizontal',
    'J': 'Sociedad Civil, con o sin Personalidad Jurídica',
    'K': 'Español menor de 14 años',
    'L': 'Español residente en el extranjero sin DNI',
    'M': 'NIF que otorga la Agencia Tributaria a extranjeros que no tienen NIE',
    'N': 'Entidad Extranjera',
    'P': 'Corporación Local',
    'Q': 'Organismo Autónomo, Estatal o no, o Asimilado, o Congregación o Institución Religiosa',
    'R': 'Congregación o Institución Religiosa (desde 2008, ORDEN EHA/451/2008)',
    'S': 'Órgano de la Administración General del Estado o de las Comunidades Autónomas',
    'U': 'Unión Temporal de Empresas',
    'V': 'Sociedad Agraria de Transformación',
    'W': 'Establecimiento permanente de entidad no residente en España',
    'X': 'Extranjero identificado por la Policía con un número de identidad de extranjero, NIE con letra "X", asignado hasta el 15 de julio de 2008',
    'Y': 'Extranjero identificado por la Policía con un NIE con letra "Y", asignado desde el 16 de julio de 2008 (Orden INT/2058/2008, BOE del 15 de julio)',
    'Z': 'Letra "Z" reservada para cuando se agoten los "Y" para Extranjeros identificados por la Policía con un NIE'
}

province_codes = {
    'No Residente': ['00'],
    'Álava': ['01'],
    'Albacete': ['02'],
    'Alicante': ['03', '53', '54'],
    'Almería': ['04'],
    'Ávila': ['05'],
    'Badajoz': ['06'],
    'Islas Baleares': ['07', '57'],
    'Barcelona': ['08', '58', '59', '60', '61', '62', '63', '64', '65', '66', '68'],
    'Burgos': ['09'],
    'Cáceres': ['10'],
    'Cádiz': ['11', '72'],
    'Castellón': ['12'],
    'Ciudad Real': ['13'],
    'Córdoba': ['14', '56'],
    'La Coruña': ['15', '70'],
    'Cuenca': ['16'],
    'Gerona': ['17', '55', '67'],
    'Granada': ['18'],
    'Guadalajara': ['19'],
    'Guipúzcoa': ['20'],
    'Navarra': ['31', '71'],
    'Huelva': ['21'],
    'Huesca': ['22'],
    'Jaén': ['23'],
    'León': ['24'],
    'Lérida': ['25'],
    'La Rioja': ['26'],
    'Pontevedra': ['27', '36', '94'],
    'Madrid': ['28', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87'],
    'Málaga': ['29', '92', '93'],
    'Murcia': ['30', '73'],
    'Orense': ['32'],
    'Asturias': ['33', '74'],
    'Palencia': ['34'],
    'Las Palmas': ['35', '76'],
    'Salamanca': ['37'],
    'Santa Cruz de Tenerife': ['38', '75'],
    'Cantabria': ['39'],
    'Segovia': ['40'],
    'Sevilla': ['41', '90', '91'],
    'Soria': ['42'],
    'Tarragona': ['43', '77'],
    'Teruel': ['44'],
    'Toledo': ['45'],
    'Valencia': ['46', '96', '97', '98'],
    'Valladolid': ['47'],
    'Vizcaya': ['48', '95'],
    'Zamora': ['49'],
    'Zaragoza': ['50', '99'],
    'Ceuta': ['51'],
    'Melilla': ['52']
}

# samples
test_ids = [
    "55883808H",  # pass, DNI
    "X2607448F",  # pass, NIE
    "D71897094",  # pass, CIF ending with control digit
    "D7189709D",  # pass, CIF ending with control letter
    "P7189709D",  # pass, CIF obligatory ending with control letter
    "A12345674", # pass, CIF obligatory ending with control digit
    "DD1897094",  # fail, starts with two letters
    "D718970940",  # fail, exceeds length requirement
    "I71897094",  # fail, starts with an invalid letter
    "D7189709I",  # fail, ends with an invalid letter
]

# CIF is outdated, now it's called NIF, same as for DNI/NIE, but for ease of differentiation, use the old name

cod_control_dni_nie = 'TRWAGMYFPDXBNJZSQVHLCKE'
valid_start_letters = ''.join(entity_types.keys())

nie_letter_to_num_map = {'X': '0', 'Y': '1', 'Z': '2'}
nie_num_to_letter_map = {v: k for k, v in nie_letter_to_num_map.items()}

cif_num_to_letter_map = {'0': 'J', '1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G', '8': 'H', '9': 'I'}

is_cif_control_letter = 'PQRSWN' # CIF starting with these has to end with control letter (or if the two following digits are 00 [No residente])
is_cif_control_digit = 'ABEH' # CIF starting with these has to end with control digit
# For CIFs not starting with letters from the two above lists, the control char can be either a letter or a digit
# Set to True if you want to convert to letter, otherwise it will be a digit
cif_control_choice_letter = False

code_to_province = {code: province for province, codes in province_codes.items() for code in codes}

def first_validity_check(id):
    if len(id) != 9:
        return False
    pattern = r'^(?:[' + re.escape(valid_start_letters) + r']\d{7}|[XYZ]\d{7}|\d{8})[' + re.escape(cod_control_dni_nie) + r'0-9]'
    return bool(re.match(pattern, id))

def calc_control_dni_nie(id):
    return cod_control_dni_nie[int(id) % 23]

def calc_control_cif(id):
    sum_digits = sum((int(digit) * (2 if index % 2 == 0 else 1)) // 10 + (int(digit) * (2 if index % 2 == 0 else 1)) % 10 for index, digit in enumerate(id))
    return str((10 - sum_digits % 10) % 10)
    
def verify(id, verbose=True):
    isvalid = first_validity_check(id)
    if not isvalid:
        print('Invalid ID pattern')
        return
    
    isDNI = False   
    isNIE = False
    isCIF = False
        
    if id[0].isdigit():
        isDNI = True
    
    if id.startswith(('X', 'Y', 'Z')): 
        isNIE = True
        id = nie_letter_to_num_map[id[0]] + id[1:] # replace the first NIE letter with the corresponding number
        
    if id[0].isalpha() and not isNIE and id[0] in valid_start_letters:
        isCIF = True
        
    idType = 'DNI' if isDNI else 'NIE' if isNIE else 'CIF'
        
    if isDNI or isNIE:
        id_num = ''.join(i for i in id if i.isdigit()) # want only numbers for the control letter/digit calculation
        control_letter = calc_control_dni_nie(id_num)
        if isNIE:
            id = nie_num_to_letter_map[id[0]] + id[1:] # reverse the NIE letter to number replacement
            
    elif isCIF:
        pcode = id[1:3]
        if pcode not in code_to_province.keys():
            print('Invalid province code')
            return
        control_digit = calc_control_cif(id[1:-1])
        if id[0] in is_cif_control_letter or pcode == '00':
            control_letter = cif_num_to_letter_map[control_digit]
        elif id[0] in is_cif_control_digit:
            control_letter = control_digit
        else:
            control_letter = cif_num_to_letter_map[control_digit] if cif_control_choice_letter else control_digit
        id = id[:-1] + control_letter

    if verbose:
        desc = f'ID type: {idType} | ID: {id} | Control letter/digit: {control_letter}'
        if isCIF:
            desc += f' | Entity type: {entity_types[id[0]]} | Province: {code_to_province[id[1:3]]}'
        print(desc)
    else:
        print(id)

'''
n = number of IDs to generate
C = CIF, D = DNI, N = NIE
ptype = entity type for CIF 
pcode = province code for CIF
'''   
def gen(n=5, t='D', ptype=None, pcode=None):
    if not ptype:
        ptype = random.choice(list(valid_start_letters.translate(str.maketrans("", "", "KLMXYZ")))) # remove invalid letters for CIF (natural person codes)
    if pcode:
        if isinstance(pcode, str):
            if pcode.isalpha():
                pcode = random.choice(province_codes[pcode])
        elif isinstance(pcode, list):
            pcode = random.choice(pcode)
        elif isinstance(pcode, int):
            pcode = str(pcode)
    if not pcode:
        pcode = random.choice(list(code_to_province.keys()))
    for _ in range(n):
        if t == 'D':
            id = ''.join(random.choices('0123456789', k=8))
            id += calc_control_dni_nie(id)
        elif t == 'N':
            start_letter = random.choices('XYZ')[0]
            id = nie_letter_to_num_map[start_letter] + ''.join(random.choices('0123456789', k=7))
            id += calc_control_dni_nie(id)
            id = start_letter + id[1:]
        elif t == 'C':
            id = ptype + pcode + ''.join(random.choices('0123456789', k=5))
            id += calc_control_cif(id[1:])
        verify(id, verbose=True)