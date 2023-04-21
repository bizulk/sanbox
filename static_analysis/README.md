DRAFT DRAFT

L'analyse statique est un outil d'amélioration du code : 
- correction des failles potentielles
- correction de la lisibilité
- correction de métrique du code (complexité)
- respect des conventions de codage.

On distingue deux axes : 
- L'analyse du code en lui-même 
- Le formatage du code.


J'ai par le passé pratiqué de l'analyse de C/C++ : 
- OC-Lint pour du code C. Project open source. L'outil intègre les retours d'autres analysiseur comme cppcheck, et possède son propre analyseur pour le code. Il se base sur LLVM pour baliser le code et applique dessus des règles que l'on aura "codé". Ces règles sont embarquées en tant que shared lib
- pmccabe pour la métrique du code, le nombre cyclomatique m'a servi de base pour 