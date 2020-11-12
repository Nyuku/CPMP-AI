# CPMP-AI

Ambiente de openai-gym (https://gym.openai.com/) para inteligencia artificial, aprendizaje por refuerzo.
Actualmente, este repositorio sólo contiene el ambiente, y puede ser probado utilizando DQN_Optimizer.py, utilizará `stable_baselines` para poder ejecutarse y probar el ambiente, pero es compatible con todo lo que sea compatible con gym.
Para más información y demonstraciones, pueden ingresar al archivo `documentation.ipynb`, también descargarlo y probar más cosas allí.

## Cómo Ejecutar
Al ser un ambiente basado en `gym`, este podrá ser ejecutado como cualquier ambiente, sin embargo en este repositorio se encuentra un archivo de python llamado [DQN_Optimizer.py](https://github.com/Nyuku/CPMP-AI/blob/master/DQN_Optimizer.py) que permite ejecutar una prueba del entorno.

Antes de ejecutar, se tendrá que generar instancias de prueba y entrenamiento. Estos enornos se podrán generar con los archivos ProblemGenerator.py y GenerateRandom.py. El primero generará problemas comenzando por un ambiente ordenado el cuál será desordenado aleatoriamente, y, el segundo generará problemas aleatorios.
Estos scripts de python guardarán la información en la carpeta asignada en la variable `rootFolder` de dichos archivos, para que no olvides cambiarla.


## Documentación / Cómo Funciona
La documentación del ambiente puede ser encontrada en [este archivo de jupyter notebook](https://github.com/Nyuku/CPMP-AI/blob/master/documentation.ipynb), en dónde se explicará cómo es que funciona este entorno.
