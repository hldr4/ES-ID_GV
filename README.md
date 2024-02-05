## Sources (thanks!)
 - https://github.com/TORR3S/Check-NIF
 - https://es.wikipedia.org/wiki/N%C3%BAmero_de_identificaci%C3%B3n_fiscal
 - https://es.wikipedia.org/wiki/C%C3%B3digo_de_identificaci%C3%B3n_fiscal
 - https://www.interior.gob.es/opencms/es/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/
 - http://www.aplicacionesinformaticas.com/programas/gratis/cif.php
 - https://www.generador-de-dni.com/generador-de-dni

## Usage

No commandline functionlity currently, so just edit the functions inside the python file or import them into your own code as you need. 

Examples:

  - Verify:
  ```py
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

  for id in test_ids:
    verify(id)
```

```
Output:

ID type: DNI | ID: 55883808H | Control letter/digit: H
ID type: NIE | ID: X2607448F | Control letter/digit: F
ID type: CIF | ID: D71897094 | Control letter/digit: 4 | Entity type: Sociedad Comanditaria | Province: Navarra
ID type: CIF | ID: D71897094 | Control letter/digit: 4 | Entity type: Sociedad Comanditaria | Province: Navarra
ID type: CIF | ID: P7189709D | Control letter/digit: D | Entity type: Corporación Local | Province: Navarra
ID type: CIF | ID: A12345674 | Control letter/digit: 4 | Entity type: Sociedad Anónima | Province: Castellón
Invalid ID pattern
Invalid ID pattern
Invalid ID pattern
Invalid ID pattern
```

  - Generate:
  ```py
  ## Generate 5 IDs of CIF type, for Sociedad Anonima entity type from Valencia
  gen(5, 'C', 'A', 'Valencia')
  ```

  ```
  Output:

  ID type: CIF | ID: A96033402 | Control letter/digit: 2 | Entity type: Sociedad Anónima | Province: Valencia
  ID type: CIF | ID: A96514013 | Control letter/digit: 3 | Entity type: Sociedad Anónima | Province: Valencia
  ID type: CIF | ID: A96415005 | Control letter/digit: 5 | Entity type: Sociedad Anónima | Province: Valencia
  ID type: CIF | ID: A96285242 | Control letter/digit: 2 | Entity type: Sociedad Anónima | Province: Valencia
  ID type: CIF | ID: A96166780 | Control letter/digit: 0 | Entity type: Sociedad Anónima | Province: Valencia
  ```





For further details study the code
