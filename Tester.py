import numpy as np
#from Yard import Yard
from containeryard.containeryard import ContainerYard

#yard = Yard(open("/home/naku/Programming/Internship/cpmp/BF/BF1/cpmp_16_5_48_10_29_10.bay","r"))
yard = ContainerYard(showDebug=True, x=5, y=5)

#Variables xd
step = 0
totalReward = 0


while True:
    yard.render()

    if False not in yard.state.getAllSorts():
        print("Already done. Next problem...")
        step = 0
        totalReward = 0
        yard.reset()
        continue
    print("REWARD TESTER MENU")
    print("1) Realizar un nuevo movimiento")
    print("2) Siguiente problema")
    print("0) Salir.")

    option = input()
    if option == "1":
        yard.render()
        print("Ingrese el movimiento")
        src  = input()
        dest = 0
        if not src.isnumeric():
            print("Parametros incorrectos.")
        else:
            _, reward, done, _ = yard.step(int(src))
            totalReward += reward
            step += 1
            print("> Step reward: " + str(reward))

            if done:
                print("> Finalizado, se ha resuelto el problema.")
                print("\t> TOTAL STEPS: " + str(step))
                print("\t> TOTAL REWARD: " + str(totalReward))
                yard.reset()
                step = 0
                totalReward = 0
                print("\t>>>>> Presiona cualquier tecla para continuar ...")
                input()

    elif option == "2":
        yard.reset()
        step = 0
        totalReward = 0
    elif option == "0":
       break
    else:
        print("Opción invalida. Seleccione de nuevo.")
